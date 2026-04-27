import mss
import base64
import logging
from io import BytesIO
from PIL import Image, ImageGrab
from typing import Dict, Any

logger = logging.getLogger(__name__)


def capture_preview_snapshot() -> str:
 try:
 screenshot = ImageGrab.grab()
 buffered = BytesIO()
 screenshot.save(buffered, format="JPEG", quality=70)
 return base64.b64encode(buffered.getvalue()).decode("utf-8")
 except Exception:
 raise


def handle_live_desktop(payload: Dict[str, Any]) -> str:
 try:
 quality = int(payload.get("quality", 40))
 quality = max(1, min(100, quality))
 except(ValueError, TypeError):
 quality = 40

 img_format = str(payload.get("format", "jpeg")).lower()
 if img_format not in["jpeg", "jpg", "png", "webp"]:
 img_format = "jpeg"

 if img_format == "jpg":
 img_format = "jpeg"

 with mss.mss() as sct:
 monitor = sct.monitors[1]
 sct_img = sct.grab(monitor)
 img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
 width, height = img.size
 new_size = (width // 2, height // 2)
 img = img.resize(new_size, Image.Resampling.NEAREST)
 buffer = BytesIO()
 img.save(buffer, format=img_format.upper(), quality=quality, optimize=True)
 img_str = base64.b64encode(buffer.getvalue()).decode()
 mime_type = f"image/{img_format}"
 return f"data:{mime_type}; base64, {img_str}"
