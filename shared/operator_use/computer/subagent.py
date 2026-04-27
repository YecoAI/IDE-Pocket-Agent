

import logging

from pydantic import BaseModel, Field
from operator_use.tools import Tool, ToolResult
from operator_use.agent.tools import ToolRegistry
from operator_use.messages import SystemMessage, HumanMessage, ToolMessage
from operator_use.providers.events import LLMEventType

logger = logging.getLogger(__name__)

MAX_ITERATIONS = 20

SYSTEM_PROMPT = """You are a desktop automation agent. Your goal is to complete the task by interacting with the computer.
You have access to a computer tool that allows you to click, type, scroll, and manage virtual desktops.
Analyze the screen(if available) or the context provided to decide the next action.
Be precise and efficient."""

@Tool(
 name="computer_task",
 description=(
 "Delegate a desktop automation task to an isolated agent with its own context window. "
 "Describe the full task — the agent handles all desktop interactions and returns a clean result."
),
 model=ComputerTask,
)
async def computer_task(task: str, **kwargs) -> ToolResult:
 llm = kwargs.get("_llm")
 if llm is None:
 return ToolResult.error_result("No LLM available.")

 plugin = kwargs.get("_plugin")
 computer_tool = kwargs.get("_computer_tool")

 if plugin is None or computer_tool is None:
 from operator_use.computer.tools import COMPUTER_TOOL
 from operator_use.computer.plugin import ComputerPlugin
 if COMPUTER_TOOL is None:
 return ToolResult.error_result("computer_task is not supported on this platform.")
 plugin = ComputerPlugin(enabled=True)
 computer_tool = COMPUTER_TOOL

 from operator_use.agent.hooks.events import BeforeLLMCallContext

 registry = ToolRegistry()
 registry.register_tools([computer_tool])
 registry.set_extension("_llm", llm)

 tools = registry.list_tools()
 history = [
 SystemMessage(content=SYSTEM_PROMPT),
 HumanMessage(content=task),
]

 result = f"(hit {MAX_ITERATIONS}-iteration limit without finishing)"
 try:
 for iteration in range(MAX_ITERATIONS):
 logger.info("[computer_task] Starting iteration %d", iteration)
 messages = list(history)
 ctx = BeforeLLMCallContext(session=None, messages=messages, iteration=iteration)
 await plugin._state_hook(ctx)

 logger.info("[computer_task] Calling LLM ainvoke(iteration %d)", iteration)
 event = await llm.ainvoke(messages=messages, tools=tools)
 logger.info("[computer_task] LLM returned event type: %s", event.type)
 match event.type:
 case LLMEventType.TOOL_CALL:
 tc = event.tool_call
 logger.info("[computer_task] iter=%d tool=%s params=%s", iteration, tc.name, tc.params)
 tr = await registry.aexecute(tc.name, tc.params)
 logger.info("[computer_task] iter=%d result_success=%s result_output_len=%d", iteration, tr.success, len(tr.output) if tr.output else 0)
 if not tr.success:
 logger.error("[computer_task] iter=%d tool_error: %s", iteration, tr.error)

 thinking_signature = event.thinking.signature if event.thinking else None
 history.append(ToolMessage(
 id=tc.id,
 name=tc.name,
 params=tc.params,
 content=tr.output if tr.success else tr.error,
 thinking_signature=thinking_signature,
))
 case LLMEventType.TEXT:
 result = event.content or "(no result)"
 logger.info("[computer_task] iter=%d final_text_response: %s", iteration, result[:100])
 break

 except Exception as e:
 logger.error("computer_task failed: %s", e, exc_info=True)
 return ToolResult.error_result(f"computer_task failed: {type(e).__name__}: {e}")

 finally:
 if plugin.watchdog is not None:
 try:
 plugin.watchdog.stop()
 except Exception:
 pass

 return ToolResult.success_result(result)
