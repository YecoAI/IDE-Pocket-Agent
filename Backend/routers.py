import os
import uuid
import datetime
import pyotp
import logging
import httpx
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models, schemas, database
from auth import (
    create_access_token,
    decode_access_token,
    TokenData,
    encrypt_secret,
    decrypt_secret,
)
from datetime import timedelta
import re

router = APIRouter(prefix="/v1/licensing", tags=["Licensing"])
logger = logging.getLogger("backend")

MASTER_ADMIN_TOKEN = os.getenv("TRAE_ADMIN_TOKEN")


async def get_db_session():
    async for db in database.get_db():
        yield db


async def get_current_token_data(
    authorization: str = Header(None),
) -> TokenData:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    token_data = decode_access_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data


@router.post("/mobile/activate", response_model=schemas.ActivateResponse)
async def activate_license(
    req: schemas.LicenseActivate, db: AsyncSession = Depends(get_db_session)
):
    dev_res = await db.execute(
        select(models.Device).where(models.Device.device_id == req.device_id)
    )
    device = dev_res.scalars().first()

    if not device:
        device = models.Device(
            device_type="mobile", device_id=req.device_id, license_id=None
        )
        db.add(device)

    pairing_code = str(uuid.uuid4().hex[:6].upper())
    device.pairing_code = pairing_code
    device.pairing_code_expires_at = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=10
    )

    otp_secret = pyotp.random_base32()
    device.otp_secret = encrypt_secret(otp_secret)

    access_token = create_access_token(
        data={
            "sub": req.device_id,
            "role": "client",
            "license_key": "OPEN-SOURCE",
        },
        expires_delta=timedelta(days=365),
    )

    await db.commit()
    return schemas.ActivateResponse(
        message="Device activated successfully (Open Source).",
        pairing_code=pairing_code,
        expires_at=device.pairing_code_expires_at,
        otp_secret=otp_secret,
        access_token=access_token,
    )


@router.get("/device/status", response_model=schemas.DeviceStatusResponse)
async def get_device_status(
    db: AsyncSession = Depends(get_db_session),
    token_data: TokenData = Depends(get_current_token_data),
):
    result = await db.execute(
        select(models.Device).where(models.Device.device_id == token_data.sub)
    )
    device = result.scalars().first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    is_paired = device.is_paired
    if not is_paired and device.device_type == "mobile":
        assoc_res = await db.execute(
            select(models.Association).where(
                models.Association.mobile_device_id == device.id,
                models.Association.status == "active",
            )
        )
        if assoc_res.scalars().first():
            is_paired = True

    access_token = create_access_token(
        data={
            "sub": device.device_id,
            "role": "client",
            "license_key": "OPEN-SOURCE",
        },
        expires_delta=timedelta(days=365),
    )

    return schemas.DeviceStatusResponse(
        device_id=device.device_id,
        is_active=True,
        is_paired=is_paired,
        license_key="OPEN-SOURCE",
        expires_at=None,
        access_token=access_token,
    )


async def get_optional_token_data(
    authorization: str = Header(None),
) -> Optional[TokenData]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    return decode_access_token(token)


@router.post("/mobile/check-pairing", response_model=schemas.DeviceStatusResponse)
async def check_pairing_status(
    req: schemas.CheckPairingRequest,
    db: AsyncSession = Depends(get_db_session),
    token_data: Optional[TokenData] = Depends(get_optional_token_data),
):
    if token_data and token_data.sub != req.device_id:
        raise HTTPException(status_code=403, detail="Forbidden: device_id mismatch")

    result = await db.execute(
        select(models.Device).where(models.Device.device_id == req.device_id)
    )
    device = result.scalars().first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    is_paired = device.is_paired
    if not is_paired and device.device_type == "mobile":
        assoc_res = await db.execute(
            select(models.Association).where(
                models.Association.mobile_device_id == device.id,
                models.Association.status == "active",
            )
        )
        if assoc_res.scalars().first():
            is_paired = True

    access_token = create_access_token(
        data={
            "sub": device.device_id,
            "role": "client",
            "license_key": "OPEN-SOURCE",
        },
        expires_delta=timedelta(days=365),
    )

    return schemas.DeviceStatusResponse(
        device_id=device.device_id,
        is_active=True,
        is_paired=is_paired,
        license_key="OPEN-SOURCE",
        expires_at=None,
        access_token=access_token,
    )


