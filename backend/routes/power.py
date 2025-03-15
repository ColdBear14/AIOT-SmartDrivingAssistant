from fastapi import APIRouter

power_router = APIRouter()

@power_router.post('/on')
def turn_on():
    