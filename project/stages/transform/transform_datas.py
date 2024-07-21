import pandas as pd
from project.contracts import ContractExtract, ContractTransform


class TransformDatas:
    def __init__(self, contract_extract: ContractExtract) -> None:
        self.datas = contract_extract.datas

    def transform(self) -> ContractTransform:
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

            return ContractTransform(
                data_frame=aggregations
            )
        except Exception as expection:
            raise self.TransformError(
                f"Error on transform datas: {expection}"
            ) from expection

    class TransformError(Exception):
        pass
