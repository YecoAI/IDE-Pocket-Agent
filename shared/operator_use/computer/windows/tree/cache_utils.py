

from operator_use.computer.windows.uia import CacheRequest, PropertyId, PatternId, TreeScope, Control
from typing import Optional
import logging

logger =logging.getLogger(__name__)

class CacheRequestFactory:

 @staticmethod
 def create_tree_traversal_cache()->CacheRequest:

 cache_request =CacheRequest()

 cache_request.TreeScope =TreeScope.TreeScope_Element |TreeScope.TreeScope_Children

 cache_request.AddProperty(PropertyId.NameProperty)
 cache_request.AddProperty(PropertyId.AutomationIdProperty)
 cache_request.AddProperty(PropertyId.LocalizedControlTypeProperty)
 cache_request.AddProperty(PropertyId.AcceleratorKeyProperty)
 cache_request.AddProperty(PropertyId.ClassNameProperty)
 cache_request.AddProperty(PropertyId.ControlTypeProperty)

 cache_request.AddProperty(PropertyId.IsEnabledProperty)
 cache_request.AddProperty(PropertyId.IsOffscreenProperty)
 cache_request.AddProperty(PropertyId.IsControlElementProperty)
 cache_request.AddProperty(PropertyId.HasKeyboardFocusProperty)
 cache_request.AddProperty(PropertyId.IsKeyboardFocusableProperty)
 cache_request.AddProperty(PropertyId.IsPasswordProperty)

 cache_request.AddProperty(PropertyId.BoundingRectangleProperty)
 cache_request.AddProperty(PropertyId.HelpTextProperty)

 cache_request.AddPattern(PatternId.LegacyIAccessiblePattern)
 cache_request.AddPattern(PatternId.ScrollPattern)
 cache_request.AddPattern(PatternId.WindowPattern)

 cache_request.AddProperty(PropertyId.LegacyIAccessibleRoleProperty)
 cache_request.AddProperty(PropertyId.LegacyIAccessibleValueProperty)
 cache_request.AddProperty(PropertyId.LegacyIAccessibleDefaultActionProperty)
 cache_request.AddProperty(PropertyId.LegacyIAccessibleStateProperty)

 cache_request.AddProperty(PropertyId.ScrollHorizontallyScrollableProperty)
 cache_request.AddProperty(PropertyId.ScrollVerticallyScrollableProperty)
 cache_request.AddProperty(PropertyId.ScrollHorizontalScrollPercentProperty)
 cache_request.AddProperty(PropertyId.ScrollVerticalScrollPercentProperty)

 cache_request.AddProperty(PropertyId.ExpandCollapseExpandCollapseStateProperty)

 cache_request.AddProperty(PropertyId.SelectionCanSelectMultipleProperty)
 cache_request.AddProperty(PropertyId.SelectionIsSelectionRequiredProperty)
 cache_request.AddProperty(PropertyId.SelectionSelectionProperty)

 cache_request.AddProperty(PropertyId.SelectionItemIsSelectedProperty)
 cache_request.AddProperty(PropertyId.SelectionItemSelectionContainerProperty)

 cache_request.AddProperty(PropertyId.WindowIsModalProperty)

 cache_request.AddProperty(PropertyId.ToggleToggleStateProperty)

 cache_request.AddProperty(PropertyId.RangeValueValueProperty)
 cache_request.AddProperty(PropertyId.RangeValueMinimumProperty)
 cache_request.AddProperty(PropertyId.RangeValueMaximumProperty)

 return cache_request

class CachedControlHelper:

 @staticmethod
 def build_cached_control(node:Control, cache_request:Optional[CacheRequest]=None)->Control:

 if cache_request is None:
 cache_request =CacheRequestFactory.create_tree_traversal_cache()

 try:
 cached_node =node.BuildUpdatedCache(cache_request)
 cached_node._is_cached =True
 return cached_node
 except Exception as e:
 logger.debug(f"Failed to build cached control: {e }")
 return node

 @staticmethod
 def get_cached_children(node:Control, cache_request:Optional[CacheRequest]=None)->list[Control]:

 if cache_request is None:
 cache_request =CacheRequestFactory.create_tree_traversal_cache()

 if(cache_request.TreeScope &TreeScope.TreeScope_Children)==0:
 logger.warning("Cache request passed to get_cached_children does not have Children scope!")

 try:

 cached_node =node.BuildUpdatedCache(cache_request)
 children =cached_node.GetCachedChildren()

 for child in children:
 child._is_cached =True

 logger.debug(f"Retrieved {len(children)} cached children(newly built)")
 return children

 except Exception as e:
 logger.debug(f"Failed to get cached children, falling back to regular access: {e }")
 return node.GetChildren()
