

import os
import sys
import time
import ctypes
import ctypes.wintypes
from enum import IntEnum, IntFlag
from typing import Any

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

class ControlType:

 AppBarControl =50040
 ButtonControl =50000
 CalendarControl =50001
 CheckBoxControl =50002
 ComboBoxControl =50003
 CustomControl =50025
 DataGridControl =50028
 DataItemControl =50029
 DocumentControl =50030
 EditControl =50004
 GroupControl =50026
 HeaderControl =50034
 HeaderItemControl =50035
 HyperlinkControl =50005
 ImageControl =50006
 ListControl =50008
 ListItemControl =50007
 MenuBarControl =50010
 MenuControl =50009
 MenuItemControl =50011
 PaneControl =50033
 ProgressBarControl =50012
 RadioButtonControl =50013
 ScrollBarControl =50014
 SemanticZoomControl =50039
 SeparatorControl =50038
 SliderControl =50015
 SpinnerControl =50016
 SplitButtonControl =50031
 StatusBarControl =50017
 TabControl =50018
 TabItemControl =50019
 TableControl =50036
 TextControl =50020
 ThumbControl =50027
 TitleBarControl =50037
 ToolBarControl =50021
 ToolTipControl =50022
 TreeControl =50023
 TreeItemControl =50024
 WindowControl =50032

ControlTypeNames ={
ControlType.AppBarControl:'AppBarControl',
ControlType.ButtonControl:'ButtonControl',
ControlType.CalendarControl:'CalendarControl',
ControlType.CheckBoxControl:'CheckBoxControl',
ControlType.ComboBoxControl:'ComboBoxControl',
ControlType.CustomControl:'CustomControl',
ControlType.DataGridControl:'DataGridControl',
ControlType.DataItemControl:'DataItemControl',
ControlType.DocumentControl:'DocumentControl',
ControlType.EditControl:'EditControl',
ControlType.GroupControl:'GroupControl',
ControlType.HeaderControl:'HeaderControl',
ControlType.HeaderItemControl:'HeaderItemControl',
ControlType.HyperlinkControl:'HyperlinkControl',
ControlType.ImageControl:'ImageControl',
ControlType.ListControl:'ListControl',
ControlType.ListItemControl:'ListItemControl',
ControlType.MenuBarControl:'MenuBarControl',
ControlType.MenuControl:'MenuControl',
ControlType.MenuItemControl:'MenuItemControl',
ControlType.PaneControl:'PaneControl',
ControlType.ProgressBarControl:'ProgressBarControl',
ControlType.RadioButtonControl:'RadioButtonControl',
ControlType.ScrollBarControl:'ScrollBarControl',
ControlType.SemanticZoomControl:'SemanticZoomControl',
ControlType.SeparatorControl:'SeparatorControl',
ControlType.SliderControl:'SliderControl',
ControlType.SpinnerControl:'SpinnerControl',
ControlType.SplitButtonControl:'SplitButtonControl',
ControlType.StatusBarControl:'StatusBarControl',
ControlType.TabControl:'TabControl',
ControlType.TabItemControl:'TabItemControl',
ControlType.TableControl:'TableControl',
ControlType.TextControl:'TextControl',
ControlType.ThumbControl:'ThumbControl',
ControlType.TitleBarControl:'TitleBarControl',
ControlType.ToolBarControl:'ToolBarControl',
ControlType.ToolTipControl:'ToolTipControl',
ControlType.TreeControl:'TreeControl',
ControlType.TreeItemControl:'TreeItemControl',
ControlType.WindowControl:'WindowControl',
}

class PatternId:

 AnnotationPattern =10023
 CustomNavigationPattern =10033
 DockPattern =10011
 DragPattern =10030
 DropTargetPattern =10031
 ExpandCollapsePattern =10005
 GridItemPattern =10007
 GridPattern =10006
 InvokePattern =10000
 ItemContainerPattern =10019
 LegacyIAccessiblePattern =10018
 MultipleViewPattern =10008
 ObjectModelPattern =10022
 RangeValuePattern =10003
 ScrollItemPattern =10017
 ScrollPattern =10004
 SelectionItemPattern =10010
 SelectionPattern =10001
 SpreadsheetItemPattern =10027
 SpreadsheetPattern =10026
 StylesPattern =10025
 SynchronizedInputPattern =10021
 TableItemPattern =10013
 TablePattern =10012
 TextChildPattern =10029
 TextEditPattern =10032
 TextPattern =10014
 TextPattern2 =10024
 TogglePattern =10015
 TransformPattern =10016
 TransformPattern2 =10028
 ValuePattern =10002
 VirtualizedItemPattern =10020
 WindowPattern =10009
 SelectionPattern2 =10034

PatternIdNames ={
PatternId.AnnotationPattern:'AnnotationPattern',
PatternId.CustomNavigationPattern:'CustomNavigationPattern',
PatternId.DockPattern:'DockPattern',
PatternId.DragPattern:'DragPattern',
PatternId.DropTargetPattern:'DropTargetPattern',
PatternId.ExpandCollapsePattern:'ExpandCollapsePattern',
PatternId.GridItemPattern:'GridItemPattern',
PatternId.GridPattern:'GridPattern',
PatternId.InvokePattern:'InvokePattern',
PatternId.ItemContainerPattern:'ItemContainerPattern',
PatternId.LegacyIAccessiblePattern:'LegacyIAccessiblePattern',
PatternId.MultipleViewPattern:'MultipleViewPattern',
PatternId.ObjectModelPattern:'ObjectModelPattern',
PatternId.RangeValuePattern:'RangeValuePattern',
PatternId.ScrollItemPattern:'ScrollItemPattern',
PatternId.ScrollPattern:'ScrollPattern',
PatternId.SelectionItemPattern:'SelectionItemPattern',
PatternId.SelectionPattern:'SelectionPattern',
PatternId.SpreadsheetItemPattern:'SpreadsheetItemPattern',
PatternId.SpreadsheetPattern:'SpreadsheetPattern',
PatternId.StylesPattern:'StylesPattern',
PatternId.SynchronizedInputPattern:'SynchronizedInputPattern',
PatternId.TableItemPattern:'TableItemPattern',
PatternId.TablePattern:'TablePattern',
PatternId.TextChildPattern:'TextChildPattern',
PatternId.TextEditPattern:'TextEditPattern',
PatternId.TextPattern:'TextPattern',
PatternId.TextPattern2:'TextPattern2',
PatternId.TogglePattern:'TogglePattern',
PatternId.TransformPattern:'TransformPattern',
PatternId.TransformPattern2:'TransformPattern2',
PatternId.ValuePattern:'ValuePattern',
PatternId.VirtualizedItemPattern:'VirtualizedItemPattern',
PatternId.WindowPattern:'WindowPattern',
PatternId.SelectionPattern2:'SelectionPattern2',
}

