from fastapi import FastAPI, Query, Path, Header, HTTPException, status
from fastapi.responses import JSONResponse
from data import data
from fastapi.concurrency import asynccontextmanager
import uvicorn
from models import House, database
from sqlalchemy import insert
from datetime import datetime

app = FastAPI()

def is_validate_token(token: str):
    return token == "bearer tripi_tropa"

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()

@app.get("/houses/", status_code=status.HTTP_200_OK)
async def get_hous_by_animal(animal: str = Query(description="вказать твой тварину", example="Лев")):
    houses = [house for house in data if house.get("animal") == animal]
    if not houses:
        raise HTTPException(status_code=404, detail="не найти дом")
    return JSONResponse(houses)

@app.get("/houses_path/{index}/")
async def get_hous_by_id(index: int = Path(..., description="вказать твой  номер дома", example=[0, 1, 2, 3])):
    house = next((house for house in data if house.get("index") == index), None)
    if not house:
        raise HTTPException(status_code=404, detail="не найти дом")
    return house

@app.get("/houses_head/{index}/")
async def get_house_by_house(
    house: str = Header(..., description="вказать твой дом"),
    Authorization: str = Header(..., description="вказать токен", example="bearer tripi_tropa")
):
    if Authorization == "bearer tripi_tropa":
        house_obj = next((h for h in data if h.get("house") == house), None)
        if not house_obj:
            raise HTTPException(status_code=404, detail="не найти дом")
        return house_obj
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="неверный токен")

@app.post("/houses/", status_code=status.HTTP_201_CREATED, summary="искать до база данних твой")
async def add_house(
    house: str = Query(..., description="искать твой до пошуку факультет"),
    Authorization: str = Header(..., description="вказать токен", example="bearer tripi_tropa"),
):
    if is_validate_token(Authorization):
        house_obj = next((h for h in data if h.get("house") == house), None)
        if not house_obj:
            raise HTTPException(status_code=404, detail="не найти такой факультет")
        query = insert(House).values(index=house_obj.get("index"), house=house_obj.get("house"), animal=house_obj.get("animal"))
        await database.execute(query)
        return {"message": "Дом добавлен"}
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="но но но мистор токен твоя бить не верный")

@app.get("/user/{user_id}/", summary="Домашнє завдання: приймає user_id, timestamp, X-Client-Version")
async def get_user_info(
    user_id: int = Path(..., description="ID користувача"),
    timestamp: str = Query(None, description="Мітка часу (необов'язково)"),
    x_client_version: str = Header(..., alias="X-Client-Version", description="Версія клієнта"),
):
    if not timestamp:
        timestamp = datetime.now().isoformat()
    return {
        "user_id": user_id,
        "timestamp": timestamp,
        "X-Client-Version": x_client_version,
        "message": f"Hello, user {user_id}!"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)