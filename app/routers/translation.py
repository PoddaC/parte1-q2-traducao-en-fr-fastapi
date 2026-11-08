from fastapi import APIRouter, Depends

from app.models.translation import TranslateRequest, TranslateResponse
from app.services.translation_service import MODEL_NAME, get_translator, translate_text

router = APIRouter(tags=["tradução"])


@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest, translator=Depends(get_translator)) -> TranslateResponse:
    translation = translate_text(req.text, translator)
    return TranslateResponse(original=req.text, translation=translation, model=MODEL_NAME)
