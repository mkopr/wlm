from dataclasses import dataclass, field
from time import time

from website_measure.constants import ROUND_VALUE


@dataclass
class WebsiteMeasurement:
    """
    Dataclass object with website measurement data.
    """
    url: str
    start_time: time
    end_time: time
    ranking_place: int = field(init=False)
    time: float = field(init=False, metadata={'unit': 'seconds'})
    time_round: float = field(init=False, metadata={'unit': 'seconds'})

    def __str__(self):
        """
        Format of print(WebsiteMeasurement())

        :return: str
        """
        return f'|{self.ranking_place}. \t| time: {self.time_round} \t| url:' \
               f' {self.url}'

    def __post_init__(self):
        """
        Calculate self.time and self.time_round after init object.

        :return: None
        """
        self.time = self.calculate_time()
        self.time_round = self.round_time()

    def round_time(self):
        """
        Round self.time value to ROUND_VALUE places after dot.
        :return: float
        """
        return round(self.time, ROUND_VALUE)

    def calculate_time(self):
        """
        Subtraction self.start_time from self.end_time.

        :return: float
        """
        return self.end_time - self.start_time

    @staticmethod
    def set_ranking_place(list_of_objects: list) -> list:
        """
        Set ranking places, like on the passed list.
        Use after sort() staticmethod.

        :param list_of_objects: list
        :return: list
        """
        place = 1
        for obj in list_of_objects:
            obj.ranking_place = place
            place += 1
        return list_of_objects

    @staticmethod
    def sort(list_of_objects: list) -> list:
        """
        Sort passed list with object time.

        :param list_of_objects: list
        :return: list
        """
        list_of_objects.sort(key=lambda obj: obj.time)
        return list_of_objects

    @staticmethod
    def get_sorted_ranking(list_of_objects: list) -> list:
        """
        Combined sort() staticmethod and set_ranking_place() staticmethod.

        :param list_of_objects: list
        :return: list
        """
        list_of_objects = WebsiteMeasurement.sort(list_of_objects)
        list_of_objects = WebsiteMeasurement.set_ranking_place(list_of_objects)
        return list_of_objects
