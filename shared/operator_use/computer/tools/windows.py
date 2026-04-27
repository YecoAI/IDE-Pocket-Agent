import asyncio
import json
from typing import Literal, Optional
from pydantic import BaseModel, Field, model_validator
from operator_use.tools import Tool, ToolResult
from operator_use.computer.windows import uia, vdm

KEY_ALIASES = {
 "backspace": "Back",
 "capslock": "Capital",
 "scrolllock": "Scroll",
 "windows": "Win",
 "win": "Win",
 "command": "Win",
 "option": "Alt",
}

class ComputerTool(BaseModel):
 action: Literal["click", "type", "scroll", "move", "shortcut", "wait", "desktop"] = Field(
...,
 description=(
 "Computer action to perform:\n"
 " click — Click at(loc) coordinates. Single, double, right-click, or hover.\n"
 " type — Click at(loc) then type text. Handles focus, clear, and Enter automatically. If loc is omitted, types at current focus.\n"
 " scroll — Scroll at(loc) or current cursor position. Vertical or horizontal.\n"
 " move — Move cursor to(loc) or drag from current position to(loc).\n"
 " shortcut — Press a keyboard shortcut, e.g. 'ctrl+c', 'alt+tab', 'enter', 'win'. Use duration(ms) to hold keys.\n"
 " wait — Pause for a number of seconds before the next action.\n"
 " desktop — Manage Windows virtual desktops: create, remove, rename, or switch.\n"
),
)

 loc: Optional[list[int]] = Field(
 default=None,
 description="[x, y] pixel coordinates from the Interactive Elements list. Required for click, move. Optional for type(omit to type at current focus) and scroll(omit to scroll at current cursor).",
 examples=[[640, 360], [100, 200]],
)

 button: Literal["left", "right", "middle"] = Field(
 default="left",
 description="Mouse button: 'left' for standard clicks, 'right' for context menus, 'middle' for middle-click(action=click).",
)
 clicks: int = Field(
 default=1,
 description="Number of clicks: 1=single click, 2=double click(open files/folders), 0=hover only(action=click).",
 examples=[1, 2],
)

 text: Optional[str] = Field(
 default=None,
 description="Text to type into the focused field(action=type).",
 examples=["hello world", "user@example.com"],
)
 clear: bool = Field(
 default=False,
 description="Select all and replace existing text before typing(action=type).",
)
 caret_position: Literal["start", "idle", "end"] = Field(
 default="idle",
 description="Where to position the cursor before typing: 'start', 'end', or 'idle' (leave as-is) (action=type).",
)
 press_enter: bool = Field(
 default=False,
 description="Press Enter after typing to submit the input(action=type).",
)

 axis: Literal["vertical", "horizontal"] = Field(
 default="vertical",
 description="Scroll axis: 'vertical' for up/down, 'horizontal' for left/right(action=scroll).",
)
 direction: Literal["up", "down", "left", "right"] = Field(
 default="down",
 description="Scroll direction. Use up/down for vertical, left/right for horizontal(action=scroll).",
)
 wheel_times: int = Field(
 default=1,
 description="Number of scroll increments. Each scrolls ~3-5 lines. Use 3-5 for moderate, 10+ for large jumps(action=scroll).",
 examples=[1, 3, 5, 10],
)

 drag: bool = Field(
 default=False,
 description="Hold left mouse button and drag from current position to loc(action=move). False = move/hover only.",
)

 shortcut: Optional[str] = Field(
 default=None,
 description="Keyboard shortcut using '+' to combine keys(action=shortcut). Use duration to hold the shortcut for X milliseconds. Examples: 'ctrl+c', 'alt+tab', 'win', 'enter', 'up'.",
 examples=["ctrl+c", "ctrl+v", "alt+tab", "win", "enter", "up"],
)

 duration: Optional[int] = Field(
 default=None,
 description="Time in milliseconds to hold keys(action=shortcut) or seconds to pause(action=wait).",
 examples=[1000, 2, 5, 10],
)

 desktop_action: Literal["create", "remove", "rename", "switch"] = Field(
 default="switch",
 description="Virtual desktop operation: 'create' new, 'remove' existing, 'rename', or 'switch' focus(action=desktop).",
)
 desktop_name: Optional[str] = Field(
 default=None,
 description="Name of the desktop to switch to, remove, or rename(action=desktop).",
)
 new_name: Optional[str] = Field(
 default=None,
 description="New name for the desktop(action=desktop, desktop_action=rename).",
)

 @model_validator(mode="before")
 @classmethod
 def _remove_empty_strings(cls, data: dict) -> dict:
 if not isinstance(data, dict):
 return data
 return {k: v for k, v in data.items() if v is not None and v != ""}

 @model_validator(mode="before")
 @classmethod
 def _coerce_params(cls, data: dict) -> dict:
 if not isinstance(data, dict):
 return data

 for field in("loc", ):
 v = data.get(field)
 if v is None or v == "null":
 data[field] = None
 elif isinstance(v, str):
 try:
 parsed = json.loads(v)
 if isinstance(parsed, list):
 data[field] = parsed
 except(json.JSONDecodeError, ValueError):
 pass

 for field in("clear", "press_enter", "drag"):
 v = data.get(field)
 if isinstance(v, str):
 data[field] = v.lower() not in("false", "0", "no", "null", "none", "")

 for field in("clicks", "wheel_times"):
 v = data.get(field)
 if isinstance(v, str):
 try:
 data[field] = int(v)
 except(ValueError, TypeError):
 pass

 for field in("duration", ):
 v = data.get(field)
 if v is None or v == "null":
 data[field] = None
 elif isinstance(v, str):
 try:
 data[field] = int(v)
 except(ValueError, TypeError):
 pass

 for field in("shortcut", "text", "desktop_name", "new_name", "desktop_action"):
 v = data.get(field)
 if v == "null":
 data[field] = None
 return data

