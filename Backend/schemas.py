from pydantic import BaseModel ,Field ,ConfigDict 
from typing import Optional ,Any 
from datetime import datetime 

def to_camel (string :str )->str :
    temp =string .split ('_')
    return temp [0 ]+''.join (ele .title ()for ele in temp [1 :])

class LicenseCreate (BaseModel ):
    duration_days :int =Field (...,gt =0 )
    max_uses :int =Field (default =1 ,gt =0 )

class LicenseResponse (BaseModel ):
    model_config =ConfigDict (from_attributes =True )
    id :int 
    key :str 
    duration_days :int 
    max_uses :int 
    current_uses :int 
    is_used :bool 
    is_active :bool 
    created_at :datetime 
    expires_at :Optional [datetime ]=None 

class LicenseActivate (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    license_key :str 
    device_id :str 

class ActivateResponse (BaseModel ):
    message :str 
    pairing_code :str 
    expires_at :datetime 
    otp_secret :str 
    access_token :str 

class AgentPairRequest (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    pairing_code :str 
    device_id :str 

class AgentPairResponse (BaseModel ):
    message :str 
    otp_secret :str 
    association_id :int 

class AgentConfirmOTP (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    association_id :int 
    otp_code :str 

class AgentConfirmResponse (BaseModel ):
    message :str 
    status :str 
    access_token :str 

class DeviceSettingsUpdate (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    device_id :str 
    keep_alive_active :bool 

class DeviceSettingsResponse (BaseModel ):
    device_id :str 
    keep_alive_active :bool 
    message :str 

class CheckPairingRequest (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    device_id :str 

class DeviceStatusResponse (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    device_id :str 
    is_active :bool 
    is_paired :bool 
    license_key :Optional [str ]=None 
    expires_at :Optional [datetime ]=None 
    access_token :Optional [str ]=None 

class AgentInfo (BaseModel ):
    agent_id :str 
    is_online :bool 
    last_seen :Optional [datetime ]=None 

class AgentListResponse (BaseModel ):
    agents :list [AgentInfo ]

class MobileActionRequest (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    agent_id :str 
    action :str 
    payload :Optional [dict ]=Field (default_factory =dict )

class MobileActionResponse (BaseModel ):
    success :bool 
    result :Optional [Any ]=None 
    message :Optional [str ]=None 
    requires_refresh :bool =True 

class CheckoutRequest (BaseModel ):
    model_config =ConfigDict (populate_by_name =True ,alias_generator =to_camel )
    paypal_order_id :str 
    duration_days :int =Field (default =30 ,gt =0 )
    max_uses :int =Field (default =1 ,gt =0 )

class CheckoutResponse (BaseModel ):
    success :bool 
    license_key :str 
    message :str 
