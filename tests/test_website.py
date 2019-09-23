import unittest

from website_measure.constants import ROUND_VALUE
from website_measure.website import WebsiteMeasurement


class TestWebsiteMeasurement(unittest.TestCase):
    def setUp(self):
        self.object_1 = WebsiteMeasurement('', 1, 2.22222)
        self.object_2 = WebsiteMeasurement('', 1, 3.33333)
        self.object_3 = WebsiteMeasurement('', 1, 4.44444)

        self.all_objects = [self.object_1, self.object_2, self.object_3]

    def test_post_init(self):
        for obj in self.all_objects:
            self.assertEqual(obj.time, obj.calculate_time())
            self.assertEqual(obj.time_round, obj.round_time())

    def test_round_time(self):
        for obj in self.all_objects:
            self.assertEqual(
                obj.time_round,
                round(obj.time, ROUND_VALUE)
            )

    def test_calculate_time(self):
        for obj in self.all_objects:
            self.assertEqual(obj.time, obj.end_time - obj.start_time)

    def test_sort(self):
        sorted_objects = WebsiteMeasurement.sort(self.all_objects)
        self.assertTrue(
            sorted_objects[0].time <
            sorted_objects[1].time <
            sorted_objects[2].time
        )

    def test_set_ranking_place(self):
        sorted_objects = WebsiteMeasurement.sort(self.all_objects)
        ranked_objects = WebsiteMeasurement.set_ranking_place(
            sorted_objects
        )
        self.assertTrue(
            ranked_objects[0].ranking_place <
            ranked_objects[1].ranking_place <
            ranked_objects[2].ranking_place
        )

    def test_get_sorted_ranking(self):
        ranked_objects = WebsiteMeasurement.get_sorted_ranking(
            self.all_objects
        )
        self.assertTrue(
            ranked_objects[0].ranking_place <
            ranked_objects[1].ranking_place <
            ranked_objects[2].ranking_place
        )
