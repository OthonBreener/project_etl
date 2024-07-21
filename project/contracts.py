from dataclasses import dataclass

from pandas import DataFrame


@dataclass(frozen=True)
class ContractExtract:
    datas: list[dict[str, float | str]]


@dataclass(frozen=True)
class ContractTransform:
    data_frame: DataFrame
