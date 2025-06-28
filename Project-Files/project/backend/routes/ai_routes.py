from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
from services.watsonx_service import watsonx_service
from services.pdf_service import PDFService

router = APIRouter()
pdf_service = PDFService()

class CodeGenerationRequest(BaseModel):
    prompt: str
    language: str = "python"

class BugFixRequest(BaseModel):
    code: str
    language: str = "python"

class TestGenerationRequest(BaseModel):
    code: str
    language: str = "python"

@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read PDF content
        content = await file.read()
        
        # Extract text
        extracted_text = pdf_service.extract_text_from_pdf(content)
        cleaned_text = pdf_service.clean_text(extracted_text)
        
        # Classify SDLC phases
        classification_result = watsonx_service.classify_sdlc_phases(cleaned_text)
        
        return {
            "success": True,
            "filename": file.filename,
            "extracted_text": cleaned_text[:1000] + "..." if len(cleaned_text) > 1000 else cleaned_text,
            "classification": classification_result,
            "text_length": len(cleaned_text)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@router.post("/generate-code")
async def generate_code(request: CodeGenerationRequest):
    try:
        generated_code = watsonx_service.generate_code(request.prompt, request.language)
        
        return {
            "success": True,
            "prompt": request.prompt,
            "language": request.language,
            "generated_code": generated_code
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")

@router.post("/fix-bug")
async def fix_bug(request: BugFixRequest):
    try:
        fixed_code = watsonx_service.fix_bug(request.code, request.language)
        
        return {
            "success": True,
            "original_code": request.code,
            "language": request.language,
            "fixed_code": fixed_code
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fixing bug: {str(e)}")

@router.post("/generate-tests")
async def generate_tests(request: TestGenerationRequest):
    try:
        test_cases = watsonx_service.generate_test_cases(request.code, request.language)
        
        return {
            "success": True,
            "original_code": request.code,
            "language": request.language,
            "test_cases": test_cases
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating tests: {str(e)}")