import asyncio
from typing import Dict, Optional, Any, Literal
import json
import uuid
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware

import logging
import datetime
from contextlib import asynccontextmanager
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field, model_validator

from auth import Token, create_access_token, decode_access_token, TokenData
from trae_instructions import get_detailed_instruction
from database import init_db, async_session, get_db
from routers import router as licensing_router
import models
import schemas

from operator_use.providers import (
    ChatZAI,
    ChatGroq,
    ChatOpenAI,
    ChatAnthropic,
    ChatOllama,
    ChatLlama,
    ChatQwen,
    SecureChatLLM,
)


class LLMProviderRegistry:
    _providers = []

    @classmethod
    def register(cls, matcher, provider_factory):
        cls._providers.append((matcher, provider_factory))

    @classmethod
    def get_provider(cls, model_name: str):
        m = model_name.lower()
        provider = None
        for matcher, factory in cls._providers:
            if matcher(m):
                provider = factory(model_name, m)
                break
        
        if provider is None:
            provider = ChatZAI(model=model_name, reasoning=False)
            
        return SecureChatLLM(provider)

LLMProviderRegistry.register(
    lambda m: "claude" in m, 
    lambda name, m: ChatAnthropic(model=name)
)
LLMProviderRegistry.register(
    lambda m: "ollama" in m, 
    lambda name, m: ChatOllama(model=name.split("/")[-1] if "/" in name else name)
)
LLMProviderRegistry.register(
    lambda m: any(x in m for x in ["gpt", "o1", "o3"]), 
    lambda name, m: ChatOpenAI(model=name)
)
LLMProviderRegistry.register(
    lambda m: "qwen" in m, 
    lambda name, m: ChatQwen(model=name)
)
LLMProviderRegistry.register(
    lambda m: "llama" in m or "scout" in m, 
    lambda name, m: ChatOpenAI(model=name) if os.environ.get("OPENAI_BASE_URL") else ChatGroq(model=name)
)

def get_llm_provider(model_name: str):
    return LLMProviderRegistry.get_provider(model_name)

from operator_use.computer.subagent import computer_task
from operator_use.tools import Tool, ToolResult
from operator_use.messages import HumanMessage

os.makedirs("logs", exist_ok=True)
log_filename = (
    f"logs/log-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_filename, encoding="utf-8"),
    ],
)
logger = logging.getLogger("backend")

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.ERROR)





class RemoteComputerTool(BaseModel):
    action: Literal[
        "click", "type", "scroll", "move", "shortcut", "wait", "desktop"
    ] = Field(..., description="Computer action to perform")
    loc: Optional[list[int]] = Field(default=None)
    button: Literal["left", "right", "middle"] = Field(default="left")
    clicks: int = Field(default=1)
    text: Optional[str] = Field(default=None)
    clear: bool = Field(default=False)
    caret_position: Literal["start", "idle", "end"] = Field(default="idle")
    press_enter: bool = Field(default=False)
    axis: Literal["vertical", "horizontal"] = Field(default="vertical")
    direction: Literal["up", "down", "left", "right"] = Field(default="down")
    wheel_times: int = Field(default=1)
    drag: bool = Field(default=False)
    shortcut: Optional[str] = Field(default=None)
    duration: Optional[int] = Field(default=None)
    desktop_action: Optional[
        Literal["create", "remove", "rename", "switch"]
    ] = Field(default=None)
    desktop_name: Optional[str] = Field(default=None)
    new_name: Optional[str] = Field(default=None)

    @model_validator(mode="before")
    @classmethod
    def _coerce_params(cls, data: dict) -> dict:
        if not isinstance(data, dict):
            return data
        for field in ("loc",):
            v = data.get(field)
            if isinstance(v, str) and v != "null":
                try:
                    data[field] = json.loads(v)
                except:
                    pass
        return data


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    keep_alive_task = asyncio.create_task(global_keep_alive_worker())
    yield
    keep_alive_task.cancel()
    try:
        await keep_alive_task
    except asyncio.CancelledError:
        pass


async def global_keep_alive_worker():
    while True:
        try:
            await asyncio.sleep(random.randint(60, 120))
            async with async_session() as db:
                result = await db.execute(
                    select(models.Device).where(
                        models.Device.device_type == "agent",
                        models.Device.keep_alive_active == True,
                    )
                )
                active_agents = result.scalars().all()
                for agent_dev in active_agents:
                    if agent_dev.device_id in manager.agents:
                        dx = random.randint(-5, 5)
                        dy = random.randint(-5, 5)
                        queue = manager.get_agent_queue(agent_dev.device_id)

                        await queue.put(
                            manager.call_agent(
                                agent_dev.device_id,
                                "EXECUTE_COMPUTER_ACTION",
                                payload={
                                    "action": "mouse_move",
                                    "loc": [500 + dx, 500 + dy],
                                },
                            )
                        )
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Keep-alive worker error: {e}")
            await asyncio.sleep(10)