class PropertyId:

 AcceleratorKeyProperty =30006
 AccessKeyProperty =30007
 AnnotationAnnotationTypeIdProperty =30113
 AnnotationAnnotationTypeNameProperty =30114
 AnnotationAuthorProperty =30115
 AnnotationDateTimeProperty =30116
 AnnotationObjectsProperty =30156
 AnnotationTargetProperty =30117
 AnnotationTypesProperty =30155
 AriaPropertiesProperty =30102
 AriaRoleProperty =30101
 AutomationIdProperty =30011
 BoundingRectangleProperty =30001
 CenterPointProperty =30165
 ClassNameProperty =30012
 ClickablePointProperty =30014
 ControlTypeProperty =30003
 ControllerForProperty =30104
 CultureProperty =30015
 DescribedByProperty =30105
 DockDockPositionProperty =30069
 DragDropEffectProperty =30139
 DragDropEffectsProperty =30140
 DragGrabbedItemsProperty =30144
 DragIsGrabbedProperty =30138
 DropTargetDropTargetEffectProperty =30142
 DropTargetDropTargetEffectsProperty =30143
 ExpandCollapseExpandCollapseStateProperty =30070
 FillColorProperty =30160
 FillTypeProperty =30162
 FlowsFromProperty =30148
 FlowsToProperty =30106
 FrameworkIdProperty =30024
 FullDescriptionProperty =30159
 GridColumnCountProperty =30063
 GridItemColumnProperty =30065
 GridItemColumnSpanProperty =30067
 GridItemContainingGridProperty =30068
 GridItemRowProperty =30064
 GridItemRowSpanProperty =30066
 GridRowCountProperty =30062
 HasKeyboardFocusProperty =30008
 HelpTextProperty =30013
 IsAnnotationPatternAvailableProperty =30118
 IsContentElementProperty =30017
 IsControlElementProperty =30016
 IsCustomNavigationPatternAvailableProperty =30151
 IsDataValidForFormProperty =30103
 IsDockPatternAvailableProperty =30027
 IsDragPatternAvailableProperty =30137
 IsDropTargetPatternAvailableProperty =30141
 IsEnabledProperty =30010
 IsExpandCollapsePatternAvailableProperty =30028
 IsGridItemPatternAvailableProperty =30029
 IsGridPatternAvailableProperty =30030
 IsInvokePatternAvailableProperty =30031
 IsItemContainerPatternAvailableProperty =30108
 IsKeyboardFocusableProperty =30009
 IsLegacyIAccessiblePatternAvailableProperty =30090
 IsMultipleViewPatternAvailableProperty =30032
 IsObjectModelPatternAvailableProperty =30112
 IsOffscreenProperty =30022
 IsPasswordProperty =30019
 IsPeripheralProperty =30150
 IsRangeValuePatternAvailableProperty =30033
 IsRequiredForFormProperty =30025
 IsScrollItemPatternAvailableProperty =30035
 IsScrollPatternAvailableProperty =30034
 IsSelectionItemPatternAvailableProperty =30036
 IsSelectionPattern2AvailableProperty =30168
 IsSelectionPatternAvailableProperty =30037
 IsSpreadsheetItemPatternAvailableProperty =30132
 IsSpreadsheetPatternAvailableProperty =30128
 IsStylesPatternAvailableProperty =30127
 IsSynchronizedInputPatternAvailableProperty =30110
 IsTableItemPatternAvailableProperty =30039
 IsTablePatternAvailableProperty =30038
 IsTextChildPatternAvailableProperty =30136
 IsTextEditPatternAvailableProperty =30149
 IsTextPattern2AvailableProperty =30119
 IsTextPatternAvailableProperty =30040
 IsTogglePatternAvailableProperty =30041
 IsTransformPattern2AvailableProperty =30134
 IsTransformPatternAvailableProperty =30042
 IsValuePatternAvailableProperty =30043
 IsVirtualizedItemPatternAvailableProperty =30109
 IsWindowPatternAvailableProperty =30044
 ItemStatusProperty =30026
 ItemTypeProperty =30021
 LabeledByProperty =30018
 LandmarkTypeProperty =30157
 LegacyIAccessibleChildIdProperty =30091
 LegacyIAccessibleDefaultActionProperty =30100
 LegacyIAccessibleDescriptionProperty =30094
 LegacyIAccessibleHelpProperty =30097
 LegacyIAccessibleKeyboardShortcutProperty =30098
 LegacyIAccessibleNameProperty =30092
 LegacyIAccessibleRoleProperty =30095
 LegacyIAccessibleSelectionProperty =30099
 LegacyIAccessibleStateProperty =30096
 LegacyIAccessibleValueProperty =30093
 LevelProperty =30154
 LiveSettingProperty =30135
 LocalizedControlTypeProperty =30004
 LocalizedLandmarkTypeProperty =30158
 MultipleViewCurrentViewProperty =30071
 MultipleViewSupportedViewsProperty =30072
 NameProperty =30005
 NativeWindowHandleProperty =30020
 OptimizeForVisualContentProperty =30111
 OrientationProperty =30023
 OutlineColorProperty =30161
 OutlineThicknessProperty =30164
 PositionInSetProperty =30152
 ProcessIdProperty =30002
 ProviderDescriptionProperty =30107
 RangeValueIsReadOnlyProperty =30048
 RangeValueLargeChangeProperty =30051
 RangeValueMaximumProperty =30050
 RangeValueMinimumProperty =30049
 RangeValueSmallChangeProperty =30052
 RangeValueValueProperty =30047
 RotationProperty =30166
 RuntimeIdProperty =30000
 ScrollHorizontalScrollPercentProperty =30053
 ScrollHorizontalViewSizeProperty =30054
 ScrollHorizontallyScrollableProperty =30057
 ScrollVerticalScrollPercentProperty =30055
 ScrollVerticalViewSizeProperty =30056
 ScrollVerticallyScrollableProperty =30058
 Selection2CurrentSelectedItemProperty =30171
 Selection2FirstSelectedItemProperty =30169
 Selection2ItemCountProperty =30172
 Selection2LastSelectedItemProperty =30170
 SelectionCanSelectMultipleProperty =30060
 SelectionIsSelectionRequiredProperty =30061
 SelectionItemIsSelectedProperty =30079
 SelectionItemSelectionContainerProperty =30080
 SelectionSelectionProperty =30059
 SizeOfSetProperty =30153
 SizeProperty =30167
 SpreadsheetItemAnnotationObjectsProperty =30130
 SpreadsheetItemAnnotationTypesProperty =30131
 SpreadsheetItemFormulaProperty =30129
 StylesExtendedPropertiesProperty =30126
 StylesFillColorProperty =30122
 StylesFillPatternColorProperty =30125
 StylesFillPatternStyleProperty =30123
 StylesShapeProperty =30124
 StylesStyleIdProperty =30120
 StylesStyleNameProperty =30121
 TableColumnHeadersProperty =30082
 TableItemColumnHeaderItemsProperty =30085
 TableItemRowHeaderItemsProperty =30084
 TableRowHeadersProperty =30081
 TableRowOrColumnMajorProperty =30083
 ToggleToggleStateProperty =30086
 Transform2CanZoomProperty =30133
 Transform2ZoomLevelProperty =30145
 Transform2ZoomMaximumProperty =30147
 Transform2ZoomMinimumProperty =30146
 TransformCanMoveProperty =30087
 TransformCanResizeProperty =30088
 TransformCanRotateProperty =30089
 ValueIsReadOnlyProperty =30046
 ValueValueProperty =30045
 VisualEffectsProperty =30163
 WindowCanMaximizeProperty =30073
 WindowCanMinimizeProperty =30074
 WindowIsModalProperty =30077
 WindowIsTopmostProperty =30078
 WindowWindowInteractionStateProperty =30076
 WindowWindowVisualStateProperty =30075

