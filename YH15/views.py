import random
from typing import List, Dict

from django.http import HttpResponse
from django.template import loader
from django.db.models.query import QuerySet
from django.db.models import Q
from django.views.generic import DetailView

from YH15.models import Bar
from YH15.filter import BarFilter
from YH15.request_helper import RequestHelper


def send_http_request(request, bar_list: QuerySet, template: str) -> HttpResponse:

    template = loader.get_template(template)
    context = {
        'bar_list': bar_list,
    }
    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def create_more():
    import random
    from YH15.models import Bar

    names =[
        "CHAIRS",
        "FULTON STREET",
        "HANDLES MIDWOOD",
        "HANDLES FROZEN YOGURT",
        "BOWERY HOLDING",
        "AVENUE GLATT",
        "ORCHARD BAR",
        "ESTRELLA",
        "HUDSON BAGEL CORP",
    ]
    for name in names:
        c = random.randrange(100, 800)
        o = int(c * random.randrange(1, 11) / 10)
        r = round(random.random() * 5 + 2, 1)
        if r >=5:
            r = 4.2

        Bar.objects.create(
            bar_name=name.lower(),
            bar_rating=r,
            bar_capacity=c,
            bar_occupancy=o,
        )


class ListBarView(DetailView):
    DEFAULT_TEMPLATE: str = 'YH15/list.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        create_more()
        RequestHelper.reset_search_request()
        RequestHelper.reset_filter_request()
        return send_http_request(
            request,
            ListBarView.get_default_bars(),
            ListBarView.DEFAULT_TEMPLATE
        )

    @staticmethod
    def get_default_bars() -> QuerySet:
        """Get all the bars sorted by bar rating by default."""
        return Bar.objects.order_by('-bar_rating')[:]


class SearchBarView(DetailView):
    DEFAULT_TEMPLATE: str = 'YH15/search.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        query = request.GET.get('name')
        RequestHelper.cache_search_request(query)

        return send_http_request(
            request,
            SearchBarView.search_bar_models(),
            SearchBarView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def search_bar_models() -> QuerySet:
        bar_list = Bar.objects.filter(
            Q(
                bar_name__icontains=RequestHelper.bar_search_request
            )
        )
        return bar_list.order_by('-bar_name')[:]


class SortBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/sort.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return send_http_request(
            request,
            SortBarView.sort_bars(request),
            SortBarView.DEFAULT_TEMPLATE
        )

    @staticmethod
    def get_sort_sort_order_and_type(request) -> List[str]:
        return [
            request.GET.get('sort_order'),
            request.GET.get('sort_type'),
        ]

    @staticmethod
    def sort_bars(request) -> QuerySet:
        bar_list = RequestHelper.get_current_bar_query()

        sort_order, sort_type = SortBarView.get_sort_sort_order_and_type(request)

        if sort_order == 'high_low':
            return bar_list.order_by(f'-bar_{sort_type}')[:]

        return bar_list.order_by(f'-bar_{sort_type}')[::-1]


class FilterBarView(DetailView):
    DEFAULT_TEMPLATE = 'YH15/filter.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return send_http_request(
            request,
            FilterBarView.filter_bars(request),
            SortBarView.DEFAULT_TEMPLATE,
        )

    @staticmethod
    def filter_bars(request) -> QuerySet:
        RequestHelper.cache_filter_request(request)
        return BarFilter.filter_bars(request)


def get_bar_details(request, bar_id: int) -> HttpResponse:
    bar = Bar.objects.get(id=bar_id)
    bar_name = bar.bar_name
    return HttpResponse(f"You're looking at bar {bar_name}.")