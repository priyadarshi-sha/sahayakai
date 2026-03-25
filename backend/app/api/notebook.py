from fastapi import APIRouter, HTTPException
import os, json
from app.core.config import NOTEBOOK_DIR

router = APIRouter(prefix="/notebook", tags=["Notebook"])

@router.get("/{user_id}")
def get_notebook(user_id: str):
    try:
        if not user_id:
            raise HTTPException(
                status_code=400,
                detail="user_id is required"
            )
        
        path = os.path.join(NOTEBOOK_DIR, user_id, "chat.json")
        if not os.path.exists(path):
            raise HTTPException(
                status_code=404,
                detail=f"No notebook found for user {user_id}"
            )

        with open(path, encoding="utf-8") as f:
            return [json.loads(line) for line in f]
    
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing notebook data: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving notebook: {str(e)}"
        )
