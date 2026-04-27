

import logging
from collections import defaultdict
from typing import Callable, Awaitable, TypeVar

from operator_use.agent.hooks.events import HookEvent

logger =logging.getLogger(__name__)

HookContext =TypeVar("HookContext")
HookHandler =Callable[[HookContext], Awaitable[None]]

class Hooks:

 def __init__(self):
 self._handlers:dict[HookEvent, list[HookHandler]]=defaultdict(list)

 def register(self, event:HookEvent, handler:HookHandler)->None:

 self._handlers[event].append(handler)

 def unregister(self, event:HookEvent, handler:HookHandler)->None:

 try:
 self._handlers[event].remove(handler)
 except ValueError:
 pass

 def on(self, event:HookEvent):

 def decorator(fn:HookHandler)->HookHandler:
 self.register(event, fn)
 return fn
 return decorator

 async def emit(self, event:HookEvent, context:HookContext)->HookContext:

 for handler in self._handlers[event]:
 try:
 await handler(context)
 except Exception as e:
 logger.error("Hook handler %s raised: %s", handler.__name__, e, exc_info =True)
 return context
