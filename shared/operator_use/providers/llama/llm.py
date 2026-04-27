import logging
from typing import Optional
from operator_use.providers.openai.llm import ChatOpenAI

class ChatLlama(ChatOpenAI):
 @property
 def provider(self)->str:
 return "llama"

class ChatQwen(ChatOpenAI):
 @property
 def provider(self)->str:
 return "qwen"
