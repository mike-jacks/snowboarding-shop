import json

from fastapi import FastAPI

from models import Snowboard, Brand


with open("snowboards.json", "r") as f:
    snowboard_list = json.load(f)

snowboards = [Snowboard(**snowboard) for snowboard in snowboard_list]

app = FastAPI()

@app.get("/snowboards")
async def get_snowboards() -> list[Snowboard]:
    return snowboards

@app.post("/snowboards")
async def add_snowboard(new_snowboard: Snowboard):
    snowboards.append(new_snowboard)

@app.put("/snowboards/{snowboard_id}")
async def update_snowboard(snowboard_id: int, new_snowboard: Snowboard):
    for i,snowboard in enumerate(snowboards):
        if snowboard.id == snowboard_id:
            snowboards[i] = new_snowboard
            
@app.delete("/snowboards/{snowboard_id}")
async def delete_snowboard(snowboard_id: int):
    for i,snowboard in enumerate(snowboards):
        if snowboard.id == snowboard_id:
            snowboards.pop(i)