import pandas as pd


class TransformDatas:
    def __init__(self, datas: list[dict[str, float | str]]) -> None:
        self.datas = datas

    def transform(self):
        data_frame = pd.DataFrame(self.datas)

        data_frame.set_index('timestamp', inplace=True)

        data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp"])

        aggregations = data_frame.resample("10min").agg(
            {
                "wind_speed": ["mean", "min", "max", "std"],
                "power": ["mean", "min", "max", "std"],
            }
        )

        return aggregations
