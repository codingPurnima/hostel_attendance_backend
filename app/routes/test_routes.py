from fastapi import APIRouter

router= APIRouter()

@router.get("/test")
def testApi():
    return {"status": "API WORKING"}