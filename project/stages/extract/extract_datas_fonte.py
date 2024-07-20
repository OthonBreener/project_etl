from datetime import datetime
from http import HTTPStatus

from httpx import Client


class ExtractDatasFonte:
    def __init__(self, date: datetime) -> None:
        self.date = date

    def extract(self) -> list[dict[str, float | str]]:
        try:
            url = f"http://localhost:8000/date?date={self.date}"

            datas = Client().get(url)

            assert datas.status_code == HTTPStatus.OK

            return datas.json()

        except Exception as expection:
            raise self.ExtractError(
                f"Error on extract datas from fonte: {expection}"
            ) from expection

    class ExtractError(Exception):
        pass