PropertyIdNames ={
PropertyId.AcceleratorKeyProperty:'AcceleratorKeyProperty',
PropertyId.AccessKeyProperty:'AccessKeyProperty',
PropertyId.AnnotationAnnotationTypeIdProperty:'AnnotationAnnotationTypeIdProperty',
PropertyId.AnnotationAnnotationTypeNameProperty:'AnnotationAnnotationTypeNameProperty',
PropertyId.AnnotationAuthorProperty:'AnnotationAuthorProperty',
PropertyId.AnnotationDateTimeProperty:'AnnotationDateTimeProperty',
PropertyId.AnnotationObjectsProperty:'AnnotationObjectsProperty',
PropertyId.AnnotationTargetProperty:'AnnotationTargetProperty',
PropertyId.AnnotationTypesProperty:'AnnotationTypesProperty',
PropertyId.AriaPropertiesProperty:'AriaPropertiesProperty',
PropertyId.AriaRoleProperty:'AriaRoleProperty',
PropertyId.AutomationIdProperty:'AutomationIdProperty',
PropertyId.BoundingRectangleProperty:'BoundingRectangleProperty',
PropertyId.CenterPointProperty:'CenterPointProperty',
PropertyId.ClassNameProperty:'ClassNameProperty',
PropertyId.ClickablePointProperty:'ClickablePointProperty',
PropertyId.ControlTypeProperty:'ControlTypeProperty',
PropertyId.ControllerForProperty:'ControllerForProperty',
PropertyId.CultureProperty:'CultureProperty',
PropertyId.DescribedByProperty:'DescribedByProperty',
PropertyId.DockDockPositionProperty:'DockDockPositionProperty',
PropertyId.DragDropEffectProperty:'DragDropEffectProperty',
PropertyId.DragDropEffectsProperty:'DragDropEffectsProperty',
PropertyId.DragGrabbedItemsProperty:'DragGrabbedItemsProperty',
PropertyId.DragIsGrabbedProperty:'DragIsGrabbedProperty',
PropertyId.DropTargetDropTargetEffectProperty:'DropTargetDropTargetEffectProperty',
PropertyId.DropTargetDropTargetEffectsProperty:'DropTargetDropTargetEffectsProperty',
PropertyId.ExpandCollapseExpandCollapseStateProperty:'ExpandCollapseExpandCollapseStateProperty',
PropertyId.FillColorProperty:'FillColorProperty',
PropertyId.FillTypeProperty:'FillTypeProperty',
PropertyId.FlowsFromProperty:'FlowsFromProperty',
PropertyId.FlowsToProperty:'FlowsToProperty',
PropertyId.FrameworkIdProperty:'FrameworkIdProperty',
PropertyId.FullDescriptionProperty:'FullDescriptionProperty',
PropertyId.GridColumnCountProperty:'GridColumnCountProperty',
PropertyId.GridItemColumnProperty:'GridItemColumnProperty',
PropertyId.GridItemColumnSpanProperty:'GridItemColumnSpanProperty',
PropertyId.GridItemContainingGridProperty:'GridItemContainingGridProperty',
PropertyId.GridItemRowProperty:'GridItemRowProperty',
PropertyId.GridItemRowSpanProperty:'GridItemRowSpanProperty',
PropertyId.GridRowCountProperty:'GridRowCountProperty',
PropertyId.HasKeyboardFocusProperty:'HasKeyboardFocusProperty',
PropertyId.HelpTextProperty:'HelpTextProperty',
PropertyId.IsAnnotationPatternAvailableProperty:'IsAnnotationPatternAvailableProperty',
PropertyId.IsContentElementProperty:'IsContentElementProperty',
PropertyId.IsControlElementProperty:'IsControlElementProperty',
PropertyId.IsCustomNavigationPatternAvailableProperty:'IsCustomNavigationPatternAvailableProperty',
PropertyId.IsDataValidForFormProperty:'IsDataValidForFormProperty',
PropertyId.IsDockPatternAvailableProperty:'IsDockPatternAvailableProperty',
PropertyId.IsDragPatternAvailableProperty:'IsDragPatternAvailableProperty',
PropertyId.IsDropTargetPatternAvailableProperty:'IsDropTargetPatternAvailableProperty',
PropertyId.IsEnabledProperty:'IsEnabledProperty',
PropertyId.IsExpandCollapsePatternAvailableProperty:'IsExpandCollapsePatternAvailableProperty',
PropertyId.IsGridItemPatternAvailableProperty:'IsGridItemPatternAvailableProperty',
PropertyId.IsGridPatternAvailableProperty:'IsGridPatternAvailableProperty',
PropertyId.IsInvokePatternAvailableProperty:'IsInvokePatternAvailableProperty',
PropertyId.IsItemContainerPatternAvailableProperty:'IsItemContainerPatternAvailableProperty',
PropertyId.IsKeyboardFocusableProperty:'IsKeyboardFocusableProperty',
PropertyId.IsLegacyIAccessiblePatternAvailableProperty:'IsLegacyIAccessiblePatternAvailableProperty',
PropertyId.IsMultipleViewPatternAvailableProperty:'IsMultipleViewPatternAvailableProperty',
PropertyId.IsObjectModelPatternAvailableProperty:'IsObjectModelPatternAvailableProperty',
PropertyId.IsOffscreenProperty:'IsOffscreenProperty',
PropertyId.IsPasswordProperty:'IsPasswordProperty',
PropertyId.IsPeripheralProperty:'IsPeripheralProperty',
PropertyId.IsRangeValuePatternAvailableProperty:'IsRangeValuePatternAvailableProperty',
PropertyId.IsRequiredForFormProperty:'IsRequiredForFormProperty',
PropertyId.IsScrollItemPatternAvailableProperty:'IsScrollItemPatternAvailableProperty',
PropertyId.IsScrollPatternAvailableProperty:'IsScrollPatternAvailableProperty',
PropertyId.IsSelectionItemPatternAvailableProperty:'IsSelectionItemPatternAvailableProperty',
PropertyId.IsSelectionPattern2AvailableProperty:'IsSelectionPattern2AvailableProperty',
PropertyId.IsSelectionPatternAvailableProperty:'IsSelectionPatternAvailableProperty',
PropertyId.IsSpreadsheetItemPatternAvailableProperty:'IsSpreadsheetItemPatternAvailableProperty',
PropertyId.IsSpreadsheetPatternAvailableProperty:'IsSpreadsheetPatternAvailableProperty',
PropertyId.IsStylesPatternAvailableProperty:'IsStylesPatternAvailableProperty',
PropertyId.IsSynchronizedInputPatternAvailableProperty:'IsSynchronizedInputPatternAvailableProperty',
PropertyId.IsTableItemPatternAvailableProperty:'IsTableItemPatternAvailableProperty',
PropertyId.IsTablePatternAvailableProperty:'IsTablePatternAvailableProperty',
PropertyId.IsTextChildPatternAvailableProperty:'IsTextChildPatternAvailableProperty',
PropertyId.IsTextEditPatternAvailableProperty:'IsTextEditPatternAvailableProperty',
PropertyId.IsTextPattern2AvailableProperty:'IsTextPattern2AvailableProperty',
PropertyId.IsTextPatternAvailableProperty:'IsTextPatternAvailableProperty',
PropertyId.IsTogglePatternAvailableProperty:'IsTogglePatternAvailableProperty',
PropertyId.IsTransformPattern2AvailableProperty:'IsTransformPattern2AvailableProperty',
PropertyId.IsTransformPatternAvailableProperty:'IsTransformPatternAvailableProperty',
PropertyId.IsValuePatternAvailableProperty:'IsValuePatternAvailableProperty',
PropertyId.IsVirtualizedItemPatternAvailableProperty:'IsVirtualizedItemPatternAvailableProperty',
PropertyId.IsWindowPatternAvailableProperty:'IsWindowPatternAvailableProperty',
PropertyId.ItemStatusProperty:'ItemStatusProperty',
PropertyId.ItemTypeProperty:'ItemTypeProperty',
PropertyId.LabeledByProperty:'LabeledByProperty',
PropertyId.LandmarkTypeProperty:'LandmarkTypeProperty',
PropertyId.LegacyIAccessibleChildIdProperty:'LegacyIAccessibleChildIdProperty',
PropertyId.LegacyIAccessibleDefaultActionProperty:'LegacyIAccessibleDefaultActionProperty',
PropertyId.LegacyIAccessibleDescriptionProperty:'LegacyIAccessibleDescriptionProperty',
PropertyId.LegacyIAccessibleHelpProperty:'LegacyIAccessibleHelpProperty',
PropertyId.LegacyIAccessibleKeyboardShortcutProperty:'LegacyIAccessibleKeyboardShortcutProperty',
PropertyId.LegacyIAccessibleNameProperty:'LegacyIAccessibleNameProperty',
PropertyId.LegacyIAccessibleRoleProperty:'LegacyIAccessibleRoleProperty',
PropertyId.LegacyIAccessibleSelectionProperty:'LegacyIAccessibleSelectionProperty',
PropertyId.LegacyIAccessibleStateProperty:'LegacyIAccessibleStateProperty',
PropertyId.LegacyIAccessibleValueProperty:'LegacyIAccessibleValueProperty',
PropertyId.LevelProperty:'LevelProperty',
PropertyId.LiveSettingProperty:'LiveSettingProperty',
PropertyId.LocalizedControlTypeProperty:'LocalizedControlTypeProperty',
PropertyId.LocalizedLandmarkTypeProperty:'LocalizedLandmarkTypeProperty',
PropertyId.MultipleViewCurrentViewProperty:'MultipleViewCurrentViewProperty',
PropertyId.MultipleViewSupportedViewsProperty:'MultipleViewSupportedViewsProperty',
PropertyId.NameProperty:'NameProperty',
PropertyId.NativeWindowHandleProperty:'NativeWindowHandleProperty',
PropertyId.OptimizeForVisualContentProperty:'OptimizeForVisualContentProperty',
PropertyId.OrientationProperty:'OrientationProperty',
PropertyId.OutlineColorProperty:'OutlineColorProperty',
PropertyId.OutlineThicknessProperty:'OutlineThicknessProperty',
PropertyId.PositionInSetProperty:'PositionInSetProperty',
PropertyId.ProcessIdProperty:'ProcessIdProperty',
PropertyId.ProviderDescriptionProperty:'ProviderDescriptionProperty',
PropertyId.RangeValueIsReadOnlyProperty:'RangeValueIsReadOnlyProperty',
PropertyId.RangeValueLargeChangeProperty:'RangeValueLargeChangeProperty',
PropertyId.RangeValueMaximumProperty:'RangeValueMaximumProperty',
PropertyId.RangeValueMinimumProperty:'RangeValueMinimumProperty',
PropertyId.RangeValueSmallChangeProperty:'RangeValueSmallChangeProperty',
PropertyId.RangeValueValueProperty:'RangeValueValueProperty',
PropertyId.RotationProperty:'RotationProperty',
PropertyId.RuntimeIdProperty:'RuntimeIdProperty',
PropertyId.ScrollHorizontalScrollPercentProperty:'ScrollHorizontalScrollPercentProperty',
PropertyId.ScrollHorizontalViewSizeProperty:'ScrollHorizontalViewSizeProperty',
PropertyId.ScrollHorizontallyScrollableProperty:'ScrollHorizontallyScrollableProperty',
PropertyId.ScrollVerticalScrollPercentProperty:'ScrollVerticalScrollPercentProperty',
PropertyId.ScrollVerticalViewSizeProperty:'ScrollVerticalViewSizeProperty',
PropertyId.ScrollVerticallyScrollableProperty:'ScrollVerticallyScrollableProperty',
PropertyId.Selection2CurrentSelectedItemProperty:'Selection2CurrentSelectedItemProperty',
PropertyId.Selection2FirstSelectedItemProperty:'Selection2FirstSelectedItemProperty',
PropertyId.Selection2ItemCountProperty:'Selection2ItemCountProperty',
PropertyId.Selection2LastSelectedItemProperty:'Selection2LastSelectedItemProperty',
PropertyId.SelectionCanSelectMultipleProperty:'SelectionCanSelectMultipleProperty',
PropertyId.SelectionIsSelectionRequiredProperty:'SelectionIsSelectionRequiredProperty',
PropertyId.SelectionItemIsSelectedProperty:'SelectionItemIsSelectedProperty',
PropertyId.SelectionItemSelectionContainerProperty:'SelectionItemSelectionContainerProperty',
PropertyId.SelectionSelectionProperty:'SelectionSelectionProperty',
PropertyId.SizeOfSetProperty:'SizeOfSetProperty',
PropertyId.SizeProperty:'SizeProperty',
PropertyId.SpreadsheetItemAnnotationObjectsProperty:'SpreadsheetItemAnnotationObjectsProperty',
PropertyId.SpreadsheetItemAnnotationTypesProperty:'SpreadsheetItemAnnotationTypesProperty',
PropertyId.SpreadsheetItemFormulaProperty:'SpreadsheetItemFormulaProperty',
PropertyId.StylesExtendedPropertiesProperty:'StylesExtendedPropertiesProperty',
PropertyId.StylesFillColorProperty:'StylesFillColorProperty',
PropertyId.StylesFillPatternColorProperty:'StylesFillPatternColorProperty',
PropertyId.StylesFillPatternStyleProperty:'StylesFillPatternStyleProperty',
PropertyId.StylesShapeProperty:'StylesShapeProperty',
PropertyId.StylesStyleIdProperty:'StylesStyleIdProperty',
PropertyId.StylesStyleNameProperty:'StylesStyleNameProperty',
PropertyId.TableColumnHeadersProperty:'TableColumnHeadersProperty',
PropertyId.TableItemColumnHeaderItemsProperty:'TableItemColumnHeaderItemsProperty',
PropertyId.TableItemRowHeaderItemsProperty:'TableItemRowHeaderItemsProperty',
PropertyId.TableRowHeadersProperty:'TableRowHeadersProperty',
PropertyId.TableRowOrColumnMajorProperty:'TableRowOrColumnMajorProperty',
PropertyId.ToggleToggleStateProperty:'ToggleToggleStateProperty',
PropertyId.Transform2CanZoomProperty:'Transform2CanZoomProperty',
PropertyId.Transform2ZoomLevelProperty:'Transform2ZoomLevelProperty',
PropertyId.Transform2ZoomMaximumProperty:'Transform2ZoomMaximumProperty',
PropertyId.Transform2ZoomMinimumProperty:'Transform2ZoomMinimumProperty',
PropertyId.TransformCanMoveProperty:'TransformCanMoveProperty',
PropertyId.TransformCanResizeProperty:'TransformCanResizeProperty',
PropertyId.TransformCanRotateProperty:'TransformCanRotateProperty',
PropertyId.ValueIsReadOnlyProperty:'ValueIsReadOnlyProperty',
PropertyId.ValueValueProperty:'ValueValueProperty',
PropertyId.VisualEffectsProperty:'VisualEffectsProperty',
PropertyId.WindowCanMaximizeProperty:'WindowCanMaximizeProperty',
PropertyId.WindowCanMinimizeProperty:'WindowCanMinimizeProperty',
PropertyId.WindowIsModalProperty:'WindowIsModalProperty',
PropertyId.WindowIsTopmostProperty:'WindowIsTopmostProperty',
PropertyId.WindowWindowInteractionStateProperty:'WindowWindowInteractionStateProperty',
PropertyId.WindowWindowVisualStateProperty:'WindowWindowVisualStateProperty',
}

