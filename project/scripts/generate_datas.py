from datetime import datetime

import numpy as np
import pandas as pd

from project.orm_fonte.models import engine_fonte


def generate_datas(
    interval: tuple[datetime, datetime],
    engine=engine_fonte,
):
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
