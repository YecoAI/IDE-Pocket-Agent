

import ctypes
import logging
import sys
import threading
from ctypes import HRESULT, POINTER, byref, c_void_p
from ctypes.wintypes import BOOL, HWND, UINT

import comtypes.client
from comtypes import COMMETHOD, GUID, IUnknown, STDMETHOD

logger =logging.getLogger(__name__)

_thread_local =threading.local()

def _get_manager():
 if not hasattr(_thread_local, "manager"):
 _thread_local.manager =VirtualDesktopManager()
 return _thread_local.manager

def is_window_on_current_desktop(hwnd:int)->bool:
 return _get_manager().is_window_on_current_desktop(hwnd)

def get_window_desktop_id(hwnd:int)->str:
 return _get_manager().get_window_desktop_id(hwnd)

def move_window_to_desktop(hwnd:int, desktop_id:str):
 _get_manager().move_window_to_desktop(hwnd, desktop_id)

CLSID_VirtualDesktopManager =GUID("{aa509086-5ca9-4c25-8f95-589d3c07b48a}")
CLSID_ImmersiveShell =GUID("{C2F03A33-21F5-47FA-B4BB-156362A2F239}")
CLSID_VirtualDesktopManagerInternal =GUID("{C5E0CDCA-7B6E-41B2-9FC4-D93975CC467B}")
IID_IServiceProvider =GUID("{6D5140C1-7436-11CE-8034-00AA006009FA}")

class IVirtualDesktopManager(IUnknown):
 _iid_ =GUID("{a5cd92ff-29be-454c-8d04-d82879fb3f1b}")
 _methods_ =[
 COMMETHOD(
 [],
 HRESULT,
 "IsWindowOnCurrentVirtualDesktop",
 (["in"], HWND, "topLevelWindow"),
 (["out", "retval"], POINTER(BOOL), "onCurrentDesktop"),
),
 COMMETHOD(
 [],
 HRESULT,
 "GetWindowDesktopId",
 (["in"], HWND, "topLevelWindow"),
 (["out", "retval"], POINTER(GUID), "desktopId"),
),
 COMMETHOD(
 [],
 HRESULT,
 "MoveWindowToDesktop",
 (["in"], HWND, "topLevelWindow"),
 (["in"], POINTER(GUID), "desktopId"),
),
]

class IServiceProvider(IUnknown):
 _iid_ =IID_IServiceProvider
 _methods_ =[
 COMMETHOD(
 [],
 HRESULT,
 "QueryService",
 (["in"], POINTER(GUID), "guidService"),
 (["in"], POINTER(GUID), "riid"),
 (["out"], POINTER(POINTER(IUnknown)), "ppvObject"),
),
]

class IObjectArray(IUnknown):
 _iid_ =GUID("{92CA9DCD-5622-4BBA-A805-5E9F541BD8CC}")
 _methods_ =[
 COMMETHOD(
 [],
 HRESULT,
 "GetCount",
 (["out"], POINTER(UINT), "pcObjects"),
),
 COMMETHOD(
 [],
 HRESULT,
 "GetAt",
 (["in"], UINT, "uiIndex"),
 (["in"], POINTER(GUID), "riid"),
 (["out"], POINTER(POINTER(IUnknown)), "ppv"),
),
]

class HSTRING(c_void_p):
 pass

try:
 _combase =ctypes.windll.combase
 _WindowsCreateString =_combase.WindowsCreateString
 _WindowsCreateString.argtypes =[ctypes.c_wchar_p, UINT, POINTER(HSTRING)]
 _WindowsCreateString.restype =HRESULT
 _WindowsDeleteString =_combase.WindowsDeleteString
 _WindowsDeleteString.argtypes =[HSTRING]
 _WindowsDeleteString.restype =HRESULT
except Exception:
 _WindowsCreateString =None
 _WindowsDeleteString =None

def create_hstring(text:str)->HSTRING:

 if not _WindowsCreateString:
 return HSTRING(0)
 hs =HSTRING()
 hr =_WindowsCreateString(text, len(text), byref(hs))
 if hr !=0:
 raise OSError(f"WindowsCreateString failed: {hr }")
 return hs

