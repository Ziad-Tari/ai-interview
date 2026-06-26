from fastapi import APIRouter

router = APIRouter()

@router.post("/start")
def start_session():
    return {"message": "sessions started"}