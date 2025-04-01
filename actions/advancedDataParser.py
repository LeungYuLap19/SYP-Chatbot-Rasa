from datetime import datetime, timedelta
import re
from typing import Optional, Tuple

class AdvancedDateParser:
    MONTHS = {
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2,
        'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
        'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
        'aug': 8, 'august': 8, 'sep': 9, 'september': 9,
        'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
        'dec': 12, 'december': 12
    }

    HOLIDAYS = {
        'new year\'s eve': (12, 31),
        'new years eve': (12, 31),
        'christmas': (12, 25),
        'christmas day': (12, 25),
        'valentine\'s day': (2, 14),
        'valentines day': (2, 14)
        # Add more holidays as needed
    }

    @staticmethod
    def parse_date(date_str: str, reference_date: datetime = None) -> Optional[Tuple[datetime, str]]:
        """Parse dates with flexible formats into (datetime, dd-mm-yyyy)"""
        if not date_str:
            return None

        if not reference_date:
            reference_date = datetime.now()

        date_str = date_str.lower().strip()
        
        # 1. Standard date formats (dd-mm-yyyy, yyyy-mm-dd, etc.)
        std_match = re.match(
            r'^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$', 
            date_str
        )
        if not std_match:
            std_match = re.match(
                r'^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$', 
                date_str
            )
            if std_match:
                year, month, day = map(int, std_match.groups())
                try:
                    dt = datetime(year, month, day)
                    return dt, dt.strftime("%Y-%m-%d")
                except ValueError:
                    pass

        if std_match:
            day, month, year = map(int, std_match.groups())
            try:
                dt = datetime(year, month, day)
                return dt, dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

        # 2. Month name patterns (15 March 2023)
        month_match = re.match(
            r'^(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+(\d{4})$', 
            date_str
        )
        if month_match:
            day, month, year = month_match.groups()
            month_num = AdvancedDateParser.MONTHS.get(month[:3])
            if month_num:
                try:
                    dt = datetime(int(year), month_num, int(day))
                    return dt, dt.strftime("%Y-%m-%d")
                except ValueError:
                    pass

        # 3. Natural language dates
        natural_result = AdvancedDateParser._parse_natural_date(date_str, reference_date)
        if natural_result:
            return natural_result

        # 4. Holidays
        holiday_result = AdvancedDateParser._parse_holiday(date_str, reference_date)
        if holiday_result:
            return holiday_result

        return None

    @staticmethod
    def _parse_natural_date(date_str: str, ref_date: datetime) -> Optional[Tuple[datetime, str]]:
        """Handle relative natural language dates"""
        if date_str == "today":
            return ref_date, ref_date.strftime("%Y-%m-%d")
        elif date_str == "tomorrow":
            dt = ref_date + timedelta(days=1)
            return dt, dt.strftime("%Y-%m-%d")
        elif date_str == "the day after tomorrow":
            dt = ref_date + timedelta(days=2)
            return dt, dt.strftime("%Y-%m-%d")
        elif date_str.startswith("next "):
            weekday = date_str[5:]
            dt = AdvancedDateParser._get_next_weekday(weekday, ref_date)
            if dt:
                return dt, dt.strftime("%Y-%m-%d")
        elif re.match(r'^\d+\s+days?\s+(later|after)$', date_str):
            days = int(re.search(r'\d+', date_str).group())
            dt = ref_date + timedelta(days=days)
            return dt, dt.strftime("%Y-%m-%d")
        return None

    @staticmethod
    def _parse_holiday(date_str: str, ref_date: datetime) -> Optional[Tuple[datetime, str]]:
        """Handle holiday names"""
        holiday = AdvancedDateParser.HOLIDAYS.get(date_str)
        if holiday:
            month, day = holiday
            year = ref_date.year
            # If holiday already passed this year, use next year
            if (month, day) < (ref_date.month, ref_date.day):
                year += 1
            try:
                dt = datetime(year, month, day)
                return dt, dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
        return None

    @staticmethod
    def _get_next_weekday(weekday: str, ref_date: datetime) -> Optional[datetime]:
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday',
                   'friday', 'saturday', 'sunday']
        try:
            target_idx = weekdays.index(weekday.lower())
            current_idx = ref_date.weekday()
            days_ahead = (target_idx - current_idx) % 7
            if days_ahead == 0:  # Today is the weekday
                days_ahead = 7
            return ref_date + timedelta(days=days_ahead)
        except ValueError:
            return None