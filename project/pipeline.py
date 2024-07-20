"""
Pipeline para transferir dados do banco de dados fonte
para o alvo.
"""
from datetime import datetime
from project.stages.extract.extract_datas_fonte import ExtractDatasFonte
from project.stages.transform.transform_datas import TransformDatas
from project.stages.load.load_datas import LoadDatas


class Pipeline:
    def __init__(self, date: datetime) -> None:
        self.date = date

    def run(self) -> None:
        datas = ExtractDatasFonte(self.date).extract()

        transformed_datas = TransformDatas(datas).transform()

        LoadDatas(transformed_datas).load()
