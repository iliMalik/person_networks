from uuid import UUID

from fastapi import APIRouter, HTTPException
from db.queries.query_screening import screening_algo

router = APIRouter(
    prefix="/screening",
    tags=["Screening"]
)

@router.post("/{session_id}")
def screening_session_id(session_id: str):
    """
        Screen mental health disorders based on session responses.
        Args:
            session_id (str): UUID of the session.
        Returns:
            dict: Disorder screening results with flags and severities.
        """
    try:
        # Validate session_id as UUID
        session_uuid = UUID(session_id)
    except ValueError:
       raise HTTPException(status_code=400, detail="Invalid session_id format. Must be a valid UUID.")

    try:
        # Call screening_algo
        results = screening_algo(str(session_uuid))


        return {
            "status": "success",
            "session_id": session_id,
            "results": results
        }
    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Error processing screening: {str(e)}")