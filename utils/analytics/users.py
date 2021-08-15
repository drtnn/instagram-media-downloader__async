from data.config import CHART_DIR
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import os
from utils.db_api.database import User


async def generate_chart(duration: int, filename: str):
    date = datetime.now()
    dates_to_count_users = await User.count_for_dates(date, duration)

    bars = tuple(dates_to_count_users.keys())
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, list(dates_to_count_users.values()))
    plt.xticks(y_pos, bars)
    plt.title(f'Новые пользователи за промежуток {(date - timedelta(duration)).strftime("%d.%m.%Y")} – {date.strftime("%d.%m.%Y")}')
    plt.xlabel(f'В базе данных {await User.count_users()} пользователя(ей)')

    if not os.path.exists(CHART_DIR):
        os.mkdir(CHART_DIR)
    plt.savefig(CHART_DIR + filename)
    plt.close()

    return CHART_DIR + filename
