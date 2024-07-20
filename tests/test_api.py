from datetime import datetime
from unittest.mock import patch

import pytest
from sqlalchemy import select

from project.orm_fonte.models import Data
from project.pipeline import Pipeline


@pytest.mark.parametrize(
    'timestamp, wind_speed, power, ambient_temperature, resultado_esperado',
    [
        (
            True, True, True, True,
            {'timestamp', 'wind_speed', 'power', 'ambient_temperature'}
        ),
        (
            True, True, False, True,
            {'timestamp', 'wind_speed', 'ambient_temperature'}
        ),
        (
            True, False, False, True,
            {'timestamp', 'ambient_temperature'}
        ),
        (
            True, True, True, False,
            {'timestamp', 'wind_speed', 'power'}
        ),
        (
            True, True, False, False,
            {'timestamp', 'wind_speed'}
        ),
        (
            True, False, False, False,
            {'timestamp'}
        ),
    ]
)
def test_api_get_data_by_options(
    client,
    session_fonte,
    timestamp,
    wind_speed,
    power,
    ambient_temperature,
    resultado_esperado,
):
    url = (
        f'http://localhost:8000/?start_date=2024-01-01&end_date=2024-01-02'
        f'&timestamp={timestamp}&wind_speed={wind_speed}&power={power}'
        f'&ambient_temperature={ambient_temperature}&limit=100&skip=0'
    )

    response = client.get(url)

    assert response.status_code == 200

    resultado = response.json()

    assert resultado

    assert resultado[0].keys() == resultado_esperado

    data = session_fonte.scalar(select(Data))

    if timestamp:
        date = datetime.strptime(
            resultado[0].get('timestamp'), '%Y-%m-%d %H:%M:%S.%f'
        )

        assert date == data.timestamp

    if wind_speed:
        assert resultado[0].get('wind_speed') == data.wind_speed

    if power:
        assert resultado[0].get('power') == data.power

    if ambient_temperature:
        assert resultado[0].get(
            'ambient_temperature'
        ) == data.ambient_temperature


def test_get_data_by_date(client, session_fonte):
    url = 'http://localhost:8000/date?date=2024-01-01'

    response = client.get(url)

    assert response.status_code == 200

    resultado = response.json()

    assert resultado

    data = session_fonte.scalar(select(Data))

    date = datetime.strptime(
        resultado[0].get('timestamp'), '%Y-%m-%dT%H:%M:%S'
    )

    assert date == data.timestamp


@pytest.mark.parametrize(
    'name',
    [
        'wind_speed',
        'power',
    ]
)
def test_get_signal_by_name(
    client, session_alvo, session_fonte, engine_alvo, name
):

    with patch(
        'project.stages.extract.extract_datas_fonte'
            '.ExtractDatasFonte._get_client',
        return_value=client
    ), patch(
        'project.stages.load.load_datas.LoadDatas._engine_alvo',
        return_value=engine_alvo
    ):
        Pipeline(date=datetime(2024, 1, 1)).run()

    url = f'http://localhost:8000/signal?name={name}'

    response = client.get(url)

    assert response.status_code == 200

    resultado = response.json()

    assert resultado.get('name') == name

    assert resultado.get('data')


def test_get_signal_by_name_and_date(
    client, session_alvo, session_fonte, engine_alvo
):
    with patch(
        'project.stages.extract.extract_datas_fonte'
            '.ExtractDatasFonte._get_client',
        return_value=client
    ), patch(
        'project.stages.load.load_datas.LoadDatas._engine_alvo',
        return_value=engine_alvo
    ):
        Pipeline(date=datetime(2024, 1, 1)).run()

    url = (
        'http://localhost:8000/signal/date?name=wind_speed'
        '&date=2024-01-01'
    )

    response = client.get(url)

    assert response.status_code == 200

    resultado = response.json()

    assert resultado.get('name') == 'wind_speed'

    assert resultado.get('data')
