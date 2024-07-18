from project.orm_fonte.models import engine_fonte
from datetime import datetime
import pandas as pd
import numpy as np


interval = (
    datetime(2024, 1, 1),
    datetime(2024, 1, 10)
)


def generate_datas():
    interval_datas = pd.date_range(interval[0], interval[1], freq="1min")

    data_frame = pd.DataFrame(
        {
            "timestamp": interval_datas,
            "wind_speed": np.random.uniform(3, 25, len(interval_datas)),
            "power": np.random.uniform(0, 1000, len(interval_datas)),
            "ambient_temperature": np.random.uniform(-50, 100, len(interval_datas)),
        }
    )

    data_frame.to_sql("data", engine_fonte, if_exists="replace", index=False)
