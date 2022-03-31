from datetime import datetime
from django.shortcuts import render
from fastparquet import ParquetFile
from django.views.generic import TemplateView

file = '/home/kir/Documents/prices.parquet'


def time_to_datetime(row):
    return datetime.fromtimestamp(row['time']).strftime("%Y%m%d %H:%M:%S")


def index(request):
    df = ParquetFile(file).to_pandas()
    ids = df.id.unique()
    return render(request, 'id_list.html', {'ids': ids})


# Chart ==============================================================================================================

from random import shuffle
from chartjs.colors import COLORS, next_color
from chartjs.views.lines import BaseLineChartView


class LineChartJSONView(BaseLineChartView):
    def get_providers(self):
        return ["Prices"]

    def get_labels(self):
        pid = 1
        if 'pid' in self.kwargs:
            pid = self.kwargs['pid']
        df = ParquetFile(file).to_pandas()
        df.set_index(['id'])
        res = df[df.id == pid]
        res['tm'] = res.apply(time_to_datetime, axis=1)
        res = res[['price', 'tm']]
        return res.tm.to_list()

    def get_data(self):
        pid = 1
        if 'pid' in self.kwargs:
            pid = self.kwargs['pid']

        df = ParquetFile(file).to_pandas()
        df.set_index(['id'])
        res = df[df.id == pid]
        res['tm'] = res.apply(time_to_datetime, axis=1)
        res = res[['price', 'tm']]
        return [res.price.to_list()]

    def get_colors(self):
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)
    pass


line_chart = TemplateView.as_view(template_name="line_chart.html")
line_chart_json = LineChartJSONView.as_view()

