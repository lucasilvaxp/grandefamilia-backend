from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
import secrets
import base64
import hashlib

router = APIRouter()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

class ImageUpload(BaseModel):
    filename: str
    content_type: str
    data: str  # Base64 encoded data URL (data:image/jpeg;base64,...)

@router.post("/upload")
async def upload_image(upload: ImageUpload):
    """
    Recebe uma imagem em base64 e retorna a data URL para armazenamento no MongoDB.
    Solução serverless-friendly que não depende de filesystem.
    """
    try:
        # Validate data URL format
        if not upload.data.startswith('data:image/'):
            raise HTTPException(status_code=400, detail="Formato de imagem inválido")
        
        # Validate content type
        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg']
        if upload.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Tipo de arquivo não permitido. Use: {', '.join(allowed_types)}"
            )
        
        # Extract and validate base64 data
        try:
            header, encoded = upload.data.split(',', 1)
            image_data = base64.b64decode(encoded)
        except Exception:
            raise HTTPException(status_code=400, detail="Dados de imagem corrompidos")
        
        # Validate size (5MB max)
        if len(image_data) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400, 
                detail=f"Imagem muito grande. Máximo: 5MB"
            )
        
        # Generate metadata
        timestamp = datetime.utcnow().isoformat()
        unique_string = f"{upload.filename}{timestamp}".encode()
        file_hash = hashlib.md5(unique_string).hexdigest()
        
        # Return the data URL - will be stored in MongoDB with the product
        return JSONResponse(content={
            "url": upload.data,
            "filename": upload.filename,
            "content_type": upload.content_type,
            "hash": file_hash,
            "size": len(image_data),
            "uploaded_at": timestamp
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar upload: {str(e)}")

@router.get("/upload/health")
async def upload_health():
    """Health check endpoint for upload service"""
    return {
        "status": "ok",
        "service": "image-upload",
        "storage": "base64-mongodb",
        "max_size": "5MB",
        "allowed_formats": ["JPEG", "PNG", "WebP"]
    }