def delete_hstring(hs:HSTRING):

 if _WindowsDeleteString and hs:
 _WindowsDeleteString(hs)

BUILD =sys.getwindowsversion().build

def _get_ubr()->int:

 try:
 import winreg

 key =winreg.OpenKey(
 winreg.HKEY_LOCAL_MACHINE,
 r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
)
 ubr, _ =winreg.QueryValueEx(key, "UBR")
 winreg.CloseKey(key)
 return ubr
 except Exception:
 return 0

UBR =_get_ubr()
_BUILD_TUPLE =(BUILD, UBR)

logger.debug(f"[VDM] Windows Build: {BUILD }.{UBR }")

if BUILD >=26100:
 _VER ="WIN11_24H2"
elif _BUILD_TUPLE >=(22631, 3085):
 _VER ="WIN11_23H2"
elif _BUILD_TUPLE >=(22621, 2215):
 _VER ="WIN11_22H2_L"
elif BUILD >=22483:
 _VER ="WIN11_22H2_E"
elif BUILD >=22000:
 _VER ="WIN11_21H2"
else:
 _VER ="WIN10"

logger.debug(f"[VDM] Version group: {_VER }")

_USES_HMONITOR =_VER in("WIN11_21H2", "WIN11_22H2_E")

_HAS_SET_NAME =_VER !="WIN10"

_IID_MAP ={
"WIN10":{
"ManagerInternal":GUID("{F31574D6-B682-4CDC-BD56-1827860ABEC6}"),
"Desktop":GUID("{FF72FFDD-BE7E-43FC-9C03-AD81681E88E4}"),
},
"WIN11_21H2":{
"ManagerInternal":GUID("{B2F925B9-5A0F-4D2E-9F4D-2B1507593C10}"),
"Desktop":GUID("{536D3495-B208-4CC9-AE26-DE8111275BF8}"),
},
"WIN11_22H2_E":{

"ManagerInternal":GUID("{B2F925B9-5A0F-4D2E-9F4D-2B1507593C10}"),
"Desktop":GUID("{536D3495-B208-4CC9-AE26-DE8111275BF8}"),
},
"WIN11_22H2_L":{
"ManagerInternal":GUID("{4970BA3D-FD4E-4647-BEA3-D89076EF4B9C}"),
"Desktop":GUID("{A3175F2D-239C-4BD2-8AA0-EEBA8B0B138E}"),
},
"WIN11_23H2":{
"ManagerInternal":GUID("{53F5CA0B-158F-4124-900C-057158060B27}"),
"Desktop":GUID("{3F07F4BE-B107-441A-AF0F-39D82529072C}"),
},
"WIN11_24H2":{

"ManagerInternal":GUID("{53F5CA0B-158F-4124-900C-057158060B27}"),
"Desktop":GUID("{3F07F4BE-B107-441A-AF0F-39D82529072C}"),
},
}

IID_IVirtualDesktopManagerInternal =_IID_MAP[_VER]["ManagerInternal"]
IID_IVirtualDesktop =_IID_MAP[_VER]["Desktop"]

class IVirtualDesktop(IUnknown):
 _iid_ =IID_IVirtualDesktop
 _methods_ =[
 STDMETHOD(HRESULT, "IsViewVisible", (POINTER(IUnknown), POINTER(UINT))),
 COMMETHOD([], HRESULT, "GetID", (["out"], POINTER(GUID), "pGuid")),
]

class IApplicationView(IUnknown):
 _iid_ =GUID("{372E1D3B-38D3-42E4-A15B-8AB2B178F513}")

