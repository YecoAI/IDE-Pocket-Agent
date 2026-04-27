import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_type = Column(String, nullable=False)
    device_id = Column(String, unique=True, index=True, nullable=False)

    pairing_code = Column(String, unique=True, index=True, nullable=True)
    pairing_code_expires_at = Column(DateTime, nullable=True)
    otp_secret = Column(String, nullable=True)

    is_paired = Column(Boolean, default=False)
    keep_alive_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Association(Base):
    __tablename__ = "associations"

    id = Column(Integer, primary_key=True, index=True)
    mobile_device_id = Column(Integer, ForeignKey("devices.id"))
    agent_device_id = Column(Integer, ForeignKey("devices.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    mobile_device = relationship("Device", foreign_keys=[mobile_device_id])
    agent_device = relationship("Device", foreign_keys=[agent_device_id])
