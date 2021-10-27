from typing import List

from django.test import TestCase, RequestFactory

from YH15.models import Bar
from YH15.views import (
    info,
    details,
)
from tests.YH15.test_view import create_test_bar_list


class TestBarListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.bar_list: List[Bar] = create_test_bar_list()

    def test_info(self):
        request = self.factory.get("/YH15/info/")
        response = info(request, bar_id=1)
        self.assertEqual(response.status_code, 200)

    def test_details(self):
        request = self.factory.get("/YH15/details/")
        response = details(request, bar_id=1)
        self.assertEqual(response.status_code, 200)


