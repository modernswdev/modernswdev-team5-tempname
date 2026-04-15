from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from backend.requests import (
    prepare_database,
    read_datasets,
    view_requests,
    view_request_details,
    create_request as db_create_request,
    update_status as db_update_status,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#hardcoded loin for MVP
requests = [
    {
        "id": "1",
        "title": "Reset MFA on account",
        "user": "Eliza Morgan",
        "description": " ",
        "created_at": "12/03/2025",
        "priority": "High",
        "status": "Open",
    },
    {
        "id": "2",
        "title": "Software Access Request",
        "user": "Mike Chang",
        "description": " ",
        "created_at": "01/21/2026",
        "priority": "Low",
        "status": "In Progress",
    },
    {
        "id": "3",
        "title": "Account lockout",
        "user": "John Smith",
        "description": " ",
        "created_at": "03/12/2026",
        "priority": "Medium",
        "status": "Open",
    }
]

# hardcoded users 
users = [
    {
        "id": "1",
        "first_name": "Eliza",
        "last_name": "Morgan",
        "email": "Testuser@gmail.com",
        "password": "test123",
        "role": "User",
    }
]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class createRequestBody(BaseModel):
    title: str
    description: str
    priority: str

class updateStatusBody(BaseModel):
    new_status: str

@app.on_event("startup")
def startup_event():
    prepare_database()
    read_datasets()

@app.get("/")
def home():
    return {"message": "Welcome to the Service Request Tracker API!"}

@app.post("/login")
def login(request: LoginRequest):
    for user in users:
        if user["email"].lower() == request.email.lower() and user["password"] == request.password:
            return {
                "message": "Login successful",
                "user": {
                    "user_id": user["id"],
                    "email": user["email"],
                    "role": user["role"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                },
            }
    raise HTTPException(status_code=401, detail="Invalid email or password")

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: RegisterUser):
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "id": str(len(users) + 1),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password, # In a real application, never store plain passwords!
        "role": "User",  # Default role for new users
    }
    users.append(new_user)
    return {
        "message": "User registered successfully",
        "user": {
             "user_id": new_user["id"], 
             "email": new_user["email"], 
             "role": new_user["role"], 
             "first_name": new_user["first_name"], 
             "last_name": new_user["last_name"],
        },
    }

@app.get("/requests")
def get_requests():
    return view_requests()

@app.get("/requests/{request_id}")
def get_request(request_id: int):
    request = view_request_details(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return request

@app.post("/requests", status_code=status.HTTP_201_CREATED)
def create_request(request: createRequestBody):
    created = db_create_request(request.title, request.description, request.priority)
    if created is None:
        raise HTTPException(status_code=400, detail="Failed to create request")
    return created

@app.put("/requests/{request_id}/status")
def update_request_status(request_id: int, body: updateStatusBody):
    updated = db_update_status(request_id, body.new_status)
    if updated is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return {
        "message": "Status updated successfully",
        "request": updated
    }


