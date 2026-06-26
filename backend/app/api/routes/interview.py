from fastapi import APIRouter

router = APIRouter()

@router.post("/start")
def start_interview():
    return {"message": "interview started"}