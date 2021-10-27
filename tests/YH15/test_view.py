from typing import List

from django.test import TestCase, RequestFactory

from YH15.models import Bar
from YH15.views import (
    list,
)

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


class TestBarListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.bar_list: List[Bar] = create_test_bar_list()

    def test_list(self):
        request = self.factory.get("/YH15/list/")
        response = list(request)
        self.assertEqual(response.status_code, 200)










