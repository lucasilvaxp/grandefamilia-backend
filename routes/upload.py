from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path
from datetime import datetime
import secrets

router = APIRouter()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file
    Returns the URL of the uploaded image
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de arquivo inválido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Validate file size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="Arquivo muito grande. Tamanho máximo: 5MB"
            )
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = secrets.token_hex(8)
        filename = f"{timestamp}_{random_str}{file_ext}"
        file_path = UPLOAD_DIR / filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Return public URL
        # Adjust this URL based on your backend's public URL
        public_url = f"/static/uploads/{filename}"
        
        return JSONResponse(content={"url": public_url})
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

@router.delete("/upload/{filename}")
async def delete_image(filename: str):
    """
    Delete an uploaded image
    """
    try:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            os.remove(file_path)
            return JSONResponse(content={"message": "Imagem deletada com sucesso"})
        else:
            raise HTTPException(status_code=404, detail="Imagem não encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar imagem: {str(e)}")
