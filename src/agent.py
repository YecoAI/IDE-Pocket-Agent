import asyncio
import json
import uuid
import logging
import httpx
import websockets
import threading
import time
from pynput import mouse
from typing import Optional, Dict, Any, Callable
from src.config import settings
from src.security import save_credentials
from src.screen import capture_preview_snapshot, handle_live_desktop

logger = logging.getLogger(__name__)

class AgentWorker:
    def __init__(self, desktop_instance, computer_tool, status_callback: Optional[Callable[[str], None]] = None):
        self.desktop = desktop_instance
        self.computer = computer_tool
        self.current_association_id: Optional[str] = None
        self.main_loop: Optional[asyncio.AbstractEventLoop] = None
        self.last_move_time = 0.0
        self.click_count = 0
        self.gesture_active = False
        self.status_callback = status_callback
        self._running = False

    def _update_status(self, msg: str):
        if self.status_callback:
            self.status_callback(msg)
        logger.info(msg)

    async def start_pairing(self, pairing_code: str, device_id: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{settings.backend_url}/v1/licensing/agent/pair",
                    json={"pairing_code": pairing_code, "device_id": device_id},
                    headers={"X-License-Key": settings.trae_license_key},
                    timeout=10.0
                )
                if resp.status_code == 200:
                    return resp.json().get("association_id")
                return None
        except Exception:
            return None

    async def confirm_otp(self, association_id: str, otp: str) -> Optional[str]:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{settings.backend_url}/v1/licensing/agent/confirm",
                    json={"association_id": int(association_id), "otp_code": otp},
                    headers={"X-License-Key": settings.trae_license_key},
                    timeout=10.0
                )
                if resp.status_code == 200:
                    access_token = resp.json().get("access_token")
                    if access_token:
                        self.current_association_id = association_id
                        save_credentials(access_token, association_id)
                        return access_token
                return None
        except Exception:
            return None

    async def send_stop_request(self):
        agent_id = self.current_association_id or "unknown"
        stop_url = f"{settings.backend_url}/v1/agent/{agent_id}/stop"
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    stop_url,
                    headers={"X-License-Key": settings.trae_license_key},
                    timeout=5.0
                )
        except Exception:
            pass

    def on_move(self, x, y):
        self.last_move_time = time.time()
        self.click_count = 0
        self.gesture_active = True

    def on_click(self, x, y, button, pressed):
        if pressed and self.gesture_active:
            now = time.time()
            if now - self.last_move_time <= 3.0:
                self.click_count += 1
                if self.click_count >= 5:
                    self.gesture_active = False
                    self.click_count = 0
                    if self.main_loop:
                        asyncio.run_coroutine_threadsafe(self.send_stop_request(), self.main_loop)
            else:
                self.gesture_active = False
                self.click_count = 0

    def start_kill_switch(self, loop):
        self.main_loop = loop
        with mouse.Listener(on_move=self.on_move, on_click=self.on_click) as listener:
            listener.join()

    async def process_command(self, websocket, data: Dict[str, Any]):
        request_id = data.get("request_id")
        action = data.get("action")
        if not request_id or not action:
            return
        try:
            if action == "GET_DESKTOP_STATE":
                state = await asyncio.get_event_loop().run_in_executor(None, self.desktop.get_state)
                result = state.to_string() if state else ""
                await websocket.send(json.dumps({"request_id": request_id, "action": action, "success": True, "result": result}))
            elif action == "GET_PREVIEW_SNAPSHOT":
                img_str = capture_preview_snapshot()
                await websocket.send(json.dumps({"request_id": request_id, "action": action, "success": True, "result": img_str, "type": "image"}))
            elif action == "GET_DESKTOP_LIVE":
                payload = data.get("payload", {})
                img_data = await asyncio.get_event_loop().run_in_executor(None, handle_live_desktop, payload)
                await websocket.send(json.dumps({"request_id": request_id, "action": action, "success": True, "result": img_data, "type": "live_stream"}))
            elif action == "EXECUTE_COMPUTER_ACTION":
                payload = data.get("payload", {})
                result = await self.computer.ainvoke(**payload)
                await websocket.send(json.dumps({"request_id": request_id, "action": action, "success": result.success, "result": result.output, "message": result.error if not result.success else None}))
        except Exception as e:
            await websocket.send(json.dumps({"request_id": request_id, "action": action, "success": False, "message": str(e)}))

    async def run(self, token: str):
        self._running = True
        ws_endpoint = f"{settings.ws_url}/ws/agent"
        headers = {"Authorization": f"Bearer {token}"}
        retry_delay = 5.0
        max_retry_delay = 60.0
        while self._running:
            try:
                self._update_status("Connecting to server...")
                async with websockets.connect(ws_endpoint, additional_headers=headers, ping_interval=20, ping_timeout=20) as websocket:
                    self._update_status("Connected and listening")
                    retry_delay = 5.0
                    while self._running:
                        try:
                            message = await websocket.recv()
                            data = json.loads(message)
                            asyncio.create_task(self.process_command(websocket, data))
                        except json.JSONDecodeError:
                            pass
                        except websockets.exceptions.ConnectionClosed:
                            raise
                        except Exception:
                            pass
            except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError, OSError):
                self._update_status(f"Connection lost, retrying in {int(retry_delay)}s...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, max_retry_delay)
            except Exception:
                self._update_status("Fatal error, retrying...")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, max_retry_delay)

    def stop(self):
        self._running = False