class IVirtualDesktopManagerInternal(IUnknown):
 _iid_ =IID_IVirtualDesktopManagerInternal

 if _VER =="WIN10":
 _methods_ =[

 COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pCount")),

 STDMETHOD(
 HRESULT,
 "MoveViewToDesktop",
 (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
),

 STDMETHOD(
 HRESULT,
 "CanViewMoveDesktops",
 (POINTER(IApplicationView), POINTER(UINT)),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetCurrentDesktop",
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetDesktops",
 (["out"], POINTER(POINTER(IObjectArray)), "array"),
),

 STDMETHOD(
 HRESULT,
 "GetAdjacentDesktop",
 (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
),

 STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop), )),

 COMMETHOD(
 [],
 HRESULT,
 "CreateDesktopW",
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "RemoveDesktop",
 (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
 (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "FindDesktop",
 (["in"], POINTER(GUID), "pGuid"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

]

 elif _VER =="WIN11_21H2":
 _methods_ =[

 COMMETHOD(
 [],
 HRESULT,
 "GetCount",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(UINT), "pCount"),
),

 STDMETHOD(
 HRESULT,
 "MoveViewToDesktop",
 (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
),

 STDMETHOD(
 HRESULT,
 "CanViewMoveDesktops",
 (POINTER(IApplicationView), POINTER(UINT)),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetCurrentDesktop",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetDesktops",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(POINTER(IObjectArray)), "array"),
),

 STDMETHOD(
 HRESULT,
 "GetAdjacentDesktop",
 (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
),

 STDMETHOD(HRESULT, "SwitchDesktop", (HWND, POINTER(IVirtualDesktop))),

 COMMETHOD(
 [],
 HRESULT,
 "CreateDesktopW",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(
 HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), HWND, UINT)
),

 COMMETHOD(
 [],
 HRESULT,
 "RemoveDesktop",
 (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
 (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "FindDesktop",
 (["in"], POINTER(GUID), "pGuid"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(
 HRESULT,
 "GetDesktopSwitchIncludeExcludeViews",
 (
 POINTER(IVirtualDesktop),
 POINTER(POINTER(IObjectArray)),
 POINTER(POINTER(IObjectArray)),
),
),

 COMMETHOD(
 [],
 HRESULT,
 "SetName",
 (["in"], POINTER(IVirtualDesktop), "pDesktop"),
 (["in"], HSTRING, "name"),
),
]

 elif _VER =="WIN11_22H2_E":

 _methods_ =[

 COMMETHOD(
 [],
 HRESULT,
 "GetCount",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(UINT), "pCount"),
),

 STDMETHOD(
 HRESULT,
 "MoveViewToDesktop",
 (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
),

 STDMETHOD(
 HRESULT,
 "CanViewMoveDesktops",
 (POINTER(IApplicationView), POINTER(UINT)),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetCurrentDesktop",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetAllCurrentDesktops",
 (["out"], POINTER(POINTER(IObjectArray)), "array"),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetDesktops",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(POINTER(IObjectArray)), "array"),
),

 STDMETHOD(
 HRESULT,
 "GetAdjacentDesktop",
 (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
),

 STDMETHOD(HRESULT, "SwitchDesktop", (HWND, POINTER(IVirtualDesktop))),

 COMMETHOD(
 [],
 HRESULT,
 "CreateDesktopW",
 (["in"], HWND, "hMon"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(
 HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), HWND, UINT)
),

 COMMETHOD(
 [],
 HRESULT,
 "RemoveDesktop",
 (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
 (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "FindDesktop",
 (["in"], POINTER(GUID), "pGuid"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(
 HRESULT,
 "GetDesktopSwitchIncludeExcludeViews",
 (
 POINTER(IVirtualDesktop),
 POINTER(POINTER(IObjectArray)),
 POINTER(POINTER(IObjectArray)),
),
),

 COMMETHOD(
 [],
 HRESULT,
 "SetName",
 (["in"], POINTER(IVirtualDesktop), "pDesktop"),
 (["in"], HSTRING, "name"),
),
]

 elif _VER in("WIN11_22H2_L", "WIN11_23H2"):

 _methods_ =[

 COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pCount")),

 STDMETHOD(
 HRESULT,
 "MoveViewToDesktop",
 (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
),

 STDMETHOD(
 HRESULT,
 "CanViewMoveDesktops",
 (POINTER(IApplicationView), POINTER(UINT)),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetCurrentDesktop",
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetDesktops",
 (["out"], POINTER(POINTER(IObjectArray)), "array"),
),

 STDMETHOD(
 HRESULT,
 "GetAdjacentDesktop",
 (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
),

 STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop), )),

 COMMETHOD(
 [],
 HRESULT,
 "CreateDesktopW",
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), UINT)),

 COMMETHOD(
 [],
 HRESULT,
 "RemoveDesktop",
 (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
 (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "FindDesktop",
 (["in"], POINTER(GUID), "pGuid"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(
 HRESULT,
 "GetDesktopSwitchIncludeExcludeViews",
 (
 POINTER(IVirtualDesktop),
 POINTER(POINTER(IObjectArray)),
 POINTER(POINTER(IObjectArray)),
),
),

 COMMETHOD(
 [],
 HRESULT,
 "SetName",
 (["in"], POINTER(IVirtualDesktop), "pDesktop"),
 (["in"], HSTRING, "name"),
),
]

 elif _VER =="WIN11_24H2":

 _methods_ =[

 COMMETHOD([], HRESULT, "GetCount", (["out"], POINTER(UINT), "pCount")),

 STDMETHOD(
 HRESULT,
 "MoveViewToDesktop",
 (POINTER(IApplicationView), POINTER(IVirtualDesktop)),
),

 STDMETHOD(
 HRESULT,
 "CanViewMoveDesktops",
 (POINTER(IApplicationView), POINTER(UINT)),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetCurrentDesktop",
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "GetDesktops",
 (["out"], POINTER(POINTER(IObjectArray)), "array"),
),

 STDMETHOD(
 HRESULT,
 "GetAdjacentDesktop",
 (POINTER(IVirtualDesktop), UINT, POINTER(POINTER(IVirtualDesktop))),
),

 STDMETHOD(HRESULT, "SwitchDesktop", (POINTER(IVirtualDesktop), )),

 STDMETHOD(
 HRESULT,
 "SwitchDesktopAndMoveForegroundView",
 (POINTER(IVirtualDesktop), ),
),

 COMMETHOD(
 [],
 HRESULT,
 "CreateDesktopW",
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(HRESULT, "MoveDesktop", (POINTER(IVirtualDesktop), UINT)),

 COMMETHOD(
 [],
 HRESULT,
 "RemoveDesktop",
 (["in"], POINTER(IVirtualDesktop), "destroyDesktop"),
 (["in"], POINTER(IVirtualDesktop), "fallbackDesktop"),
),

 COMMETHOD(
 [],
 HRESULT,
 "FindDesktop",
 (["in"], POINTER(GUID), "pGuid"),
 (["out"], POINTER(POINTER(IVirtualDesktop)), "pDesktop"),
),

 STDMETHOD(
 HRESULT,
 "GetDesktopSwitchIncludeExcludeViews",
 (
 POINTER(IVirtualDesktop),
 POINTER(POINTER(IObjectArray)),
 POINTER(POINTER(IObjectArray)),
),
),

 COMMETHOD(
 [],
 HRESULT,
 "SetName",
 (["in"], POINTER(IVirtualDesktop), "pDesktop"),
 (["in"], HSTRING, "name"),
),
]

class VirtualDesktopManager:

 def __init__(self):
 self._manager =None
 self._internal_manager =None
 self._uses_hmonitor =_USES_HMONITOR
 self._has_set_name =_HAS_SET_NAME

 try:
 ctypes.windll.ole32.CoInitialize(None)
 except Exception:
 pass

 try:
 self._manager =comtypes.client.CreateObject(
 CLSID_VirtualDesktopManager, interface =IVirtualDesktopManager
)

 try:
 service_provider =comtypes.client.CreateObject(
 CLSID_ImmersiveShell, interface =IServiceProvider
)
 unk =service_provider.QueryService(
 byref(CLSID_VirtualDesktopManagerInternal),
 byref(IVirtualDesktopManagerInternal._iid_),
)
 self._internal_manager =unk.QueryInterface(
 IVirtualDesktopManagerInternal
)
 except Exception as e:
 if "No such interface supported"in str(e):
 logger.info("VirtualDesktopManagerInternal not available on this system")
 else:
 logger.warning(
 f"Failed to initialize VirtualDesktopManagerInternal: {e }"
)
 self._internal_manager =None

 except Exception as e:
 logger.error(f"Failed to initialize VirtualDesktopManager: {e }")

 def _get_desktops(self):

 if self._uses_hmonitor:
 return self._internal_manager.GetDesktops(0)
 return self._internal_manager.GetDesktops()

 def _get_current_desktop_raw(self):

 if self._uses_hmonitor:
 return self._internal_manager.GetCurrentDesktop(0)
 return self._internal_manager.GetCurrentDesktop()

 def _create_desktop_raw(self):

 if self._uses_hmonitor:
 return self._internal_manager.CreateDesktopW(0)
 return self._internal_manager.CreateDesktopW()

 def _switch_desktop_raw(self, desktop):

 if self._uses_hmonitor:
 self._internal_manager.SwitchDesktop(0, desktop)
 else:
 self._internal_manager.SwitchDesktop(desktop)

 def is_window_on_current_desktop(self, hwnd:int)->bool:

 if not self._manager:
 return True
 try:
 return self._manager.IsWindowOnCurrentVirtualDesktop(hwnd)
 except Exception:
 return True

 def get_window_desktop_id(self, hwnd:int)->str:

 if not self._manager:
 return ""
 try:
 guid =self._manager.GetWindowDesktopId(hwnd)
 return str(guid)
 except Exception:
 return ""

 def move_window_to_desktop(self, hwnd:int, desktop_name:str):

 if not self._manager:
 return
 try:
 target_guid_str =self._resolve_to_guid(desktop_name)
 if not target_guid_str:
 logger.error(f"Desktop '{desktop_name }' not found.")
 return
 guid =GUID(target_guid_str)
 self._manager.MoveWindowToDesktop(hwnd, byref(guid))
 except Exception as e:
 logger.error(f"Failed to move window to desktop: {e }")

 def _get_name_from_registry(self, guid_str:str)->str:

 try:
 import winreg

 path =(
 "Software\\Microsoft\\Windows\\CurrentVersion"
 f"\\Explorer\\VirtualDesktops\\Desktops\\{guid_str }"
)
 with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path)as key:
 name, _ =winreg.QueryValueEx(key, "Name")
 return name
 except Exception:
 return None

 def _resolve_to_guid(self, name:str)->str:

 if name and name.strip().lower()=="current":
 try:
 current =self._get_current_desktop_raw()
 if current:
 guid =current.GetID()
 if guid:
 return str(guid)
 except Exception:
 pass

 desktops_map ={}

 try:
 desktops_array =self._get_desktops()
 count =desktops_array.GetCount()

 for i in range(count):
 unk =desktops_array.GetAt(i, byref(IVirtualDesktop._iid_))
 desktop =unk.QueryInterface(IVirtualDesktop)
 guid =desktop.GetID()
 if not guid:
 continue
 guid_str =str(guid)

 reg_name =self._get_name_from_registry(guid_str)
 display_name =reg_name if reg_name else f"Desktop {i +1 }"

 desktops_map[display_name.lower()]=guid_str
 if name.lower()==guid_str.lower():
 return guid_str

 except Exception as e:
 logger.error(f"Error scanning desktops for resolution: {e }")
 return None

 if name.lower()in desktops_map:
 return desktops_map[name.lower()]

 return None

 def create_desktop(self, name:str =None)->str:

 if not self._internal_manager:
 raise RuntimeError("Internal VDM not initialized")

 desktop =self._create_desktop_raw()
 guid =desktop.GetID()
 guid_str =str(guid)

 if name and self._has_set_name:
 self.rename_desktop_by_guid(guid_str, name)
 return name
 else:
 desktops =self.get_all_desktops()
 return desktops[-1]["name"]

 def remove_desktop(self, desktop_name:str):

 if not self._internal_manager:
 raise RuntimeError("Internal VDM not initialized")

 target_guid_str =self._resolve_to_guid(desktop_name)
 if not target_guid_str:
 logger.error(f"Desktop '{desktop_name }' not found.")
 return

 target_guid =GUID(target_guid_str)
 try:
 target_desktop =self._internal_manager.FindDesktop(target_guid)
 except Exception:
 logger.error(f"Could not find desktop with GUID {target_guid_str }")
 return

 desktops_array =self._get_desktops()
 count =desktops_array.GetCount()
 fallback_desktop =None

 for i in range(count):
 unk =desktops_array.GetAt(i, byref(IVirtualDesktop._iid_))
 candidate =unk.QueryInterface(IVirtualDesktop)
 candidate_id =candidate.GetID()
 if str(candidate_id)!=str(target_guid):
 fallback_desktop =candidate
 break

 if not fallback_desktop:
 logger.error("No fallback desktop found(cannot delete the only desktop)")
 return

 self._internal_manager.RemoveDesktop(target_desktop, fallback_desktop)

 def rename_desktop(self, desktop_name:str, new_name:str):

 if not self._has_set_name:
 logger.warning("Rename is not supported on this Windows version.")
 return

 target_guid_str =self._resolve_to_guid(desktop_name)
 if not target_guid_str:
 logger.error(f"Desktop '{desktop_name }' not found.")
 return

 self.rename_desktop_by_guid(target_guid_str, new_name)

 def rename_desktop_by_guid(self, guid_str:str, new_name:str):

 if not self._internal_manager or not self._has_set_name:
 return

 target_guid =GUID(guid_str)
 try:
 target_desktop =self._internal_manager.FindDesktop(target_guid)
 except Exception:
 return

 hs_name =create_hstring(new_name)
 try:
 self._internal_manager.SetName(target_desktop, hs_name)
 except Exception as e:
 logger.error(f"Failed to rename desktop: {e }")
 finally:
 delete_hstring(hs_name)

 def switch_desktop(self, desktop_name:str):

 if not self._internal_manager:
 raise RuntimeError("Internal VDM not initialized")

 target_guid_str =self._resolve_to_guid(desktop_name)
 if not target_guid_str:
 logger.error(f"Desktop '{desktop_name }' not found")
 return

 target_guid =GUID(target_guid_str)
 try:
 target_desktop =self._internal_manager.FindDesktop(target_guid)
 self._switch_desktop_raw(target_desktop)
 except Exception as e:
 logger.error(f"Failed to switch desktop: {e }")

 def get_all_desktops(self)->list[dict]:

 if not self._internal_manager:
 return[
 {
 "id":"00000000-0000-0000-0000-000000000000",
 "name":"Default Desktop",
 }
]

 desktops_array =self._get_desktops()
 count =desktops_array.GetCount()

 result =[]
 for i in range(count):
 try:
 unk =desktops_array.GetAt(i, byref(IVirtualDesktop._iid_))
 desktop =unk.QueryInterface(IVirtualDesktop)
 guid =desktop.GetID()
 if not guid:
 continue

 guid_str =str(guid)
 reg_name =self._get_name_from_registry(guid_str)
 name =reg_name if reg_name else f"Desktop {i +1 }"

 result.append({"id":guid_str, "name":name })
 except Exception as e:
 logger.error(f"Error retrieving desktop at index {i }: {e }")
 continue

 return result

 def get_current_desktop(self)->dict:

 if not self._internal_manager:
 return {
 "id":"00000000-0000-0000-0000-000000000000",
 "name":"Default Desktop",
 }

 current_desktop =self._get_current_desktop_raw()
 guid =current_desktop.GetID()
 guid_str =str(guid)

 all_desktops =self.get_all_desktops()
 for d in all_desktops:
 if d["id"]==guid_str:
 return d

 return {"id":guid_str, "name":"Unknown"}

def create_desktop(name:str =None)->str:
 return _get_manager().create_desktop(name)

def remove_desktop(desktop_name:str):
 _get_manager().remove_desktop(desktop_name)

def rename_desktop(desktop_name:str, new_name:str):
 _get_manager().rename_desktop(desktop_name, new_name)

def switch_desktop(desktop_name:str):
 _get_manager().switch_desktop(desktop_name)

def get_all_desktops()->list[dict]:
 return _get_manager().get_all_desktops()

def get_current_desktop()->dict:
 return _get_manager().get_current_desktop()
