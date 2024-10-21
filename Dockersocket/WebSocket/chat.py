from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database import new_session, TaskModel
from sqlalchemy import select

router = APIRouter(tags=["Chat"], prefix="/chat")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{client_id} says: {data}")
            if data == "get_all":
                query = select(TaskModel)
                async with new_session() as session:
                    result = await session.execute(query)
                tasks = result.scalars().all()
                for task in tasks:
                    await manager.broadcast(f'id={task.id}    description={task.description}    complete={task.complete}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