@Tool(
 name="computer",
 description=(
 "Control the Windows desktop. "
 "The current desktop state(active window, open windows, interactive elements with coordinates, scrollable elements) "
 "is provided automatically before each call — use element coordinates from the state for click, type, scroll, and move."
),
 model=ComputerTool,
)
async def computer(
 action: str,
 loc: Optional[list[int]] = None,
 button: str = "left",
 clicks: int = 1,
 text: Optional[str] = None,
 clear: bool = False,
 caret_position: str = "idle",
 press_enter: bool = False,
 axis: str = "vertical",
 direction: str = "down",
 wheel_times: int = 1,
 drag: bool = False,
 shortcut: Optional[str] = None,
 duration: Optional[int] = None,
 desktop_action: Optional[str] = None,
 desktop_name: Optional[str] = None,
 new_name: Optional[str] = None,
 **kwargs,
) -> ToolResult:
 match action:
 case "click":
 if not loc:
 return ToolResult.error_result("loc is required for click.")
 x, y = loc[0], loc[1]
 if clicks == 0:
 uia.SetCursorPos(x, y)
 return ToolResult.success_result(f"Moved cursor to({x}, {y}).")
 match button:
 case "left":
 if clicks >= 2:
 uia.DoubleClick(x, y)
 else:
 uia.Click(x, y)
 case "right":
 uia.RightClick(x, y)
 case "middle":
 uia.MiddleClick(x, y)
 labels = {1: "Single", 2: "Double", 3: "Triple"}
 return ToolResult.success_result(f"{labels.get(clicks, str(clicks))} {button} clicked at({x}, {y}).")

 case "type":
 if text is None:
 return ToolResult.error_result("text is required for type.")
 if loc:
 x, y = loc[0], loc[1]
 uia.Click(x, y)
 log_msg = f"Typed at({x}, {y})."
 else:
 log_msg = "Typed at current focus."
 if caret_position == "start":
 uia.SendKeys("{Home}", waitTime=0.05)
 elif caret_position == "end":
 uia.SendKeys("{End}", waitTime=0.05)
 if clear:
 await asyncio.sleep(0.5)
 uia.SendKeys("{Ctrl}a", waitTime=0.05)
 uia.SendKeys("{Back}", waitTime=0.05)
 escaped = uia._escape_text_for_sendkeys(text)
 uia.SendKeys(escaped, interval=0.01, waitTime=0.05)
 if press_enter:
 uia.SendKeys("{Enter}", waitTime=0.05)
 return ToolResult.success_result(log_msg)

 case "scroll":
 if loc:
 uia.MoveTo(loc[0], loc[1])
 match axis:
 case "vertical":
 if direction == "up":
 uia.WheelUp(wheel_times)
 elif direction == "down":
 uia.WheelDown(wheel_times)
 else:
 return ToolResult.error_result('Invalid direction for vertical scroll. Use "up" or "down".')
 case "horizontal":
 if direction == "left":
 uia.WheelLeft(wheel_times)
 elif direction == "right":
 uia.WheelRight(wheel_times)
 else:
 return ToolResult.error_result('Invalid direction for horizontal scroll. Use "left" or "right".')
 case _:
 return ToolResult.error_result('Invalid axis. Use "vertical" or "horizontal".')
 return ToolResult.success_result(f"Scrolled {axis} {direction} by {wheel_times}.")

 case "move":
 if not loc:
 return ToolResult.error_result("loc is required for move.")
 x, y = loc[0], loc[1]
 if drag:
 cx, cy = uia.GetCursorPos()
 uia.DragTo(cx, cy, x, y)
 return ToolResult.success_result(f"Dragged to({x}, {y}).")
 uia.MoveTo(x, y, moveSpeed=10)
 return ToolResult.success_result(f"Moved to({x}, {y}).")

 case "shortcut":
 if not shortcut:
 return ToolResult.error_result("shortcut is required for shortcut.")

 if duration and duration > 0:
 keys = shortcut.split("+")
 vk_keys = []
 for key in keys:
 key = key.strip().lower()
 name = KEY_ALIASES.get(key, key).upper()
 if name in uia.SpecialKeyNames:
 vk_keys.append(uia.SpecialKeyNames[name])
 elif len(key) == 1 and key.upper() in uia.CharacterCodes:
 vk_keys.append(uia.CharacterCodes[key.upper()])
 else:
 vk_keys = []
 break

 if vk_keys:
 for vk in vk_keys:
 uia.keybd_event(vk, 0, uia.KeyboardEventFlag.KeyDown | uia.KeyboardEventFlag.ExtendedKey, 0)

 await asyncio.sleep(duration / 1000.0)

 for vk in reversed(vk_keys):
 uia.keybd_event(vk, 0, uia.KeyboardEventFlag.KeyUp | uia.KeyboardEventFlag.ExtendedKey, 0)
 return ToolResult.success_result(f"Pressed shortcut: {shortcut} for {duration}ms")
 else:
 return ToolResult.error_result(f"Failed to parse shortcut: {shortcut}")
 else:
 uia.SendKeys(f"{{{shortcut}}}" if "+" not in shortcut and shortcut.upper() in uia.SpecialKeyNames else shortcut)
 return ToolResult.success_result(f"Pressed shortcut: {shortcut}")

 case _:
 return ToolResult.error_result(f"Unknown action: {action}")
