from typing import List

from django.test import TestCase, RequestFactory

from YH15.models import Bar
from YH15.views import (
    ListBarView,
    FilterBarView,
    SearchBarView,
)
from tests.YH15.test_views import create_test_bar_list


class TestBarList(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_list(self) -> None:
        request = self.factory.get("/YH15/")
        response = ListBarView().get(request)
        self.assertEqual(response.status_code, 200)

        self.assertIn(
            b'csrfmiddlewaretoken',
            response.content,
        )


class TestBarSearch(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_bar_search(self) -> None:
        with self.assertRaises(ValueError):
            request = self.factory.get("/YH15/")
            SearchBarView().get(request)

        request = self.factory.get("/YH15/search/?name=bar")
        response = SearchBarView().get(request)
        self.assertIn(
            b'csrfmiddlewaretoken',
            response.content,
        )

        self.assertEqual(
            len(response.content),
            2166,
        )


class TestBarFilter(TestCase):
    def setUp(self) -> None:
        self.bar_list: List[Bar] = create_test_bar_list()
        self.factory = RequestFactory()

    def test_filter_bar(self) -> None:
        request = self.factory.get("/YH15/filter/?rating=&capacity=100&occupancy=")
        response = FilterBarView().get(request)

        self.assertIn(
            b'<title>Sort Result</title>',
            response.content,
        )