app = FastAPI(
    title="IDEPocket Backend",
    description="Unified backend for IDEPocket automation and licensing",
    version="1.0.0",
    lifespan=lifespan,
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(licensing_router)


@app.get("/ping")
async def ping():
    return {"status": "ok", "timestamp": datetime.datetime.now().isoformat()}


from connection_manager import manager


def get_model_for_task(task: str) -> str:
    return "glm-5v-turbo"


class RemoteComputerPlugin:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.watchdog = None

    async def _state_hook(self, ctx):
        manager.check_stop(self.agent_id)
        try:
            res = await manager.call_agent(self.agent_id, "GET_DESKTOP_STATE")
            state_str = res.get("result", "")
            if state_str:
                ctx.messages.append(HumanMessage(content=state_str))
        except Exception as e:
            if "TASK_STOPPED_BY_USER" in str(e):
                raise e
            logger.error(f"Desktop state capture failed: {e}")
        return ctx


def create_remote_computer_tool(agent_id: str):
    @Tool(
        name="computer",
        description="Control the desktop using coordinates from the desktop state.",
        model=RemoteComputerTool,
    )
    async def remote_computer_tool(**kwargs) -> ToolResult:
        manager.check_stop(agent_id)
        payload = {k: v for k, v in kwargs.items() if not k.startswith("_")}
        try:
            res = await manager.call_agent(
                agent_id, "EXECUTE_COMPUTER_ACTION", payload=payload
            )
            return ToolResult.success_result(res.get("result", ""))
        except Exception as e:
            if "TASK_STOPPED_BY_USER" in str(e):
                raise e
            return ToolResult.error_result(str(e))

    return remote_computer_tool


async def execute_task_on_backend(
    client_id: str, agent_id: str, action: str, payload: dict
):
    task_key = f"{agent_id}:{action}"
    if task_key in manager.active_tasks:
        return
    manager.active_tasks.add(task_key)
    try:
        if action == "MODE_SWITCH":
            try:
                res = await manager.call_agent(
                    agent_id,
                    "EXECUTE_COMPUTER_ACTION",
                    payload={"action": "click", "loc": [30, 30], "button": "left"},
                )
                await manager.send_to_client(
                    client_id,
                    {
                        "client_id": client_id,
                        "action": action,
                        "result": "MODE_SWITCH_EXECUTED_DIRECTLY",
                        "success": res.get("success", False),
                        "requires_refresh": False,
                    },
                )
                return
            except Exception as e:
                logger.error(f"Direct MODE_SWITCH error: {e}")
                return

        if agent_id in manager.stop_signals:
            manager.stop_signals[agent_id].clear()

        task_description = get_detailed_instruction(action, payload)
        logger.info(f"--- [MAPPED_TASK] -> {task_description} ---")

        if action == "TASK_CONTROL" and payload.get("command") == "stop":
            await manager.force_stop_agent_task(agent_id)
            await manager.send_to_client(
                client_id,
                {
                    "client_id": client_id,
                    "action": action,
                    "result": "STOP_EXECUTED_PRIORITY",
                    "success": True,
                    "requires_refresh": True,
                },
            )
            return

        model = get_model_for_task(task_description)
        if action == "GET_WORKSPACE":
            model = "meta-llama/llama-4-scout-17b-16e-instruct"

        fallback_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

        if action == "GET_WORKSPACE":
            try:
                res = await manager.call_agent(agent_id, "GET_DESKTOP_STATE")
                state_str = res.get("result", "")

                groq_model = "meta-llama/llama-4-scout-17b-16e-instruct"
                try:
                    llm = get_llm_provider(groq_model)
                    resp = await llm.ainvoke(
                        [
                            HumanMessage(
                                content=f"{task_description}\n\nDESKTOP STATE:\n{state_str}"
                            )
                        ]
                    )
                    clean_output = resp.content.strip()
                    if "{" in clean_output and "}" in clean_output:
                        clean_output = clean_output[
                            clean_output.find("{") : clean_output.rfind("}") + 1
                        ]
                    result_data = json.loads(clean_output)
                    await manager.send_to_client(
                        client_id,
                        {
                            "client_id": client_id,
                            "action": action,
                            "result": result_data,
                            "success": True,
                            "requires_refresh": False,
                        },
                    )
                    return
                except Exception as e:
                    if "429" in str(e) or "limit" in str(e).lower():
                        llm = get_llm_provider("llama-3.3-70b-versatile")
                        resp = await llm.ainvoke(
                            [
                                HumanMessage(
                                    content=f"{task_description}\n\nDESKTOP STATE:\n{state_str}"
                                )
                            ]
                        )

                        clean_output = resp.content.strip()
                        if "{" in clean_output and "}" in clean_output:
                            clean_output = clean_output[
                                clean_output.find("{") : clean_output.rfind("}") + 1
                            ]
                        result_data = json.loads(clean_output)
                        await manager.send_to_client(
                            client_id,
                            {
                                "client_id": client_id,
                                "action": action,
                                "result": result_data,
                                "success": True,
                                "requires_refresh": False,
                            },
                        )
                        return
            except Exception as e:
                logger.error(f"GET_WORKSPACE optimization error: {e}")

        plugin = RemoteComputerPlugin(agent_id)
        computer_tool = create_remote_computer_tool(agent_id)

        async def try_execute(current_model: str):
            llm = get_llm_provider(current_model)
            return await computer_task.ainvoke(
                task=task_description,
                _llm=llm,
                _plugin=plugin,
                _computer_tool=computer_tool,
            )

        try:
            result = await try_execute(model)

            if not result.success:
                err_str = str(result.error).lower()
                if any(
                    err in err_str
                    for err in [
                        "400",
                        "429",
                        "limit",
                        "balance",
                        "overloaded",
                        "failed",
                        "unsafe",
                        "sensitive",
                    ]
                ):
                    logger.warning(
                        f"Primary model {model} failed with: {result.error}. Trying fallbacks..."
                    )
                    for fb_model in fallback_models:
                        if fb_model == model:
                            continue
                        logger.info(f"Trying fallback model: {fb_model }")
                        result = await try_execute(fb_model)
                        if result.success:
                            logger.info(f"Fallback to {fb_model} successful.")
                            break
                        else:
                            logger.warning(
                                f"Fallback model {fb_model} failed: {result.error}"
                            )

            result_output = (
                result.output if result.success else f"Error: {result.error}"
            )
            if result.success:
                try:
                    clean_output = result_output.strip()
                    if "{" in clean_output and "}" in clean_output:
                        clean_output = clean_output[
                            clean_output.find("{") : clean_output.rfind("}") + 1
                        ]
                    result_output = json.loads(clean_output)
                except:
                    pass

            await manager.send_to_client(
                client_id,
                {
                    "client_id": client_id,
                    "action": action,
                    "result": result_output,
                    "success": result.success,
                    "requires_refresh": action
                    not in ["MODE_SWITCH", "GET_WORKSPACE"],
                },
            )
        except Exception as e:
            logger.error(f"Task execution error: {e}")
            await manager.send_to_client(
                client_id,
                {
                    "client_id": client_id,
                    "action": action,
                    "result": str(e),
                    "success": False,
                    "requires_refresh": action
                    not in ["MODE_SWITCH", "GET_WORKSPACE"],
                },
            )
    finally:
        manager.active_tasks.discard(task_key)


async def get_current_mobile_user(
    authorization: str = Header(None),
) -> TokenData:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    token_data = decode_access_token(token)
    if not token_data or token_data.role != "client":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data


@app.get("/v1/mobile/info")
async def mobile_get_info(
    token_data: TokenData = Depends(get_current_mobile_user),
):
    return {
        "status": "online",
        "version": "2.0.0",
        "client_id": token_data.sub,
        "features": ["licensing", "computer_use", "queuing", "keep_alive"],
    }


async def get_first_associated_agent_id(
    client_id: str, log_prefix: str = "Fallback"
) -> Optional[str]:
    try:
        async with async_session() as db:
            mob_res = await db.execute(
                select(models.Device).where(models.Device.device_id == client_id)
            )
            mobile_dev = mob_res.scalars().first()
            if not mobile_dev:
                logger.warning(
                    f"{log_prefix} check failed: mobile device {client_id} not found in DB"
                )
                return None

            assoc_res = await db.execute(
                select(models.Device)
                .join(
                    models.Association,
                    models.Association.agent_device_id == models.Device.id,
                )
                .where(
                    models.Association.mobile_device_id == mobile_dev.id,
                    models.Association.status == "active",
                )
            )
            associated_agents = assoc_res.scalars().all()

            if not associated_agents:
                return None

            for agent in associated_agents:
                return agent.device_id
    except Exception as e:
        logger.error(f"{log_prefix} agent ID lookup failed: {e}")
        return None
