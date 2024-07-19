from datetime import datetime

from httpx import Client


class ExtractDatasFonte:
    def __init__(self, date: datetime) -> None:
        self.date = date

    def extract(self) -> dict[str, float | str]:
        url = f"http://localhost:8000/date?date={self.date}"

        datas = Client().get(url).json()

        return datas
