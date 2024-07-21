from datetime import datetime
from http import HTTPStatus

from httpx import Client
from loguru import logger

from project.contracts import ContractExtract


class ExtractDatasFonte:
    def __init__(self, date: datetime) -> None:
        self.date = date

    def _get_client(self) -> Client:
        return Client()

    def extract(self) -> ContractExtract:
        try:
            logger.info("Extracting datas from fonte")
            url = f"http://localhost:8000/date?date={self.date}"

            datas = self._get_client().get(url)
            logger.info(
                f"Request to {url} with status code {datas.status_code}"
            )

            assert datas.status_code == HTTPStatus.OK, "Datas not found"

            logger.info("Datas extracted from fonte")
            return ContractExtract(
                datas=datas.json()
            )

        except Exception as expection:
            logger.error(f"Error on extract datas from fonte: {expection}")
            raise self.ExtractError(
                f"Error on extract datas from fonte: {expection}"
            ) from expection

    class ExtractError(Exception):
        pass