class AccessibleRole:

 TitleBar =0x1
 MenuBar =0x2
 ScrollBar =0x3
 Grip =0x4
 Sound =0x5
 Cursor =0x6
 Caret =0x7
 Alert =0x8
 Window =0x9
 Client =0xa
 MenuPopup =0xb
 MenuItem =0xc
 ToolTip =0xd
 Application =0xe
 Document =0xf
 Pane =0x10
 Chart =0x11
 Dialog =0x12
 Border =0x13
 Grouping =0x14
 Separator =0x15
 Toolbar =0x16
 StatusBar =0x17
 Table =0x18
 ColumnHeader =0x19
 RowHeader =0x1a
 Column =0x1b
 Row =0x1c
 Cell =0x1d
 Link =0x1e
 HelpBalloon =0x1f
 Character =0x20
 List =0x21
 ListItem =0x22
 Outline =0x23
 OutlineItem =0x24
 PageTab =0x25
 PropertyPage =0x26
 Indicator =0x27
 Graphic =0x28
 StaticText =0x29
 Text =0x2a
 PushButton =0x2b
 CheckButton =0x2c
 RadioButton =0x2d
 ComboBox =0x2e
 DropList =0x2f
 ProgressBar =0x30
 Dial =0x31
 HotkeyField =0x32
 Slider =0x33
 SpinButton =0x34
 Diagram =0x35
 Animation =0x36
 Equation =0x37
 ButtonDropDown =0x38
 ButtonMenu =0x39
 ButtonDropDownGrid =0x3a
 WhiteSpace =0x3b
 PageTabList =0x3c
 Clock =0x3d
 SplitButton =0x3e
 IpAddress =0x3f
 OutlineButton =0x40

AccessibleRoleNames ={v:k for k, v in AccessibleRole.__dict__.items()if not k.startswith('_')}

class AccessibleState():

 Normal =0
 Unavailable =0x1
 Selected =0x2
 Focused =0x4
 Pressed =0x8
 Checked =0x10
 Mixed =0x20
 Indeterminate =0x20
 ReadOnly =0x40
 HotTracked =0x80
 Default =0x100
 Expanded =0x200
 Collapsed =0x400
 Busy =0x800
 Floating =0x1000
 Marqueed =0x2000
 Animated =0x4000
 Invisible =0x8000
 Offscreen =0x10000
 Sizeable =0x20000
 Moveable =0x40000
 SelfVoicing =0x80000
 Focusable =0x100000
 Selectable =0x200000
 Linked =0x400000
 Traversed =0x800000
 MultiSelectable =0x1000000
 ExtSelectable =0x2000000
 AlertLow =0x4000000
 AlertMedium =0x8000000
 AlertHigh =0x10000000
 Protected =0x20000000
 Valid =0x7fffffff
 HasPopup =0x40000000

class AccessibleSelection:

 None_ =0
 TakeFocus =0x1
 TakeSelection =0x2
 ExtendSelection =0x4
 AddSelection =0x8
 RemoveSelection =0x10

class AnnotationType:

 AdvancedProofingIssue =60020
 Author =60019
 CircularReferenceError =60022
 Comment =60003
 ConflictingChange =60018
 DataValidationError =60021
 DeletionChange =60012
 EditingLockedChange =60016
 Endnote =60009
 ExternalChange =60017
 Footer =60007
 Footnote =60010
 FormatChange =60014
 FormulaError =60004
 GrammarError =60002
 Header =60006
 Highlighted =60008
 InsertionChange =60011
 Mathematics =60023
 MoveChange =60013
 SpellingError =60001
 TrackChanges =60005
 Unknown =60000
 UnsyncedChange =60015

class NavigateDirection:

 Parent =0
 NextSibling =1
 PreviousSibling =2
 FirstChild =3
 LastChild =4

class DockPosition:

 Top =0
 Left =1
 Bottom =2
 Right =3
 Fill =4
 None_ =5

class ScrollAmount:

 LargeDecrement =0
 SmallDecrement =1
 NoAmount =2
 LargeIncrement =3
 SmallIncrement =4

class StyleId:

 Custom =70000
 Heading1 =70001
 Heading2 =70002
 Heading3 =70003
 Heading4 =70004
 Heading5 =70005
 Heading6 =70006
 Heading7 =70007
 Heading8 =70008
 Heading9 =70009
 Title =70010
 Subtitle =70011
 Normal =70012
 Emphasis =70013
 Quote =70014
 BulletedList =70015
 NumberedList =70016

class RowOrColumnMajor:

 RowMajor =0
 ColumnMajor =1
 Indeterminate =2

class ExpandCollapseState:

 Collapsed =0
 Expanded =1
 PartiallyExpanded =2
 LeafNode =3

class OrientationType:

 None_ =0
 Horizontal =1
 Vertical =2

class ToggleState:

 Off =0
 On =1
 Indeterminate =2

class TextPatternRangeEndpoint:

 Start =0
 End =1

class TextAttributeId:

 AfterParagraphSpacingAttribute =40042
 AnimationStyleAttribute =40000
 AnnotationObjectsAttribute =40032
 AnnotationTypesAttribute =40031
 BackgroundColorAttribute =40001
 BeforeParagraphSpacingAttribute =40041
 BulletStyleAttribute =40002
 CapStyleAttribute =40003
 CaretBidiModeAttribute =40039
 CaretPositionAttribute =40038
 CultureAttribute =40004
 FontNameAttribute =40005
 FontSizeAttribute =40006
 FontWeightAttribute =40007
 ForegroundColorAttribute =40008
 HorizontalTextAlignmentAttribute =40009
 IndentationFirstLineAttribute =40010
 IndentationLeadingAttribute =40011
 IndentationTrailingAttribute =40012
 IsActiveAttribute =40036
 IsHiddenAttribute =40013
 IsItalicAttribute =40014
 IsReadOnlyAttribute =40015
 IsSubscriptAttribute =40016
 IsSuperscriptAttribute =40017
 LineSpacingAttribute =40040
 LinkAttribute =40035
 MarginBottomAttribute =40018
 MarginLeadingAttribute =40019
 MarginTopAttribute =40020
 MarginTrailingAttribute =40021
 OutlineStylesAttribute =40022
 OverlineColorAttribute =40023
 OverlineStyleAttribute =40024
 SayAsInterpretAsAttribute =40043
 SelectionActiveEndAttribute =40037
 StrikethroughColorAttribute =40025
 StrikethroughStyleAttribute =40026
 StyleIdAttribute =40034
 StyleNameAttribute =40033
 TabsAttribute =40027
 TextFlowDirectionsAttribute =40028
 UnderlineColorAttribute =40029
 UnderlineStyleAttribute =40030

