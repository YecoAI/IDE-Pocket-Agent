import os
import logging
from typing import Optional
from operator_use.providers.openai.llm import ChatOpenAI

logger =logging.getLogger(__name__)

class ChatOllama(ChatOpenAI):
 def __init__(
 self,
 model:str ="llama3",
 base_url:str ="http://localhost:11434/v1",
 api_key:str ="ollama",
 timeout:float =600.0,
 max_retries:int =2,
 temperature:Optional[float]=None,
 **kwargs
):
 super().__init__(
 model =model,
 api_key =api_key,
 base_url =base_url,
 timeout =timeout,
 max_retries =max_retries,
 temperature =temperature,
 **kwargs
)

 @property
 def provider(self)->str:
 return "ollama"
