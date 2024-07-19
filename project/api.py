from datetime import datetime
from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from project.orm_fonte.models import Data, get_session_fonte

app = FastAPI()


class DataSchema(BaseModel):
    timestamp: datetime
    wind_speed: float
    power: float
    ambient_temperature: float


@app.get("/", response_model=list[DataSchema])
def get_all_data(
    start_date: datetime,
    end_date: datetime,
    timestamp: int = 1,
    wind_speed: int = 1,
    power: int = 1,
    ambient_temperature: int = 1,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session_fonte)
):
    # sub_query = []
    # if timestamp:
    #     sub_query.append(Data.timestamp)
    #
    # if wind_speed:
    #     sub_query.append(Data.wind_speed)
    #
    # if power:
    #     sub_query.append(Data.power)
    #
    # if ambient_temperature:
    #     sub_query.append(Data.ambient_temperature)

    datas = session.scalars(
        select(Data).where(
            and_(Data.timestamp >= start_date, Data.timestamp <= end_date)
        ).limit(limit).offset(skip)
    ).all()

    return datas


@app.get("/date", response_model=list[DataSchema])
def get_data_by_date(
    date: datetime,
    session: Session = Depends(get_session_fonte)
):
    datas = session.scalars(
        select(Data).where(
            and_(Data.timestamp >= date, Data.timestamp <= date.replace(hour=23, minute=59, second=59))
        )
    ).all()

    return datas