class TextUnit:

 Character =0
 Format =1
 Word =2
 Line =3
 Paragraph =4
 Page =5
 Document =6

class ZoomUnit:

 NoAmount =0
 LargeDecrement =1
 SmallDecrement =2
 LargeIncrement =3
 SmallIncrement =4

class WindowInteractionState:

 Running =0
 Closing =1
 ReadyForUserInteraction =2
 BlockedByModalWindow =3
 NotResponding =4

class WindowVisualState:

 Normal =0
 Maximized =1
 Minimized =2

class ConsoleColor:

 Default =-1
 Black =0
 DarkBlue =1
 DarkGreen =2
 DarkCyan =3
 DarkRed =4
 DarkMagenta =5
 DarkYellow =6
 Gray =7
 DarkGray =8
 Blue =9
 Green =10
 Cyan =11
 Red =12
 Magenta =13
 Yellow =14
 White =15

class GAFlag:

 Parent =1
 Root =2
 RootOwner =3

class MouseEventFlag:

 Move =0x0001
 LeftDown =0x0002
 LeftUp =0x0004
 RightDown =0x0008
 RightUp =0x0010
 MiddleDown =0x0020
 MiddleUp =0x0040
 XDown =0x0080
 XUp =0x0100
 Wheel =0x0800
 HWheel =0x1000
 MoveNoCoalesce =0x2000
 VirtualDesk =0x4000
 Absolute =0x8000

class KeyboardEventFlag:

 KeyDown =0x0000
 ExtendedKey =0x0001
 KeyUp =0x0002
 KeyUnicode =0x0004
 KeyScanCode =0x0008

class InputType:

 Mouse =0
 Keyboard =1
 Hardware =2

class ModifierKey:

 Alt =0x0001
 Control =0x0002
 Shift =0x0004
 Win =0x0008
 NoRepeat =0x4000

class SW:

 Hide =0
 ShowNormal =1
 Normal =1
 ShowMinimized =2
 ShowMaximized =3
 Maximize =3
 ShowNoActivate =4
 Show =5
 Minimize =6
 ShowMinNoActive =7
 ShowNA =8
 Restore =9
 ShowDefault =10
 ForceMinimize =11
 Max =11

class SWP:

 HWND_Top =0
 HWND_Bottom =1
 HWND_Topmost =-1
 HWND_NoTopmost =-2
 SWP_NoSize =0x0001
 SWP_NoMove =0x0002
 SWP_NoZOrder =0x0004
 SWP_NoRedraw =0x0008
 SWP_NoActivate =0x0010
 SWP_FrameChanged =0x0020
 SWP_ShowWindow =0x0040
 SWP_HideWindow =0x0080
 SWP_NoCopyBits =0x0100
 SWP_NoOwnerZOrder =0x0200
 SWP_NoSendChanging =0x0400
 SWP_DrawFrame =SWP_FrameChanged
 SWP_NoReposition =SWP_NoOwnerZOrder
 SWP_DeferErase =0x2000
 SWP_AsyncWindowPos =0x4000

class MB:

 Ok =0x00000000
 OkCancel =0x00000001
 AbortRetryIgnore =0x00000002
 YesNoCancel =0x00000003
 YesNo =0x00000004
 RetryCancel =0x00000005
 CancelTryContinue =0x00000006
 IconHand =0x00000010
 IconQuestion =0x00000020
 IconExclamation =0x00000030
 IconAsterisk =0x00000040
 UserIcon =0x00000080
 IconWarning =0x00000030
 IconError =0x00000010
 IconInformation =0x00000040
 IconStop =0x00000010
 DefButton1 =0x00000000
 DefButton2 =0x00000100
 DefButton3 =0x00000200
 DefButton4 =0x00000300
 ApplModal =0x00000000
 SystemModal =0x00001000
 TaskModal =0x00002000
 Help =0x00004000
 NoFocus =0x00008000
 SetForeground =0x00010000
 DefaultDesktopOnly =0x00020000
 Topmost =0x00040000
 Right =0x00080000
 RtlReading =0x00100000
 ServiceNotification =0x00200000
 ServiceNotificationNT3X =0x00040000

 TypeMask =0x0000000f
 IconMask =0x000000f0
 DefMask =0x00000f00
 ModeMask =0x00003000
 MiscMask =0x0000c000

 IdOk =1
 IdCancel =2
 IdAbort =3
 IdRetry =4
 IdIgnore =5
 IdYes =6
 IdNo =7
 IdClose =8
 IdHelp =9
 IdTryAgain =10
 IdContinue =11
 IdTimeout =32000

class GWL:
 ExStyle =-20
 HInstance =-6
 HwndParent =-8
 ID =-12
 Style =-16
 UserData =-21
 WndProc =-4

class ProcessDpiAwareness:
 DpiUnaware =0
 SystemDpiAware =1
 PerMonitorDpiAware =2

class DpiAwarenessContext:
 Unaware =-1
 SystemAware =-2
 PerMonitorAware =-3
 PerMonitorAwareV2 =-4
 UnawareGdiScaled =-5

class Keys:

 VK_LBUTTON =0x01
 VK_RBUTTON =0x02
 VK_CANCEL =0x03
 VK_MBUTTON =0x04
 VK_XBUTTON1 =0x05
 VK_XBUTTON2 =0x06
 VK_BACK =0x08
 VK_TAB =0x09
 VK_CLEAR =0x0C
 VK_RETURN =0x0D
 VK_ENTER =0x0D
 VK_SHIFT =0x10
 VK_CONTROL =0x11
 VK_MENU =0x12
 VK_PAUSE =0x13
 VK_CAPITAL =0x14
 VK_KANA =0x15
 VK_HANGUEL =0x15
 VK_HANGUL =0x15
 VK_JUNJA =0x17
 VK_FINAL =0x18
 VK_HANJA =0x19
 VK_KANJI =0x19
 VK_ESCAPE =0x1B
 VK_CONVERT =0x1C
 VK_NONCONVERT =0x1D
 VK_ACCEPT =0x1E
 VK_MODECHANGE =0x1F
 VK_SPACE =0x20
 VK_PRIOR =0x21
 VK_PAGEUP =0x21
 VK_NEXT =0x22
 VK_PAGEDOWN =0x22
 VK_END =0x23
 VK_HOME =0x24
 VK_LEFT =0x25
 VK_UP =0x26
 VK_RIGHT =0x27
 VK_DOWN =0x28
 VK_SELECT =0x29
 VK_PRINT =0x2A
 VK_EXECUTE =0x2B
 VK_SNAPSHOT =0x2C
 VK_INSERT =0x2D
 VK_DELETE =0x2E
 VK_HELP =0x2F
 VK_0 =0x30
 VK_1 =0x31
 VK_2 =0x32
 VK_3 =0x33
 VK_4 =0x34
 VK_5 =0x35
 VK_6 =0x36
 VK_7 =0x37
 VK_8 =0x38
 VK_9 =0x39
 VK_A =0x41
 VK_B =0x42
 VK_C =0x43
 VK_D =0x44
 VK_E =0x45
 VK_F =0x46
 VK_G =0x47
 VK_H =0x48
 VK_I =0x49
 VK_J =0x4A
 VK_K =0x4B
 VK_L =0x4C
 VK_M =0x4D
 VK_N =0x4E
 VK_O =0x4F
 VK_P =0x50
 VK_Q =0x51
 VK_R =0x52
 VK_S =0x53
 VK_T =0x54
 VK_U =0x55
 VK_V =0x56
 VK_W =0x57
 VK_X =0x58
 VK_Y =0x59
 VK_Z =0x5A
 VK_LWIN =0x5B
 VK_RWIN =0x5C
 VK_APPS =0x5D
 VK_SLEEP =0x5F
 VK_NUMPAD0 =0x60
 VK_NUMPAD1 =0x61
 VK_NUMPAD2 =0x62
 VK_NUMPAD3 =0x63
 VK_NUMPAD4 =0x64
 VK_NUMPAD5 =0x65
 VK_NUMPAD6 =0x66
 VK_NUMPAD7 =0x67
 VK_NUMPAD8 =0x68
 VK_NUMPAD9 =0x69
 VK_MULTIPLY =0x6A
 VK_ADD =0x6B
 VK_SEPARATOR =0x6C
 VK_SUBTRACT =0x6D
 VK_DECIMAL =0x6E
 VK_DIVIDE =0x6F
 VK_F1 =0x70
 VK_F2 =0x71
 VK_F3 =0x72
 VK_F4 =0x73
 VK_F5 =0x74
 VK_F6 =0x75
 VK_F7 =0x76
 VK_F8 =0x77
 VK_F9 =0x78
 VK_F10 =0x79
 VK_F11 =0x7A
 VK_F12 =0x7B
 VK_F13 =0x7C
 VK_F14 =0x7D
 VK_F15 =0x7E
 VK_F16 =0x7F
 VK_F17 =0x80
 VK_F18 =0x81
 VK_F19 =0x82
 VK_F20 =0x83
 VK_F21 =0x84
 VK_F22 =0x85
 VK_F23 =0x86
 VK_F24 =0x87
 VK_NUMLOCK =0x90
 VK_SCROLL =0x91
 VK_LSHIFT =0xA0
 VK_RSHIFT =0xA1
 VK_LCONTROL =0xA2
 VK_RCONTROL =0xA3
 VK_LMENU =0xA4
 VK_RMENU =0xA5
 VK_BROWSER_BACK =0xA6
 VK_BROWSER_FORWARD =0xA7
 VK_BROWSER_REFRESH =0xA8
 VK_BROWSER_STOP =0xA9
 VK_BROWSER_SEARCH =0xAA
 VK_BROWSER_FAVORITES =0xAB
 VK_BROWSER_HOME =0xAC
 VK_VOLUME_MUTE =0xAD
 VK_VOLUME_DOWN =0xAE
 VK_VOLUME_UP =0xAF
 VK_MEDIA_NEXT_TRACK =0xB0
 VK_MEDIA_PREV_TRACK =0xB1
 VK_MEDIA_STOP =0xB2
 VK_MEDIA_PLAY_PAUSE =0xB3
 VK_LAUNCH_MAIL =0xB4
 VK_LAUNCH_MEDIA_SELECT =0xB5
 VK_LAUNCH_APP1 =0xB6
 VK_LAUNCH_APP2 =0xB7
 VK_OEM_1 =0xBA
 VK_OEM_PLUS =0xBB
 VK_OEM_COMMA =0xBC
 VK_OEM_MINUS =0xBD
 VK_OEM_PERIOD =0xBE
 VK_OEM_2 =0xBF
 VK_OEM_3 =0xC0
 VK_OEM_4 =0xDB
 VK_OEM_5 =0xDC
 VK_OEM_6 =0xDD
 VK_OEM_7 =0xDE
 VK_OEM_8 =0xDF
 VK_OEM_102 =0xE2
 VK_PROCESSKEY =0xE5
 VK_PACKET =0xE7
 VK_ATTN =0xF6
 VK_CRSEL =0xF7
 VK_EXSEL =0xF8
 VK_EREOF =0xF9
 VK_PLAY =0xFA
 VK_ZOOM =0xFB
 VK_NONAME =0xFC
 VK_PA1 =0xFD
 VK_OEM_CLEAR =0xFE

