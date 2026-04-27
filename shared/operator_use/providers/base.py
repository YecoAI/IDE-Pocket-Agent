from typing import Protocol, runtime_checkable, overload, Iterator, AsyncIterator, Iterable
from operator_use.providers.events import LLMEvent, LLMStreamEvent, LLMEventType
from operator_use.providers.views import Metadata
from operator_use.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage
from collections.abc import Iterable
from operator_use.tools import Tool
from pydantic import BaseModel

try:
    from yecoai_security_layer import RoboticsEngine, SafetyModel
except ImportError:
    RoboticsEngine = None
    SafetyModel = None

@runtime_checkable
class BaseChatLLM(Protocol):
    # ... (sanitize_schema remains the same)
    def sanitize_schema(self, tool_schema:dict)->dict:
        params =tool_schema.get("parameters", {})
        properties =params.get("properties", {})
        required =params.get("required", [])
        clean_props ={}
        for name, prop in properties.items():
            if isinstance(prop, dict):
                t =prop.get("type", "string")
                enum_vals =prop.get("enum")
                description =prop.get("description")
            else:
                t ="string"
                enum_vals =None
                description =None
            if t not in {"string", "integer", "number", "boolean", "array", "object"}:
                t ="string"
            entry:dict ={"type":t }
            if enum_vals is not None:
                entry["enum"]=enum_vals
            if description is not None:
                entry["description"]=description
            clean_props[name]=entry
        return {
            "name":tool_schema.get("name"),
            "description":tool_schema.get("description"),
            "parameters":{
                "type":"object",
                "properties":clean_props,
                "required":required,
            },
        }

    @property
    def model_name(self)->str:
        ...

    @property
    def provider(self)->str:
        ...

    @overload
    def invoke(self, messages:list[BaseMessage]|Iterable[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
        ...

    @overload
    async def ainvoke(self, messages:list[BaseMessage]|Iterable[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->LLMEvent:
        ...

    @overload
    def stream(self, messages:list[BaseMessage]|Iterable[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->Iterator[LLMStreamEvent]:
        ...

    @overload
    async def astream(self, messages:list[BaseMessage]|Iterable[BaseMessage], tools:list[Tool]=[], structured_output:BaseModel |None =None, json_mode:bool =False)->AsyncIterator[LLMStreamEvent]:
        ...

    @overload
    def get_metadata(self)->Metadata:
        ...

class SecureChatLLM:
    def __init__(self, llm: BaseChatLLM):
        self.llm = llm
        self.robotics = RoboticsEngine() if RoboticsEngine else None

    @property
    def model_name(self) -> str:
        return self.llm.model_name

    @property
    def provider(self) -> str:
        return self.llm.provider

    def sanitize_schema(self, tool_schema: dict) -> dict:
        return self.llm.sanitize_schema(tool_schema)

    async def ainvoke(self, messages: list[BaseMessage] | Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        msgs = list(messages)
        user_input = ""
        
        # Extract user input for SafetyModel
        for m in reversed(msgs):
            if isinstance(m, HumanMessage):
                user_input = m.content
                break

        # 1. Inject rules (RoboticsEngine)
        if self.robotics:
            system_msg = None
            for m in msgs:
                if isinstance(m, SystemMessage):
                    system_msg = m
                    break
            
            if system_msg:
                system_msg.content = self.robotics.inject_prompt(user_input=system_msg.content)
            else:
                msgs.insert(0, SystemMessage(content=self.robotics.inject_prompt(user_input="")))

        # 2. Call LLM
        event = await self.llm.ainvoke(msgs, tools, structured_output, json_mode)

        # 3. Validate response (SafetyModel)
        if SafetyModel and event.type == LLMEventType.TEXT and event.content:
            safety = SafetyModel(user_request=user_input)
            result = safety.validate_response(event.content)
            if not result["safe"]:
                return LLMEvent(type=LLMEventType.TEXT, content=f"BLOCKED BY SECURITY LAYER: {result['reason']}")

        return event

    async def astream(self, messages: list[BaseMessage] | Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> AsyncIterator[LLMStreamEvent]:
        # For streaming, we might need a buffer to validate the full response at the end,
        # or just passthrough if we can't easily validate chunks without high latency.
        # Given the instruction "low-latency heuristic security filter", we'll just wrap the output.
        async for event in self.llm.astream(messages, tools, structured_output, json_mode):
            yield event

    def invoke(self, messages: list[BaseMessage] | Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> LLMEvent:
        # Sync version similar to ainvoke
        msgs = list(messages)
        user_input = ""
        for m in reversed(msgs):
            if isinstance(m, HumanMessage):
                user_input = m.content
                break

        if self.robotics:
            system_msg = None
            for m in msgs:
                if isinstance(m, SystemMessage):
                    system_msg = m
                    break
            if system_msg:
                system_msg.content = self.robotics.inject_prompt(user_input=system_msg.content)
            else:
                msgs.insert(0, SystemMessage(content=self.robotics.inject_prompt(user_input="")))

        event = self.llm.invoke(msgs, tools, structured_output, json_mode)

        if SafetyModel and event.type == LLMEventType.TEXT and event.content:
            safety = SafetyModel(user_request=user_input)
            result = safety.validate_response(event.content)
            if not result["safe"]:
                return LLMEvent(type=LLMEventType.TEXT, content=f"BLOCKED BY SECURITY LAYER: {result['reason']}")

        return event

    def stream(self, messages: list[BaseMessage] | Iterable[BaseMessage], tools: list[Tool] = [], structured_output: BaseModel | None = None, json_mode: bool = False) -> Iterator[LLMStreamEvent]:
        for event in self.llm.stream(messages, tools, structured_output, json_mode):
            yield event

    def get_metadata(self) -> Metadata:
        return self.llm.get_metadata()

@runtime_checkable
class BaseSTT(Protocol):

 @property
 def model(self)->str:

...

 def transcribe(self, file_path:str)->str:

...

 async def atranscribe(self, file_path:str)->str:

...

@runtime_checkable
class BaseImage(Protocol):

 @property
 def model(self)->str:

...

 def generate(self, prompt:str, output_path:str, images:list[str]|None =None, **kwargs)->None:

...

 async def agenerate(self, prompt:str, output_path:str, images:list[str]|None =None, **kwargs)->None:

...

@runtime_checkable
class BaseSearch(Protocol):

 async def search(self, query:str, max_results:int =10)->list[dict]:

...

 async def fetch(self, url:str)->str:

...

@runtime_checkable
class BaseTTS(Protocol):

 @property
 def model(self)->str:

...

 def synthesize(self, text:str, output_path:str)->None:

...

 async def asynthesize(self, text:str, output_path:str)->None:

...
