from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest
from sqlalchemy import select

from project.contracts import ContractTransform
from project.orm_alvo.models import Data, Signal
from project.stages.extract.extract_datas_fonte import ExtractDatasFonte
from project.stages.load.load_datas import LoadDatas
from project.stages.transform.transform_datas import TransformDatas


def test_load_datas(client, engine_alvo, session_alvo):

    date = datetime(2024, 1, 1)

    with patch(
        'project.stages.extract.extract_datas_fonte'
            '.ExtractDatasFonte._get_client',
        return_value=client
    ):
        result = ExtractDatasFonte(date).extract()

    result_transform = TransformDatas(result).transform()

    with patch(
        'project.stages.load.load_datas.LoadDatas._engine_alvo',
        return_value=engine_alvo
    ):
        LoadDatas(result_transform).load()

    signal_wind = session_alvo.scalar(
        select(Signal).where(Signal.name == 'wind_speed')
    )

    assert isinstance(signal_wind, Signal)
    assert signal_wind.name == 'wind_speed'
    assert signal_wind.data
    assert isinstance(signal_wind.data[0], Data)

    signal_power = session_alvo.scalar(
        select(Signal).where(Signal.name == 'power')
    )

    assert isinstance(signal_power, Signal)
    assert signal_power.name == 'power'
    assert signal_power.data
    assert isinstance(signal_power.data[0], Data)


def test_load_datas_exception(client):
    transform_contract = ContractTransform(
        data_frame=pd.DataFrame({'a': [1]})
    )

    with pytest.raises(LoadDatas.LoadError) as excinfo:
        LoadDatas(transform_contract).load()

    assert str(excinfo.value) == "Error on load datas: 'wind_speed'"
