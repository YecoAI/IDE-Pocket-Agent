import os
import json
import logging
from typing import Iterator, AsyncIterator, List, Optional, Any, overload
from openai import OpenAI, AsyncOpenAI
from pydantic import BaseModel
from operator_use.providers.base import BaseChatLLM
from operator_use.providers.views import TokenUsage, Metadata
from operator_use.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, ImageMessage, ToolMessage
from operator_use.tools import Tool
from operator_use.providers.events import LLMEvent, LLMEventType, LLMStreamEvent, LLMStreamEventType, ToolCall, Thinking

logger =logging.getLogger(__name__)

class ChatOpenAI(BaseChatLLM):

 MODELS ={

 "gpt-5.4":1050000,
 "gpt-5.4-mini":400000,
 "gpt-5.4-nano":400000,

 "gpt-5.2":400000,

 "gpt-4.1":1000000,
 "gpt-4.1-mini":1000000,
 "gpt-4.1-nano":1000000,

 "gpt-4o":128000,
 "gpt-4o-mini":128000,

 "o1":200000,
 "o3":200000,
 "o3-mini":200000,
 "o3-pro":200000,
 "o4-mini":200000,
 }

 REASONING_PATTERNS =("o1", "o3", "o4")

 def __init__(
 self,
 model:str ="gpt-4.1",
 api_key:Optional[str]=None,
 base_url:Optional[str]=None,
 timeout:float =600.0,
 max_retries:int =2,
 temperature:Optional[float]=None,
 **kwargs
):

 self._model =model
 self.api_key =api_key or os.environ.get("OPENAI_API_KEY")
 self.base_url =base_url or os.environ.get("OPENAI_BASE_URL")
 self.temperature =temperature

 self.client =OpenAI(
 api_key =self.api_key,
 base_url =self.base_url,
 timeout =timeout,
 max_retries =max_retries,
)
 self.aclient =AsyncOpenAI(
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
 return "openai"

 def _is_reasoning_model(self)->bool:

 return self._model.startswith(self.REASONING_PATTERNS)

 def _convert_messages(self, messages:List[BaseMessage])->List[dict]:

 openai_messages =[]
 for msg in messages:
 if isinstance(msg, SystemMessage):
 openai_messages.append({"role":"system", "content":msg.content })
 elif isinstance(msg, HumanMessage):
 openai_messages.append({"role":"user", "content":msg.content })
 elif isinstance(msg, ImageMessage):
 content_list =[]
 if msg.content:
 content_list.append({"type":"text", "text":msg.content })

 b64_imgs =msg.convert_images(format ="base64")
 for b64 in b64_imgs:
 content_list.append({
 "type":"image_url",
 "image_url":{"url":f"data:{msg.mime_type }; base64, {b64 }"}
 })
 openai_messages.append({"role":"user", "content":content_list })
 elif isinstance(msg, AIMessage):

 content =msg.content
 msg_dict:dict ={"role":"assistant", "content":content }

 tool_call =getattr(msg, "tool_call", None)
 if tool_call:
 msg_dict["tool_calls"]=[{
 "id":tool_call.id,
 "type":"function",
 "function":{
 "name":tool_call.name,
 "arguments":json.dumps(tool_call.params)
 }
 }]

 if self._is_reasoning_model()and getattr(msg, "thinking", None):
 msg_dict["reasoning_content"]=msg.thinking

 if content is None and not tool_call and not getattr(msg, "thinking", None):
 continue

 openai_messages.append(msg_dict)
 elif isinstance(msg, ToolMessage):

 last_msg =openai_messages[-1]if openai_messages else None
 if last_msg and last_msg.get("role")=="assistant"and last_msg.get("tool_calls"):

 if last_msg["tool_calls"][0]["id"]==msg.id:

 openai_messages.append({
 "role":"tool",
 "tool_call_id":msg.id,
 "content":msg.content or ""
 })
 continue

 tool_call ={
 "id":msg.id,
 "type":"function",
 "function":{
 "name":msg.name,
 "arguments":json.dumps(msg.params)
 }
 }
 openai_messages.append({
 "role":"assistant",
 "content":None,
 "tool_calls":[tool_call]
 })
 openai_messages.append({
 "role":"tool",
 "tool_call_id":msg.id,
 "content":msg.content or ""
 })
 return openai_messages

 def _convert_tools(self, tools:List[Tool])->List[dict]:

 converted =[]
 for tool in tools:
 schema =tool.json_schema
 if "parameters"in schema and "properties"in schema["parameters"]:
 props =schema["parameters"]["properties"]

 schema["parameters"]["properties"]={
 k:v for k, v in props.items()
 if v.get("type")!="null"
 }
 converted.append({
 "type":"function",
 "function":schema
 })
 return converted

 def _process_response(self, response:Any)->LLMEvent:

 choice =response.choices[0]
 message =choice.message
 usage_data =response.usage

 thinking_tokens =None
 if hasattr(usage_data, "completion_tokens_details")and usage_data.completion_tokens_details:
 thinking_tokens =getattr(
 usage_data.completion_tokens_details, "reasoning_tokens", None
)or getattr(
 usage_data.completion_tokens_details, "thinking_tokens", None
)
 if thinking_tokens is not None:
 logger.debug(f"Reasoning tokens used: {thinking_tokens }")

 usage =TokenUsage(
 prompt_tokens =usage_data.prompt_tokens,
 completion_tokens =usage_data.completion_tokens,
 total_tokens =usage_data.total_tokens,
 thinking_tokens =thinking_tokens,
)

 thinking =None
 if self._is_reasoning_model():
 if hasattr(message, "reasoning_content"):
 thinking =message.reasoning_content
 elif hasattr(choice, "reasoning_content"):
 thinking =choice.reasoning_content

 thinking_obj =Thinking(content =thinking, signature =None)if thinking else None

 if message.tool_calls:
 tool_call =message.tool_calls[0]
 try:
 params =json.loads(tool_call.function.arguments)
 except json.JSONDecodeError:
 params ={}
 return LLMEvent(
 type =LLMEventType.TOOL_CALL,
 tool_call =ToolCall(
 id =tool_call.id,
 name =tool_call.function.name,
 params =params
),
 usage =usage
)
 return LLMEvent(type =LLMEventType.TEXT, content =message.content or "", thinking =thinking_obj, usage =usage)

 @overload
 def invoke(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
...

 def invoke(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
 openai_messages =self._convert_messages(messages)
 openai_tools =self._convert_tools(tools)if tools else None

 params ={
 "model":self._model,
 "messages":openai_messages,
 **self.kwargs
 }

 logger.info(f"[*] OpenAI LLM Request(invoke): model={self._model } base_url={self.base_url } tools={bool(openai_tools)}")

 if openai_tools:
 params["tools"]=openai_tools

 if self.temperature is not None and not self._is_reasoning_model():
 params["temperature"]=self.temperature

 if structured_output:

 response =self.client.beta.chat.completions.parse(
 **params,
 response_format =structured_output,
)

 thinking_tokens =None
 if hasattr(response.usage, "completion_tokens_details")and response.usage.completion_tokens_details:
 thinking_tokens =getattr(
 response.usage.completion_tokens_details, "reasoning_tokens", None
)or getattr(
 response.usage.completion_tokens_details, "thinking_tokens", None
)

 TokenUsage(
 prompt_tokens =response.usage.prompt_tokens,
 completion_tokens =response.usage.completion_tokens,
 total_tokens =response.usage.total_tokens,
 thinking_tokens =thinking_tokens,
)
 parsed =response.choices[0].message.parsed
 content =parsed.model_dump()if hasattr(parsed, "model_dump")else str(parsed)
 return LLMEvent(type =LLMEventType.TEXT, content =json.dumps(content)if isinstance(content, dict)else content)

 if json_mode:
 params["response_format"]={"type":"json_object"}

 response =self.client.chat.completions.create(**params)
 return self._process_response(response)

 @overload
 async def ainvoke(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
...

 async def ainvoke(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
 openai_messages =self._convert_messages(messages)
 openai_tools =self._convert_tools(tools)if tools else None

 params ={
 "model":self._model,
 "messages":openai_messages,
 **self.kwargs
 }

 logger.info(f"[*] OpenAI LLM Request(ainvoke): model={self._model } base_url={self.base_url } tools={bool(openai_tools)}")

 if openai_tools:
 params["tools"]=openai_tools

 if self.temperature is not None and not self._is_reasoning_model():
 params["temperature"]=self.temperature

 if structured_output:
 response =await self.aclient.beta.chat.completions.parse(
 **params,
 response_format =structured_output,
)

 thinking_tokens =None
 if hasattr(response.usage, "completion_tokens_details")and response.usage.completion_tokens_details:
 thinking_tokens =getattr(
 response.usage.completion_tokens_details, "reasoning_tokens", None
)or getattr(
 response.usage.completion_tokens_details, "thinking_tokens", None
)

 usage =TokenUsage(
 prompt_tokens =response.usage.prompt_tokens,
 completion_tokens =response.usage.completion_tokens,
 total_tokens =response.usage.total_tokens,
 thinking_tokens =thinking_tokens,
)
 parsed =response.choices[0].message.parsed
 content =parsed.model_dump()if hasattr(parsed, "model_dump")else str(parsed)
 return LLMEvent(type =LLMEventType.TEXT, content =json.dumps(content)if isinstance(content, dict)else content, usage =usage)

 if json_mode:
 params["response_format"]={"type":"json_object"}

 response =await self.aclient.chat.completions.create(**params)
 return self._process_response(response)

 @overload
 def stream(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->Iterator[LLMStreamEvent]:
...

 def stream(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->Iterator[LLMStreamEvent]:
 openai_messages =self._convert_messages(messages)
 openai_tools =self._convert_tools(tools)if tools else None

 params ={
 "model":self._model,
 "messages":openai_messages,
 "stream":True,
 "stream_options":{"include_usage":True },
 **self.kwargs
 }

 logger.info(f"[*] OpenAI LLM Request(stream): model={self._model } base_url={self.base_url } tools={bool(openai_tools)}")

 if openai_tools:
 params["tools"]=openai_tools

 if self.temperature is not None and not self._is_reasoning_model():
 params["temperature"]=self.temperature

 if json_mode:
 params["response_format"]={"type":"json_object"}

 response =self.client.chat.completions.create(**params)

 tool_call_id =None
 tool_call_name =None
 tool_call_args =""
 usage =None

 text_started =False
 think_started =False
 usage =None

 for chunk in response:
 if not chunk.choices:

 if chunk.usage:
 thinking_tokens =None
 if hasattr(chunk.usage, "completion_tokens_details")and chunk.usage.completion_tokens_details:
 thinking_tokens =getattr(
 chunk.usage.completion_tokens_details, "reasoning_tokens", None
)or getattr(
 chunk.usage.completion_tokens_details, "thinking_tokens", None
)

 usage =TokenUsage(
 prompt_tokens =chunk.usage.prompt_tokens,
 completion_tokens =chunk.usage.completion_tokens,
 total_tokens =chunk.usage.total_tokens,
 thinking_tokens =thinking_tokens,
)
 continue

 delta =chunk.choices[0].delta

 if self._is_reasoning_model()and hasattr(delta, "reasoning_content")and delta.reasoning_content:
 if not think_started:
 think_started =True
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_START)
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_DELTA, content =delta.reasoning_content)

 if delta.content:
 if think_started:
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_END)
 think_started =False
 if not text_started:
 text_started =True
 yield LLMStreamEvent(type =LLMStreamEventType.TEXT_START)
 yield LLMStreamEvent(type =LLMStreamEventType.TEXT_DELTA, content =delta.content)

 if hasattr(delta, 'tool_calls')and delta.tool_calls:
 tc_delta =delta.tool_calls[0]
 if tc_delta.id:
 tool_call_id =tc_delta.id

 if tc_delta.function:
 if tc_delta.function.name:
 tool_call_name =tc_delta.function.name
 if tc_delta.function.arguments:
 tool_call_args +=tc_delta.function.arguments

 if think_started:
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_END)

 if tool_call_id and tool_call_name:
 try:
 tool_params =json.loads(tool_call_args)
 except json.JSONDecodeError:
 tool_params ={}

 yield LLMStreamEvent(
 type =LLMStreamEventType.TOOL_CALL,
 tool_call =ToolCall(
 id =tool_call_id,
 name =tool_call_name,
 params =tool_params
),
 usage =usage
)
 elif text_started:
 yield LLMStreamEvent(type =LLMStreamEventType.TEXT_END, usage =usage)

 @overload
 async def astream(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->AsyncIterator[LLMStreamEvent]:
...

 async def astream(self, messages:list[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->AsyncIterator[LLMStreamEvent]:
 openai_messages =self._convert_messages(messages)
 openai_tools =self._convert_tools(tools)if tools else None

 params ={
 "model":self._model,
 "messages":openai_messages,
 "stream":True,
 "stream_options":{"include_usage":True },
 **self.kwargs
 }

 logger.info(f"[*] OpenAI LLM Request(astream): model={self._model } base_url={self.base_url } tools={bool(openai_tools)}")

 if openai_tools:
 params["tools"]=openai_tools

 if self.temperature is not None and not self._is_reasoning_model():
 params["temperature"]=self.temperature

 if json_mode:
 params["response_format"]={"type":"json_object"}

 response =await self.aclient.chat.completions.create(**params)

 tool_call_id =None
 tool_call_name =None
 tool_call_args =""
 usage =None

 text_started =False
 think_started =False

 async for chunk in response:
 if not chunk.choices:

 if chunk.usage:
 thinking_tokens =None
 if hasattr(chunk.usage, "completion_tokens_details")and chunk.usage.completion_tokens_details:
 thinking_tokens =getattr(
 chunk.usage.completion_tokens_details, "reasoning_tokens", None
)or getattr(
 chunk.usage.completion_tokens_details, "thinking_tokens", None
)

 usage =TokenUsage(
 prompt_tokens =chunk.usage.prompt_tokens,
 completion_tokens =chunk.usage.completion_tokens,
 total_tokens =chunk.usage.total_tokens,
 thinking_tokens =thinking_tokens,
)
 continue

 delta =chunk.choices[0].delta

 if self._is_reasoning_model()and hasattr(delta, "reasoning_content")and delta.reasoning_content:
 if not think_started:
 think_started =True
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_START)
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_DELTA, content =delta.reasoning_content)

 if delta.content:
 if think_started:
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_END)
 think_started =False
 if not text_started:
 text_started =True
 yield LLMStreamEvent(type =LLMStreamEventType.TEXT_START)
 yield LLMStreamEvent(type =LLMStreamEventType.TEXT_DELTA, content =delta.content)

 if hasattr(delta, 'tool_calls')and delta.tool_calls:
 tc_delta =delta.tool_calls[0]
 if tc_delta.id:
 tool_call_id =tc_delta.id

 if tc_delta.function:
 if tc_delta.function.name:
 tool_call_name =tc_delta.function.name
 if tc_delta.function.arguments:
 tool_call_args +=tc_delta.function.arguments

 if think_started:
 yield LLMStreamEvent(type =LLMStreamEventType.THINK_END)

 if tool_call_id and tool_call_name:
 try:
 tool_params =json.loads(tool_call_args)
 except json.JSONDecodeError:
 tool_params ={}

 yield LLMStreamEvent(
 type =LLMStreamEventType.TOOL_CALL,
 tool_call =ToolCall(
 id =tool_call_id,
 name =tool_call_name,
 params =tool_params
),
 usage =usage
)
 elif text_started:
 yield LLMStreamEvent(type =LLMStreamEventType.TEXT_END, usage =usage)

 def get_metadata(self)->Metadata:
 context_window =self.MODELS.get(self._model, 128000)
 return Metadata(
 name =self._model,
 context_window =context_window,
 owned_by ="openai"
)
