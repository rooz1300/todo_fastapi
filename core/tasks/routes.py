from fastapi import APIRouter

router = APIRouter()



@router.get("/tasks/", tags=["tasks"])
async def retrieve_task_list():

    
    return []