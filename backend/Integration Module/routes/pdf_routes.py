from fastapi import APIRouter, UploadFile, File, HTTPException
import sys
from pathlib import Path

# Ensure Integration Module directory is on sys.path for bare imports
_INTEGRATION_DIR = Path(__file__).resolve().parents[1]
if str(_INTEGRATION_DIR) not in sys.path:
    sys.path.insert(0, str(_INTEGRATION_DIR))

from pdf import extract_text_from_pdf_bytes, extract_text_from_docx_bytes

router = APIRouter(
    prefix="/pdf",
    tags=["pdf"]
)

@router.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    """
    Takes a document (PDF, TXT, or DOCX) from the user and parses it using the integration module's logic.
    """
    allowed_types = [
        "application/pdf", 
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"File must be one of: {', '.join(allowed_types)}")
    
    try:
        content_bytes = await file.read()
        if not content_bytes:
             raise HTTPException(status_code=400, detail="The file is empty.")
             
        if file.content_type == "application/pdf":
            parsed_text = extract_text_from_pdf_bytes(content_bytes)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            parsed_text = extract_text_from_docx_bytes(content_bytes)
        else:
            # Handle plain text files
            try:
                parsed_text = content_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # Fallback to latin-1 if utf-8 fails
                parsed_text = content_bytes.decode('latin-1')
        
        if not parsed_text:
            return {
                "filename": file.filename,
                "status": "warning",
                "message": "No text could be extracted from the document.",
                "parsed_text": ""
            }
            
        return {
            "filename": file.filename,
            "status": "success",
            "parsed_text": parsed_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing document: {str(e)}")
    finally:
        await file.close()
