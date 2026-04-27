

def escape_text_for_sendkeys(text:str)->str:

 result =[]
 for ch in text:
 if ch =="{":
 result.append("{{}")
 elif ch =="}":
 result.append("{}}")
 elif ch =="\n":
 result.append("{Enter}")
 elif ch =="\t":
 result.append("{Tab}")
 elif ch =="\r":
 continue
 else:
 result.append(ch)
 return "".join(result)
