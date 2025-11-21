from operator import ne
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

from pymongo import MongoClient
from bson.objectid import ObjectId




load_dotenv()




MONGO_URI = os.getenv("MONGO_URI")

assert os.getenv("MONGO_URI"), "Set MONGO_URI env var before running"

#MONGO_URI = "mongodb+srv://thotaproject_db_user:Vibhu321@cluster0.o9zylpd.mongodb.net/?appName=Cluster0"


client = AsyncIOMotorClient(MONGO_URI)
db = client["euron"]
euron_data = db["euron_coll"]

app = FastAPI()
class eurondata(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/euron/insert")
async def euron_data_insert_helper(data:eurondata):
    result = await euron_data.insert_one(data.dict())
    return str(result.inserted_id)

def euron_helper(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

@app.get("/euron/getdata")
async def get_euron_data():
    iterms = []
    cursor = euron_data.find({})
    async for document in cursor:
        iterms.append(euron_helper(document))
    return iterms


@app.get("/euron/showdata")
async def show_euron_data():
    iterms = []
    cursor = euron_data.find({})
    async for document in cursor:
        iterms.append(euron_helper(document))
    return iterms


@app.get("/euron/deletedata")
async def delete_euron_data(name: str):
    print(f"Document {name} DELTED")
    result = await euron_data.delete_many({"name": name})
    
    return "result.deleted_count {name} "
    

@app.post("/euron/updatedata")
async def update_euron_data(student_data: eurondata):
    query_filter = {"name": student_data.name}
    update_fileds = student_data.dict(exclude_unset=True)
    new_values = {"$set": update_fileds}
    print(f"Attempting to update records with name: '{student_data.name}'")
    print(f"New values to set: {update_fileds}")

    # Corrected: Call update_many on the 'euron_data' collection object
    result = await euron_data.update_many(query_filter, new_values)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"No records found for name: '{student_data.name}' to update.")

    return {
        "message": f"Successfully updated {result.modified_count} record(s).",
        "matched_count": result.matched_count,
        "modified_count": result.modified_count
    }

