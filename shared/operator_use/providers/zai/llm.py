import os
from operator_use.providers.openai.llm import ChatOpenAI

ZAI_BASE_URL = "https://api.z.ai/api/paas/v4/"

class ChatZAI(ChatOpenAI):
 MODELS = {
 "glm-4": 128000,
 "glm-4-plus": 128000,
 "glm-4-air": 128000,
 "glm-4-airx": 128000,
 "glm-4-flash": 128000,
 "glm-4-flashx": 128000,
 "glm-4v": 8192,
 "glm-4v-flash": 8192,
 "glm-4.6v-flashx": 128000,
 "glm-4.7-flashx": 128000,
 "glm-5-turbo": 128000,
 "glm-5v-turbo": 128000,
 }

 def __init__(self, model: str, api_key: str | None = None, base_url: str | None = None, reasoning: bool = False, **kwargs):
 api_key = api_key or os.environ.get("ZAI_API_KEY") or os.environ.get("ZHIPUAI_API_KEY")
 base_url = base_url or ZAI_BASE_URL
 self.reasoning = reasoning

 super().__init__(model=model, api_key=api_key, base_url=base_url, max_retries=0, **kwargs)

 def _is_reasoning_model(self) -> bool:
 return self.reasoning

 @property
 def provider(self) -> str:
 return "zai"
