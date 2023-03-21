from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel


class SensorData(BaseModel):
    # device_id: int
    time: datetime
    temp_c: float
    humidity: float
        
    class Config:
        orm_mode = True


#===============================================


class DeviceCreate(BaseModel):
    station_id: int
    name: str | None = None


class Device(BaseModel):
    id: int
    station_id: int
    name: str | None = None
    
    class Config:
        orm_mode = True


class DeviceWithData(Device):
    data: list[SensorData] = []


#===============================================


class StationCreate(BaseModel):
    name: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None


class Station(BaseModel):
    id: int
    name: str
    latitude: Decimal | None = None
    longitude: Decimal | None = None

    class Config:
        orm_mode = True


class StationWithDevices(Station):
    devices: list[Device] = []


class StationWithInfo(BaseModel):
    station: Station
    avg_temp: float
    avg_hum: float

    class Config:
        orm_mode = True
