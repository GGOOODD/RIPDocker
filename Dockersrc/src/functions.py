from fastapi import HTTPException, status, Request
from database import new_session, UserModel
from sqlalchemy import select
import jwt


class Functions:
    @classmethod
    async def get_user_id(cls, request: Request):
        token = request.cookies.get("token")
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login cookie was not found",
            )
        key = "RSGSDFGEFA3W5Y"
        algorithm = "HS256"
        cookie = jwt.decode(token, key, algorithm)
        query = select(UserModel).filter_by(id=cookie["id"])
        async with new_session() as session:
            result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User cookie is outdated",
            )

        return user.id
