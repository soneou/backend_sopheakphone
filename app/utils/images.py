import cloudinary
import cloudinary.uploader
from flask import current_app

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def _configure_cloudinary() -> None:
    cloudinary.config(
        cloud_name=current_app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=current_app.config["CLOUDINARY_API_KEY"],
        api_secret=current_app.config["CLOUDINARY_API_SECRET"],
        secure=True,
    )


def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_product_image(file_storage) -> str:
    """Uploads an image file to Cloudinary and returns its secure URL."""
    _configure_cloudinary()
    result = cloudinary.uploader.upload(
        file_storage,
        folder="sopheak_capital/products",
        resource_type="image",
    )
    return result["secure_url"]


def delete_product_image(public_url: str) -> None:
    """Best-effort deletion of a Cloudinary image given its secure URL."""
    if "res.cloudinary.com" not in public_url:
        return
    _configure_cloudinary()
    try:
        parts = public_url.split("/upload/")[-1]
        parts = parts.split(".")[0]
        if "/" in parts and parts.split("/")[0].startswith("v") and parts.split("/")[0][1:].isdigit():
            parts = "/".join(parts.split("/")[1:])
        cloudinary.uploader.destroy(parts, resource_type="image")
    except Exception:
        current_app.logger.warning("Failed to delete Cloudinary image: %s", public_url)
