from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional
# FastAPI app initialization
app = FastAPI()

# MongoDB connection
MONGO_URI = "mongodb+srv://zaidimurtaza102:bhGZYgqn4GpWXNfX@student.mzgp2.mongodb.net/?retryWrites=true&w=majority&appName=student"
client = AsyncIOMotorClient(MONGO_URI)
db = client["StudentManagementSystem"]  # Replace with your database name
collection = db["students"]  # Replace with your collection name


# Models for validation and serialization
class Address(BaseModel):
    city: str = Field(..., example="New York")
    country: str = Field(..., example="USA")


class Student(BaseModel):
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=20)
    address: Address


class UpdateStudent(BaseModel):
    name: Optional[str] = Field(None, example="John Doe")
    age: Optional[int] = Field(None, example=20)
    address: Optional[Address]


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    address: Address


# Helper function to convert MongoDB object to response format
def mongo_to_response(student):
    student["id"] = str(student["_id"])
    del student["_id"]
    return student


# Create a student
@app.post("/students", status_code=201)
async def create_student(student: Student):
    print(student)
    result = await collection.insert_one(student.dict())
    return {"id": str(result.inserted_id)}


@app.get("/students", response_model=List[StudentResponse])
async def list_students(
    country: Optional[str] = Query(None, description="Filter by country"),
    age: Optional[int] = Query(None, description="Filter by minimum age"),
):
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}

    try:
        students = await collection.find(query).to_list(100)
        return [mongo_to_response(student) for student in students]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# Get a specific student by ID
@app.get("/students/{id}", response_model=StudentResponse)
async def get_student(id: str = Path(..., description="ID of the student")):
    student = await collection.find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return mongo_to_response(student)


# Update a student's details
@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: UpdateStudent):
    update_data = {k: v for k, v in student.dict().items() if v is not None}
    result = await collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found or no changes made")
    return None

@app.get("/m")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# Delete a student
@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
