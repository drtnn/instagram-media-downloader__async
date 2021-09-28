from data.config import CHART_DIR
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import os
from utils.db_api.database import Requests


async def generate_chart(duration: int, filename: str):
    date = datetime.now()
    dates_to_sum = await Requests.count_for_dates(date=date, duration=duration)

    bars = tuple(dates_to_sum.keys())
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, list(dates_to_sum.values()))
    plt.xticks(y_pos, bars)
    plt.title(f'Запросы за промежуток {(date - timedelta(duration)).strftime("%d.%m.%Y")} – {date.strftime("%d.%m.%Y")}')

    if not os.path.exists(CHART_DIR):
        os.mkdir(CHART_DIR)
    plt.savefig(CHART_DIR + filename)
    plt.close()

    return CHART_DIR + filename


async def generate_pie_chart(filename: str, duration: int = None):
    date = datetime.now()

    content_types = 'instagram_users', 'instagram_posts', 'instagram_stories', 'instagram_highlights'
    values = [await Requests.count_of_content_type(content_type[10]) for content_type in content_types]

    plt.title(f'Запросы за промежуток {(date - timedelta(duration)).strftime("%d.%m.%Y")} – {date.strftime("%d.%m.%Y")}')
    plt.pie(values, labels=content_types, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})

    if not os.path.exists(CHART_DIR):
        os.mkdir(CHART_DIR)
    plt.savefig(CHART_DIR + filename)
    plt.close()

    return CHART_DIR + filename