SpecialKeyNames ={
'LBUTTON':Keys.VK_LBUTTON,
'RBUTTON':Keys.VK_RBUTTON,
'CANCEL':Keys.VK_CANCEL,
'MBUTTON':Keys.VK_MBUTTON,
'XBUTTON1':Keys.VK_XBUTTON1,
'XBUTTON2':Keys.VK_XBUTTON2,
'BACK':Keys.VK_BACK,
'TAB':Keys.VK_TAB,
'CLEAR':Keys.VK_CLEAR,
'RETURN':Keys.VK_RETURN,
'ENTER':Keys.VK_RETURN,
'SHIFT':Keys.VK_SHIFT,
'CTRL':Keys.VK_CONTROL,
'CONTROL':Keys.VK_CONTROL,
'ALT':Keys.VK_MENU,
'PAUSE':Keys.VK_PAUSE,
'CAPITAL':Keys.VK_CAPITAL,
'KANA':Keys.VK_KANA,
'HANGUEL':Keys.VK_HANGUEL,
'HANGUL':Keys.VK_HANGUL,
'JUNJA':Keys.VK_JUNJA,
'FINAL':Keys.VK_FINAL,
'HANJA':Keys.VK_HANJA,
'KANJI':Keys.VK_KANJI,
'ESC':Keys.VK_ESCAPE,
'ESCAPE':Keys.VK_ESCAPE,
'CONVERT':Keys.VK_CONVERT,
'NONCONVERT':Keys.VK_NONCONVERT,
'ACCEPT':Keys.VK_ACCEPT,
'MODECHANGE':Keys.VK_MODECHANGE,
'SPACE':Keys.VK_SPACE,
'PRIOR':Keys.VK_PRIOR,
'PAGEUP':Keys.VK_PRIOR,
'NEXT':Keys.VK_NEXT,
'PAGEDOWN':Keys.VK_NEXT,
'END':Keys.VK_END,
'HOME':Keys.VK_HOME,
'LEFT':Keys.VK_LEFT,
'UP':Keys.VK_UP,
'RIGHT':Keys.VK_RIGHT,
'DOWN':Keys.VK_DOWN,
'SELECT':Keys.VK_SELECT,
'PRINT':Keys.VK_PRINT,
'EXECUTE':Keys.VK_EXECUTE,
'SNAPSHOT':Keys.VK_SNAPSHOT,
'PRINTSCREEN':Keys.VK_SNAPSHOT,
'INSERT':Keys.VK_INSERT,
'INS':Keys.VK_INSERT,
'DELETE':Keys.VK_DELETE,
'DEL':Keys.VK_DELETE,
'HELP':Keys.VK_HELP,
'WIN':Keys.VK_LWIN,
'LWIN':Keys.VK_LWIN,
'RWIN':Keys.VK_RWIN,
'APPS':Keys.VK_APPS,
'SLEEP':Keys.VK_SLEEP,
'NUMPAD0':Keys.VK_NUMPAD0,
'NUMPAD1':Keys.VK_NUMPAD1,
'NUMPAD2':Keys.VK_NUMPAD2,
'NUMPAD3':Keys.VK_NUMPAD3,
'NUMPAD4':Keys.VK_NUMPAD4,
'NUMPAD5':Keys.VK_NUMPAD5,
'NUMPAD6':Keys.VK_NUMPAD6,
'NUMPAD7':Keys.VK_NUMPAD7,
'NUMPAD8':Keys.VK_NUMPAD8,
'NUMPAD9':Keys.VK_NUMPAD9,
'MULTIPLY':Keys.VK_MULTIPLY,
'ADD':Keys.VK_ADD,
'SEPARATOR':Keys.VK_SEPARATOR,
'SUBTRACT':Keys.VK_SUBTRACT,
'DECIMAL':Keys.VK_DECIMAL,
'DIVIDE':Keys.VK_DIVIDE,
'F1':Keys.VK_F1,
'F2':Keys.VK_F2,
'F3':Keys.VK_F3,
'F4':Keys.VK_F4,
'F5':Keys.VK_F5,
'F6':Keys.VK_F6,
'F7':Keys.VK_F7,
'F8':Keys.VK_F8,
'F9':Keys.VK_F9,
'F10':Keys.VK_F10,
'F11':Keys.VK_F11,
'F12':Keys.VK_F12,
'F13':Keys.VK_F13,
'F14':Keys.VK_F14,
'F15':Keys.VK_F15,
'F16':Keys.VK_F16,
'F17':Keys.VK_F17,
'F18':Keys.VK_F18,
'F19':Keys.VK_F19,
'F20':Keys.VK_F20,
'F21':Keys.VK_F21,
'F22':Keys.VK_F22,
'F23':Keys.VK_F23,
'F24':Keys.VK_F24,
'NUMLOCK':Keys.VK_NUMLOCK,
'SCROLL':Keys.VK_SCROLL,
'LSHIFT':Keys.VK_LSHIFT,
'RSHIFT':Keys.VK_RSHIFT,
'LCONTROL':Keys.VK_LCONTROL,
'LCTRL':Keys.VK_LCONTROL,
'RCONTROL':Keys.VK_RCONTROL,
'RCTRL':Keys.VK_RCONTROL,
'LALT':Keys.VK_LMENU,
'RALT':Keys.VK_RMENU,
'BROWSER_BACK':Keys.VK_BROWSER_BACK,
'BROWSER_FORWARD':Keys.VK_BROWSER_FORWARD,
'BROWSER_REFRESH':Keys.VK_BROWSER_REFRESH,
'BROWSER_STOP':Keys.VK_BROWSER_STOP,
'BROWSER_SEARCH':Keys.VK_BROWSER_SEARCH,
'BROWSER_FAVORITES':Keys.VK_BROWSER_FAVORITES,
'BROWSER_HOME':Keys.VK_BROWSER_HOME,
'VOLUME_MUTE':Keys.VK_VOLUME_MUTE,
'VOLUME_DOWN':Keys.VK_VOLUME_DOWN,
'VOLUME_UP':Keys.VK_VOLUME_UP,
'MEDIA_NEXT_TRACK':Keys.VK_MEDIA_NEXT_TRACK,
'MEDIA_PREV_TRACK':Keys.VK_MEDIA_PREV_TRACK,
'MEDIA_STOP':Keys.VK_MEDIA_STOP,
'MEDIA_PLAY_PAUSE':Keys.VK_MEDIA_PLAY_PAUSE,
'LAUNCH_MAIL':Keys.VK_LAUNCH_MAIL,
'LAUNCH_MEDIA_SELECT':Keys.VK_LAUNCH_MEDIA_SELECT,
'LAUNCH_APP1':Keys.VK_LAUNCH_APP1,
'LAUNCH_APP2':Keys.VK_LAUNCH_APP2,
'OEM_1':Keys.VK_OEM_1,
'OEM_PLUS':Keys.VK_OEM_PLUS,
'OEM_COMMA':Keys.VK_OEM_COMMA,
'OEM_MINUS':Keys.VK_OEM_MINUS,
'OEM_PERIOD':Keys.VK_OEM_PERIOD,
'OEM_2':Keys.VK_OEM_2,
'OEM_3':Keys.VK_OEM_3,
'OEM_4':Keys.VK_OEM_4,
'OEM_5':Keys.VK_OEM_5,
'OEM_6':Keys.VK_OEM_6,
'OEM_7':Keys.VK_OEM_7,
'OEM_8':Keys.VK_OEM_8,
'OEM_102':Keys.VK_OEM_102,
'PROCESSKEY':Keys.VK_PROCESSKEY,
'PACKET':Keys.VK_PACKET,
'ATTN':Keys.VK_ATTN,
'CRSEL':Keys.VK_CRSEL,
'EXSEL':Keys.VK_EXSEL,
'EREOF':Keys.VK_EREOF,
'PLAY':Keys.VK_PLAY,
'ZOOM':Keys.VK_ZOOM,
'NONAME':Keys.VK_NONAME,
'PA1':Keys.VK_PA1,
'OEM_CLEAR':Keys.VK_OEM_CLEAR,
}

