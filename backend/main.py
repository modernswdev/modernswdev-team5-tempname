from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.setup import initialize_database_if_needed
from backend.requests import (
    validate_credentials,
    role_int_to_str,
    view_requests,
    view_request_details,
    create_request as create_request_db,
    update_status,
    status_str_to_int,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestCreate(BaseModel):
    title: str
    description: str
    priority: str

class LoginRequest(BaseModel):
    email: str
    password: str
    
class UpdateStatusBody(BaseModel):
    new_status: str

initialize_database_if_needed()

@app.post("/login")
def login(login_data: LoginRequest):
    role_num = validate_credentials(login_data.email, login_data.password)

    if role_num == 0:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "user": {
            "email": login_data.email,
            "role": role_int_to_str(role_num),
        },
    }


#endpoint to get all requests
@app.get("/requests")
def get_requests():
    return view_requests()

#endpoint for specific request
@app.get("/requests/{request_id}")
def get_request(request_id: str):
    request = view_request_details(request_id)
    if request is not None:
        return request
    raise HTTPException(status_code=404, detail="Request not found")

@app.post("/requests")
def create_request(new_request: RequestCreate):
    request_data = create_request_db(
        new_request.title,
        new_request.description,
        new_request.priority,
    )
    return {"message": "Request created successfully", "request": request_data}

@app.put("/requests/{request_id}/status")
def update_request_status(request_id: str, body: UpdateStatusBody):
    if status_str_to_int(body.new_status) is None:
        raise HTTPException(status_code=400, detail="Invalid status value")

    updated = update_status(request_id, body.new_status)
    if not updated:
        raise HTTPException(status_code=404, detail="Request not found")

    request = view_request_details(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")

    return {"message": "Status updated successfully", "request": request}