@router.get("/mobile/agents", response_model=schemas.AgentListResponse)
async def list_associated_agents(
    db: AsyncSession = Depends(get_db_session),
    token_data: TokenData = Depends(get_current_token_data),
):
    if token_data.role != "client":
        raise HTTPException(status_code=403, detail="Unauthorized role")

    mob_res = await db.execute(
        select(models.Device).where(models.Device.device_id == token_data.sub)
    )
    mobile_dev = mob_res.scalars().first()

    if not mobile_dev:
        return schemas.AgentListResponse(agents=[])

    agent_res = await db.execute(
        select(models.Device)
        .join(
            models.Association,
            models.Association.agent_device_id == models.Device.id,
        )
        .where(
            models.Association.mobile_device_id == mobile_dev.id,
            models.Association.status == "active",
            models.Device.device_type == "agent",
            models.Device.is_paired == True,
        )
    )
    agents = agent_res.scalars().all()

    from connection_manager import manager

    agent_list = []
    for a in agents:
        agent_list.append(
            schemas.AgentInfo(
                agent_id=a.device_id,
                is_online=a.device_id in manager.agents,
                last_seen=None,
            )
        )

    return schemas.AgentListResponse(agents=agent_list)


@router.post("/agent/pair", response_model=schemas.AgentPairResponse)
async def agent_pair(
    req: schemas.AgentPairRequest, db: AsyncSession = Depends(get_db_session)
):
    logger.info(
        f"Agent pair request received: pairing_code={req.pairing_code}, device_id={req.device_id}"
    )
    result = await db.execute(
        select(models.Device).where(
            models.Device.pairing_code == req.pairing_code,
            models.Device.device_type == "mobile",
        )
    )
    mobile_dev = result.scalars().first()

    if not mobile_dev:
        logger.warning(f"Pairing failed: Invalid pairing code {req.pairing_code}")
        raise HTTPException(status_code=404, detail="Invalid pairing code")

    now = datetime.datetime.utcnow()
    if now > mobile_dev.pairing_code_expires_at:
        logger.warning(
            f"Pairing failed: Pairing code expired for {req.pairing_code}. Expires at: {mobile_dev.pairing_code_expires_at}, Now: {now}"
        )
        raise HTTPException(status_code=400, detail="Pairing code expired")

    logger.info(
        f"Pairing code valid for mobile device {mobile_dev.device_id}. Proceeding with agent {req.device_id}"
    )
    agent_res = await db.execute(
        select(models.Device).where(models.Device.device_id == req.device_id)
    )
    agent_dev = agent_res.scalars().first()
    if not agent_dev:
        agent_dev = models.Device(
            device_type="agent", device_id=req.device_id, license_id=None
        )
        db.add(agent_dev)
        await db.flush()

    assoc = models.Association(
        mobile_device_id=mobile_dev.id,
        agent_device_id=agent_dev.id,
        status="pending",
    )
    db.add(assoc)
    await db.commit()
    await db.refresh(assoc)

    return schemas.AgentPairResponse(
        message="Pairing initiated.",
        otp_secret=decrypt_secret(mobile_dev.otp_secret),
        association_id=assoc.id,
    )


@router.post("/agent/confirm", response_model=schemas.AgentConfirmResponse)
async def confirm_association(
    req: schemas.AgentConfirmOTP, db: AsyncSession = Depends(get_db_session)
):
    result = await db.execute(
        select(models.Association).where(models.Association.id == req.association_id)
    )
    assoc = result.scalars().first()

    if not assoc or assoc.status != "pending":
        raise HTTPException(status_code=400, detail="Invalid association")

    mob_res = await db.execute(
        select(models.Device).where(models.Device.id == assoc.mobile_device_id)
    )
    mobile_dev = mob_res.scalars().first()

    totp = pyotp.TOTP(decrypt_secret(mobile_dev.otp_secret))
    if not totp.verify(req.otp_code, valid_window=1):
        raise HTTPException(status_code=403, detail="Invalid OTP")

    assoc.status = "active"
    mobile_dev.is_paired = True
    mobile_dev.pairing_code = None

    agent_res = await db.execute(
        select(models.Device).where(models.Device.id == assoc.agent_device_id)
    )
    agent_dev = agent_res.scalars().first()
    if agent_dev:
        agent_dev.is_paired = True

    access_token = create_access_token(
        data={"sub": agent_dev.device_id, "role": "worker"},
        expires_delta=timedelta(days=30),
    )

    await db.commit()
    return schemas.AgentConfirmResponse(
        message="Success", status="active", access_token=access_token
    )


@router.post("/device/settings", response_model=schemas.DeviceSettingsResponse)
async def update_device_settings(
    req: schemas.DeviceSettingsUpdate,
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(
        select(models.Device).where(models.Device.device_id == req.device_id)
    )
    device = result.scalars().first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device.keep_alive_active = req.keep_alive_active
    await db.commit()

    return schemas.DeviceSettingsResponse(
        device_id=device.device_id,
        keep_alive_active=device.keep_alive_active,
        message="Settings updated",
    )
