rom fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pymongo import MongoClient

app = FastAPI()

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")
db = client.userLogins
collection = db.logins

# Pydantic Model for Request Validation
class LoginEvent(BaseModel):
    userKey: str
    deviceType: str

@app.post("/Log/auth", status_code=status.HTTP_200_OK)
def store_user_login_event(login_event: LoginEvent):
    try:
        # Insert data into MongoDB
        collection.insert_one(login_event.dict())
        return {"statusCode": 200, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="bad_request")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)