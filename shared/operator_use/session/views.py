

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from operator_use.messages.service import BaseMessage

@dataclass
class Session:

 id:str
 messages:list[BaseMessage]=field(default_factory =list)
 created_at:datetime =field(default_factory =datetime.now)
 updated_at:datetime =field(default_factory =datetime.now)
 metadata:dict[str, Any]=field(default_factory =dict)

 def add_message(self, message:BaseMessage)->None:

 self.messages.append(message)
 self.updated_at =datetime.now()

 def get_history(self)->list[BaseMessage]:

 return list(self.messages)

 def clear(self)->None:

 self.messages.clear()
 self.updated_at =datetime.now()
