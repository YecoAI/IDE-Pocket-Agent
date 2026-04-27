import os
import logging
from typing import Optional, Any
from operator_use.providers.openai import ChatOpenAI
from openai import OpenAI, AsyncOpenAI, RateLimitError

logger =logging.getLogger(__name__)

class ChatGroq(ChatOpenAI):

 def __init__(
 self,
 model:str ="llama-3.3-70b-versatile",
 api_key:Optional[str]=None,
 base_url:Optional[str]="https://api.groq.com/openai/v1",
 timeout:float =600.0,
 max_retries:int =0,
 temperature:Optional[float]=None,
 **kwargs
):

 self.api_keys =[]
 for key_name in["GROQ_API_KEY", "GROQ_API_KEY2", "GROQ_API_KEY3", "GROQ_API_KEY4"]:
 val =os.environ.get(key_name)
 if val:
 self.api_keys.append(val)

 if api_key and api_key not in self.api_keys:
 self.api_keys.insert(0, api_key)

 if not self.api_keys:
 logger.warning("No Groq API keys found in environment.")
 self.api_keys =[None]

 self.current_key_index =0
 self.base_url =base_url
 self.timeout =timeout
 self.max_retries =max_retries

 super().__init__(
 model =model,
 api_key =self.api_keys[0],
 base_url =base_url,
 timeout =timeout,
 max_retries =0,
 temperature =temperature,
 **kwargs
)

 def _rotate_key(self):

 if len(self.api_keys)<=1:
 return False

 self.current_key_index =(self.current_key_index +1)%len(self.api_keys)
 new_key =self.api_keys[self.current_key_index]

 logger.info(f"[*] Groq Rate Limit reached. Rotating to API Key #{self.current_key_index +1 }")

 self.api_key =new_key
 self.client =OpenAI(
 api_key =new_key,
 base_url =self.base_url,
 timeout =self.timeout,
 max_retries =self.max_retries,
)
 self.aclient =AsyncOpenAI(
 api_key =new_key,
 base_url =self.base_url,
 timeout =self.timeout,
 max_retries =self.max_retries,
)
 return True

 async def ainvoke(self, *args, **kwargs)->Any:

 max_attempts =len(self.api_keys)
 for attempt in range(max_attempts):
 try:
 return await super().ainvoke(*args, **kwargs)
 except RateLimitError as e:
 if attempt <max_attempts -1 and self._rotate_key():
 continue
 raise e
 except Exception as e:

 if "rate_limit_exceeded"in str(e).lower()or "429"in str(e):
 if attempt <max_attempts -1 and self._rotate_key():
 continue
 raise e

 def invoke(self, *args, **kwargs)->Any:

 max_attempts =len(self.api_keys)
 for attempt in range(max_attempts):
 try:
 return super().invoke(*args, **kwargs)
 except RateLimitError as e:
 if attempt <max_attempts -1 and self._rotate_key():
 continue
 raise e
 except Exception as e:
 if "rate_limit_exceeded"in str(e).lower()or "429"in str(e):
 if attempt <max_attempts -1 and self._rotate_key():
 continue
 raise e
