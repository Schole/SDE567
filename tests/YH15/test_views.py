from typing import List, Dict

from django.test import TestCase, RequestFactory

from YH15.models import Bar
import YH15.views as views
from YH15.views import (
    ListBarView,
    SortBarView,
    get_bar_details,
    FilterBarView,
)
from YH15.filter import BarFilter


def create_test_bar_list(total_bar_num: int = 10) -> List[Bar]:
    test_bar_list = []
    for index in range(1, total_bar_num):
        bar = Bar.objects.create(
            bar_name=f"test_bar_name_{index}",
            bar_rating=(1 + index) / 10,
            bar_capacity=Bar.MAX_BAR_CAPACITY - index * 10,
            bar_occupancy=Bar.MAX_BAR_CAPACITY // 2 - index * 10
        )
        test_bar_list.append(bar)
    return test_bar_list


class TestBarSearchView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.bar_list: List[Bar] = create_test_bar_list()

    def test_get_default_bars(self) -> None:
        bars = ListBarView.get_default_bars()
        self.assertEqual(
            list(bars),
            self.bar_list[::-1],
        )


class TestBarFilterView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.bar_list: List[Bar] = create_test_bar_list()

    def test_to_filter_invalid_query(self) -> None:
        request = self.factory.get("/YH15/filter/?occupancy=")
        query_set = BarFilter.filter_bars(request)
        self.assertEqual(len(query_set), 0)

    def test_to_filter_bar_search_not_none(self) -> None:
        views.BAR_SEARCH_QUERY = "test"
        request = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        query_set = BarFilter.filter_bars(request)
        self.assertEqual(len(query_set), 9)

    def test_to_filter(self) -> None:
        request = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        query_set = BarFilter.filter_bars(request)
        self.assertEqual(len(query_set), 9)

    def test_get_bar_details(self) -> None:
        response = get_bar_details(None, 1)
        self.assertEqual(
            response.content,
            b"You're looking at bar test_bar_name_1."
        )


class TestBarSortView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.bar_list: List[Bar] = create_test_bar_list()

    def test_bar_sort_low_high(self) -> None:
        request = self.factory.get("/YH15/sort/?sort_type=rating&sort_order=low_high")
        response = SortBarView().get(request)
        self.assertEqual(response.status_code, 200)

    def test_bar_sort_high_low(self) -> None:
        request = self.factory.get("/YH15/sort/?sort_type=rating&sort_order=high_low")
        response = SortBarView().get(request)
        self.assertEqual(response.status_code, 200)

    def test_bar_sort_bar_search_is_not_none(self) -> None:
        views.BAR_SEARCH_QUERY = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        request = self.factory.get("/YH15/sort/?sort_type=rating&sort_order=low_high")
        response = SortBarView().get(request)
        self.assertEqual(response.status_code, 200)

    def test_bar_sort_bar_search_is_none(self) -> None:
        views.BAR_SEARCH_QUERY = None
        views.BAR_FILTER_QUERY = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        request = self.factory.get("/YH15/sort/?sort_type=rating&sort_order=low_high")
        response = SortBarView().get(request)
        self.assertEqual(response.status_code, 200)

    def test_bar_sort_bar_filter_is_none(self) -> None:
        views.BAR_SEARCH_QUERY = None
        views.BAR_FILTER_QUERY = None
        request = self.factory.get("/YH15/sort/?sort_type=rating&sort_order=low_high")
        response = SortBarView().get(request)
        self.assertEqual(response.status_code, 200)