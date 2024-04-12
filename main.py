import json
from uuid import UUID
from uuid import uuid4 as new_uuid
from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, select, update, delete

from models import Snowboard, Brand, CreateSnowboardRequest, UpdateSnowboardRequest

from db import engine

# with open("snowboards.json", "r") as f:
#     snowboard_list = json.load(f)
# 
# snowboards = [Snowboard(**snowboard) for snowboard in snowboard_list]
# 
# with Session(bind=engine) as session:
#     for sb in snowboards:
#         if not session.exec(select(Snowboard).where(sb.id == Snowboard.id)).first():
#             session.add(sb)
#     session.commit()

app = FastAPI()

@app.get("/snowboards")
async def get_snowboards() -> list[Snowboard]:
    with Session(bind=engine) as session:
        return session.exec(select(Snowboard)).all()

@app.post("/snowboards")
async def add_snowboard(new_snowboard: CreateSnowboardRequest):
    with Session(bind=engine) as session:
        snowboard = Snowboard(**new_snowboard.model_dump())
        session.add(snowboard)
        session.commit()
        session.refresh(snowboard)
        return snowboard

@app.put("/snowboards/{snowboard_id}")
async def update_snowboard(snowboard_id: int, new_snowboard: UpdateSnowboardRequest):
    with Session(bind=engine) as session:
        updated_snowboard = session.exec(select(Snowboard).where(Snowboard.id == snowboard_id)).first()
        if not updated_snowboard:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Snowboard ID: {snowboard_id} not found.")
        session.exec(update(Snowboard).where(Snowboard.id == snowboard_id).values(
            length = new_snowboard.length if new_snowboard.length is not None else Snowboard.length,
            color = new_snowboard.color if new_snowboard.color is not None else Snowboard.color,
            has_bindings = new_snowboard.has_bindings if new_snowboard.has_bindings is not None else Snowboard.has_bindings,
            brand=new_snowboard.brand if new_snowboard.brand is not None else Snowboard.brand
        ))
        session.commit()
        session.refresh(updated_snowboard)
        return updated_snowboard

        
            
@app.delete("/snowboards/{snowboard_id}")
async def delete_snowboard(snowboard_id: int):
    with Session(bind=engine) as session:
        deleted_snowboard = session.exec(select(Snowboard).where(Snowboard.id == snowboard_id)).first()
        if not deleted_snowboard:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Snowboard ID: {snowboard_id} not found.")
        session.exec(delete(Snowboard).where(Snowboard.id == snowboard_id))
        session.commit()
        return deleted_snowboard
