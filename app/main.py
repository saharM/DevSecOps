from typing import Optional
from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# MongoDB Configuration
client = AsyncIOMotorClient("mongodb://mongo:27017/")  # Ensure this matches your Docker setup
db = client.userLogins

class DeviceRegister(BaseModel):
    userKey: str
    deviceType: str

class LoginEvent(BaseModel):
    userKey: str
    deviceType: str

@app.post("/Device/register", status_code=status.HTTP_200_OK)
async def register_device(device: DeviceRegister):
    # You could add logic here to check if the device is already registered
    await db.devices.insert_one(device.dict())
    return {"statusCode": 200, "message": "Device registered successfully"}

@app.post("/Log/auth", status_code=status.HTTP_200_OK)
async def store_user_login_event(login_event: LoginEvent, background_tasks: BackgroundTasks):
    # Assuming DeviceRegistrationAPI is part of this same application
    background_tasks.add_task(register_device, device=login_event)
    return {"statusCode": 200, "message": "success"}

@app.get("/Log/auth/statistics", status_code=status.HTTP_200_OK)
async def get_device_statistics(deviceType: Optional[str] = None):
    if deviceType:
        count = await db.devices.count_documents({"deviceType": deviceType})
        return {"deviceType": deviceType, "count": count}
    else:
        device_types = await db.devices.distinct("deviceType")
        results = []
        for dtype in device_types:
            count = await db.devices.count_documents({"deviceType": dtype})
            results.append({"deviceType": dtype, "count": count})
        return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
