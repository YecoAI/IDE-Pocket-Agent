

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
 from operator_use.messages import AIMessage, BaseMessage
 from operator_use.session import Session
 from operator_use.providers.events import LLMToolCall, LLMEvent
 from operator_use.agent.tools import ToolResult

class HookEvent(str, Enum):
 BEFORE_AGENT_START ="before_agent_start"
 AFTER_AGENT_START ="after_agent_start"
 BEFORE_AGENT_END ="before_agent_end"
 AFTER_AGENT_END ="after_agent_end"
 BEFORE_TOOL_CALL ="before_tool_call"
 AFTER_TOOL_CALL ="after_tool_call"
 BEFORE_LLM_CALL ="before_llm_call"
 AFTER_LLM_CALL ="after_llm_call"

@dataclass
class BeforeAgentStartContext:

 session:"Session"

@dataclass
class AfterAgentStartContext:

 session:"Session"
 iteration:int

@dataclass
class BeforeAgentEndContext:

 session:"Session"
 response:"AIMessage"

@dataclass
class AfterAgentEndContext:

 session:"Session"
 response:"AIMessage"

@dataclass
class BeforeToolCallContext:

 session:"Session"
 tool_call:"LLMToolCall"
 skip:bool =False
 result:Any =None

@dataclass
class AfterToolCallContext:

 session:"Session"
 tool_call:"LLMToolCall"
 tool_result:"ToolResult"
 content:Any

@dataclass
class BeforeLLMCallContext:

 session:"Session"
 messages:"list[BaseMessage]"
 iteration:int

@dataclass
class AfterLLMCallContext:

 session:"Session"
 messages:"list[BaseMessage]"
 event:"LLMEvent"
 iteration:int
