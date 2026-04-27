

import os
import sys
import time
import datetime
import re
import ctypes
import comtypes
from typing import(Any, Callable, Generator, List, Optional, Tuple)
from.enums import *
from.core import *
from.core import _AutomationClient, IUIAutomationElement
from.patterns import *

METRO_WINDOW_CLASS_NAME ='Windows.UI.Core.CoreWindow'
SEARCH_INTERVAL =0.5
MAX_MOVE_SECOND =1
TIME_OUT_SECOND =10
OPERATION_WAIT_TIME =0.5
MAX_PATH =260
DEBUG_SEARCH_TIME =False
DEBUG_EXIST_DISAPPEAR =False
S_OK =0

IsPy38OrHigher =sys.version_info[:2]>=(3, 8)
IsNT6orHigher =os.sys.getwindowsversion().major >=6
CurrentProcessIs64Bit =sys.maxsize >0xFFFFFFFF
ProcessTime =time.perf_counter
ProcessTime()
TreeNode =Any

class Control():
 ValidKeys =set(['ControlType', 'ClassName', 'AutomationId', 'Name', 'SubName', 'RegexName', 'Depth', 'Compare'])

 def __init__(self, searchFromControl:Optional['Control']=None, searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL, foundIndex:int =1, element =None,
 ControlType:Optional[int]=None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):

 self._element =element
 self._elementDirectAssign =True if element else False
 self.searchFromControl =searchFromControl
 self.searchDepth =Depth or searchDepth
 self.searchInterval =searchInterval
 self.foundIndex =foundIndex
 self.searchProperties =searchProperties
 if Name is not None:
 searchProperties['Name']=Name
 if SubName is not None:
 searchProperties['SubName']=SubName
 if RegexName is not None:
 searchProperties['RegexName']=RegexName
 self.regexName =re.compile(RegexName)
 else:
 self.regexName =None
 if ClassName is not None:
 searchProperties['ClassName']=ClassName
 if AutomationId is not None:
 searchProperties['AutomationId']=AutomationId
 if ControlType is not None:
 searchProperties['ControlType']=ControlType
 if Depth is not None:
 searchProperties['Depth']=Depth
 if Compare is not None:
 searchProperties['Compare']=Compare
 self._supportedPatterns ={}

 def __str__(self)->str:
 return 'ControlType: {0} ClassName: {1} AutomationId: {2} Rect: {3} Name: {4} Handle: 0x{5:X}({5})'.format(
 self.ControlTypeName, self.ClassName, self.AutomationId, self.BoundingRectangle, self.Name, self.NativeWindowHandle)

 def __repr__(self)->str:
 return '<{0} ClassName={1!r} AutomationId={2} Rect={3} Name={4!r} Handle=0x{5:X}({5})>'.format(
 self.__class__.__name__, self.ClassName, self.AutomationId, self.BoundingRectangle, self.Name, self.NativeWindowHandle)

 def __getitem__(self, pos:int)->Optional['Control']:
 if pos ==1:
 return self.GetFirstChildControl()
 elif pos ==-1:
 return self.GetLastChildControl()
 elif pos >1:
 child =self.GetFirstChildControl()
 for _ in range(pos -1):
 if child is None:
 return None
 child =child.GetNextSiblingControl()
 return child
 elif pos <-1:
 child =self.GetLastChildControl()
 for _ in range(-pos -1):
 if child is None:
 return None
 child =child.GetPreviousSiblingControl()
 return child
 else:
 raise ValueError

 @staticmethod
 def CreateControlFromElement(element:ctypes.POINTER(IUIAutomationElement))->Optional["Control"]:

 if element:
 controlType =element.CurrentControlType
 if controlType in ControlConstructors:
 return ControlConstructors[controlType](element =element)
 return None

 @staticmethod
 def CreateControlsFromRawElementArray(raw_pointer)->List['Control']:

 if not raw_pointer:
 return[]
 try:
 ele_array =raw_pointer.QueryInterface(
 _AutomationClient.instance().UIAutomationCore.IUIAutomationElementArray
)
 controls =[]
 for i in range(ele_array.Length):
 ele =ele_array.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 except Exception:
 return[]

 @staticmethod
 def CreateControlFromControl(control:'Control')->Optional['Control']:

 newControl =Control.CreateControlFromElement(control.Element)
 return newControl

 def SetSearchFromControl(self, searchFromControl:'Control')->None:

 self.searchFromControl =searchFromControl

 def SetSearchDepth(self, searchDepth:int)->None:
 self.searchDepth =searchDepth

 def AddSearchProperties(self, **searchProperties)->None:

 self.searchProperties.update(searchProperties)
 if 'Depth'in searchProperties:
 self.searchDepth =searchProperties['Depth']
 if 'RegexName'in searchProperties:
 regName =searchProperties['RegexName']
 self.regexName =re.compile(regName)if regName else None

 def RemoveSearchProperties(self, **searchProperties)->None:

 for key in searchProperties:
 del self.searchProperties[key]
 if key =='RegexName':
 self.regexName =None

 def GetSearchPropertiesStr(self)->str:
 strs =['{}: {}'.format(k, ControlTypeNames[v]if k =='ControlType'else repr(v))for k, v in self.searchProperties.items()]
 return '{'+', '.join(strs)+'}'

 def GetColorfulSearchPropertiesStr(self, keyColor ='DarkGreen', valueColor ='DarkCyan')->str:

 strs =['<Color={}>{}</Color>: <Color={}>{}</Color>'.format(keyColor if k in Control.ValidKeys else 'DarkYellow', k, valueColor,
 ControlTypeNames[v]if k =='ControlType'else repr(v))for k, v in self.searchProperties.items()]
 return '{'+', '.join(strs)+'}'

 def BuildUpdatedCache(self, cacheRequest:'CacheRequest')->'Control':

 updatedElement =self.Element.BuildUpdatedCache(cacheRequest.check_request)
 return Control.CreateControlFromElement(updatedElement)

 @property
 def CachedAcceleratorKey(self)->str:

 return self.Element.CachedAcceleratorKey

 @property
 def CachedAccessKey(self)->str:

 return self.Element.CachedAccessKey

 @property
 def CachedAriaProperties(self)->str:

 return self.Element.CachedAriaProperties

 @property
 def CachedAriaRole(self)->str:

 return self.Element.CachedAriaRole

 @property
 def CachedAutomationId(self)->str:

 return self.Element.CachedAutomationId

 @property
 def CachedBoundingRectangle(self)->Rect:

 rect =self.Element.CachedBoundingRectangle
 return Rect(rect.left, rect.top, rect.right, rect.bottom)

 @property
 def CachedClassName(self)->str:

 return self.Element.CachedClassName

 @property
 def CachedControlType(self)->int:

 return self.Element.CachedControlType

 @property
 def CachedControlTypeName(self)->str:

 try:
 return ControlTypeNames.get(self.CachedControlType, "Unknown")
 except:
 return "Unknown"

 @property
 def CachedControllerFor(self)->Any:

 return self.Element.CachedControllerFor

 @property
 def CachedCulture(self)->int:

 return self.Element.CachedCulture

 @property
 def CachedDescribedBy(self)->Any:

 return self.Element.CachedDescribedBy

 @property
 def CachedFlowsTo(self)->Any:

 return self.Element.CachedFlowsTo

 @property
 def CachedFrameworkId(self)->str:

 return self.Element.CachedFrameworkId

 @property
 def CachedHasKeyboardFocus(self)->bool:

 return self.Element.CachedHasKeyboardFocus

 @property
 def CachedHelpText(self)->str:

 return self.Element.CachedHelpText

 @property
 def CachedIsContentElement(self)->bool:

 return self.Element.CachedIsContentElement

 @property
 def CachedIsControlElement(self)->bool:

 return self.Element.CachedIsControlElement

 @property
 def CachedIsDataValidForForm(self)->bool:

 return self.Element.CachedIsDataValidForForm

 @property
 def CachedIsEnabled(self)->bool:

 return self.Element.CachedIsEnabled

 @property
 def CachedIsKeyboardFocusable(self)->bool:

 return self.Element.CachedIsKeyboardFocusable

 @property
 def CachedIsOffscreen(self)->bool:

 return self.Element.CachedIsOffscreen

 @property
 def CachedIsPassword(self)->bool:

 return self.Element.CachedIsPassword

 @property
 def CachedIsRequiredForForm(self)->bool:

 return self.Element.CachedIsRequiredForForm

 @property
 def CachedItemStatus(self)->str:

 return self.Element.CachedItemStatus

 @property
 def CachedItemType(self)->str:

 return self.Element.CachedItemType

 @property
 def CachedLabeledBy(self)->Any:

 return self.Element.CachedLabeledBy

 @property
 def CachedLocalizedControlType(self)->str:

 return self.Element.CachedLocalizedControlType

 @property
 def CachedName(self)->str:

 return self.Element.CachedName

 @property
 def CachedNativeWindowHandle(self)->int:

 return self.Element.CachedNativeWindowHandle

 @property
 def CachedOrientation(self)->int:

 return self.Element.CachedOrientation

 @property
 def CachedProcessId(self)->int:

 return self.Element.CachedProcessId

 @property
 def CachedProviderDescription(self)->str:

 return self.Element.CachedProviderDescription

 @property
 def AcceleratorKey(self)->str:

 return self.Element.CurrentAcceleratorKey

 @property
 def AccessKey(self)->str:

 return self.Element.CurrentAccessKey

 @property
 def AriaProperties(self)->str:

 return self.Element.CurrentAriaProperties

 @property
 def AriaRole(self)->str:

 return self.Element.CurrentAriaRole

 @property
 def AutomationId(self)->str:

 return self.Element.CurrentAutomationId

 @property
 def BoundingRectangle(self)->Rect:

 rect =self.Element.CurrentBoundingRectangle
 return Rect(rect.left, rect.top, rect.right, rect.bottom)

 def contains(self, other:'Control')->bool:

 self_rect =self.BoundingRectangle
 other_rect =other.BoundingRectangle
 return self_rect.intersect(other_rect)==other_rect

 @property
 def ClassName(self)->str:

 return self.Element.CurrentClassName

 @property
 def ControlType(self)->int:

 return self.Element.CurrentControlType

 @property
 def Culture(self)->int:

 return self.Element.CurrentCulture

 @property
 def FrameworkId(self)->str:

 return self.Element.CurrentFrameworkId

 @property
 def HasKeyboardFocus(self)->bool:

 return bool(self.Element.CurrentHasKeyboardFocus)

 @property
 def HelpText(self)->str:

 return self.Element.CurrentHelpText

 @property
 def IsContentElement(self)->bool:

 return bool(self.Element.CurrentIsContentElement)

 @property
 def IsControlElement(self)->bool:

 return bool(self.Element.CurrentIsControlElement)

 @property
 def IsDataValidForForm(self)->bool:

 return bool(self.Element.CurrentIsDataValidForForm)

 @property
 def IsEnabled(self)->bool:

 return bool(self.Element.CurrentIsEnabled)

 @property
 def IsKeyboardFocusable(self)->bool:

 return bool(self.Element.CurrentIsKeyboardFocusable)

 @property
 def IsOffscreen(self)->bool:

 return bool(self.Element.CurrentIsOffscreen)

 @property
 def IsPassword(self)->bool:

 return bool(self.Element.CurrentIsPassword)

 @property
 def IsRequiredForForm(self)->bool:

 return bool(self.Element.CurrentIsRequiredForForm)

 @property
 def ItemStatus(self)->str:

 return self.Element.CurrentItemStatus

 @property
 def ItemType(self)->str:

 return self.Element.CurrentItemType

 @property
 def LocalizedControlType(self)->str:

 return self.Element.CurrentLocalizedControlType

 @property
 def Name(self)->str:

 return self.Element.CurrentName or ''

 @property
 def NativeWindowHandle(self)->int:

 try:
 handle =self.Element.CurrentNativeWindowHandle
 except comtypes.COMError:
 return 0
 return 0 if handle is None else handle

 @property
 def Orientation(self)->int:

 return self.Element.CurrentOrientation

 @property
 def ProcessId(self)->int:

 return self.Element.CurrentProcessId

 @property
 def ProviderDescription(self)->str:

 return self.Element.CurrentProviderDescription

 def FindAll(self, scope:int, condition)->List['Control']:

 elementArray =self.Element.FindAll(scope, condition)
 if not elementArray:
 return[]

 controls =[]
 length =elementArray.Length
 for i in range(length):
 element =elementArray.GetElement(i)
 control =Control.CreateControlFromElement(element)
 if control:
 controls.append(control)
 return controls

 def FindAllBuildCache(self, scope:int, condition, cacheRequest:'CacheRequest')->List['Control']:

 elementArray =self.Element.FindAllBuildCache(scope, condition, cacheRequest.check_request)
 if not elementArray:
 return[]

 controls =[]
 length =elementArray.Length
 for i in range(length):
 element =elementArray.GetElement(i)
 control =Control.CreateControlFromElement(element)
 if control:
 controls.append(control)
 return controls

 def FindFirst(self, scope:int, condition)->Optional['Control']:

 element =self.Element.FindFirst(scope, condition)
 return Control.CreateControlFromElement(element)

 def FindFirstBuildCache(self, scope:int, condition, cacheRequest:'CacheRequest')->Optional['Control']:

 element =self.Element.FindFirstBuildCache(scope, condition, cacheRequest.check_request)
 return Control.CreateControlFromElement(element)

 def GetCachedChildren(self)->List['Control']:

 try:
 elementArray =self.Element.GetCachedChildren()
 if not elementArray:
 return[]

 controls =[]
 length =elementArray.Length
 for i in range(length):
 element =elementArray.GetElement(i)
 control =Control.CreateControlFromElement(element)
 if control:
 controls.append(control)
 return controls
 except comtypes.COMError:
 return[]

 def GetCachedParent(self)->Optional['Control']:

 try:
 element =self.Element.GetCachedParent()
 return Control.CreateControlFromElement(element)
 except comtypes.COMError:
 return None

 def GetCachedPattern(self, patternId:int):

 try:
 pattern =self.Element.GetCachedPattern(patternId)
 if pattern:
 return CreatePattern(patternId, pattern)
 except comtypes.COMError:
 return None

 def GetCachedPatternAs(self, patternId:int, riid):

 try:
 return self.Element.GetCachedPatternAs(patternId, riid)
 except comtypes.COMError:
 return None

 def GetCachedPropertyValue(self, propertyId:int)->Any:

 try:
 return self.Element.GetCachedPropertyValue(propertyId)
 except comtypes.COMError:
 return None

 def GetCachedPropertyValueEx(self, propertyId:int, ignoreDefaultValue:int)->Any:

 try:
 return self.Element.GetCachedPropertyValueEx(propertyId, ignoreDefaultValue)
 except comtypes.COMError:
 return None

 def GetClickablePoint(self)->Tuple[int, int, bool]:

 point, gotClickable =self.Element.GetClickablePoint()
 return(point.x, point.y, bool(gotClickable))

 def GetPattern(self, patternId:int):

 try:
 pattern =self.Element.GetCurrentPattern(patternId)
 if pattern:
 subPattern =CreatePattern(patternId, pattern)
 self._supportedPatterns[patternId]=subPattern
 return subPattern
 except comtypes.COMError:
 pass

 def GetPatternAs(self, patternId:int, riid):

 return self.Element.GetCurrentPatternAs(patternId, riid)

 def GetPropertyValue(self, propertyId:int)->Any:

 return self.Element.GetCurrentPropertyValue(propertyId)

 def GetPropertyValueEx(self, propertyId:int, ignoreDefaultValue:int)->Any:

 return self.Element.GetCurrentPropertyValueEx(propertyId, ignoreDefaultValue)

 def GetRuntimeId(self)->List[int]:

 return self.Element.GetRuntimeId()

 def SetFocus(self)->bool:

 try:
 return self.Element.SetFocus()==S_OK
 except comtypes.COMError:
 return False

 @property
 def Element(self):

 if not self._element:
 self.Refind(maxSearchSeconds =TIME_OUT_SECOND, searchIntervalSeconds =self.searchInterval)
 return self._element

 @property
 def ControlTypeName(self)->str:

 return ControlTypeNames[self.ControlType]

 def GetCachedPattern(self, patternId:int, cache:bool):

 if cache:
 pattern =self._supportedPatterns.get(patternId, None)
 if pattern:
 return pattern
 else:
 pattern =self.GetPattern(patternId)
 if pattern:
 self._supportedPatterns[patternId]=pattern
 return pattern
 else:
 pattern =self.GetPattern(patternId)
 if pattern:
 self._supportedPatterns[patternId]=pattern
 return pattern

 def GetLegacyIAccessiblePattern(self)->LegacyIAccessiblePattern:

 return self.GetPattern(PatternId.LegacyIAccessiblePattern)

 def GetAncestorControl(self, condition:Callable[['Control', int], bool])->Optional['Control']:

 ancestor =self
 depth =0
 while ancestor is not None:
 ancestor =ancestor.GetParentControl()
 depth -=1
 if ancestor:
 if condition(ancestor, depth):
 return ancestor
 return None

 def GetParentControl(self)->Optional['Control']:

 ele =_AutomationClient.instance().ViewWalker.GetParentElement(self.Element)
 return Control.CreateControlFromElement(ele)

 def GetFirstChildControl(self)->Optional['Control']:

 ele =_AutomationClient.instance().ViewWalker.GetFirstChildElement(self.Element)
 return Control.CreateControlFromElement(ele)

 def GetLastChildControl(self)->Optional['Control']:

 ele =_AutomationClient.instance().ViewWalker.GetLastChildElement(self.Element)
 return Control.CreateControlFromElement(ele)

 def GetNextSiblingControl(self)->Optional['Control']:

 ele =_AutomationClient.instance().ViewWalker.GetNextSiblingElement(self.Element)
 return Control.CreateControlFromElement(ele)

 def GetPreviousSiblingControl(self)->Optional['Control']:

 ele =_AutomationClient.instance().ViewWalker.GetPreviousSiblingElement(self.Element)
 return Control.CreateControlFromElement(ele)

 def GetSiblingControl(self, condition:Callable[['Control'], bool], forward:bool =True)->Optional['Control']:

 if not forward:
 prev =self
 while True:
 prev =prev.GetPreviousSiblingControl()
 if prev:
 if condition(prev):
 return prev
 else:
 break
 next_ =self
 while True:
 next_ =next_.GetNextSiblingControl()
 if next_:
 if condition(next_):
 return next_
 else:
 break

 def GetChildren(self)->List['Control']:

 children =[]
 child =self.GetFirstChildControl()
 while child:
 children.append(child)
 child =child.GetNextSiblingControl()
 return children

 def _CompareFunction(self, control:'Control', depth:int)->bool:

 compareFunc =None
 for key, value in self.searchProperties.items():
 if 'ControlType'==key:
 if value !=control.ControlType:
 return False
 elif 'ClassName'==key:
 if value !=control.ClassName:
 return False
 elif 'AutomationId'==key:
 if value !=control.AutomationId:
 return False
 elif 'Depth'==key:
 if value !=depth:
 return False
 elif 'Name'==key:
 if value !=control.Name:
 return False
 elif 'SubName'==key:
 if value not in control.Name:
 return False
 elif 'RegexName'==key:
 if not self.regexName.match(control.Name):
 return False
 elif 'Compare'==key:
 compareFunc =value

 if compareFunc and not compareFunc(control, depth):
 return False
 return True

 def Exists(self, maxSearchSeconds:float =5, searchIntervalSeconds:float =SEARCH_INTERVAL, printIfNotExist:bool =False)->bool:

 if self._element and self._elementDirectAssign:

 rootElement =_AutomationClient.instance().IUIAutomation.GetRootElement()
 if _AutomationClient.instance().IUIAutomation.CompareElements(self._element, rootElement):
 return True
 else:
 parentElement =_AutomationClient.instance().ViewWalker.GetParentElement(self._element)
 if parentElement:
 return True
 else:
 return False

 if not self.searchProperties:
 raise LookupError("control's searchProperties must not be empty!")
 self._element =None
 startTime =ProcessTime()

 prev =self.searchFromControl
 if prev and not prev._element and not prev.Exists(maxSearchSeconds, searchIntervalSeconds):
 return False
 startTime2 =ProcessTime()
 if DEBUG_SEARCH_TIME:
 startDateTime =datetime.datetime.now()
 while True:
 control =FindControl(self.searchFromControl, self._CompareFunction, self.searchDepth, False, self.foundIndex)
 if control:
 self._element =control.Element
 control._element =0
 return True
 else:
 remain =startTime +maxSearchSeconds -ProcessTime()
 if remain >0:
 time.sleep(min(remain, searchIntervalSeconds))
 else:
 return False

 def Disappears(self, maxSearchSeconds:float =5, searchIntervalSeconds:float =SEARCH_INTERVAL, printIfNotDisappear:bool =False)->bool:

 global DEBUG_EXIST_DISAPPEAR
 start =ProcessTime()
 while True:
 temp =DEBUG_EXIST_DISAPPEAR
 DEBUG_EXIST_DISAPPEAR =False
 if not self.Exists(0, 0, False):
 DEBUG_EXIST_DISAPPEAR =temp
 return True
 DEBUG_EXIST_DISAPPEAR =temp
 remain =start +maxSearchSeconds -ProcessTime()
 if remain >0:
 time.sleep(min(remain, searchIntervalSeconds))
 else:
 return False

 def Refind(self, maxSearchSeconds:float =TIME_OUT_SECOND, searchIntervalSeconds:float =SEARCH_INTERVAL, raiseException:bool =True)->bool:

 if not self.Exists(maxSearchSeconds, searchIntervalSeconds, False if raiseException else DEBUG_EXIST_DISAPPEAR):
 if raiseException:
 raise LookupError('Find Control Timeout({}s): {}'.format(maxSearchSeconds, self.GetSearchPropertiesStr()))
 else:
 return False
 return True

 def GetPosition(self, ratioX:float =0.5, ratioY:float =0.5)->Optional[Tuple[int, int]]:

 rect =self.BoundingRectangle
 if rect.width()==0 or rect.height()==0:
 return None
 x =rect.left +int(rect.width()*ratioX)
 y =rect.top +int(rect.height()*ratioY)
 return x, y

 def MoveCursorToInnerPos(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, simulateMove:bool =True)->Optional[Tuple[int, int]]:

 rect =self.BoundingRectangle
 if rect.width()==0 or rect.height()==0:
 return None
 if x is None:
 x =rect.left +int(rect.width()*ratioX)
 else:
 x =(rect.left if x >=0 else rect.right)+x
 if y is None:
 y =rect.top +int(rect.height()*ratioY)
 else:
 y =(rect.top if y >=0 else rect.bottom)+y
 if simulateMove and MAX_MOVE_SECOND >0:
 MoveTo(x, y, waitTime =0)
 else:
 SetCursorPos(x, y)
 return x, y

 def MoveCursorToMyCenter(self, simulateMove:bool =True)->Optional[Tuple[int, int]]:

 return self.MoveCursorToInnerPos(simulateMove =simulateMove)

 def Click(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, simulateMove:bool =True, waitTime:float =OPERATION_WAIT_TIME)->None:

 point =self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove)
 if point:
 Click(point[0], point[1], waitTime)

 def MiddleClick(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, simulateMove:bool =True, waitTime:float =OPERATION_WAIT_TIME)->None:

 point =self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove)
 if point:
 MiddleClick(point[0], point[1], waitTime)

 def RightClick(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, simulateMove:bool =True, waitTime:float =OPERATION_WAIT_TIME)->None:

 point =self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove)
 if point:
 RightClick(point[0], point[1], waitTime)

 def DoubleClick(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, simulateMove:bool =True, waitTime:float =OPERATION_WAIT_TIME)->None:

 x, y =self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove)
 Click(x, y, GetDoubleClickTime()*1.0 /2000)
 Click(x, y, waitTime)

 def DragDrop(self, x1:int, y1:int, x2:int, y2:int, moveSpeed:float =1, waitTime:float =OPERATION_WAIT_TIME)->None:
 rect =self.BoundingRectangle
 if rect.width()==0 or rect.height()==0:
 return
 x1 =(rect.left if x1 >=0 else rect.right)+x1
 y1 =(rect.top if y1 >=0 else rect.bottom)+y1
 x2 =(rect.left if x2 >=0 else rect.right)+x2
 y2 =(rect.top if y2 >=0 else rect.bottom)+y2
 DragDrop(x1, y1, x2, y2, moveSpeed, waitTime)

 def RightDragDrop(self, x1:int, y1:int, x2:int, y2:int, moveSpeed:float =1, waitTime:float =OPERATION_WAIT_TIME)->None:
 rect =self.BoundingRectangle
 if rect.width()==0 or rect.height()==0:
 return
 x1 =(rect.left if x1 >=0 else rect.right)+x1
 y1 =(rect.top if y1 >=0 else rect.bottom)+y1
 x2 =(rect.left if x2 >=0 else rect.right)+x2
 y2 =(rect.top if y2 >=0 else rect.bottom)+y2
 RightDragDrop(x1, y1, x2, y2, moveSpeed, waitTime)

 def WheelDown(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, wheelTimes:int =1, interval:float =0.05, waitTime:float =OPERATION_WAIT_TIME)->None:

 cursorX, cursorY =GetCursorPos()
 self.SetFocus()
 self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove =False)
 WheelDown(wheelTimes, interval, waitTime)
 SetCursorPos(cursorX, cursorY)

 def WheelUp(self, x:Optional[int]=None, y:Optional[int]=None, ratioX:float =0.5, ratioY:float =0.5, wheelTimes:int =1, interval:float =0.05, waitTime:float =OPERATION_WAIT_TIME)->None:

 cursorX, cursorY =GetCursorPos()
 self.SetFocus()
 self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove =False)
 WheelUp(wheelTimes, interval, waitTime)
 SetCursorPos(cursorX, cursorY)

 def ShowWindow(self, cmdShow:int, waitTime:float =OPERATION_WAIT_TIME)->Optional[bool]:

 handle =self.NativeWindowHandle
 if not handle:
 control =self
 while not handle and control:
 control =control.GetParentControl()
 if control:
 handle =control.NativeWindowHandle
 else:
 handle =0
 break
 if handle:
 ret =ShowWindow(handle, cmdShow)
 time.sleep(waitTime)
 return ret
 return None

 def Show(self, waitTime:float =OPERATION_WAIT_TIME)->Optional[bool]:

 return self.ShowWindow(SW.Show, waitTime)

 def Hide(self, waitTime:float =OPERATION_WAIT_TIME)->Optional[bool]:

 return self.ShowWindow(SW.Hide, waitTime)

 def MoveWindow(self, x:int, y:int, width:int, height:int, repaint:bool =True)->bool:

 handle =self.NativeWindowHandle
 if handle:
 return MoveWindow(handle, x, y, width, height, int(repaint))
 return False

 def GetWindowText(self)->Optional[str]:

 handle =self.NativeWindowHandle
 if handle:
 return GetWindowText(handle)
 return None

 def SetWindowText(self, text:str)->bool:

 handle =self.NativeWindowHandle
 if handle:
 return SetWindowText(handle, text)
 return False

 def SendKey(self, key:int, waitTime:float =OPERATION_WAIT_TIME)->None:

 self.SetFocus()
 SendKey(key, waitTime)

 def SendKeys(self, text:str, interval:float =0.01, waitTime:float =OPERATION_WAIT_TIME, charMode:bool =True)->None:

 self.SetFocus()
 SendKeys(text, interval, waitTime, charMode)

 def IsTopLevel(self)->bool:

 handle =self.NativeWindowHandle
 if handle:
 return GetAncestor(handle, GAFlag.Root)==handle
 return False

 def GetTopLevelControl(self)->Optional['Control']:

 handle =self.NativeWindowHandle
 if handle:
 topHandle =GetAncestor(handle, GAFlag.Root)
 if topHandle:
 if topHandle ==handle:
 return self
 else:
 return ControlFromHandle(topHandle)
 else:

 pass
 else:
 control =self
 while True:
 control =control.GetParentControl()
 if not control:
 break
 handle =control.NativeWindowHandle
 if handle:
 topHandle =GetAncestor(handle, GAFlag.Root)
 return ControlFromHandle(topHandle)
 return None

 def Control(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'Control':
 return Control(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ButtonControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ButtonControl':
 return ButtonControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def CalendarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'CalendarControl':
 return CalendarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def CheckBoxControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'CheckBoxControl':
 return CheckBoxControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ComboBoxControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ComboBoxControl':
 return ComboBoxControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def CustomControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'CustomControl':
 return CustomControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def DataGridControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'DataGridControl':
 return DataGridControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def DataItemControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'DataItemControl':
 return DataItemControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def DocumentControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'DocumentControl':
 return DocumentControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def EditControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'EditControl':
 return EditControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GroupControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'GroupControl':
 return GroupControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def HeaderControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'HeaderControl':
 return HeaderControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def HeaderItemControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'HeaderItemControl':
 return HeaderItemControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def HyperlinkControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'HyperlinkControl':
 return HyperlinkControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ImageControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ImageControl':
 return ImageControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ListControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ListControl':
 return ListControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ListItemControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ListItemControl':
 return ListItemControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def MenuControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'MenuControl':
 return MenuControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def MenuBarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'MenuBarControl':
 return MenuBarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def MenuItemControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'MenuItemControl':
 return MenuItemControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def PaneControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'PaneControl':
 return PaneControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ProgressBarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ProgressBarControl':
 return ProgressBarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def RadioButtonControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'RadioButtonControl':
 return RadioButtonControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ScrollBarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ScrollBarControl':
 return ScrollBarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def SemanticZoomControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'SemanticZoomControl':
 return SemanticZoomControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def SeparatorControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'SeparatorControl':
 return SeparatorControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def SliderControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'SliderControl':
 return SliderControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def SpinnerControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'SpinnerControl':
 return SpinnerControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def SplitButtonControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'SplitButtonControl':
 return SplitButtonControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def StatusBarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'StatusBarControl':
 return StatusBarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TabControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TabControl':
 return TabControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TabItemControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TabItemControl':
 return TabItemControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TableControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TableControl':
 return TableControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TextControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TextControl':
 return TextControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ThumbControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ThumbControl':
 return ThumbControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TitleBarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TitleBarControl':
 return TitleBarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ToolBarControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ToolBarControl':
 return ToolBarControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def ToolTipControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'ToolTipControl':
 return ToolTipControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TreeControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TreeControl':
 return TreeControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def TreeItemControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'TreeItemControl':
 return TreeItemControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def WindowControl(self, searchDepth =0xFFFFFFFF, searchInterval =SEARCH_INTERVAL, foundIndex =1, element =0,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties)->'WindowControl':
 return WindowControl(searchFromControl =self, searchDepth =searchDepth, searchInterval =searchInterval,
 foundIndex =foundIndex, element =element,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class AppBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.AppBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class ButtonControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ButtonControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

 def GetTogglePattern(self)->TogglePattern:

 return self.GetPattern(PatternId.TogglePattern)

class CalendarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.CalendarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridPattern(self)->GridPattern:

 return self.GetPattern(PatternId.GridPattern)

 def GetTablePattern(self)->TablePattern:

 return self.GetPattern(PatternId.TablePattern)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

class CheckBoxControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.CheckBoxControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetTogglePattern(self)->TogglePattern:

 return self.GetPattern(PatternId.TogglePattern)

 def SetChecked(self, checked:bool)->bool:

 tp =self.GetTogglePattern()
 if tp:
 return tp.SetToggleState(ToggleState.On if checked else ToggleState.Off)
 return False

class ComboBoxControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ComboBoxControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

 def Select(self, itemName:str ='', condition:Optional[Callable[[str], bool]]=None, simulateMove:bool =True, waitTime:float =OPERATION_WAIT_TIME)->bool:

 expandCollapsePattern =self.GetExpandCollapsePattern()
 if expandCollapsePattern:
 expandCollapsePattern.Expand()
 else:

 self.Click(x =-10, ratioY =0.5, simulateMove =simulateMove)
 find =False
 if condition:
 listItemControl =self.ListItemControl(Compare =lambda c, d:condition(c.Name))
 else:
 listItemControl =self.ListItemControl(Name =itemName)
 if listItemControl.Exists(1):
 scrollItemPattern =listItemControl.GetScrollItemPattern()
 if scrollItemPattern:
 scrollItemPattern.ScrollIntoView(waitTime =0.1)
 listItemControl.Click(simulateMove =simulateMove, waitTime =waitTime)
 find =True
 else:

 listControl =ListControl(searchDepth =1)
 if listControl.Exists(1):
 if condition:
 listItemControl =listControl.ListItemControl(Compare =lambda c, d:condition(c.Name))
 else:
 listItemControl =listControl.ListItemControl(Name =itemName)
 if listItemControl.Exists(0, 0):
 scrollItemPattern =listItemControl.GetScrollItemPattern()
 if scrollItemPattern:
 scrollItemPattern.ScrollIntoView(waitTime =0.1)
 listItemControl.Click(simulateMove =simulateMove, waitTime =waitTime)
 find =True
 if not find:
 if expandCollapsePattern:
 expandCollapsePattern.Collapse(waitTime)
 else:
 self.Click(x =-10, ratioY =0.5, simulateMove =simulateMove, waitTime =waitTime)
 return find

class CustomControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.CustomControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class DataGridControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.DataGridControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridPattern(self)->GridPattern:

 return self.GetPattern(PatternId.GridPattern)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

 def GetTablePattern(self)->TablePattern:

 return self.GetPattern(PatternId.TablePattern)

class DataItemControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.DataItemControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetSelectionItemPattern(self)->SelectionItemPattern:

 return self.GetPattern(PatternId.SelectionItemPattern)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetGridItemPattern(self)->GridItemPattern:

 return self.GetPattern(PatternId.GridItemPattern)

 def GetScrollItemPattern(self)->ScrollItemPattern:

 return self.GetPattern(PatternId.ScrollItemPattern)

 def GetTableItemPattern(self)->TableItemPattern:

 return self.GetPattern(PatternId.TableItemPattern)

 def GetTogglePattern(self)->TogglePattern:

 return self.GetPattern(PatternId.TogglePattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class DocumentControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.DocumentControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetTextPattern(self)->TextPattern:

 return self.GetPattern(PatternId.TextPattern)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class EditControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.EditControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetRangeValuePattern(self)->RangeValuePattern:

 return self.GetPattern(PatternId.RangeValuePattern)

 def GetTextPattern(self)->TextPattern:

 return self.GetPattern(PatternId.TextPattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class GroupControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.GroupControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

class HeaderControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.HeaderControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

class HeaderItemControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.HeaderItemControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

class HyperlinkControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.HyperlinkControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class ImageControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ImageControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridItemPattern(self)->GridItemPattern:

 return self.GetPattern(PatternId.GridItemPattern)

 def GetTableItemPattern(self)->TableItemPattern:

 return self.GetPattern(PatternId.TableItemPattern)

class ListControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ListControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridPattern(self)->GridPattern:

 return self.GetPattern(PatternId.GridPattern)

 def GetMultipleViewPattern(self)->MultipleViewPattern:

 return self.GetPattern(PatternId.MultipleViewPattern)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

class ListItemControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ListItemControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetSelectionItemPattern(self)->SelectionItemPattern:

 return self.GetPattern(PatternId.SelectionItemPattern)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetGridItemPattern(self)->GridItemPattern:

 return self.GetPattern(PatternId.GridItemPattern)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

 def GetScrollItemPattern(self)->ScrollItemPattern:

 return self.GetPattern(PatternId.ScrollItemPattern)

 def GetTogglePattern(self)->TogglePattern:

 return self.GetPattern(PatternId.TogglePattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class MenuControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.MenuControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class MenuBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.MenuBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetDockPattern(self)->DockPattern:

 return self.GetPattern(PatternId.DockPattern)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

class MenuItemControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.MenuItemControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

 def GetSelectionItemPattern(self)->SelectionItemPattern:

 return self.GetPattern(PatternId.SelectionItemPattern)

 def GetTogglePattern(self)->TogglePattern:

 return self.GetPattern(PatternId.TogglePattern)

class TopLevel():

 def SetTopmost(self, isTopmost:bool =True, waitTime:float =OPERATION_WAIT_TIME)->bool:

 if self.IsTopLevel():
 ret =SetWindowTopmost(self.NativeWindowHandle, isTopmost)
 time.sleep(waitTime)
 return ret
 return False

 def IsTopmost(self)->bool:
 if self.IsTopLevel():
 WS_EX_TOPMOST =0x00000008
 return bool(GetWindowLong(self.NativeWindowHandle, GWL.ExStyle)&WS_EX_TOPMOST)
 return False

 def SwitchToThisWindow(self, waitTime:float =OPERATION_WAIT_TIME)->None:
 if self.IsTopLevel():
 SwitchToThisWindow(self.NativeWindowHandle)
 time.sleep(waitTime)

 def Maximize(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 if self.IsTopLevel():
 return self.ShowWindow(SW.ShowMaximized, waitTime)
 return False

 def IsMaximize(self)->bool:
 if self.IsTopLevel():
 return bool(IsZoomed(self.NativeWindowHandle))
 return False

 def Minimize(self, waitTime:float =OPERATION_WAIT_TIME)->bool:
 if self.IsTopLevel():
 return self.ShowWindow(SW.Minimize, waitTime)
 return False

 def IsMinimize(self)->bool:
 if self.IsTopLevel():
 return bool(IsIconic(self.NativeWindowHandle))
 return False

 def Restore(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 if self.IsTopLevel():
 return self.ShowWindow(SW.Restore, waitTime)
 return False

 def MoveToCenter(self)->bool:

 if self.IsTopLevel():
 rect =self.BoundingRectangle
 screenWidth, screenHeight =GetScreenSize()
 x, y =(screenWidth -rect.width())//2, (screenHeight -rect.height())//2
 if x <0:
 x =0
 if y <0:
 y =0
 return SetWindowPos(self.NativeWindowHandle, SWP.HWND_Top, x, y, 0, 0, SWP.SWP_NoSize)
 return False

 def SetActive(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 if self.IsTopLevel():
 handle =self.NativeWindowHandle
 if IsIconic(handle):
 ret =ShowWindow(handle, SW.Restore)
 elif not IsWindowVisible(handle):
 ret =ShowWindow(handle, SW.Show)
 ret =SetForegroundWindow(handle)
 time.sleep(waitTime)
 return ret
 return False

class PaneControl(Control, TopLevel):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.PaneControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetDockPattern(self)->DockPattern:

 return self.GetPattern(PatternId.DockPattern)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

class ProgressBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ProgressBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetRangeValuePattern(self)->RangeValuePattern:

 return self.GetPattern(PatternId.RangeValuePattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class RadioButtonControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.RadioButtonControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetSelectionItemPattern(self)->SelectionItemPattern:

 return self.GetPattern(PatternId.SelectionItemPattern)

class ScrollBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ScrollBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetRangeValuePattern(self)->RangeValuePattern:

 return self.GetPattern(PatternId.RangeValuePattern)

class SemanticZoomControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.SemanticZoomControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class SeparatorControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.SeparatorControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class SliderControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.SliderControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetRangeValuePattern(self)->RangeValuePattern:

 return self.GetPattern(PatternId.RangeValuePattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class SpinnerControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.SpinnerControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetRangeValuePattern(self)->RangeValuePattern:

 return self.GetPattern(PatternId.RangeValuePattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

 def GetValuePattern(self)->ValuePattern:

 return self.GetPattern(PatternId.ValuePattern)

class SplitButtonControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.SplitButtonControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

class StatusBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.StatusBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridPattern(self)->GridPattern:

 return self.GetPattern(PatternId.GridPattern)

class TabControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TabControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

class TabItemControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TabItemControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetSelectionItemPattern(self)->SelectionItemPattern:

 return self.GetPattern(PatternId.SelectionItemPattern)

class TableControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TableControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridPattern(self)->GridPattern:

 return self.GetPattern(PatternId.GridPattern)

 def GetGridItemPattern(self)->GridItemPattern:

 return self.GetPattern(PatternId.GridItemPattern)

 def GetTablePattern(self)->TablePattern:

 return self.GetPattern(PatternId.TablePattern)

 def GetTableItemPattern(self)->TableItemPattern:

 return self.GetPattern(PatternId.TableItemPattern)

 def GetTableItemsValue(self, row:int =-1, column:int =-1):

 table =[]
 for item in self.GetChildren():
 table.append([cell.GetLegacyIAccessiblePattern().Value for cell in item.GetChildren()])
 if row >0 and column >0:
 return table[row][column]
 if row >0:
 return table[row]
 return table

class TextControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TextControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetGridItemPattern(self)->GridItemPattern:

 return self.GetPattern(PatternId.GridItemPattern)

 def GetTableItemPattern(self)->TableItemPattern:

 return self.GetPattern(PatternId.TableItemPattern)

 def GetTextPattern(self)->TextPattern:

 return self.GetPattern(PatternId.TextPattern)

class ThumbControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ThumbControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

class TitleBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TitleBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

class ToolBarControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ToolBarControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetDockPattern(self)->DockPattern:

 return self.GetPattern(PatternId.DockPattern)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

class ToolTipControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.ToolTipControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetTextPattern(self)->TextPattern:

 return self.GetPattern(PatternId.TextPattern)

 def GetWindowPattern(self)->WindowPattern:

 return self.GetPattern(PatternId.WindowPattern)

class TreeControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TreeControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetScrollPattern(self)->ScrollPattern:

 return self.GetPattern(PatternId.ScrollPattern)

 def GetSelectionPattern(self)->SelectionPattern:

 return self.GetPattern(PatternId.SelectionPattern)

class TreeItemControl(Control):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.TreeItemControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)

 def GetExpandCollapsePattern(self)->ExpandCollapsePattern:

 return self.GetPattern(PatternId.ExpandCollapsePattern)

 def GetInvokePattern(self)->InvokePattern:

 return self.GetPattern(PatternId.InvokePattern)

 def GetScrollItemPattern(self)->ScrollItemPattern:

 return self.GetPattern(PatternId.ScrollItemPattern)

 def GetSelectionItemPattern(self)->SelectionItemPattern:

 return self.GetPattern(PatternId.SelectionItemPattern)

 def GetTogglePattern(self)->TogglePattern:

 return self.GetPattern(PatternId.TogglePattern)

class WindowControl(Control, TopLevel):
 def __init__(self, searchFromControl:Optional[Control]=None,
 searchDepth:int =0xFFFFFFFF,
 searchInterval:float =SEARCH_INTERVAL,
 foundIndex:int =1,
 element =None,
 Name:Optional[str]=None,
 SubName:Optional[str]=None,
 RegexName:Optional[str]=None,
 ClassName:Optional[str]=None,
 AutomationId:Optional[str]=None,
 Depth:Optional[int]=None,
 Compare:Optional[Callable[[TreeNode], bool]]=None,
 **searchProperties):
 Control.__init__(self, searchFromControl, searchDepth, searchInterval, foundIndex, element,
 ControlType =ControlType.WindowControl,
 Name =Name,
 SubName =SubName,
 RegexName =RegexName,
 ClassName =ClassName,
 AutomationId =AutomationId,
 Depth =Depth,
 Compare =Compare,
 **searchProperties)
 self._DockPattern =None
 self._TransformPattern =None

 def GetTransformPattern(self)->TransformPattern:

 return self.GetPattern(PatternId.TransformPattern)

 def GetWindowPattern(self)->WindowPattern:

 return self.GetPattern(PatternId.WindowPattern)

 def GetDockPattern(self)->DockPattern:

 return self.GetPattern(PatternId.DockPattern)

 def MetroClose(self, waitTime:float =OPERATION_WAIT_TIME)->None:

 if self.ClassName ==METRO_WINDOW_CLASS_NAME:
 screenWidth, screenHeight =GetScreenSize()
 MoveTo(screenWidth //2, 0, waitTime =0)
 DragDrop(screenWidth //2, 0, screenWidth //2, screenHeight, waitTime =waitTime)

ControlConstructors ={
ControlType.AppBarControl:AppBarControl,
ControlType.ButtonControl:ButtonControl,
ControlType.CalendarControl:CalendarControl,
ControlType.CheckBoxControl:CheckBoxControl,
ControlType.ComboBoxControl:ComboBoxControl,
ControlType.CustomControl:CustomControl,
ControlType.DataGridControl:DataGridControl,
ControlType.DataItemControl:DataItemControl,
ControlType.DocumentControl:DocumentControl,
ControlType.EditControl:EditControl,
ControlType.GroupControl:GroupControl,
ControlType.HeaderControl:HeaderControl,
ControlType.HeaderItemControl:HeaderItemControl,
ControlType.HyperlinkControl:HyperlinkControl,
ControlType.ImageControl:ImageControl,
ControlType.ListControl:ListControl,
ControlType.ListItemControl:ListItemControl,
ControlType.MenuBarControl:MenuBarControl,
ControlType.MenuControl:MenuControl,
ControlType.MenuItemControl:MenuItemControl,
ControlType.PaneControl:PaneControl,
ControlType.ProgressBarControl:ProgressBarControl,
ControlType.RadioButtonControl:RadioButtonControl,
ControlType.ScrollBarControl:ScrollBarControl,
ControlType.SemanticZoomControl:SemanticZoomControl,
ControlType.SeparatorControl:SeparatorControl,
ControlType.SliderControl:SliderControl,
ControlType.SpinnerControl:SpinnerControl,
ControlType.SplitButtonControl:SplitButtonControl,
ControlType.StatusBarControl:StatusBarControl,
ControlType.TabControl:TabControl,
ControlType.TabItemControl:TabItemControl,
ControlType.TableControl:TableControl,
ControlType.TextControl:TextControl,
ControlType.ThumbControl:ThumbControl,
ControlType.TitleBarControl:TitleBarControl,
ControlType.ToolBarControl:ToolBarControl,
ControlType.ToolTipControl:ToolTipControl,
ControlType.TreeControl:TreeControl,
ControlType.TreeItemControl:TreeItemControl,
ControlType.WindowControl:WindowControl,
}

def SetGlobalSearchTimeout(seconds:float)->None:

 global TIME_OUT_SECOND
 TIME_OUT_SECOND =seconds

def WaitForExist(control:Control, timeout:float)->bool:

 return control.Exists(timeout, 1)

def WaitForDisappear(control:Control, timeout:float)->bool:

 return control.Disappears(timeout, 1)

def WalkTree(top, getChildren:Optional[Callable[[TreeNode], List[TreeNode]]]=None,
getFirstChild:Optional[Callable[[TreeNode], TreeNode]]=None, getNextSibling:Optional[Callable[[TreeNode], TreeNode]]=None,
yieldCondition:Optional[Callable[[TreeNode, int], bool]]=None, includeTop:bool =False, maxDepth:int =0xFFFFFFFF):

 if maxDepth <=0:
 return
 depth =0
 if getChildren:
 if includeTop:
 if not yieldCondition or yieldCondition(top, 0):
 yield top, 0, 0
 children =getChildren(top)
 childList =[children]
 while depth >=0:
 lastItems =childList[-1]
 if lastItems:
 if not yieldCondition or yieldCondition(lastItems[0], depth +1):
 yield lastItems[0], depth +1, len(lastItems)-1
 if depth +1 <maxDepth:
 children =getChildren(lastItems[0])
 if children:
 depth +=1
 childList.append(children)
 del lastItems[0]
 else:
 del childList[depth]
 depth -=1
 elif getFirstChild and getNextSibling:
 if includeTop:
 if not yieldCondition or yieldCondition(top, 0):
 yield top, 0
 child =getFirstChild(top)
 childList =[child]
 while depth >=0:
 lastItem =childList[-1]
 if lastItem:
 if not yieldCondition or yieldCondition(lastItem, depth +1):
 yield lastItem, depth +1
 child =getNextSibling(lastItem)
 childList[depth]=child
 if depth +1 <maxDepth:
 child =getFirstChild(lastItem)
 if child:
 depth +=1
 childList.append(child)
 else:
 del childList[depth]
 depth -=1

def GetRootControl()->PaneControl:

 control =Control.CreateControlFromElement(_AutomationClient.instance().IUIAutomation.GetRootElement())
 if isinstance(control, PaneControl):
 return control

 if control is None:
 raise AssertionError('Expected valid root element')
 raise AssertionError('Expected root element to be a PaneControl. Found: %s(%s)'%(type(control), control))

def GetFocusedControl()->Optional[Control]:

 return Control.CreateControlFromElement(_AutomationClient.instance().IUIAutomation.GetFocusedElement())

def GetForegroundControl()->Control:

 return ControlFromHandle(GetForegroundWindow())

def GetConsoleWindow()->Optional[WindowControl]:

 consoleWindow =ControlFromHandle(ctypes.windll.kernel32.GetConsoleWindow())
 if consoleWindow and consoleWindow.ClassName =='PseudoConsoleWindow':

 consoleWindow =consoleWindow.GetParentControl()
 return consoleWindow

def ControlFromPoint(x:int, y:int)->Optional[Control]:

 element =_AutomationClient.instance().IUIAutomation.ElementFromPoint(ctypes.wintypes.POINT(x, y))
 return Control.CreateControlFromElement(element)

def ControlFromPoint2(x:int, y:int)->Optional[Control]:

 return Control.CreateControlFromElement(_AutomationClient.instance().IUIAutomation.ElementFromHandle(WindowFromPoint(x, y)))

def ControlFromCursor()->Optional[Control]:

 x, y =GetCursorPos()
 return ControlFromPoint(x, y)

def ControlFromCursor2()->Optional[Control]:

 x, y =GetCursorPos()
 return ControlFromPoint2(x, y)

def ControlFromHandle(handle:int)->Optional[Control]:

 if handle:
 return Control.CreateControlFromElement(_AutomationClient.instance().IUIAutomation.ElementFromHandle(handle))
 return None

def ControlsAreSame(control1:Control, control2:Control)->bool:

 return bool(_AutomationClient.instance().IUIAutomation.CompareElements(control1.Element, control2.Element))

def WalkControl(control:Control, includeTop:bool =False, maxDepth:int =0xFFFFFFFF)->Generator[Tuple[Control, int], None, None]:

 if includeTop:
 yield control, 0
 if maxDepth <=0:
 return
 depth =0
 child =control.GetFirstChildControl()
 controlList =[child]
 while depth >=0:
 lastControl =controlList[-1]
 if lastControl:
 yield lastControl, depth +1
 child =lastControl.GetNextSiblingControl()
 controlList[depth]=child
 if depth +1 <maxDepth:
 child =lastControl.GetFirstChildControl()
 if child:
 depth +=1
 controlList.append(child)
 else:
 del controlList[depth]
 depth -=1

def LogControl(control:Control, depth:int =0, showAllName:bool =True, showPid:bool =False)->None:

 pass

def EnumAndLogControl(control:Control, maxDepth:int =0xFFFFFFFF, showAllName:bool =True, showPid:bool =False, startDepth:int =0)->None:

 for c, d in WalkControl(control, True, maxDepth):
 LogControl(c, d +startDepth, showAllName, showPid)

def EnumAndLogControlAncestors(control:Control, showAllName:bool =True, showPid:bool =False)->None:

 curr =control
 lists =[]
 while curr:
 lists.insert(0, curr)
 curr =curr.GetParentControl()
 for i, curr in enumerate(lists):
 LogControl(curr, i, showAllName, showPid)

def FindControl(control:Optional[Control], compare:Callable[[Control, int], bool], maxDepth:int =0xFFFFFFFF, findFromSelf:bool =False, foundIndex:int =1)->Optional[Control]:

 foundCount =0
 if not control:
 control =GetRootControl()
 traverseCount =0
 for child, depth in WalkControl(control, findFromSelf, maxDepth):
 traverseCount +=1
 if compare(child, depth):
 foundCount +=1
 if foundCount ==foundIndex:
 child.traverseCount =traverseCount
 return child
 return None

def ShowDesktop(waitTime:float =1)->None:

 SendKeys('{Win}d', waitTime =waitTime)

def WaitHotKeyReleased(hotkey:Tuple[int, int])->None:

 mod ={ModifierKey.Alt:Keys.VK_MENU,
 ModifierKey.Control:Keys.VK_CONTROL,
 ModifierKey.Shift:Keys.VK_SHIFT,
 ModifierKey.Win:Keys.VK_LWIN
 }
 while True:
 time.sleep(0.05)
 if IsKeyPressed(hotkey[1]):
 continue
 for k, v in mod.items():
 if k &hotkey[0]:
 if IsKeyPressed(v):
 break
 else:
 break

