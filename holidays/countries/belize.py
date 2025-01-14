#  python-holidays
#  ---------------
#  A fast, efficient Python library for generating country, province and state
#  specific sets of holidays on the fly. It aims to make determining whether a
#  specific date is a holiday as fast and flexible as possible.
#
#  Authors: dr-prodigy <dr.prodigy.github@gmail.com> (c) 2017-2023
#           ryanss <ryanssdev@icloud.com> (c) 2014-2017
#  Website: https://github.com/dr-prodigy/python-holidays
#  License: MIT (see LICENSE file)

from datetime import date
from datetime import timedelta as td
from typing import Optional

from holidays.calendars import _get_nth_weekday_from
from holidays.constants import JAN, MAR, MAY, AUG, SEP, OCT, NOV, MON
from holidays.holiday_base import HolidayBase
from holidays.holiday_groups import ChristianHolidays, InternationalHolidays


class Belize(HolidayBase, ChristianHolidays, InternationalHolidays):
    """
    References:
      - https://en.wikipedia.org/wiki/Public_holidays_in_Belize
      - http://www.belizelaw.org/web/lawadmin/PDF%20files/cap289.pdf
      - https://www.pressoffice.gov.bz/public-and-bank-holidays-2022-updated/
      - https://www.pressoffice.gov.bz/government-of-belize-establishes-new-public-and-bank-holidays/  # noqa: E501
    """

    country = "BZ"

    def __init__(self, *args, **kwargs) -> None:
        ChristianHolidays.__init__(self)
        InternationalHolidays.__init__(self)
        super().__init__(*args, **kwargs)

    def _add_movable_holiday(self, *args) -> None:
        # Chapter 289 of the laws of Belize states that if the holiday falls
        # on a Sunday or a Friday, the following Monday is observed as public
        # holiday; further, if the holiday falls on a Tuesday, Wednesday or
        # Thursday, the preceding Monday is observed as public holiday
        name, dt = self._parse_holiday(*args)
        if self.observed:
            if self._is_friday(dt) or self._is_sunday(dt):
                dt = _get_nth_weekday_from(1, MON, dt)
                name = "%s (Observed)" % name
            elif (
                self._is_tuesday(dt)
                or self._is_wednesday(dt)
                or self._is_thursday(dt)
            ):
                dt = _get_nth_weekday_from(-1, MON, dt)
                name = "%s (Observed)" % name
        self._add_holiday(name, dt)

    def _add_holiday(self, *args) -> Optional[date]:
        # Chapter 289 of the laws of Belize states that if the holiday falls
        # on a Sunday, the following Monday is observed as public holiday
        name, dt = self._parse_holiday(*args)
        if (
            self.observed
            and self._is_sunday(dt)
            and dt + td(days=+1) not in self
        ):
            name = "%s (Observed)" % name
            dt += td(days=+1)
        return super()._add_holiday(name, dt)

    def _populate(self, year: int) -> None:
        # Belize was granted independence on 21.09.1981.
        if year <= 1981:
            return None
        super()._populate(year)

        # New Year's Day.
        self._add_new_years_day("New Year's Day")

        if year >= 2021:
            # George Price Day.
            self._add_holiday("George Price Day", JAN, 15)

        # National Heroes and Benefactors Day.
        self._add_movable_holiday(
            "National Heroes and Benefactors Day", MAR, 9
        )

        # Good Friday.
        self._add_good_friday("Good Friday")

        # Holy Saturday.
        self._add_holy_saturday("Holy Saturday")

        # Easter Monday.
        self._add_easter_monday("Easter Monday")

        # Labour Day.
        self._add_labor_day("Labour Day")

        if year <= 2021:
            # Commonwealth Day.
            self._add_movable_holiday("Commonwealth Day", MAY, 24)

        if year >= 2021:
            # Emancipation Day.
            self._add_movable_holiday("Emancipation Day", AUG, 1)

        # Saint George's Caye Day.
        self._add_holiday("Saint George's Caye Day", SEP, 10)

        # Independence Day.
        self._add_holiday("Independence Day", SEP, 21)

        # Indigenous Peoples' Resistance Day / Pan American Day.
        self._add_movable_holiday(
            "Indigenous Peoples' Resistance Day"
            if year >= 2021
            else "Pan American Day",
            date(year, OCT, 12),
        )

        # Garifuna Settlement Day.
        self._add_holiday("Garifuna Settlement Day", NOV, 19)

        # Populated before Christmas for right obvserved Christmas calculation
        # (if Christmas falls on Sunday, there should be no observed Christmas
        # on Monday)
        # Boxing Day.
        self._add_christmas_day_two("Boxing Day")

        # Christmas Day.
        self._add_christmas_day("Christmas Day")


class BZ(Belize):
    pass


class BLZ(Belize):
    pass
