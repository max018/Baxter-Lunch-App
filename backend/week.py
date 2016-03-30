import datetime
import functools

@functools.total_ordering
class Week:
    @classmethod
    def from_offset(cls, offset):
        this_week = cls(datetime.date.today())
        return this_week + offset

    def __init__(self, date):
        delta = datetime.timedelta(days=date.weekday())
        self._first_day = date - delta

    def day(self, n):
        assert 0 <= n < 5, 'nonexistent day of the week'
        delta = datetime.timedelta(days=n)
        return self._first_day + delta

    def days(self):
        return [self.day(n) for n in range(5)]

    def __add__(self, weeks):
        delta = datetime.timedelta(weeks=weeks)
        new_date = self._first_day + delta
        return Week(new_date)

    def __sub__(self, weeks):
        return self + (-weeks)

    def __eq__(self, other):
        return self._first_day == other._first_day

    def __le__(self, other):
        return self._first_day <= other._first_day

