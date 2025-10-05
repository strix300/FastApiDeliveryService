from fastapi import Request, Response
from uuid import uuid4

async def get_or_create_session(request: Request, response: Response) -> str:
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid4())
        response.set_cookie(
            key="session_id",
            value=session_id,
            max_age=60 * 60 * 24 * 7,
            httponly=True,
        )
    return session_id