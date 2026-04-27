

import asyncio
import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
 from operator_use.agent.hooks.events import BeforeLLMCallContext, AfterToolCallContext
 from operator_use.agent.tools import ToolRegistry
 from operator_use.agent.context import Context

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a specialized computer-use plugin. Your responsibility is to provide the agent with the ability to interact with the desktop environment.
Ensure all interactions are safe and follow the user's intent."""

class ComputerPlugin:

 name = "computer_use"

 def __init__(self, enabled: bool = False):
 self._registry: "ToolRegistry | None" = None
 self._hooks: "Hooks | None" = None
 self._context: "Context | None" = None
 self.desktop = None
 self.watchdog = None
 self._enabled = enabled
 if enabled:
 self._init_sync()

 def get_tools(self) -> list:
 from operator_use.computer.subagent import computer_task
 return[computer_task]

 def get_system_prompt(self) -> str | None:
 return SYSTEM_PROMPT if self._enabled else None

 def register_tools(self, registry: "ToolRegistry") -> None:
 self._registry = registry
 if self._enabled:
 for tool in self.get_tools():
 registry.register(tool)

 def unregister_tools(self, registry: "ToolRegistry") -> None:
 for tool in self.get_tools():
 if registry.get(tool.name) is not None:
 registry.unregister(tool.name)

 def register_hooks(self, hooks: "Hooks") -> None:
 self._hooks = hooks
 def unregister_hooks(self, hooks:"Hooks")->None:

 pass

 def attach_prompt(self, context:"Context")->None:
 self._context =context
 if self._enabled:
 context.register_plugin_prompt(SYSTEM_PROMPT)

 def detach_prompt(self, context:"Context")->None:
 if self._context is not None:
 self._context.unregister_plugin_prompt(SYSTEM_PROMPT)

 def _init_sync(self)->None:

 if sys.platform =="win32":
 from operator_use.computer.windows.desktop.service import Desktop
 from operator_use.computer.windows.watchdog.service import WatchDog
 if self.desktop is None:
 self.desktop =Desktop(use_vision =False, use_annotation =False, use_accessibility =True)
 if self.watchdog is None:
 self.watchdog =WatchDog()
 self.watchdog.start()
 elif sys.platform =="darwin":
 from operator_use.computer.macos.desktop.service import Desktop
 from operator_use.computer.macos.watchdog.service import WatchDog
 if self.desktop is None:
 self.desktop =Desktop()
 if self.watchdog is None:
 self.watchdog =WatchDog()
 self.watchdog.start()

 async def enable(self)->None:

 self._enabled =True
 if self._registry is not None:
 for tool in self.get_tools():
 if self._registry.get(tool.name)is None:
 self._registry.register(tool)
 if self._context is not None:
 self._context.register_plugin_prompt(SYSTEM_PROMPT)
 logger.info("computer_use enabled")

 async def disable(self)->None:

 self._enabled =False
 if self._registry is not None:
 self.unregister_tools(self._registry)
 if self._context is not None:
 self._context.unregister_plugin_prompt(SYSTEM_PROMPT)
 logger.info("computer_use disabled")

 async def _state_hook(self, ctx:"BeforeLLMCallContext")->"BeforeLLMCallContext":
 from operator_use.messages import HumanMessage
 try:
 state =await asyncio.get_event_loop().run_in_executor(None, self.desktop.get_state)
 if state:
 ctx.messages.append(HumanMessage(content =state.to_string()))
 except Exception as e:
 logger.debug("Desktop state capture failed: %s", e)
 return ctx

 async def _wait_for_ui_hook(self, ctx:"AfterToolCallContext")->"AfterToolCallContext":
 if self.watchdog is None:
 await asyncio.sleep(0.5)
 return ctx
 timeout =1.5
 quiet_window =0.3
 loop =asyncio.get_event_loop()
 deadline =loop.time()+timeout
 while loop.time()<deadline:
 self.watchdog.ui_changed.clear()
 await asyncio.sleep(quiet_window)
 if not self.watchdog.ui_changed.is_set():
 break
 return ctx
