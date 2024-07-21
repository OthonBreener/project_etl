from project.stages.extract.extract_datas_fonte import (
    ExtractDatasFonte
)
from project.contracts import ContractExtract
from datetime import datetime
from unittest.mock import patch
import pytest


def test_extract_datas_fonte(client):
    date = datetime(2024, 1, 1)

    with patch(
        'project.stages.extract.extract_datas_fonte'
            '.ExtractDatasFonte._get_client',
        return_value=client
    ):
        result = ExtractDatasFonte(date).extract()

    assert isinstance(result, ContractExtract)
    assert result.datas
    assert result.datas[0].keys() == {
        'timestamp', 'wind_speed', 'power', 'ambient_temperature'
    }
    assert result.datas[0].values()


def test_extract_datas_fonte_exception(client):
    date = datetime(2024, 1, 5)

    with patch(
        'project.stages.extract.extract_datas_fonte'
            '.ExtractDatasFonte._get_client',
        return_value=client
    ):
        with pytest.raises(ExtractDatasFonte.ExtractError) as excinfo:
            ExtractDatasFonte(date).extract()

    assert str(excinfo.value) == (
        'Error on extract datas from fonte: Datas not found'
    )
