"""
Date-Time Reasoner Tool - Perform date and time calculations and reasoning.
"""

from .base_tool import BaseTool
from datetime import datetime, timedelta
import re


class DateTimeReasonerTool(BaseTool):
    """Perform date and time calculations, comparisons, and reasoning."""
    
    def __init__(self):
        super().__init__()
        self.name = "datetime_reasoner"
        self.description = "Calculate date differences, add/subtract time, find weekdays, parse dates, and perform time zone conversions."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Date/time query or calculation"
                },
                "operation": {
                    "type": "string",
                    "enum": ["parse", "difference", "add", "subtract", "weekday", "info", "compare", "format", "now"],
                    "description": "Operation to perform",
                    "default": "parse"
                },
                "date1": {
                    "type": "string",
                    "description": "First date (YYYY-MM-DD or natural language)"
                },
                "date2": {
                    "type": "string",
                    "description": "Second date for comparison/difference"
                },
                "amount": {
                    "type": "integer",
                    "description": "Amount to add/subtract"
                },
                "unit": {
                    "type": "string",
                    "enum": ["days", "weeks", "months", "years", "hours", "minutes", "seconds"],
                    "description": "Time unit for add/subtract",
                    "default": "days"
                }
            },
            "required": ["query"]
        }
        
        self._weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        self._months = {
            "january": 1, "jan": 1,
            "february": 2, "feb": 2,
            "march": 3, "mar": 3,
            "april": 4, "apr": 4,
            "may": 5,
            "june": 6, "jun": 6,
            "july": 7, "jul": 7,
            "august": 8, "aug": 8,
            "september": 9, "sep": 9, "sept": 9,
            "october": 10, "oct": 10,
            "november": 11, "nov": 11,
            "december": 12, "dec": 12
        }
        
        self._timezones = {
            "utc": 0,
            "gmt": 0,
            "est": -5,
            "edt": -4,
            "cst": -6,
            "cdt": -5,
            "mst": -7,
            "mdt": -6,
            "pst": -8,
            "pdt": -7,
            "ist": 5.5,
            "jst": 9,
            "cet": 1,
            "cest": 2,
            "aest": 10,
            "aedt": 11,
            "bst": 1,
            "hkt": 8,
            "sgt": 8,
            "kst": 9
        }
    
    def execute(self, query, operation="parse", date1=None, date2=None, amount=None, unit="days"):
        try:
            if not query and not date1:
                return "Please provide a date query or date value."
            
            if operation == "now":
                return self._get_current_time()
            elif operation == "parse":
                return self._parse_date(query if query else date1)
            elif operation == "difference":
                return self._calculate_difference(date1, date2)
            elif operation == "add":
                return self._add_time(date1 if date1 else query, amount, unit)
            elif operation == "subtract":
                return self._subtract_time(date1 if date1 else query, amount, unit)
            elif operation == "weekday":
                return self._get_weekday(date1 if date1 else query)
            elif operation == "info":
                return self._get_date_info(date1 if date1 else query)
            elif operation == "compare":
                return self._compare_dates(date1, date2)
            elif operation == "format":
                return self._format_date(date1 if date1 else query)
            else:
                return self._parse_natural_query(query)
                
        except Exception as e:
            return "DateTime error: " + str(e)
    
    def _get_current_time(self):
        now = datetime.now()
        utc_now = datetime.utcnow()
        
        result = "CURRENT DATE AND TIME\n"
        result += "=" * 50 + "\n\n"
        
        result += "Local Time:\n"
        result += "-" * 30 + "\n"
        result += "Date: " + now.strftime("%Y-%m-%d") + "\n"
        result += "Time: " + now.strftime("%H:%M:%S") + "\n"
        result += "Day: " + now.strftime("%A") + "\n"
        result += "Full: " + now.strftime("%A, %B %d, %Y %I:%M:%S %p") + "\n\n"
        
        result += "UTC Time:\n"
        result += "-" * 30 + "\n"
        result += "Date: " + utc_now.strftime("%Y-%m-%d") + "\n"
        result += "Time: " + utc_now.strftime("%H:%M:%S") + "\n"
        result += "ISO: " + utc_now.strftime("%Y-%m-%dT%H:%M:%SZ") + "\n\n"
        
        result += "Timestamps:\n"
        result += "-" * 30 + "\n"
        result += "Unix: " + str(int(now.timestamp())) + "\n"
        result += "Unix (ms): " + str(int(now.timestamp() * 1000)) + "\n\n"
        
        result += "Week Info:\n"
        result += "-" * 30 + "\n"
        result += "Week number: " + str(now.isocalendar()[1]) + "\n"
        result += "Day of year: " + str(now.timetuple().tm_yday) + "\n"
        result += "Quarter: Q" + str((now.month - 1) // 3 + 1) + "\n"
        
        return result
    
    def _parse_date(self, date_str):
        if not date_str:
            return "Please provide a date to parse."
        
        parsed = self._try_parse_date(date_str)
        
        if parsed is None:
            return "Could not parse date: " + date_str + "\n\nSupported formats:\n- YYYY-MM-DD\n- DD/MM/YYYY\n- MM/DD/YYYY\n- Month DD, YYYY\n- today, tomorrow, yesterday"
        
        result = "DATE PARSING\n"
        result += "=" * 50 + "\n\n"
        
        result += "Input: " + date_str + "\n\n"
        
        result += "Parsed Date:\n"
        result += "-" * 30 + "\n"
        result += "Standard: " + parsed.strftime("%Y-%m-%d") + "\n"
        result += "Full: " + parsed.strftime("%A, %B %d, %Y") + "\n"
        result += "US format: " + parsed.strftime("%m/%d/%Y") + "\n"
        result += "EU format: " + parsed.strftime("%d/%m/%Y") + "\n"
        result += "ISO: " + parsed.strftime("%Y-%m-%dT00:00:00") + "\n\n"
        
        result += "Components:\n"
        result += "-" * 30 + "\n"
        result += "Year: " + str(parsed.year) + "\n"
        result += "Month: " + str(parsed.month) + " (" + parsed.strftime("%B") + ")\n"
        result += "Day: " + str(parsed.day) + "\n"
        result += "Weekday: " + parsed.strftime("%A") + "\n"
        result += "Week number: " + str(parsed.isocalendar()[1]) + "\n"
        result += "Day of year: " + str(parsed.timetuple().tm_yday) + "\n"
        
        return result
    
    def _try_parse_date(self, date_str):
        if not date_str:
            return None
        
        date_str = date_str.strip().lower()
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        if date_str == "today":
            return today
        elif date_str == "tomorrow":
            return today + timedelta(days=1)
        elif date_str == "yesterday":
            return today - timedelta(days=1)
        elif date_str == "now":
            return datetime.now()
        
        relative_match = re.match(r"(\d+)\s*(day|week|month|year)s?\s*(ago|from now|later)", date_str)
        if relative_match:
            amount = int(relative_match.group(1))
            unit = relative_match.group(2)
            direction = relative_match.group(3)
            
            if direction == "ago":
                amount = -amount
            
            if unit == "day":
                return today + timedelta(days=amount)
            elif unit == "week":
                return today + timedelta(weeks=amount)
            elif unit == "month":
                new_month = today.month + amount
                new_year = today.year
                while new_month > 12:
                    new_month -= 12
                    new_year += 1
                while new_month < 1:
                    new_month += 12
                    new_year -= 1
                day = min(today.day, 28)
                return today.replace(year=new_year, month=new_month, day=day)
            elif unit == "year":
                return today.replace(year=today.year + amount)
        
        next_match = re.match(r"next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", date_str)
        if next_match:
            target_day = next_match.group(1)
            target_idx = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(target_day)
            current_idx = today.weekday()
            days_ahead = target_idx - current_idx
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
        
        last_match = re.match(r"last\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", date_str)
        if last_match:
            target_day = last_match.group(1)
            target_idx = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(target_day)
            current_idx = today.weekday()
            days_behind = current_idx - target_idx
            if days_behind <= 0:
                days_behind += 7
            return today - timedelta(days=days_behind)
        
        formats = [
            "%Y-%m-%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            "%Y%m%d"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.title(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _calculate_difference(self, date1, date2):
        if not date1 or not date2:
            return "Please provide two dates for difference calculation."
        
        parsed1 = self._try_parse_date(date1)
        parsed2 = self._try_parse_date(date2)
        
        if parsed1 is None:
            return "Could not parse first date: " + date1
        if parsed2 is None:
            return "Could not parse second date: " + date2
        
        diff = parsed2 - parsed1
        days = abs(diff.days)
        
        years = days // 365
        remaining_days = days % 365
        months = remaining_days // 30
        remaining_days = remaining_days % 30
        weeks = days // 7
        
        result = "DATE DIFFERENCE\n"
        result += "=" * 50 + "\n\n"
        
        result += "From: " + parsed1.strftime("%A, %B %d, %Y") + "\n"
        result += "To: " + parsed2.strftime("%A, %B %d, %Y") + "\n\n"
        
        if diff.days >= 0:
            result += "Direction: Forward (future)\n\n"
        else:
            result += "Direction: Backward (past)\n\n"
        
        result += "Difference:\n"
        result += "-" * 30 + "\n"
        result += "Total days: " + str(days) + "\n"
        result += "Total weeks: " + str(weeks) + " weeks and " + str(days % 7) + " days\n"
        result += "Approximate: " + str(years) + " years, " + str(months) + " months, " + str(remaining_days) + " days\n\n"
        
        result += "In other units:\n"
        result += "-" * 30 + "\n"
        result += "Hours: " + str(days * 24) + "\n"
        result += "Minutes: " + str(days * 24 * 60) + "\n"
        result += "Seconds: " + str(days * 24 * 60 * 60) + "\n"
        
        return result
    
    def _add_time(self, date_str, amount, unit):
        if not date_str:
            return "Please provide a date."
        if amount is None:
            return "Please provide an amount to add."
        
        parsed = self._try_parse_date(date_str)
        if parsed is None:
            return "Could not parse date: " + date_str
        
        if unit == "days":
            new_date = parsed + timedelta(days=amount)
        elif unit == "weeks":
            new_date = parsed + timedelta(weeks=amount)
        elif unit == "months":
            new_month = parsed.month + amount
            new_year = parsed.year
            while new_month > 12:
                new_month -= 12
                new_year += 1
            while new_month < 1:
                new_month += 12
                new_year -= 1
            day = min(parsed.day, 28)
            new_date = parsed.replace(year=new_year, month=new_month, day=day)
        elif unit == "years":
            new_date = parsed.replace(year=parsed.year + amount)
        elif unit == "hours":
            new_date = parsed + timedelta(hours=amount)
        elif unit == "minutes":
            new_date = parsed + timedelta(minutes=amount)
        elif unit == "seconds":
            new_date = parsed + timedelta(seconds=amount)
        else:
            return "Unknown unit: " + unit
        
        result = "DATE ADDITION\n"
        result += "=" * 50 + "\n\n"
        
        result += "Original: " + parsed.strftime("%A, %B %d, %Y") + "\n"
        result += "Added: " + str(amount) + " " + unit + "\n"
        result += "Result: " + new_date.strftime("%A, %B %d, %Y") + "\n\n"
        
        if unit in ["hours", "minutes", "seconds"]:
            result += "Time: " + new_date.strftime("%H:%M:%S") + "\n"
        
        return result
    
    def _subtract_time(self, date_str, amount, unit):
        if amount is None:
            return "Please provide an amount to subtract."
        return self._add_time(date_str, -amount, unit)
    
    def _get_weekday(self, date_str):
        if not date_str:
            return "Please provide a date."
        
        parsed = self._try_parse_date(date_str)
        if parsed is None:
            return "Could not parse date: " + date_str
        
        weekday = parsed.strftime("%A")
        weekday_num = parsed.weekday()
        
        is_weekend = weekday_num >= 5
        
        result = "WEEKDAY INFO\n"
        result += "=" * 50 + "\n\n"
        
        result += "Date: " + parsed.strftime("%B %d, %Y") + "\n"
        result += "Weekday: " + weekday + "\n"
        result += "Day number: " + str(weekday_num + 1) + " of 7\n"
        result += "Type: " + ("Weekend" if is_weekend else "Weekday") + "\n\n"
        
        result += "Days until:\n"
        result += "-" * 30 + "\n"
        
        for i, day in enumerate(self._weekdays):
            days_until = (i - weekday_num) % 7
            if days_until == 0:
                result += day + ": Today\n"
            else:
                result += day + ": " + str(days_until) + " days\n"
        
        return result
    
    def _get_date_info(self, date_str):
        if not date_str:
            return "Please provide a date."
        
        parsed = self._try_parse_date(date_str)
        if parsed is None:
            return "Could not parse date: " + date_str
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        diff = (parsed - today).days
        
        day_of_year = parsed.timetuple().tm_yday
        week_number = parsed.isocalendar()[1]
        quarter = (parsed.month - 1) // 3 + 1
        
        is_leap = (parsed.year % 4 == 0 and parsed.year % 100 != 0) or (parsed.year % 400 == 0)
        days_in_year = 366 if is_leap else 365
        
        result = "DATE INFORMATION\n"
        result += "=" * 50 + "\n\n"
        
        result += "Date: " + parsed.strftime("%A, %B %d, %Y") + "\n\n"
        
        result += "Calendar Info:\n"
        result += "-" * 30 + "\n"
        result += "Year: " + str(parsed.year) + "\n"
        result += "Month: " + parsed.strftime("%B") + " (" + str(parsed.month) + "/12)\n"
        result += "Day: " + str(parsed.day) + "\n"
        result += "Weekday: " + parsed.strftime("%A") + "\n"
        result += "Week number: " + str(week_number) + " of 52\n"
        result += "Day of year: " + str(day_of_year) + " of " + str(days_in_year) + "\n"
        result += "Quarter: Q" + str(quarter) + "\n"
        result += "Leap year: " + ("Yes" if is_leap else "No") + "\n\n"
        
        result += "Relative to Today:\n"
        result += "-" * 30 + "\n"
        
        if diff == 0:
            result += "This is today\n"
        elif diff == 1:
            result += "Tomorrow\n"
        elif diff == -1:
            result += "Yesterday\n"
        elif diff > 0:
            result += str(diff) + " days from now\n"
        else:
            result += str(abs(diff)) + " days ago\n"
        
        return result
    
    def _compare_dates(self, date1, date2):
        if not date1 or not date2:
            return "Please provide two dates to compare."
        
        parsed1 = self._try_parse_date(date1)
        parsed2 = self._try_parse_date(date2)
        
        if parsed1 is None:
            return "Could not parse first date: " + date1
        if parsed2 is None:
            return "Could not parse second date: " + date2
        
        result = "DATE COMPARISON\n"
        result += "=" * 50 + "\n\n"
        
        result += "Date 1: " + parsed1.strftime("%A, %B %d, %Y") + "\n"
        result += "Date 2: " + parsed2.strftime("%A, %B %d, %Y") + "\n\n"
        
        result += "Comparison:\n"
        result += "-" * 30 + "\n"
        
        if parsed1 < parsed2:
            result += "Date 1 is BEFORE Date 2\n"
            result += "Date 1 is " + str((parsed2 - parsed1).days) + " days earlier\n"
        elif parsed1 > parsed2:
            result += "Date 1 is AFTER Date 2\n"
            result += "Date 1 is " + str((parsed1 - parsed2).days) + " days later\n"
        else:
            result += "Dates are EQUAL\n"
        
        result += "\n"
        result += "Same year: " + ("Yes" if parsed1.year == parsed2.year else "No") + "\n"
        result += "Same month: " + ("Yes" if parsed1.month == parsed2.month else "No") + "\n"
        result += "Same weekday: " + ("Yes" if parsed1.weekday() == parsed2.weekday() else "No") + "\n"
        
        return result
    
    def _format_date(self, date_str):
        if not date_str:
            return "Please provide a date."
        
        parsed = self._try_parse_date(date_str)
        if parsed is None:
            return "Could not parse date: " + date_str
        
        result = "DATE FORMATS\n"
        result += "=" * 50 + "\n\n"
        
        result += "Input: " + date_str + "\n\n"
        
        result += "Standard Formats:\n"
        result += "-" * 30 + "\n"
        result += "ISO 8601: " + parsed.strftime("%Y-%m-%d") + "\n"
        result += "ISO DateTime: " + parsed.strftime("%Y-%m-%dT%H:%M:%S") + "\n"
        result += "US: " + parsed.strftime("%m/%d/%Y") + "\n"
        result += "EU: " + parsed.strftime("%d/%m/%Y") + "\n"
        result += "Long: " + parsed.strftime("%B %d, %Y") + "\n"
        result += "Full: " + parsed.strftime("%A, %B %d, %Y") + "\n"
        result += "Short: " + parsed.strftime("%b %d, %Y") + "\n"
        result += "Compact: " + parsed.strftime("%Y%m%d") + "\n\n"
        
        result += "Technical:\n"
        result += "-" * 30 + "\n"
        result += "Unix timestamp: " + str(int(parsed.timestamp())) + "\n"
        result += "RFC 2822: " + parsed.strftime("%a, %d %b %Y %H:%M:%S") + "\n"
        
        return result
    
    def _parse_natural_query(self, query):
        query_lower = query.lower()
        
        if "today" in query_lower or "now" in query_lower or "current" in query_lower:
            return self._get_current_time()
        
        if "difference" in query_lower or "between" in query_lower or "until" in query_lower:
            dates = re.findall(r"\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}", query)
            if len(dates) >= 2:
                return self._calculate_difference(dates[0], dates[1])
        
        if "weekday" in query_lower or "day of week" in query_lower:
            date_match = re.search(r"\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}", query)
            if date_match:
                return self._get_weekday(date_match.group())
        
        return self._parse_date(query)