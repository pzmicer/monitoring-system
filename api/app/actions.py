from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from . import schemas
from .models import Station, Device, SensorData


def get_stations(db: Session):
    return db.scalars(select(Station)).all()


def get_station(db: Session, station_id: int):
    return db.get(Station, station_id)


def get_station_info(db: Session, station_id: int):
    stmt = (
        select(
            Station, 
            func.avg(SensorData.temp_c).label("avg_temp"),
            func.avg(SensorData.humidity).label("avg_hum"),
        )
        .join(Station.devices)
        .join(Device.data)
        .where(Station.id == station_id)
        .group_by(Station.id)
    )
    return db.execute(stmt).first()


def get_device_data(db: Session, device_id: int, days: int):
    stmt = (
        select(SensorData)
        .where(and_(
            SensorData.device_id == device_id,
            SensorData.time > (datetime.utcnow()-timedelta(days=days)),
        ))
    )
    return db.scalars(stmt).all()


def get_device(db: Session, device_id: int):
    return db.get(Device, device_id)


def create_station(db: Session, station: schemas.StationCreate):
    db_station = Station(
        name=station.name, 
        latitude=station.latitude, 
        longitude=station.longitude
    )
    db.add(db_station)
    db.commit()
    db.refresh(db_station)
    return db_station


def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = Device(name=device.name, station_id=device.station_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def delete_station(db: Session, station_id: int):
    db_station = db.get(Station, station_id)
    if db_station is not None:
        db.delete(db_station)
        db.commit()
    return db_station


def delete_device(db: Session, device_id: int):
    db_device = db.get(Device, device_id)
    if db_device is not None:
        db.delete(db_device)
        db.commit()
    return db_device


def update_station(db: Session, station: schemas.Station):
    db_station = db.get(Station, station.id)
    if db_station is not None:
        db_station.name = station.name
        db_station.latitude = station.latitude
        db_station.longitude = station.longitude
        db.commit()
        db.refresh(db_station)
    return db_station


def update_device(db: Session, device: schemas.Device):
    db_device = db.get(Device, device.id)
    if db_device is not None:
        db_device.name = device.name
        db_device.station_id = device.station_id
        db.commit()
        db.refresh(db_device)
    return db_device