CharacterCodes ={
'0':Keys.VK_0,
'1':Keys.VK_1,
'2':Keys.VK_2,
'3':Keys.VK_3,
'4':Keys.VK_4,
'5':Keys.VK_5,
'6':Keys.VK_6,
'7':Keys.VK_7,
'8':Keys.VK_8,
'9':Keys.VK_9,
'a':Keys.VK_A,
'A':Keys.VK_A,
'b':Keys.VK_B,
'B':Keys.VK_B,
'c':Keys.VK_C,
'C':Keys.VK_C,
'd':Keys.VK_D,
'D':Keys.VK_D,
'e':Keys.VK_E,
'E':Keys.VK_E,
'f':Keys.VK_F,
'F':Keys.VK_F,
'g':Keys.VK_G,
'G':Keys.VK_G,
'h':Keys.VK_H,
'H':Keys.VK_H,
'i':Keys.VK_I,
'I':Keys.VK_I,
'j':Keys.VK_J,
'J':Keys.VK_J,
'k':Keys.VK_K,
'K':Keys.VK_K,
'l':Keys.VK_L,
'L':Keys.VK_L,
'm':Keys.VK_M,
'M':Keys.VK_M,
'n':Keys.VK_N,
'N':Keys.VK_N,
'o':Keys.VK_O,
'O':Keys.VK_O,
'p':Keys.VK_P,
'P':Keys.VK_P,
'q':Keys.VK_Q,
'Q':Keys.VK_Q,
'r':Keys.VK_R,
'R':Keys.VK_R,
's':Keys.VK_S,
'S':Keys.VK_S,
't':Keys.VK_T,
'T':Keys.VK_T,
'u':Keys.VK_U,
'U':Keys.VK_U,
'v':Keys.VK_V,
'V':Keys.VK_V,
'w':Keys.VK_W,
'W':Keys.VK_W,
'x':Keys.VK_X,
'X':Keys.VK_X,
'y':Keys.VK_Y,
'Y':Keys.VK_Y,
'z':Keys.VK_Z,
'Z':Keys.VK_Z,
' ':Keys.VK_SPACE,
'`':Keys.VK_OEM_3,

'-':Keys.VK_OEM_MINUS,

'=':Keys.VK_OEM_PLUS,

'[':Keys.VK_OEM_4,

']':Keys.VK_OEM_6,

'\\':Keys.VK_OEM_5,

'; ':Keys.VK_OEM_1,

'\'':Keys.VK_OEM_7,

', ':Keys.VK_OEM_COMMA,

'.':Keys.VK_OEM_PERIOD,

'/':Keys.VK_OEM_2,

}

class ConsoleScreenBufferInfo(ctypes.Structure):
 _fields_ =[
 ('dwSize', ctypes.wintypes._COORD),
 ('dwCursorPosition', ctypes.wintypes._COORD),
 ('wAttributes', ctypes.c_uint),
 ('srWindow', ctypes.wintypes.SMALL_RECT),
 ('dwMaximumWindowSize', ctypes.wintypes._COORD),
]

class MOUSEINPUT(ctypes.Structure):
 _fields_ =(('dx', ctypes.wintypes.LONG),
 ('dy', ctypes.wintypes.LONG),
 ('mouseData', ctypes.wintypes.DWORD),
 ('dwFlags', ctypes.wintypes.DWORD),
 ('time', ctypes.wintypes.DWORD),
 ('dwExtraInfo', ctypes.wintypes.PULONG))

class KEYBDINPUT(ctypes.Structure):
 _fields_ =(('wVk', ctypes.wintypes.WORD),
 ('wScan', ctypes.wintypes.WORD),
 ('dwFlags', ctypes.wintypes.DWORD),
 ('time', ctypes.wintypes.DWORD),
 ('dwExtraInfo', ctypes.wintypes.PULONG))

class HARDWAREINPUT(ctypes.Structure):
 _fields_ =(('uMsg', ctypes.wintypes.DWORD),
 ('wParamL', ctypes.wintypes.WORD),
 ('wParamH', ctypes.wintypes.WORD))

