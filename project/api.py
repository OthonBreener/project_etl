from datetime import datetime

from fastapi import Depends, FastAPI
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from project.orm_alvo.models import Data as DataAlvo
from project.orm_alvo.models import Signal, get_session_alvo
from project.orm_fonte.models import Data, get_session_fonte
from project.schemas import DataSchema, Options, SignalName, SignalSchema

app = FastAPI()


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


@app.get(
    "/signal",
    response_model=SignalSchema,
)
def get_signal_by_name(
    name: SignalName,
    session: Session = Depends(get_session_alvo),
):
    signal = session.scalar(select(Signal).where(Signal.name == name.value))

    return signal


@app.get(
    "/signal/date",
    response_model=SignalSchema,
)
def get_signal_by_name_and_date(
    name: SignalName,
    date: datetime,
    session: Session = Depends(get_session_alvo),
):
    signal = session.scalar(
        select(Signal)
        .join(DataAlvo)
        .where(
            and_(
                DataAlvo.timestamp >= date,
                DataAlvo.timestamp
                <= date.replace(hour=23, minute=59, second=59),
            )
        )
        .where(Signal.name == name.value)
    )

    return signal
