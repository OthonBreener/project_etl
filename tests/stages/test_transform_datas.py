from datetime import datetime
from unittest.mock import patch

import pytest
from pandas import DataFrame

from project.contracts import ContractExtract, ContractTransform
from project.stages.extract.extract_datas_fonte import ExtractDatasFonte
from project.stages.transform.transform_datas import TransformDatas


def test_transform_datas(client):
    date = datetime(2024, 1, 1)

    with patch(
        'project.stages.extract.extract_datas_fonte'
            '.ExtractDatasFonte._get_client',
        return_value=client
    ):
        datas = ExtractDatasFonte(date).extract()

    result_transform = TransformDatas(datas).transform()

    assert isinstance(result_transform, ContractTransform)
    assert isinstance(result_transform.data_frame, DataFrame)
    assert result_transform.data_frame['power'].empty is False
    assert result_transform.data_frame['wind_speed'].empty is False


def test_transform_datas_excpetion(client):
    datas = ContractExtract(
        datas=[{'a': 1}]
    )

    with pytest.raises(TransformDatas.TransformError) as excinfo:
        TransformDatas(datas).transform()

    assert str(excinfo.value) == "Error on transform datas: 'timestamp'"
