from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
import os
import uuid
import base64
import json
from datetime import datetime
from database import get_db
from models.models import User, UserGeneratedDesign, DesignRequest, Jeweler, DesignRequestStatus
from schemas import (
    UserGeneratedDesignCreate, UserGeneratedDesignResponse,
    DesignRequestCreate, DesignRequestResponse
)
from auth import get_current_active_user
from config import settings

router = APIRouter(prefix="/api/ai", tags=["AI Design"])

GENERATED_DESIGNS_DIR = "static/generated_designs"
os.makedirs(GENERATED_DESIGNS_DIR, exist_ok=True)

def construct_design_prompt(data: UserGeneratedDesignCreate) -> str:
    prompt = f"""Create a stunning, photorealistic image of a {data.type.lower()} jewelry piece.

Design specifications:
- Type: {data.type}
- Material: {data.material} ({data.karat})
- Color: {data.color}
- Shape: {data.shape}
"""
    
    if data.gemstone_type and data.gemstone_type.lower() != "none":
        prompt += f"- Gemstone: {data.gemstone_type}"
        if data.gemstone_color:
            prompt += f" ({data.gemstone_color})"
        prompt += "\n"
    
    prompt += """
Style requirements:
- Professional jewelry photography
- Clean, elegant presentation
- High-end luxury appearance
- Soft lighting with subtle reflections
- White or light gray background
- Focus on the jewelry piece
- Show intricate details and craftsmanship
- Realistic metallic finish appropriate for the material
- If gemstones are specified, show proper brilliance and clarity

The image should look like it belongs in a high-end jewelry catalog or advertisement."""
    
    return prompt

async def generate_image_with_gemini(prompt: str) -> Optional[str]:
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        response = await model.generate_content_async(prompt)
        
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    return part.inline_data.data
        
        return None
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None

def save_generated_image(image_data: str, filename: str) -> str:
    file_path = os.path.join(GENERATED_DESIGNS_DIR, filename)
    
    if isinstance(image_data, str):
        try:
            image_bytes = base64.b64decode(image_data)
        except:
            image_bytes = image_data.encode('utf-8')
    else:
        image_bytes = image_data
    
    with open(file_path, 'wb') as f:
        f.write(image_bytes)
    
    return file_path

@router.post("/generate-design", response_model=UserGeneratedDesignResponse)
async def generate_design(
    design_data: UserGeneratedDesignCreate,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    prompt = construct_design_prompt(design_data)
    
    image_data = await generate_image_with_gemini(prompt)
    
    if not image_data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate image with AI"
        )
    
    filename = f"{uuid.uuid4()}.png"
    image_path = save_generated_image(image_data, filename)
    
    selected_options = {
        "type": design_data.type,
        "color": design_data.color,
        "shape": design_data.shape,
        "material": design_data.material,
        "karat": design_data.karat,
        "gemstone_type": design_data.gemstone_type,
        "gemstone_color": design_data.gemstone_color
    }
    
    new_design = UserGeneratedDesign(
        user_id=current_user.id if current_user else None,
        selected_options=selected_options,
        generated_image_url=image_path
    )
    db.add(new_design)
    db.commit()
    db.refresh(new_design)
    
    return new_design

@router.get("/designs", response_model=list[UserGeneratedDesignResponse])
def get_user_designs(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    designs = db.query(UserGeneratedDesign).filter(
        UserGeneratedDesign.user_id == current_user.id
    ).order_by(UserGeneratedDesign.created_at.desc()).all()
    return designs

@router.get("/designs/{design_id}", response_model=UserGeneratedDesignResponse)
def get_design(
    design_id: int,
    db: Session = Depends(get_db)
):
    design = db.query(UserGeneratedDesign).filter(UserGeneratedDesign.id == design_id).first()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design

@router.post("/design-requests", response_model=DesignRequestResponse, status_code=status.HTTP_201_CREATED)
def create_design_request(
    request_data: DesignRequestCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if request_data.jeweler_id:
        jeweler = db.query(Jeweler).filter(Jeweler.id == request_data.jeweler_id).first()
        if not jeweler:
            raise HTTPException(status_code=404, detail="Jeweler not found")
    
    if request_data.generated_design_id:
        design = db.query(UserGeneratedDesign).filter(
            UserGeneratedDesign.id == request_data.generated_design_id
        ).first()
        if not design:
            raise HTTPException(status_code=404, detail="Generated design not found")
    
    new_request = DesignRequest(
        user_id=current_user.id,
        jeweler_id=request_data.jeweler_id,
        generated_design_id=request_data.generated_design_id,
        description=request_data.description,
        attachment_url=request_data.attachment_url,
        estimated_budget=request_data.estimated_budget
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/design-requests", response_model=list[DesignRequestResponse])
def get_user_design_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    requests = db.query(DesignRequest).filter(
        DesignRequest.user_id == current_user.id
    ).order_by(DesignRequest.request_date.desc()).all()
    return requests

@router.get("/jewelers", response_model=list[dict])
def get_jewelers_for_design(db: Session = Depends(get_db)):
    jewelers = db.query(Jeweler).all()
    return [
        {
            "id": j.id,
            "name": j.name,
            "shop_name": j.shop_name,
            "rating": j.rating
        }
        for j in jewelers
    ]
