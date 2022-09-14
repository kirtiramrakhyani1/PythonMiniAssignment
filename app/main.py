from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import DataItem
from sqlalchemy.orm import Session
import uvicorn
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi_health import health

app = FastAPI(title="HashedIn University Tracker",
              description="FastAPI Application with Sqlalchemy Database",
              version="1.0.0", )

models.Base.metadata.create_all(bind=engine)


def healthy_condition():
    return {"database": "online"}


def sick_condition():
    return False

app.add_api_route("/health", health([healthy_condition, sick_condition]))


@app.get("/")
def root():
    return "HashedIn University Tracker"

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post('/hutracker', tags=["Item"], response_model=schemas.Item, status_code=201)
async def create_entry(item_request: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an entry in database
    """

    db_item = DataItem.fetch_by_name(db, name=item_request.name)
    if db_item:
        raise HTTPException(status_code=400, detail="Data entry already exists!")

    return await DataItem.create(db=db, item=item_request)


@app.get('/hutracker', tags=["Item"], response_model=List[schemas.Item])
def get_all_enteries(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the data
    """
    if name:
        items = []
        db_item = DataItem.fetch_by_name(db, name)
        items.append(db_item)
        return items
    else:
        return DataItem.fetch_all(db)


@app.get('/hutracker/{item_id}', tags=["Item"], response_model=schemas.Item)
def get_entry(item_id: int, db: Session = Depends(get_db)):
    """
    Get the data with the given ID provided by User stored in database
    """
    db_item = DataItem.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Data not found !!")
    return db_item

@app.get('/hutracker/{item_name}', tags=["Item"], response_model=schemas.ItemName)
def get_entry_by_name(item_name: str, db: Session = Depends(get_db)):
    """
    Get the data with the given Username provided by User stored in database
    """
    db_item = DataItem.fetch_by_name(db, item_name)
    print(db_item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Data not found")
    return db_item


@app.delete('/hutracker/{item_id}', tags=["Item"])
async def delete_entry(item_id: int, db: Session = Depends(get_db)):
    """
    Delete the data with the given ID provided by User stored in database
    """
    db_item = DataItem.fetch_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Data not found with the given ID")
    await DataItem.delete(db, item_id)
    return "Data deleted successfully!"


@app.put('/hutracker/{item_id}', tags=["Item"], response_model=schemas.Item)
async def update_entry(item_id: int, item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update an data stored in the database
    """
    db_item = DataItem.fetch_by_id(db, item_id)
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.name = update_item_encoded['name']
        db_item.keyName = update_item_encoded['keyName']
        db_item.description = update_item_encoded['description']
        db_item.tags = update_item_encoded['tags']
        db_item.datatypes = update_item_encoded['datatypes']
        db_item.email = update_item_encoded['email']
        return await DataItem.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Data not found with the given ID")


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)