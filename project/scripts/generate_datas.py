from datetime import datetime

import numpy as np
import pandas as pd

import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))


def generate_datas(
    interval: tuple[datetime, datetime] = (
        datetime(2024, 1, 1),
        datetime(2024, 1, 10)
    ),
    engine=None,
):
    from project.orm_fonte.models import engine_fonte

    if not engine:
        engine = engine_fonte

    interval_datas = pd.date_range(interval[0], interval[1], freq="1min")

    data_frame = pd.DataFrame(
        {
            "timestamp": interval_datas,
            "wind_speed": np.random.uniform(3, 25, len(interval_datas)),
            "power": np.random.uniform(0, 1000, len(interval_datas)),
            "ambient_temperature": np.random.uniform(
                -50, 100, len(interval_datas)
            ),
        }
    )

    data_frame.to_sql("data", engine, if_exists="append", index=False)
