"""
Unit and Currency Converter Tool - Convert between units and currencies.
"""

from .base_tool import BaseTool


class UnitCurrencyConverterTool(BaseTool):
    """Convert between units of measurement and currencies."""
    
    def __init__(self):
        super().__init__()
        self.name = "unit_currency_converter"
        self.description = "Convert between units (length, weight, temperature, volume, area, time, data) and currencies."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "value": {
                    "type": "number",
                    "description": "Value to convert"
                },
                "from_unit": {
                    "type": "string",
                    "description": "Source unit or currency code"
                },
                "to_unit": {
                    "type": "string",
                    "description": "Target unit or currency code"
                },
                "category": {
                    "type": "string",
                    "enum": ["auto", "length", "weight", "temperature", "volume", "area", "time", "data", "currency"],
                    "description": "Conversion category",
                    "default": "auto"
                }
            },
            "required": ["value", "from_unit", "to_unit"]
        }
        
        self._length = {
            "m": 1.0,
            "meter": 1.0,
            "meters": 1.0,
            "km": 1000.0,
            "kilometer": 1000.0,
            "kilometers": 1000.0,
            "cm": 0.01,
            "centimeter": 0.01,
            "centimeters": 0.01,
            "mm": 0.001,
            "millimeter": 0.001,
            "millimeters": 0.001,
            "mi": 1609.344,
            "mile": 1609.344,
            "miles": 1609.344,
            "yd": 0.9144,
            "yard": 0.9144,
            "yards": 0.9144,
            "ft": 0.3048,
            "foot": 0.3048,
            "feet": 0.3048,
            "in": 0.0254,
            "inch": 0.0254,
            "inches": 0.0254,
            "nm": 1852.0,
            "nautical mile": 1852.0,
            "nautical miles": 1852.0
        }
        
        self._weight = {
            "kg": 1.0,
            "kilogram": 1.0,
            "kilograms": 1.0,
            "g": 0.001,
            "gram": 0.001,
            "grams": 0.001,
            "mg": 0.000001,
            "milligram": 0.000001,
            "milligrams": 0.000001,
            "lb": 0.453592,
            "lbs": 0.453592,
            "pound": 0.453592,
            "pounds": 0.453592,
            "oz": 0.0283495,
            "ounce": 0.0283495,
            "ounces": 0.0283495,
            "ton": 1000.0,
            "tons": 1000.0,
            "tonne": 1000.0,
            "tonnes": 1000.0,
            "st": 6.35029,
            "stone": 6.35029,
            "stones": 6.35029
        }
        
        self._volume = {
            "l": 1.0,
            "liter": 1.0,
            "liters": 1.0,
            "litre": 1.0,
            "litres": 1.0,
            "ml": 0.001,
            "milliliter": 0.001,
            "milliliters": 0.001,
            "gal": 3.78541,
            "gallon": 3.78541,
            "gallons": 3.78541,
            "qt": 0.946353,
            "quart": 0.946353,
            "quarts": 0.946353,
            "pt": 0.473176,
            "pint": 0.473176,
            "pints": 0.473176,
            "cup": 0.236588,
            "cups": 0.236588,
            "floz": 0.0295735,
            "fl oz": 0.0295735,
            "fluid ounce": 0.0295735,
            "tbsp": 0.0147868,
            "tablespoon": 0.0147868,
            "tablespoons": 0.0147868,
            "tsp": 0.00492892,
            "teaspoon": 0.00492892,
            "teaspoons": 0.00492892,
            "m3": 1000.0,
            "cubic meter": 1000.0,
            "cubic meters": 1000.0
        }
        
        self._area = {
            "m2": 1.0,
            "sqm": 1.0,
            "square meter": 1.0,
            "square meters": 1.0,
            "km2": 1000000.0,
            "sqkm": 1000000.0,
            "square kilometer": 1000000.0,
            "square kilometers": 1000000.0,
            "cm2": 0.0001,
            "sqcm": 0.0001,
            "square centimeter": 0.0001,
            "ft2": 0.092903,
            "sqft": 0.092903,
            "square foot": 0.092903,
            "square feet": 0.092903,
            "in2": 0.00064516,
            "sqin": 0.00064516,
            "square inch": 0.00064516,
            "square inches": 0.00064516,
            "mi2": 2589988.0,
            "sqmi": 2589988.0,
            "square mile": 2589988.0,
            "square miles": 2589988.0,
            "acre": 4046.86,
            "acres": 4046.86,
            "hectare": 10000.0,
            "hectares": 10000.0,
            "ha": 10000.0
        }
        
        self._time = {
            "s": 1.0,
            "sec": 1.0,
            "second": 1.0,
            "seconds": 1.0,
            "ms": 0.001,
            "millisecond": 0.001,
            "milliseconds": 0.001,
            "min": 60.0,
            "minute": 60.0,
            "minutes": 60.0,
            "h": 3600.0,
            "hr": 3600.0,
            "hour": 3600.0,
            "hours": 3600.0,
            "d": 86400.0,
            "day": 86400.0,
            "days": 86400.0,
            "wk": 604800.0,
            "week": 604800.0,
            "weeks": 604800.0,
            "mo": 2592000.0,
            "month": 2592000.0,
            "months": 2592000.0,
            "yr": 31536000.0,
            "year": 31536000.0,
            "years": 31536000.0
        }
        
        self._data = {
            "b": 1.0,
            "bit": 1.0,
            "bits": 1.0,
            "B": 8.0,
            "byte": 8.0,
            "bytes": 8.0,
            "kb": 8000.0,
            "kilobyte": 8000.0,
            "kilobytes": 8000.0,
            "kib": 8192.0,
            "kibibyte": 8192.0,
            "mb": 8000000.0,
            "megabyte": 8000000.0,
            "megabytes": 8000000.0,
            "mib": 8388608.0,
            "mebibyte": 8388608.0,
            "gb": 8000000000.0,
            "gigabyte": 8000000000.0,
            "gigabytes": 8000000000.0,
            "gib": 8589934592.0,
            "gibibyte": 8589934592.0,
            "tb": 8000000000000.0,
            "terabyte": 8000000000000.0,
            "terabytes": 8000000000000.0,
            "tib": 8796093022208.0,
            "tebibyte": 8796093022208.0,
            "pb": 8000000000000000.0,
            "petabyte": 8000000000000000.0,
            "petabytes": 8000000000000000.0
        }
        
        self._currencies = {
            "usd": "US Dollar",
            "eur": "Euro",
            "gbp": "British Pound",
            "jpy": "Japanese Yen",
            "cny": "Chinese Yuan",
            "inr": "Indian Rupee",
            "aud": "Australian Dollar",
            "cad": "Canadian Dollar",
            "chf": "Swiss Franc",
            "hkd": "Hong Kong Dollar",
            "sgd": "Singapore Dollar",
            "krw": "South Korean Won",
            "mxn": "Mexican Peso",
            "brl": "Brazilian Real",
            "rub": "Russian Ruble",
            "zar": "South African Rand",
            "aed": "UAE Dirham",
            "sar": "Saudi Riyal",
            "nzd": "New Zealand Dollar",
            "thb": "Thai Baht",
            "myr": "Malaysian Ringgit",
            "php": "Philippine Peso",
            "idr": "Indonesian Rupiah",
            "vnd": "Vietnamese Dong",
            "pln": "Polish Zloty",
            "sek": "Swedish Krona",
            "nok": "Norwegian Krone",
            "dkk": "Danish Krone",
            "try": "Turkish Lira",
            "egp": "Egyptian Pound"
        }
    
    def execute(self, value, from_unit, to_unit, category="auto"):
        try:
            if value is None:
                return "Please provide a value to convert."
            
            if not from_unit or not to_unit:
                return "Please provide source and target units."
            
            from_unit = from_unit.lower().strip()
            to_unit = to_unit.lower().strip()
            
            if category == "auto":
                category = self._detect_category(from_unit, to_unit)
            
            if category == "temperature":
                return self._convert_temperature(value, from_unit, to_unit)
            elif category == "currency":
                return self._convert_currency(value, from_unit, to_unit)
            elif category == "length":
                return self._convert_unit(value, from_unit, to_unit, self._length, "Length")
            elif category == "weight":
                return self._convert_unit(value, from_unit, to_unit, self._weight, "Weight")
            elif category == "volume":
                return self._convert_unit(value, from_unit, to_unit, self._volume, "Volume")
            elif category == "area":
                return self._convert_unit(value, from_unit, to_unit, self._area, "Area")
            elif category == "time":
                return self._convert_unit(value, from_unit, to_unit, self._time, "Time")
            elif category == "data":
                return self._convert_unit(value, from_unit, to_unit, self._data, "Data")
            else:
                return "Unknown category: " + category
                
        except Exception as e:
            return "Conversion error: " + str(e)
    
    def _detect_category(self, from_unit, to_unit):
        temp_units = ["c", "f", "k", "celsius", "fahrenheit", "kelvin"]
        if from_unit in temp_units or to_unit in temp_units:
            return "temperature"
        
        if from_unit in self._currencies or to_unit in self._currencies:
            return "currency"
        
        if from_unit in self._length or to_unit in self._length:
            return "length"
        
        if from_unit in self._weight or to_unit in self._weight:
            return "weight"
        
        if from_unit in self._volume or to_unit in self._volume:
            return "volume"
        
        if from_unit in self._area or to_unit in self._area:
            return "area"
        
        if from_unit in self._time or to_unit in self._time:
            return "time"
        
        if from_unit in self._data or to_unit in self._data:
            return "data"
        
        return "unknown"
    
    def _convert_unit(self, value, from_unit, to_unit, units_dict, category_name):
        if from_unit not in units_dict:
            available = ", ".join(list(units_dict.keys())[:10])
            return "Unknown " + category_name.lower() + " unit: " + from_unit + "\nAvailable: " + available + "..."
        
        if to_unit not in units_dict:
            available = ", ".join(list(units_dict.keys())[:10])
            return "Unknown " + category_name.lower() + " unit: " + to_unit + "\nAvailable: " + available + "..."
        
        base_value = value * units_dict[from_unit]
        result = base_value / units_dict[to_unit]
        
        output = "UNIT CONVERSION\n"
        output += "=" * 50 + "\n\n"
        output += "Category: " + category_name + "\n\n"
        output += str(value) + " " + from_unit + " = " + str(round(result, 6)) + " " + to_unit + "\n\n"
        
        output += "Conversion factor:\n"
        output += "1 " + from_unit + " = " + str(round(units_dict[from_unit] / units_dict[to_unit], 6)) + " " + to_unit + "\n"
        
        return output
    
    def _convert_temperature(self, value, from_unit, to_unit):
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()
        
        if from_unit in ["c", "celsius"]:
            celsius = value
        elif from_unit in ["f", "fahrenheit"]:
            celsius = (value - 32) * 5 / 9
        elif from_unit in ["k", "kelvin"]:
            celsius = value - 273.15
        else:
            return "Unknown temperature unit: " + from_unit + ". Use c, f, or k."
        
        if to_unit in ["c", "celsius"]:
            result = celsius
            to_name = "Celsius"
        elif to_unit in ["f", "fahrenheit"]:
            result = celsius * 9 / 5 + 32
            to_name = "Fahrenheit"
        elif to_unit in ["k", "kelvin"]:
            result = celsius + 273.15
            to_name = "Kelvin"
        else:
            return "Unknown temperature unit: " + to_unit + ". Use c, f, or k."
        
        from_names = {
            "c": "Celsius",
            "celsius": "Celsius",
            "f": "Fahrenheit",
            "fahrenheit": "Fahrenheit",
            "k": "Kelvin",
            "kelvin": "Kelvin"
        }
        from_name = from_names.get(from_unit, from_unit)
        
        output = "TEMPERATURE CONVERSION\n"
        output += "=" * 50 + "\n\n"
        output += str(value) + " " + from_name + " = " + str(round(result, 2)) + " " + to_name + "\n\n"
        
        output += "All conversions from " + str(value) + " " + from_name + ":\n"
        output += "-" * 30 + "\n"
        output += "Celsius: " + str(round(celsius, 2)) + " C\n"
        output += "Fahrenheit: " + str(round(celsius * 9 / 5 + 32, 2)) + " F\n"
        output += "Kelvin: " + str(round(celsius + 273.15, 2)) + " K\n"
        
        return output
    
    def _convert_currency(self, value, from_currency, to_currency):
        from_currency = from_currency.lower()
        to_currency = to_currency.lower()
        
        if from_currency not in self._currencies:
            return "Unknown currency: " + from_currency
        
        if to_currency not in self._currencies:
            return "Unknown currency: " + to_currency
        
        try:
            import requests
            
            url = "https://api.exchangerate-api.com/v4/latest/" + from_currency.upper()
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get("rates", {})
                
                to_key = to_currency.upper()
                if to_key in rates:
                    rate = rates[to_key]
                    result = value * rate
                    
                    output = "CURRENCY CONVERSION\n"
                    output += "=" * 50 + "\n\n"
                    output += str(value) + " " + from_currency.upper()
                    output += " (" + self._currencies[from_currency] + ")\n"
                    output += "= " + str(round(result, 2)) + " " + to_currency.upper()
                    output += " (" + self._currencies[to_currency] + ")\n\n"
                    output += "Exchange rate: 1 " + from_currency.upper() + " = " + str(round(rate, 4)) + " " + to_currency.upper() + "\n"
                    output += "Rate date: " + data.get("date", "N/A") + "\n"
                    
                    return output
        except Exception:
            pass
        
        output = "CURRENCY CONVERSION\n"
        output += "=" * 50 + "\n\n"
        output += "From: " + str(value) + " " + from_currency.upper()
        output += " (" + self._currencies[from_currency] + ")\n"
        output += "To: " + to_currency.upper()
        output += " (" + self._currencies[to_currency] + ")\n\n"
        output += "Note: Live exchange rates unavailable.\n"
        output += "Please check online for current rates:\n"
        output += "- xe.com\n"
        output += "- google.com/finance\n"
        output += "- exchangerate-api.com\n"
        
        return output