import pandas as pd


class TransformDatas:
    def __init__(self, datas: list[dict[str, float | str]]) -> None:
        self.datas = datas

    def transform(self) -> pd.DataFrame:
        try:
            data_frame = pd.DataFrame(self.datas)

            data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp"])

            data_frame.set_index("timestamp", inplace=True)

            aggregations = data_frame.resample("10min").agg(
                {
                    "wind_speed": ["mean", "min", "max", "std"],
                    "power": ["mean", "min", "max", "std"],
                }
            )
        except Exception as expection:
            raise self.TransformError(
                f"Error on transform datas: {expection}"
            ) from expection

        return aggregations

    class TransformError(Exception):
        pass
