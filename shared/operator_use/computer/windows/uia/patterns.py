

import os
import sys
import time
import ctypes
from typing import(Any, List, TYPE_CHECKING)
from.enums import *
from.core import *
from.core import _AutomationClient
if TYPE_CHECKING:
 from.controls import Control

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

_PatternIdInterfaces =None

def GetPatternIdInterface(patternId:int):

 global _PatternIdInterfaces
 if not _PatternIdInterfaces:
 _PatternIdInterfaces ={

 PatternId.DockPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationDockPattern,

 PatternId.ExpandCollapsePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationExpandCollapsePattern,
 PatternId.GridItemPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationGridItemPattern,
 PatternId.GridPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationGridPattern,
 PatternId.InvokePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationInvokePattern,
 PatternId.ItemContainerPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationItemContainerPattern,
 PatternId.LegacyIAccessiblePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationLegacyIAccessiblePattern,
 PatternId.MultipleViewPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationMultipleViewPattern,

 PatternId.RangeValuePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationRangeValuePattern,
 PatternId.ScrollItemPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationScrollItemPattern,
 PatternId.ScrollPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationScrollPattern,
 PatternId.SelectionItemPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationSelectionItemPattern,
 PatternId.SelectionPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationSelectionPattern,

 PatternId.SynchronizedInputPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationSynchronizedInputPattern,
 PatternId.TableItemPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationTableItemPattern,
 PatternId.TablePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationTablePattern,

 PatternId.TextPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationTextPattern,

 PatternId.TogglePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationTogglePattern,
 PatternId.TransformPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationTransformPattern,

 PatternId.ValuePattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationValuePattern,
 PatternId.VirtualizedItemPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationVirtualizedItemPattern,
 PatternId.WindowPattern:_AutomationClient.instance().UIAutomationCore.IUIAutomationWindowPattern,
 }
 debug =False

 try:
 _PatternIdInterfaces[PatternId.AnnotationPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationAnnotationPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.CustomNavigationPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationCustomNavigationPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.DragPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationDragPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.DropTargetPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationDropTargetPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.ObjectModelPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationObjectModelPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.SpreadsheetItemPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationSpreadsheetItemPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.SpreadsheetPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationSpreadsheetPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.StylesPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationStylesPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.SelectionPattern2]=_AutomationClient.instance().UIAutomationCore.IUIAutomationSelectionPattern2
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.TextChildPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationTextChildPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.TextEditPattern]=_AutomationClient.instance().UIAutomationCore.IUIAutomationTextEditPattern
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.TextPattern2]=_AutomationClient.instance().UIAutomationCore.IUIAutomationTextPattern2
 except:
 pass
 try:
 _PatternIdInterfaces[PatternId.TransformPattern2]=_AutomationClient.instance().UIAutomationCore.IUIAutomationTransformPattern2
 except:
 pass
 return _PatternIdInterfaces[patternId]

class AnnotationPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def AnnotationTypeId(self)->int:

 return self.pattern.CurrentAnnotationTypeId

 @property
 def AnnotationTypeName(self)->str:

 return self.pattern.CurrentAnnotationTypeName

 @property
 def Author(self)->str:

 return self.pattern.CurrentAuthor

 @property
 def DateTime(self)->str:

 return self.pattern.CurrentDateTime

 @property
 def Target(self)->'Control':

 ele =self.pattern.CurrentTarget
 return Control.CreateControlFromElement(ele)

class CustomNavigationPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def Navigate(self, direction:int)->'Control':

 ele =self.pattern.Navigate(direction)
 return Control.CreateControlFromElement(ele)

class DockPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def DockPosition(self)->int:

 return self.pattern.CurrentDockPosition

 def SetDockPosition(self, dockPosition:int, waitTime:float =OPERATION_WAIT_TIME)->int:

 ret =self.pattern.SetDockPosition(dockPosition)
 time.sleep(waitTime)
 return ret

class DragPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def DropEffect(self)->str:

 return self.pattern.CurrentDropEffect

 @property
 def DropEffects(self)->List[str]:

 return self.pattern.CurrentDropEffects

 @property
 def IsGrabbed(self)->bool:

 return bool(self.pattern.CurrentIsGrabbed)

 def GetGrabbedItems(self)->List['Control']:

 eleArray =self.pattern.GetCurrentGrabbedItems()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

class DropTargetPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def DropTargetEffect(self)->str:

 return self.pattern.CurrentDropTargetEffect

 @property
 def DropTargetEffects(self)->List[str]:

 return self.pattern.CurrentDropTargetEffects

class ExpandCollapsePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def ExpandCollapseState(self)->int:

 return self.pattern.CurrentExpandCollapseState

 def Collapse(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 try:
 ret =self.pattern.Collapse()==S_OK
 time.sleep(waitTime)
 return ret
 except:
 pass
 return False

 def Expand(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 try:
 ret =self.pattern.Expand()==S_OK
 time.sleep(waitTime)
 return ret
 except:
 pass
 return False

class GridItemPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def Column(self)->int:

 return self.pattern.CurrentColumn

 @property
 def ColumnSpan(self)->int:

 return self.pattern.CurrentColumnSpan

 @property
 def ContainingGrid(self)->'Control':

 return Control.CreateControlFromElement(self.pattern.CurrentContainingGrid)

 @property
 def Row(self)->int:

 return self.pattern.CurrentRow

 @property
 def RowSpan(self)->int:

 return self.pattern.CurrentRowSpan

class GridPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def ColumnCount(self)->int:

 return self.pattern.CurrentColumnCount

 @property
 def RowCount(self)->int:

 return self.pattern.CurrentRowCount

 def GetItem(self, row:int, column:int)->'Control':

 return Control.CreateControlFromElement(self.pattern.GetItem(row, column))

class InvokePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def Invoke(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Invoke()==S_OK
 time.sleep(waitTime)
 return ret

class ItemContainerPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def FindItemByProperty(self, control:'Control', propertyId:int, propertyValue)->'Control':

 ele =self.pattern.FindItemByProperty(control.Element, propertyId, propertyValue)
 return Control.CreateControlFromElement(ele)

class LegacyIAccessiblePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def ChildId(self)->int:

 return self.pattern.CurrentChildId

 @property
 def DefaultAction(self)->str:

 return self.pattern.CurrentDefaultAction

 @property
 def Description(self)->str:

 return self.pattern.CurrentDescription

 @property
 def Help(self)->str:

 return self.pattern.CurrentHelp

 @property
 def KeyboardShortcut(self)->str:

 return self.pattern.CurrentKeyboardShortcut

 @property
 def Name(self)->str:

 return self.pattern.CurrentName or ''

 @property
 def Role(self)->int:

 return self.pattern.CurrentRole

 @property
 def State(self)->int:

 return self.pattern.CurrentState

 @property
 def Value(self)->str:

 return self.pattern.CurrentValue

 def DoDefaultAction(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.DoDefaultAction()==S_OK
 time.sleep(waitTime)
 return ret

 def GetSelection(self)->List['Control']:

 eleArray =self.pattern.GetCurrentSelection()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

 def GetIAccessible(self):

 return self.pattern.GetIAccessible()

 def Select(self, flagsSelect:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Select(flagsSelect)==S_OK
 time.sleep(waitTime)
 return ret

 def SetValue(self, value:str, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.SetValue(value)==S_OK
 time.sleep(waitTime)
 return ret

class MultipleViewPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def CurrentView(self)->int:

 return self.pattern.CurrentCurrentView

 def GetSupportedViews(self)->List[int]:

 return self.pattern.GetCurrentSupportedViews()

 def GetViewName(self, view:int)->str:

 return self.pattern.GetViewName(view)

 def SetView(self, view:int)->bool:

 return self.pattern.SetCurrentView(view)==S_OK

class ObjectModelPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

class RangeValuePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def IsReadOnly(self)->bool:

 return bool(self.pattern.CurrentIsReadOnly)

 @property
 def LargeChange(self)->float:

 return self.pattern.CurrentLargeChange

 @property
 def Maximum(self)->float:

 return self.pattern.CurrentMaximum

 @property
 def Minimum(self)->float:

 return self.pattern.CurrentMinimum

 @property
 def SmallChange(self)->float:

 return self.pattern.CurrentSmallChange

 @property
 def Value(self)->float:

 return self.pattern.CurrentValue

 def SetValue(self, value:float, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.SetValue(value)==S_OK
 time.sleep(waitTime)
 return ret

class ScrollItemPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def ScrollIntoView(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.ScrollIntoView()==S_OK
 time.sleep(waitTime)
 return ret

class ScrollPattern():
 NoScrollValue =-1

 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def HorizontallyScrollable(self)->bool:

 return bool(self.pattern.CurrentHorizontallyScrollable)

 @property
 def HorizontalScrollPercent(self)->float:

 return self.pattern.CurrentHorizontalScrollPercent

 @property
 def HorizontalViewSize(self)->float:

 return self.pattern.CurrentHorizontalViewSize

 @property
 def VerticallyScrollable(self)->bool:

 return bool(self.pattern.CurrentVerticallyScrollable)

 @property
 def VerticalScrollPercent(self)->float:

 return self.pattern.CurrentVerticalScrollPercent

 @property
 def VerticalViewSize(self)->float:

 return self.pattern.CurrentVerticalViewSize

 def Scroll(self, horizontalAmount:int, verticalAmount:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Scroll(horizontalAmount, verticalAmount)==S_OK
 time.sleep(waitTime)
 return ret

 def SetScrollPercent(self, horizontalPercent:float, verticalPercent:float, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.SetScrollPercent(horizontalPercent, verticalPercent)==S_OK
 time.sleep(waitTime)
 return ret

class SelectionItemPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def AddToSelection(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.AddToSelection()==S_OK
 time.sleep(waitTime)
 return ret

 @property
 def IsSelected(self)->bool:

 return bool(self.pattern.CurrentIsSelected)

 @property
 def SelectionContainer(self)->'Control':

 ele =self.pattern.CurrentSelectionContainer
 return Control.CreateControlFromElement(ele)

 def RemoveFromSelection(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.RemoveFromSelection()==S_OK
 time.sleep(waitTime)
 return ret

 def Select(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Select()==S_OK
 time.sleep(waitTime)
 return ret

class SelectionPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def CanSelectMultiple(self)->bool:

 return bool(self.pattern.CurrentCanSelectMultiple)

 @property
 def IsSelectionRequired(self)->bool:

 return bool(self.pattern.CurrentIsSelectionRequired)

 def GetSelection(self)->List['Control']:

 eleArray =self.pattern.GetCurrentSelection()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

class SelectionPattern2(SelectionPattern):

 def __init__(self, pattern =None):
 super().__init__(pattern)

 @property
 def CurrentSelectedItem(self):

 ele =self.pattern.CurrentCurrentSelectedItem
 return Control.CreateControlFromElement(element =ele)if ele else None

 @property
 def FirstSelectedItem(self):

 ele =self.pattern.CurrentFirstSelectedItem
 return Control.CreateControlFromElement(element =ele)if ele else None

 @property
 def LastSelectedItem(self):

 ele =self.pattern.CurrentLastSelectedItem
 return Control.CreateControlFromElement(element =ele)if ele else None

 @property
 def ItemCount(self)->int:

 return self.pattern.CurrentItemCount

class SpreadsheetItemPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def Formula(self)->str:

 return self.pattern.CurrentFormula

 def GetAnnotationObjects(self)->List['Control']:

 eleArray =self.pattern.GetCurrentAnnotationObjects()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

 def GetAnnotationTypes(self)->List[int]:

 return self.pattern.GetCurrentAnnotationTypes()

class SpreadsheetPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def GetItemByName(self, name:str)->'Control':

 ele =self.pattern.GetItemByName(name)
 return Control.CreateControlFromElement(element =ele)

class StylesPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def ExtendedProperties(self)->str:

 return self.pattern.CurrentExtendedProperties

 @property
 def FillColor(self)->int:

 return self.pattern.CurrentFillColor

 @property
 def FillPatternColor(self)->int:

 return self.pattern.CurrentFillPatternColor

 @property
 def Shape(self)->str:

 return self.pattern.CurrentShape

 @property
 def StyleId(self)->int:

 return self.pattern.CurrentStyleId

 @property
 def StyleName(self)->str:

 return self.pattern.CurrentStyleName

class SynchronizedInputPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def Cancel(self)->bool:

 return self.pattern.Cancel()==S_OK

 def StartListening(self)->bool:

 return self.pattern.StartListening()==S_OK

class TableItemPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def GetColumnHeaderItems(self)->List['Control']:

 eleArray =self.pattern.GetCurrentColumnHeaderItems()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

 def GetRowHeaderItems(self)->List['Control']:

 eleArray =self.pattern.GetCurrentRowHeaderItems()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

class TablePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def RowOrColumnMajor(self)->int:

 return self.pattern.CurrentRowOrColumnMajor

 def GetColumnHeaders(self)->List['Control']:

 eleArray =self.pattern.GetCurrentColumnHeaders()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

 def GetRowHeaders(self)->List['Control']:

 eleArray =self.pattern.GetCurrentRowHeaders()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

class TextRange():
 def __init__(self, textRange =None):

 self.textRange =textRange

 def AddToSelection(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.textRange.AddToSelection()==S_OK
 time.sleep(waitTime)
 return ret

 def Clone(self)->'TextRange':

 return TextRange(textRange =self.textRange.Clone())

 def Compare(self, textRange:'TextRange')->bool:

 return bool(self.textRange.Compare(textRange.textRange))

 def CompareEndpoints(self, srcEndPoint:int, textRange:'TextRange', targetEndPoint:int)->int:

 return self.textRange.CompareEndpoints(srcEndPoint, textRange, targetEndPoint)

 def ExpandToEnclosingUnit(self, unit:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.textRange.ExpandToEnclosingUnit(unit)==S_OK
 time.sleep(waitTime)
 return ret

 def FindAttribute(self, textAttributeId:int, val, backward:bool)->Optional['TextRange']:

 textRange =self.textRange.FindAttribute(textAttributeId, val, int(backward))
 if textRange:
 return TextRange(textRange =textRange)
 return None

 def FindText(self, text:str, backward:bool, ignoreCase:bool)->Optional['TextRange']:

 textRange =self.textRange.FindText(text, int(backward), int(ignoreCase))
 if textRange:
 return TextRange(textRange =textRange)
 return None

 def GetAttributeValue(self, textAttributeId:int)->ctypes.POINTER(comtypes.IUnknown):

 return self.textRange.GetAttributeValue(textAttributeId)

 def GetBoundingRectangles(self)->List[Rect]:

 floats =self.textRange.GetBoundingRectangles()
 rects =[]
 for i in range(len(floats)//4):
 rect =Rect(int(floats[i *4]), int(floats[i *4 +1]),
 int(floats[i *4])+int(floats[i *4 +2]), int(floats[i *4 +1])+int(floats[i *4 +3]))
 rects.append(rect)
 return rects

 def GetChildren(self)->List['Control']:

 eleArray =self.textRange.GetChildren()
 if eleArray:
 controls =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 con =Control.CreateControlFromElement(element =ele)
 if con:
 controls.append(con)
 return controls
 return[]

 def GetEnclosingControl(self)->'Control':

 return Control.CreateControlFromElement(self.textRange.GetEnclosingElement())

 def GetText(self, maxLength:int =-1)->str:

 return self.textRange.GetText(maxLength)

 def Move(self, unit:int, count:int, waitTime:float =OPERATION_WAIT_TIME)->int:

 ret =self.textRange.Move(unit, count)
 time.sleep(waitTime)
 return ret

 def MoveEndpointByRange(self, srcEndPoint:int, textRange:'TextRange', targetEndPoint:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.textRange.MoveEndpointByRange(srcEndPoint, textRange.textRange, targetEndPoint)==S_OK
 time.sleep(waitTime)
 return ret

 def MoveEndpointByUnit(self, endPoint:int, unit:int, count:int, waitTime:float =OPERATION_WAIT_TIME)->int:

 ret =self.textRange.MoveEndpointByUnit(endPoint, unit, count)
 time.sleep(waitTime)
 return ret

 def RemoveFromSelection(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.textRange.RemoveFromSelection()==S_OK
 time.sleep(waitTime)
 return ret

 def ScrollIntoView(self, alignTop:bool =True, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.textRange.ScrollIntoView(int(alignTop))==S_OK
 time.sleep(waitTime)
 return ret

 def Select(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.textRange.Select()==S_OK
 time.sleep(waitTime)
 return ret

class TextChildPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def TextContainer(self)->'Control':

 return Control.CreateControlFromElement(self.pattern.TextContainer)

 @property
 def TextRange(self)->TextRange:

 return TextRange(self.pattern.TextRange)

class TextEditPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def GetActiveComposition(self)->Optional[TextRange]:

 textRange =self.pattern.GetActiveComposition()
 if textRange:
 return TextRange(textRange =textRange)
 return None

 def GetConversionTarget(self)->Optional[TextRange]:

 textRange =self.pattern.GetConversionTarget()
 if textRange:
 return TextRange(textRange =textRange)
 return None

class TextPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def DocumentRange(self)->TextRange:

 return TextRange(self.pattern.DocumentRange)

 @property
 def SupportedTextSelection(self)->bool:

 return bool(self.pattern.SupportedTextSelection)

 def GetSelection(self)->List[TextRange]:

 eleArray =self.pattern.GetSelection()
 if eleArray:
 textRanges =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 textRanges.append(TextRange(textRange =ele))
 return textRanges
 return[]

 def GetVisibleRanges(self)->List[TextRange]:

 eleArray =self.pattern.GetVisibleRanges()
 if eleArray:
 textRanges =[]
 for i in range(eleArray.Length):
 ele =eleArray.GetElement(i)
 textRanges.append(TextRange(textRange =ele))
 return textRanges
 return[]

 def RangeFromChild(self, child)->Optional[TextRange]:

 textRange =self.pattern.RangeFromChild(Control.Element)
 if textRange:
 return TextRange(textRange =textRange)
 return None

 def RangeFromPoint(self, x:int, y:int)->Optional[TextRange]:

 textRange =self.pattern.RangeFromPoint(ctypes.wintypes.POINT(x, y))
 if textRange:
 return TextRange(textRange =textRange)
 return None

class TextPattern2():
 def __init__(self, pattern =None):

 self.pattern =pattern

class TogglePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def ToggleState(self)->int:

 return self.pattern.CurrentToggleState

 def Toggle(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Toggle()==S_OK
 time.sleep(waitTime)
 return ret

 def SetToggleState(self, toggleState:int, waitTime:float =OPERATION_WAIT_TIME)->bool:
 for i in range(6):
 if self.ToggleState ==toggleState:
 return True
 self.Toggle(waitTime)
 return False

class TransformPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def CanMove(self)->bool:

 return bool(self.pattern.CurrentCanMove)

 @property
 def CanResize(self)->bool:

 return bool(self.pattern.CurrentCanResize)

 @property
 def CanRotate(self)->bool:

 return bool(self.pattern.CurrentCanRotate)

 def Move(self, x:int, y:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Move(x, y)==S_OK
 time.sleep(waitTime)
 return ret

 def Resize(self, width:int, height:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Resize(width, height)==S_OK
 time.sleep(waitTime)
 return ret

 def Rotate(self, degrees:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Rotate(degrees)==S_OK
 time.sleep(waitTime)
 return ret

class TransformPattern2():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def CanZoom(self)->bool:

 return bool(self.pattern.CurrentCanZoom)

 @property
 def ZoomLevel(self)->float:

 return self.pattern.CurrentZoomLevel

 @property
 def ZoomMaximum(self)->float:

 return self.pattern.CurrentZoomMaximum

 @property
 def ZoomMinimum(self)->float:

 return self.pattern.CurrentZoomMinimum

 def Zoom(self, zoomLevel:float, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Zoom(zoomLevel)==S_OK
 time.sleep(waitTime)
 return ret

 def ZoomByUnit(self, zoomUnit:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.ZoomByUnit(zoomUnit)==S_OK
 time.sleep(waitTime)
 return ret

class ValuePattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 @property
 def IsReadOnly(self)->bool:

 return bool(self.pattern.CurrentIsReadOnly)

 @property
 def Value(self)->str:

 return self.pattern.CurrentValue

 def SetValue(self, value:str, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.SetValue(value)==S_OK
 time.sleep(waitTime)
 return ret

class VirtualizedItemPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def Realize(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Realize()==S_OK
 time.sleep(waitTime)
 return ret

class WindowPattern():
 def __init__(self, pattern =None):

 self.pattern =pattern

 def Close(self, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.Close()==S_OK
 time.sleep(waitTime)
 return ret

 @property
 def CanMaximize(self)->bool:

 return bool(self.pattern.CurrentCanMaximize)

 @property
 def CanMinimize(self)->bool:

 return bool(self.pattern.CurrentCanMinimize)

 @property
 def IsModal(self)->bool:

 return bool(self.pattern.CurrentIsModal)

 @property
 def IsTopmost(self)->bool:

 return bool(self.pattern.CurrentIsTopmost)

 @property
 def WindowInteractionState(self)->int:

 return self.pattern.CurrentWindowInteractionState

 @property
 def WindowVisualState(self)->int:

 return self.pattern.CurrentWindowVisualState

 def SetWindowVisualState(self, state:int, waitTime:float =OPERATION_WAIT_TIME)->bool:

 ret =self.pattern.SetWindowVisualState(state)==S_OK
 time.sleep(waitTime)
 return ret

 def WaitForInputIdle(self, milliseconds:int)->bool:

 return self.pattern.WaitForInputIdle(milliseconds)==S_OK

PatternConstructors ={
PatternId.AnnotationPattern:AnnotationPattern,
PatternId.CustomNavigationPattern:CustomNavigationPattern,
PatternId.DockPattern:DockPattern,
PatternId.DragPattern:DragPattern,
PatternId.DropTargetPattern:DropTargetPattern,
PatternId.ExpandCollapsePattern:ExpandCollapsePattern,
PatternId.GridItemPattern:GridItemPattern,
PatternId.GridPattern:GridPattern,
PatternId.InvokePattern:InvokePattern,
PatternId.ItemContainerPattern:ItemContainerPattern,
PatternId.LegacyIAccessiblePattern:LegacyIAccessiblePattern,
PatternId.MultipleViewPattern:MultipleViewPattern,
PatternId.ObjectModelPattern:ObjectModelPattern,
PatternId.RangeValuePattern:RangeValuePattern,
PatternId.ScrollItemPattern:ScrollItemPattern,
PatternId.ScrollPattern:ScrollPattern,
PatternId.SelectionItemPattern:SelectionItemPattern,
PatternId.SelectionPattern:SelectionPattern,
PatternId.SpreadsheetItemPattern:SpreadsheetItemPattern,
PatternId.SpreadsheetPattern:SpreadsheetPattern,
PatternId.StylesPattern:StylesPattern,
PatternId.SynchronizedInputPattern:SynchronizedInputPattern,
PatternId.TableItemPattern:TableItemPattern,
PatternId.TablePattern:TablePattern,
PatternId.TextChildPattern:TextChildPattern,
PatternId.TextEditPattern:TextEditPattern,
PatternId.TextPattern:TextPattern,
PatternId.TextPattern2:TextPattern2,
PatternId.TogglePattern:TogglePattern,
PatternId.TransformPattern:TransformPattern,
PatternId.TransformPattern2:TransformPattern2,
PatternId.ValuePattern:ValuePattern,
PatternId.VirtualizedItemPattern:VirtualizedItemPattern,
PatternId.WindowPattern:WindowPattern,
}

def CreatePattern(patternId:int, pattern:ctypes.POINTER(comtypes.IUnknown)):

 subPattern =pattern.QueryInterface(GetPatternIdInterface(patternId))
 if subPattern:
 return PatternConstructors[patternId](pattern =subPattern)

