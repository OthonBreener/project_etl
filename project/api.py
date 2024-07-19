from datetime import datetime

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from project.orm_fonte.models import Data, get_session_fonte

app = FastAPI()


class DataSchema(BaseModel):
    timestamp: datetime
    wind_speed: float
    power: float
    ambient_temperature: float


class Options(BaseModel):
    timestamp: int = 1
    wind_speed: int = 1
    power: int = 1
    ambient_temperature: int = 1
    skip: int = (0,)
    limit: int = (10,)


@app.get("/", response_model=list[DataSchema])
def get_all_data(
    start_date: datetime,
    end_date: datetime,
    options: Options,
    session: Session = Depends(get_session_fonte),
):
    sub_query = []
    if options.timestamp:
        sub_query.append(Data.timestamp)

    if options.wind_speed:
        sub_query.append(Data.wind_speed)

    if options.power:
        sub_query.append(Data.power)

    if options.ambient_temperature:
        sub_query.append(Data.ambient_temperature)

    datas = session.scalars(
        select(Data)
        .where(and_(Data.timestamp >= start_date, Data.timestamp <= end_date))
        .limit(options.limit)
        .offset(options.skip)
    ).all()

    return datas


@app.get("/date", response_model=list[DataSchema])
def get_data_by_date(
    date: datetime, session: Session = Depends(get_session_fonte)
):
    datas = session.scalars(
        select(Data).where(
            and_(
                Data.timestamp >= date,
                Data.timestamp <= date.replace(hour=23, minute=59, second=59),
            )
        )
    ).all()

    return datas
