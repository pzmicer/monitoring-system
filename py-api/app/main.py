from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import actions, schemas
from .database import SessionLocal


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/stations", response_model=list[schemas.Station])
def get_stations(db: Session = Depends(get_db)):
    res = actions.get_stations(db)
    return res


@app.get("/stations/{station_id}", response_model=schemas.StationWithDevices)
def get_station(station_id: int, db: Session = Depends(get_db)):
    res = actions.get_station(db, station_id)
    return res


@app.get("/stations/{station_id}/info", response_model=schemas.StationWithInfo)
def get_station_info(station_id: int, db: Session = Depends(get_db)):
    res = actions.get_station_info(db, station_id)
    return schemas.StationWithInfo(station=res[0], avg_temp=res[1], avg_hum=res[2])


@app.get("/devices/{device_id}/data", response_model=list[schemas.SensorData])
def get_device_data(device_id: int, days: int, db: Session = Depends(get_db)):
    res = actions.get_device_data(db, device_id, days)
    return res


@app.post("/stations", response_model=schemas.Station)
def create_station(station: schemas.StationCreate, db: Session = Depends(get_db)):
    db_station = actions.create_station(db, station)
    return db_station


@app.post("/devices", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_device = actions.create_device(db, device)
    if db_device:
        raise HTTPException(status_code=400)
    return db_device


@app.delete("/stations/{station_id}", response_model=schemas.Station)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    db_station = actions.delete_station(db, station_id)
    if db_station is None:
        raise HTTPException(status_code=400, detail=f"No object with id={station_id}")
    return db_station


@app.delete("/devices/{device_id}", response_model=schemas.Device)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = actions.delete_device(db, device_id)
    if db_device is None:
        raise HTTPException(status_code=400, detail=f"No object with id={device_id}")
    return db_device


@app.put("/stations", response_model=schemas.Station)
def update_station(station: schemas.Station, db: Session = Depends(get_db)):
    db_station = actions.update_station(db, station)
    if db_station is None:
        raise HTTPException(status_code=400, detail=f"No object with id={station.id}")
    return db_station


@app.put("/devices", response_model=schemas.Device)
def update_devices(device: schemas.Device, db: Session = Depends(get_db)):
    db_device = actions.update_device(db, device)
    if db_device is None:
        raise HTTPException(status_code=400, detail=f"No object with id={device.id}")
    return db_device
