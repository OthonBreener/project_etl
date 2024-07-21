import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from project.orm_alvo.models import Signal, engine_alvo
from project.contracts import ContractTransform


class LoadDatas:
    def __init__(self, contract_transform: ContractTransform) -> None:
        self.datas = contract_transform.data_frame

    def _engine_alvo(self):
        return engine_alvo

    def load(self) -> None:
        data_frame = self.datas

        data_frame_wind_speed = data_frame["wind_speed"].copy()
        self._save_dataframe_wind_speed(data_frame_wind_speed)

        data_frame_power = data_frame["power"].copy()
        self._save_dataframe_power(data_frame_power)

    def _save_dataframe_wind_speed(
        self, data_frame_wind_speed: pd.DataFrame
    ) -> None:
        try:
            signal = self._get_signal_by_name("wind_speed")

            data_frame_wind_speed["signal_id"] = signal.id

            data_frame_wind_speed.to_sql(
                "data",
                self._engine_alvo(),
                if_exists="append",
                index=True,
                index_label="timestamp",
            )
        except Exception as exception:
            raise self.LoadErrorSaveSignal(
                f"Error on save dataframe wind speed: {exception}"
            ) from exception

    def _save_dataframe_power(self, data_frame_power: pd.DataFrame) -> None:
        try:
            signal = self._get_signal_by_name("power")

            data_frame_power["signal_id"] = signal.id

            data_frame_power.to_sql(
                "data",
                self._engine_alvo(),
                if_exists="append",
                index=True,
                index_label="timestamp",
            )
        except Exception as exception:
            raise self.LoadErrorSaveSignal(
                f"Error on save dataframe power: {exception}"
            ) from exception

    def _save_signal(self, name: str) -> Signal:
        try:
            with Session(self._engine_alvo()) as session:
                signal = Signal(name=name)
                session.add(signal)
                session.commit()
                session.refresh(signal)

            return signal

        except Exception as exception:
            raise self.LoadErrorSaveSignal(
                f"Error on save signal: {exception}"
            ) from exception

    def _get_signal_by_name(self, name: str) -> Signal:
        with Session(self._engine_alvo()) as session:
            signal = session.scalar(select(Signal).where(Signal.name == name))

        if not signal:
            signal = self._save_signal(name)

        return signal

    class LoadErrorSaveSignal(Exception):
        pass

    class LoadError(Exception):
        pass