class INPUTUnion(ctypes.Union):
 _fields_ =(('mi', MOUSEINPUT),
 ('ki', KEYBDINPUT),
 ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
 _fields_ =(('type', ctypes.wintypes.DWORD),
 ('union', INPUTUnion))

class Rect():

 def __init__(self, left:int =0, top:int =0, right:int =0, bottom:int =0):
 self.left =left
 self.top =top
 self.right =right
 self.bottom =bottom

 def width(self)->int:
 return self.right -self.left

 def height(self)->int:
 return self.bottom -self.top

 def xcenter(self)->int:
 return self.left +self.width()//2

 def ycenter(self)->int:
 return self.top +self.height()//2

 def isempty(self)->int:
 return self.width()==0 or self.height()==0

 def contains(self, x:int, y:int)->bool:
 return self.left <=x <self.right and self.top <=y <self.bottom

 def intersect(self, rect:'Rect')->'Rect':
 left, top, right, bottom =max(self.left, rect.left), max(self.top, rect.top), min(self.right, rect.right), min(self.bottom, rect.bottom)
 return Rect(left, top, right, bottom)

 def offset(self, x:int, y:int)->None:
 self.left +=x
 self.right +=x
 self.top +=y
 self.bottom +=y

 def __eq__(self, rect):
 return self.left ==rect.left and self.top ==rect.top and self.right ==rect.right and self.bottom ==rect.bottom

 def __str__(self)->str:
 return '({}, {}, {}, {})[{}x{}]'.format(self.left, self.top, self.right, self.bottom, self.width(), self.height())

 def __repr__(self)->str:
 return '{}({}, {}, {}, {})[{}x{}]'.format(self.__class__.__name__, self.left, self.top, self.right, self.bottom, self.width(), self.height())

class ClipboardFormat:
 CF_TEXT =1
 CF_BITMAP =2
 CF_METAFILEPICT =3
 CF_SYLK =4
 CF_DIF =5
 CF_TIFF =6
 CF_OEMTEXT =7
 CF_DIB =8
 CF_PALETTE =9
 CF_PENDATA =10
 CF_RIFF =11
 CF_WAVE =12
 CF_UNICODETEXT =13
 CF_ENHMETAFILE =14
 CF_HDROP =15
 CF_LOCALE =16
 CF_DIBV5 =17
 CF_MAX =18
 CF_HTML =ctypes.windll.user32.RegisterClipboardFormatW("HTML Format")

class ActiveEnd(IntEnum):
 ActiveEnd_None =0
 ActiveEnd_Start =1
 ActiveEnd_End =2

class AnimationStyle(IntEnum):
 AnimationStyle_None =0
 AnimationStyle_LasVegasLights =1
 AnimationStyle_BlinkingBackground =2
 AnimationStyle_SparkleText =3
 AnimationStyle_MarchingBlackAnts =4
 AnimationStyle_MarchingRedAnts =5
 AnimationStyle_Shimmer =6
 AnimationStyle_Other =-1

class AsyncContentLoadedState(IntEnum):
 AsyncContentLoadedState_Beginning =0
 AsyncContentLoadedState_Progress =1
 AsyncContentLoadedState_Completed =2

class AutomationElementMode(IntEnum):
 AutomationElementMode_None =0
 AutomationElementMode_Full =1

class AutomationIdentifierType(IntEnum):
 AutomationIdentifierType_Property =0
 AutomationIdentifierType_Pattern =1
 AutomationIdentifierType_Event =2
 AutomationIdentifierType_ControlType =3
 AutomationIdentifierType_TextAttribute =4
 AutomationIdentifierType_LandmarkType =5
 AutomationIdentifierType_Annotation =6
 AutomationIdentifierType_Changes =7
 AutomationIdentifierType_Style =8

class BulletStyle(IntEnum):
 BulletStyle_None =0
 BulletStyle_HollowRoundBullet =1
 BulletStyle_FilledRoundBullet =2
 BulletStyle_HollowSquareBullet =3
 BulletStyle_FilledSquareBullet =4
 BulletStyle_DashBullet =5
 BulletStyle_Other =-1

class CapStyle(IntEnum):
 CapStyle_None =0
 CapStyle_SmallCap =1
 CapStyle_AllCap =2
 CapStyle_AllPetiteCaps =3
 CapStyle_PetiteCaps =4
 CapStyle_Unicase =5
 CapStyle_Titling =6
 CapStyle_Other =-1

class CaretBidiMode(IntEnum):
 CaretBidiMode_LTR =0
 CaretBidiMode_RTL =1

class CaretPosition(IntEnum):
 CaretPosition_Unknown =0
 CaretPosition_EndOfLine =1
 CaretPosition_BeginningOfLine =2

class CoalesceEventsOptions(IntFlag):
 CoalesceEventsOptions_Disabled =0
 CoalesceEventsOptions_Enabled =1

class ConditionType(IntEnum):
 ConditionType_True =0
 ConditionType_False =1
 ConditionType_Property =2
 ConditionType_And =3
 ConditionType_Or =4
 ConditionType_Not =5

class ConnectionRecoveryBehaviorOptions(IntFlag):
 ConnectionRecoveryBehaviorOptions_Disabled =0
 ConnectionRecoveryBehaviorOptions_Enabled =1

class EventArgsType(IntEnum):
 EventArgsType_Simple =0
 EventArgsType_PropertyChanged =1
 EventArgsType_StructureChanged =2
 EventArgsType_AsyncContentLoaded =3
 EventArgsType_WindowClosed =4
 EventArgsType_TextEditTextChanged =5
 EventArgsType_Changes =6
 EventArgsType_Notification =7
 EventArgsType_ActiveTextPositionChanged =8
 EventArgsType_StructuredMarkup =9

class FillType(IntEnum):
 FillType_None =0
 FillType_Color =1
 FillType_Gradient =2
 FillType_Picture =3
 FillType_Pattern =4

class FlowDirections(IntEnum):
 FlowDirections_Default =0
 FlowDirections_RightToLeft =1
 FlowDirections_BottomToTop =2
 FlowDirections_Vertical =4

class LiveSetting(IntEnum):
 Off =0
 Polite =1
 Assertive =2

class NormalizeState(IntEnum):
 NormalizeState_None =0
 NormalizeState_View =1
 NormalizeState_Custom =2

class NotificationKind(IntEnum):
 NotificationKind_ItemAdded =0
 NotificationKind_ItemRemoved =1
 NotificationKind_ActionCompleted =2
 NotificationKind_ActionAborted =3
 NotificationKind_Other =4

class NotificationProcessing(IntEnum):
 NotificationProcessing_ImportantAll =0
 NotificationProcessing_ImportantMostRecent =1
 NotificationProcessing_All =2
 NotificationProcessing_MostRecent =3
 NotificationProcessing_CurrentThenMostRecent =4
 NotificationProcessing_ImportantCurrentThenMostRecent =5

class OutlineStyles(IntEnum):
 OutlineStyles_None =0
 OutlineStyles_Outline =1
 OutlineStyles_Shadow =2
 OutlineStyles_Engraved =4
 OutlineStyles_Embossed =8

class PropertyConditionFlags(IntFlag):
 PropertyConditionFlags_None =0
 PropertyConditionFlags_IgnoreCase =1
 PropertyConditionFlags_MatchSubstring =2

class ProviderOptions(IntFlag):
 ProviderOptions_ClientSideProvider =1
 ProviderOptions_ServerSideProvider =2
 ProviderOptions_NonClientAreaProvider =4
 ProviderOptions_OverrideProvider =8
 ProviderOptions_ProviderOwnsSetFocus =16
 ProviderOptions_UseComThreading =32
 ProviderOptions_RefuseNonClientSupport =64
 ProviderOptions_HasNativeIAccessible =128
 ProviderOptions_UseClientCoordinates =256

class ProviderType(IntEnum):
 ProviderType_BaseHwnd =0
 ProviderType_Proxy =1
 ProviderType_NonClientArea =2

class SayAsInterpretAs(IntEnum):
 SayAsInterpretAs_None =0
 SayAsInterpretAs_Spell =1
 SayAsInterpretAs_Cardinal =2
 SayAsInterpretAs_Ordinal =3
 SayAsInterpretAs_Number =4
 SayAsInterpretAs_Date =5
 SayAsInterpretAs_Time =6
 SayAsInterpretAs_Telephone =7
 SayAsInterpretAs_Currency =8
 SayAsInterpretAs_Net =9
 SayAsInterpretAs_Url =10
 SayAsInterpretAs_Address =11
 SayAsInterpretAs_Alphanumeric =12
 SayAsInterpretAs_Name =13
 SayAsInterpretAs_Media =14
 SayAsInterpretAs_Date_MonthDayYear =15
 SayAsInterpretAs_Date_DayMonthYear =16
 SayAsInterpretAs_Date_YearMonthDay =17
 SayAsInterpretAs_Date_YearMonth =18
 SayAsInterpretAs_Date_MonthYear =19
 SayAsInterpretAs_Date_DayMonth =20
 SayAsInterpretAs_Date_MonthDay =21
 SayAsInterpretAs_Date_Year =22
 SayAsInterpretAs_Time_HoursMinutesSeconds12 =23
 SayAsInterpretAs_Time_HoursMinutes12 =24
 SayAsInterpretAs_Time_HoursMinutesSeconds24 =25
 SayAsInterpretAs_Time_HoursMinutes24 =26

class StructureChangeType(IntEnum):
 StructureChangeType_ChildAdded =0
 StructureChangeType_ChildRemoved =1
 StructureChangeType_ChildrenInvalidated =2
 StructureChangeType_ChildrenBulkAdded =3
 StructureChangeType_ChildrenBulkRemoved =4
 StructureChangeType_ChildrenReordered =5

class SupportedTextSelection(IntEnum):
 SupportedTextSelection_None =0
 SupportedTextSelection_Single =1
 SupportedTextSelection_Multiple =2

class SynchronizedInputType(IntEnum):
 SynchronizedInputType_KeyUp =1
 SynchronizedInputType_KeyDown =2
 SynchronizedInputType_LeftMouseUp =4
 SynchronizedInputType_LeftMouseDown =8
 SynchronizedInputType_RightMouseUp =16
 SynchronizedInputType_RightMouseDown =32

class TextDecorationLineStyle(IntEnum):
 TextDecorationLineStyle_None =0
 TextDecorationLineStyle_Single =1
 TextDecorationLineStyle_WordsOnly =2
 TextDecorationLineStyle_Double =3
 TextDecorationLineStyle_Dot =4
 TextDecorationLineStyle_Dash =5
 TextDecorationLineStyle_DashDot =6
 TextDecorationLineStyle_DashDotDot =7
 TextDecorationLineStyle_Wavy =8
 TextDecorationLineStyle_ThickSingle =9
 TextDecorationLineStyle_DoubleWavy =11
 TextDecorationLineStyle_ThickWavy =12
 TextDecorationLineStyle_LongDash =13
 TextDecorationLineStyle_ThickDash =14
 TextDecorationLineStyle_ThickDashDot =15
 TextDecorationLineStyle_ThickDashDotDot =16
 TextDecorationLineStyle_ThickDot =17
 TextDecorationLineStyle_ThickLongDash =18
 TextDecorationLineStyle_Other =-1

class TextEditChangeType(IntEnum):
 TextEditChangeType_None =0
 TextEditChangeType_AutoCorrect =1
 TextEditChangeType_Composition =2
 TextEditChangeType_CompositionFinalized =3
 TextEditChangeType_AutoComplete =4

class TreeScope(IntEnum):
 TreeScope_None =0
 TreeScope_Element =1
 TreeScope_Children =2
 TreeScope_Descendants =4
 TreeScope_Parent =8
 TreeScope_Ancestors =16
 TreeScope_Subtree =7

class TreeTraversalOptions(IntFlag):
 TreeTraversalOptions_Default =0
 TreeTraversalOptions_PostOrder =1
 TreeTraversalOptions_LastToFirstOrder =2

class UIAutomationType(IntEnum):
 UIAutomationType_Int =1
 UIAutomationType_Bool =2
 UIAutomationType_String =3
 UIAutomationType_Double =4
 UIAutomationType_Point =5
 UIAutomationType_Rect =6
 UIAutomationType_Element =7
 UIAutomationType_Array =65536
 UIAutomationType_Out =131072
 UIAutomationType_IntArray =131073
 UIAutomationType_BoolArray =131074
 UIAutomationType_StringArray =131075
 UIAutomationType_DoubleArray =131076
 UIAutomationType_PointArray =131077
 UIAutomationType_RectArray =131078
 UIAutomationType_ElementArray =131079
 UIAutomationType_OutInt =131080
 UIAutomationType_OutBool =131081
 UIAutomationType_OutString =131082
 UIAutomationType_OutDouble =131083
 UIAutomationType_OutPoint =131084
 UIAutomationType_OutRect =131085
 UIAutomationType_OutElement =131086
 UIAutomationType_OutIntArray =131087
 UIAutomationType_OutBoolArray =131088
 UIAutomationType_OutStringArray =131089
 UIAutomationType_OutDoubleArray =131090
 UIAutomationType_OutPointArray =131091
 UIAutomationType_OutRectArray =131092
 UIAutomationType_OutElementArray =131093

class VisualEffects(IntEnum):
 VisualEffects_None =0
 VisualEffects_Shadow =1
 VisualEffects_Reflection =2
 VisualEffects_Glow =3
 VisualEffects_SoftEdges =4
 VisualEffects_Bevel =5

