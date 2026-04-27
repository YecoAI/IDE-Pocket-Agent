import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, overload
import anthropic
from pydantic import BaseModel
from operator_use.providers.base import BaseChatLLM
from operator_use.providers.views import TokenUsage, Metadata
from operator_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from operator_use.tools import Tool
from operator_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger =logging.getLogger(__name__)

class ChatAnthropic(BaseChatLLM):

 MODELS ={
 "claude-3-5-sonnet-20241022":200000,
 "claude-3-5-haiku-20241022":200000,
 "claude-3-opus-20240229":200000,
 "claude-3-sonnet-20240229":200000,
 "claude-3-haiku-20240307":200000,
 }

 def __init__(
 self,
 model:str ="claude-3-5-sonnet-20241022",
 api_key:Optional[str]=None,
 base_url:Optional[str]=None,
 timeout:float =600.0,
 max_retries:int =2,
 temperature:Optional[float]=None,
 **kwargs
):

 self._model =model
 self.api_key =api_key or os.environ.get("ANTHROPIC_API_KEY")
 self.base_url =base_url
 self.temperature =temperature

 self.client =anthropic.Anthropic(
 api_key =self.api_key,
 base_url =self.base_url,
 timeout =timeout,
 max_retries =max_retries,
)
 self.aclient =anthropic.AsyncAnthropic(
 api_key =self.api_key,
 base_url =self.base_url,
 timeout =timeout,
 max_retries =max_retries,
)
 self.kwargs =kwargs

 @property
 def model_name(self)->str:
 return self._model

 @property
 def provider(self)->str:
 return "anthropic"

 def _convert_messages(self, messages:List[BaseMessage])->tuple[Optional[str], List[dict]]:
 system_prompt =None
 anthropic_messages =[]

 for msg in messages:
 if isinstance(msg, SystemMessage):
 system_prompt =msg.content
 elif isinstance(msg, HumanMessage):
 anthropic_messages.append({"role":"user", "content":msg.content })
 elif isinstance(msg, ImageMessage):
 content =[]
 if msg.content:
 content.append({"type":"text", "text":msg.content })

 b64_imgs =msg.convert_images(format ="base64")
 for b64 in b64_imgs:
 content.append({
 "type":"image",
 "source":{
 "type":"base64",
 "media_type":msg.mime_type,
 "data":b64
 }
 })
 anthropic_messages.append({"role":"user", "content":content })
 elif isinstance(msg, AIMessage):
 content =[]
 if msg.content:
 content.append({"type":"text", "text":msg.content })

 tool_call =getattr(msg, "tool_call", None)
 if tool_call:
 content.append({
 "type":"tool_use",
 "id":tool_call.id,
 "name":tool_call.name,
 "input":tool_call.params
 })

 if not content: continue
 anthropic_messages.append({"role":"assistant", "content":content })
 elif isinstance(msg, ToolMessage):
 anthropic_messages.append({
 "role":"user",
 "content":[{
 "type":"tool_result",
 "tool_use_id":msg.id,
 "content":msg.content or ""
 }]
 })
 return system_prompt, anthropic_messages

 def _convert_tools(self, tools:List[Tool])->List[dict]:
 converted =[]
 for tool in tools:
 schema =tool.json_schema
 converted.append({
 "name":schema["name"],
 "description":schema["description"],
 "input_schema":schema["parameters"]
 })
 return converted

 async def ainvoke(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
 system, anthropic_messages =self._convert_messages(messages)
 anthropic_tools =self._convert_tools(tools) if tools else None

 params ={
 "model":self._model,
 "messages":anthropic_messages,
 "max_tokens":4096,
 **self.kwargs
 }
 if system: params["system"]=system
 if anthropic_tools: params["tools"]=anthropic_tools
 if self.temperature is not None: params["temperature"]=self.temperature

 logger.info(f"[*] Anthropic LLM Request: model={self._model }")

 response =await self.aclient.messages.create(**params)

 usage =TokenUsage(
 prompt_tokens =response.usage.input_tokens,
 completion_tokens =response.usage.output_tokens,
 total_tokens =response.usage.input_tokens +response.usage.output_tokens
)

 content_text =""
 tool_call =None

 for content in response.content:
 if content.type =="text":
 content_text +=content.text
 elif content.type =="tool_use":
 tool_call =ToolCall(id =content.id, name =content.name, params =content.input)

 if tool_call:
 return LLMEvent(type =LLMEventType.TOOL_CALL, tool_call =tool_call, usage =usage)
 return LLMEvent(type =LLMEventType.TEXT, content =content_text, usage =usage)

 def get_metadata(self)->Metadata:
 return Metadata(name =self._model, context_window =self.MODELS.get(self._model, 200000), owned_by ="anthropic")
