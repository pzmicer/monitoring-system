from datetime import datetime
from decimal import Decimal
from typing import Optional
from typing import List
from sqlalchemy import ForeignKey, Numeric, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class SensorData(Base):
    __tablename__ = "sensor_data"

    device_id: Mapped[int] = mapped_column(ForeignKey("device.device_id", ondelete="SET NULL"), primary_key=True)
    time: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    temp_c: Mapped[float]
    humidity: Mapped[float]

    device: Mapped["Device"] = relationship(back_populates="data")


class Device(Base):
    __tablename__ = "device"

    id: Mapped[int] = mapped_column("device_id", primary_key=True)
    name: Mapped[Optional[str]] = mapped_column("device_name")
    station_id: Mapped[int] = mapped_column(ForeignKey("station.station_id", ondelete="SET NULL"))

    station: Mapped["Station"] = relationship(back_populates="devices")
    data: Mapped[List["SensorData"]] = relationship(back_populates="device")


class Station(Base):
    __tablename__ = "station"

    id: Mapped[int] = mapped_column("station_id", primary_key=True)
    name: Mapped[str] = mapped_column("station_name")
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric)

    devices: Mapped[List["Device"]] = relationship(back_populates="station")