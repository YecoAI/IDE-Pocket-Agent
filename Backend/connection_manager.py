import asyncio
import json
import uuid
import logging
from typing import Dict
from fastapi import WebSocket

logger = logging.getLogger("backend")

class ConnectionManager:
    def __init__(self):
        self.clients: Dict[str, WebSocket] = {}
        self.agents: Dict[str, WebSocket] = {}
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.active_tasks: set = set()
        self.stop_signals: Dict[str, asyncio.Event] = {}
        self.agent_queues: Dict[str, asyncio.Queue] = {}
        self.agent_workers: Dict[str, asyncio.Task] = {}

    def get_agent_queue(self, agent_id: str) -> asyncio.Queue:
        if agent_id not in self.agent_queues:
            self.agent_queues[agent_id] = asyncio.Queue()
            self.agent_workers[agent_id] = asyncio.create_task(
                self.process_agent_queue(agent_id)
            )
        return self.agent_queues[agent_id]

    async def process_agent_queue(self, agent_id: str):
        queue = self.agent_queues[agent_id]
        while True:
            try:
                task_coro = await queue.get()
                await task_coro
                queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing queue for agent {agent_id}: {e}")

    async def connect_client(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.clients[client_id] = websocket

    def disconnect_client(self, client_id: str):
        if client_id in self.clients:
            del self.clients[client_id]

    async def connect_agent(self, websocket: WebSocket, agent_id: str):
        await websocket.accept()
        self.agents[agent_id] = websocket
        logger.info(f"Agent connected: {agent_id}")

    def disconnect_agent(self, agent_id: str, websocket: WebSocket = None):
        if agent_id in self.agents:
            if websocket and self.agents[agent_id] != websocket:
                logger.info(f"Stale agent disconnect ignored: {agent_id}")
                return
            del self.agents[agent_id]
            logger.info(f"Agent disconnected: {agent_id}")

        if agent_id in self.stop_signals:
            del self.stop_signals[agent_id]
        if agent_id in self.agent_workers:
            self.agent_workers[agent_id].cancel()
            del self.agent_workers[agent_id]
        if agent_id in self.agent_queues:
            del self.agent_queues[agent_id]

    async def force_stop_agent_task(self, agent_id: str):
        if agent_id in self.agents:
            if agent_id not in self.stop_signals:
                self.stop_signals[agent_id] = asyncio.Event()
            self.stop_signals[agent_id].set()
            await self.send_to_agent(
                agent_id,
                {
                    "action": "FORCE_STOP",
                    "payload": {"reason": "Emergency stop requested"},
                },
            )
            return True
        return False

    def check_stop(self, agent_id: str):
        if agent_id in self.stop_signals and self.stop_signals[agent_id].is_set():
            raise Exception("TASK_STOPPED_BY_USER")

    async def send_to_agent(self, agent_id: str, message: dict):
        if agent_id in self.agents:
            await self.agents[agent_id].send_text(json.dumps(message))
            return True
        return False

    async def call_agent(
        self, agent_id: str, action: str, payload: dict = None
    ) -> dict:
        if agent_id not in self.agents:
            raise Exception("Agent offline")
        request_id = str(uuid.uuid4())
        future = asyncio.get_event_loop().create_future()
        self.pending_requests[request_id] = future
        message = {"request_id": request_id, "action": action}
        if payload:
            message["payload"] = payload
        await self.send_to_agent(agent_id, message)
        try:
            result = await asyncio.wait_for(future, timeout=30.0)
            if not result.get("success"):
                raise Exception(result.get("error", "Unknown error in agent"))
            return result
        finally:
            self.pending_requests.pop(request_id, None)

    async def send_to_client(self, client_id: str, message: dict):
        if client_id in self.clients:
            await self.clients[client_id].send_text(json.dumps(message))
            return True
        return False

manager = ConnectionManager()
