"""
Log Analyzer Tool - Analyze log files and extract insights.
"""

from .base_tool import BaseTool
import re


class LogAnalyzerTool(BaseTool):
    """Analyze log files to extract patterns, errors, and statistics."""
    
    def __init__(self):
        super().__init__()
        self.name = "log_analyzer"
        self.description = "Analyze log files to find errors, patterns, statistics, and anomalies. Supports common log formats."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "log_data": {
                    "type": "string",
                    "description": "Log content as string"
                },
                "operation": {
                    "type": "string",
                    "enum": ["summary", "errors", "patterns", "timeline", "search", "stats"],
                    "description": "Operation to perform",
                    "default": "summary"
                },
                "search_term": {
                    "type": "string",
                    "description": "Term to search for"
                },
                "log_format": {
                    "type": "string",
                    "enum": ["auto", "apache", "nginx", "syslog", "json", "custom"],
                    "description": "Log format",
                    "default": "auto"
                }
            },
            "required": ["log_data"]
        }
        
        self._log_levels = {
            "fatal": 5,
            "critical": 5,
            "error": 4,
            "err": 4,
            "warning": 3,
            "warn": 3,
            "info": 2,
            "debug": 1,
            "trace": 0
        }
        
        self._error_patterns = [
            r"error",
            r"exception",
            r"failed",
            r"failure",
            r"fatal",
            r"critical",
            r"crash",
            r"abort",
            r"denied",
            r"refused",
            r"timeout",
            r"unauthorized",
            r"forbidden",
            r"not found",
            r"500",
            r"502",
            r"503",
            r"504"
        ]
        
        self._timestamp_patterns = [
            r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}",
            r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}",
            r"\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}",
            r"\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2}:\d{2}",
            r"\d{10,13}"
        ]
    
    def execute(self, log_data, operation="summary", search_term=None, log_format="auto"):
        try:
            if not log_data or not log_data.strip():
                return "Please provide log data to analyze."
            
            lines = log_data.strip().split("\n")
            
            if len(lines) == 0:
                return "No log lines found."
            
            if log_format == "auto":
                log_format = self._detect_format(lines)
            
            if operation == "summary":
                return self._get_summary(lines, log_format)
            elif operation == "errors":
                return self._get_errors(lines)
            elif operation == "patterns":
                return self._get_patterns(lines)
            elif operation == "timeline":
                return self._get_timeline(lines)
            elif operation == "search":
                return self._search_logs(lines, search_term)
            elif operation == "stats":
                return self._get_stats(lines)
            else:
                return self._get_summary(lines, log_format)
                
        except Exception as e:
            return "Log analysis error: " + str(e)
    
    def _detect_format(self, lines):
        sample = "\n".join(lines[:10])
        
        if '{"' in sample or "'{" in sample:
            return "json"
        
        if re.search(r'\d+\.\d+\.\d+\.\d+.*"(GET|POST|PUT|DELETE)', sample):
            if "nginx" in sample.lower():
                return "nginx"
            return "apache"
        
        if re.search(r"^\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}", sample):
            return "syslog"
        
        return "custom"
    
    def _get_summary(self, lines, log_format):
        total_lines = len(lines)
        
        error_count = 0
        warning_count = 0
        info_count = 0
        
        for line in lines:
            line_lower = line.lower()
            
            if any(re.search(p, line_lower) for p in self._error_patterns[:8]):
                error_count += 1
            elif "warn" in line_lower:
                warning_count += 1
            elif "info" in line_lower:
                info_count += 1
        
        timestamps = []
        for line in lines[:100]:
            for pattern in self._timestamp_patterns:
                match = re.search(pattern, line)
                if match:
                    timestamps.append(match.group())
                    break
        
        unique_ips = set()
        for line in lines:
            ip_match = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line)
            for ip in ip_match:
                unique_ips.add(ip)
        
        result = "LOG ANALYSIS SUMMARY\n"
        result += "=" * 50 + "\n\n"
        
        result += "OVERVIEW\n"
        result += "-" * 30 + "\n"
        result += "Total lines: " + str(total_lines) + "\n"
        result += "Detected format: " + log_format + "\n"
        result += "Unique IPs: " + str(len(unique_ips)) + "\n\n"
        
        result += "LOG LEVELS\n"
        result += "-" * 30 + "\n"
        result += "Errors: " + str(error_count)
        if total_lines > 0:
            result += " (" + str(round(error_count / total_lines * 100, 1)) + "%)"
        result += "\n"
        
        result += "Warnings: " + str(warning_count)
        if total_lines > 0:
            result += " (" + str(round(warning_count / total_lines * 100, 1)) + "%)"
        result += "\n"
        
        result += "Info: " + str(info_count)
        if total_lines > 0:
            result += " (" + str(round(info_count / total_lines * 100, 1)) + "%)"
        result += "\n\n"
        
        if timestamps:
            result += "TIME RANGE\n"
            result += "-" * 30 + "\n"
            result += "First: " + timestamps[0] + "\n"
            result += "Last: " + timestamps[-1] + "\n\n"
        
        result += "HEALTH STATUS\n"
        result += "-" * 30 + "\n"
        
        if error_count == 0:
            result += "Status: HEALTHY\n"
            result += "No errors detected.\n"
        elif error_count < total_lines * 0.01:
            result += "Status: GOOD\n"
            result += "Very few errors detected.\n"
        elif error_count < total_lines * 0.05:
            result += "Status: WARNING\n"
            result += "Some errors detected. Review recommended.\n"
        else:
            result += "Status: CRITICAL\n"
            result += "High error rate detected. Immediate attention needed.\n"
        
        return result
    
    def _get_errors(self, lines):
        errors = []
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            for pattern in self._error_patterns:
                if re.search(pattern, line_lower):
                    errors.append({
                        "line_num": i + 1,
                        "content": line,
                        "pattern": pattern
                    })
                    break
        
        result = "ERROR ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        
        result += "Total errors found: " + str(len(errors)) + "\n\n"
        
        if not errors:
            result += "No errors detected in the log.\n"
            return result
        
        error_types = {}
        for error in errors:
            pattern = error["pattern"]
            error_types[pattern] = error_types.get(pattern, 0) + 1
        
        result += "ERROR TYPES\n"
        result += "-" * 30 + "\n"
        
        sorted_types = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
        for pattern, count in sorted_types:
            result += pattern + ": " + str(count) + "\n"
        
        result += "\n"
        result += "ERROR DETAILS (first 20)\n"
        result += "-" * 30 + "\n"
        
        for error in errors[:20]:
            line_content = error["content"]
            if len(line_content) > 100:
                line_content = line_content[:100] + "..."
            
            result += "Line " + str(error["line_num"]) + ": " + line_content + "\n"
        
        if len(errors) > 20:
            result += "\n... and " + str(len(errors) - 20) + " more errors\n"
        
        return result
    
    def _get_patterns(self, lines):
        ip_addresses = {}
        urls = {}
        http_methods = {}
        status_codes = {}
        user_agents = {}
        
        for line in lines:
            ip_matches = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", line)
            for ip in ip_matches:
                ip_addresses[ip] = ip_addresses.get(ip, 0) + 1
            
            url_matches = re.findall(r'"(?:GET|POST|PUT|DELETE|PATCH)\s+([^\s"]+)', line)
            for url in url_matches:
                path = url.split("?")[0]
                urls[path] = urls.get(path, 0) + 1
            
            method_matches = re.findall(r'"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)', line)
            for method in method_matches:
                http_methods[method] = http_methods.get(method, 0) + 1
            
            status_matches = re.findall(r'"\s+(\d{3})\s+', line)
            for status in status_matches:
                status_codes[status] = status_codes.get(status, 0) + 1
        
        result = "PATTERN ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        
        result += "TOP IP ADDRESSES\n"
        result += "-" * 30 + "\n"
        
        if ip_addresses:
            sorted_ips = sorted(ip_addresses.items(), key=lambda x: x[1], reverse=True)
            for ip, count in sorted_ips[:10]:
                result += ip.ljust(20) + ": " + str(count) + " requests\n"
        else:
            result += "No IP addresses found.\n"
        
        result += "\n"
        result += "HTTP METHODS\n"
        result += "-" * 30 + "\n"
        
        if http_methods:
            sorted_methods = sorted(http_methods.items(), key=lambda x: x[1], reverse=True)
            for method, count in sorted_methods:
                result += method.ljust(10) + ": " + str(count) + "\n"
        else:
            result += "No HTTP methods found.\n"
        
        result += "\n"
        result += "STATUS CODES\n"
        result += "-" * 30 + "\n"
        
        if status_codes:
            sorted_codes = sorted(status_codes.items(), key=lambda x: x[1], reverse=True)
            for code, count in sorted_codes:
                status_text = self._get_status_text(code)
                result += code + " " + status_text.ljust(20) + ": " + str(count) + "\n"
        else:
            result += "No status codes found.\n"
        
        result += "\n"
        result += "TOP URLS\n"
        result += "-" * 30 + "\n"
        
        if urls:
            sorted_urls = sorted(urls.items(), key=lambda x: x[1], reverse=True)
            for url, count in sorted_urls[:10]:
                if len(url) > 40:
                    url = url[:40] + "..."
                result += url.ljust(45) + ": " + str(count) + "\n"
        else:
            result += "No URLs found.\n"
        
        return result
    
    def _get_status_text(self, code):
        status_texts = {
            "200": "OK",
            "201": "Created",
            "204": "No Content",
            "301": "Moved",
            "302": "Found",
            "304": "Not Modified",
            "400": "Bad Request",
            "401": "Unauthorized",
            "403": "Forbidden",
            "404": "Not Found",
            "405": "Method Not Allowed",
            "500": "Server Error",
            "502": "Bad Gateway",
            "503": "Unavailable",
            "504": "Timeout"
        }
        return status_texts.get(code, "")
    
    def _get_timeline(self, lines):
        hourly_counts = {}
        hourly_errors = {}
        
        for line in lines:
            hour = None
            
            match = re.search(r"(\d{2}):\d{2}:\d{2}", line)
            if match:
                hour = match.group(1)
            
            if hour:
                hourly_counts[hour] = hourly_counts.get(hour, 0) + 1
                
                line_lower = line.lower()
                if any(re.search(p, line_lower) for p in self._error_patterns[:8]):
                    hourly_errors[hour] = hourly_errors.get(hour, 0) + 1
        
        result = "TIMELINE ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        
        if not hourly_counts:
            result += "No timestamps found in logs.\n"
            return result
        
        result += "HOURLY DISTRIBUTION\n"
        result += "-" * 30 + "\n"
        
        max_count = max(hourly_counts.values()) if hourly_counts else 1
        
        for hour in sorted(hourly_counts.keys()):
            count = hourly_counts[hour]
            error_count = hourly_errors.get(hour, 0)
            
            bar_len = int((count / max_count) * 30)
            bar = "#" * bar_len
            
            result += hour + ":00 | " + bar + " " + str(count)
            if error_count > 0:
                result += " (errors: " + str(error_count) + ")"
            result += "\n"
        
        result += "\n"
        result += "PEAK HOURS\n"
        result += "-" * 30 + "\n"
        
        sorted_hours = sorted(hourly_counts.items(), key=lambda x: x[1], reverse=True)
        for hour, count in sorted_hours[:3]:
            result += hour + ":00 - " + str(count) + " events\n"
        
        result += "\n"
        result += "QUIET HOURS\n"
        result += "-" * 30 + "\n"
        
        for hour, count in sorted_hours[-3:]:
            result += hour + ":00 - " + str(count) + " events\n"
        
        return result
    
    def _search_logs(self, lines, search_term):
        if not search_term:
            return "Please provide a search term."
        
        matches = []
        search_lower = search_term.lower()
        
        for i, line in enumerate(lines):
            if search_lower in line.lower():
                matches.append({
                    "line_num": i + 1,
                    "content": line
                })
        
        result = "LOG SEARCH RESULTS\n"
        result += "=" * 50 + "\n\n"
        
        result += "Search term: " + search_term + "\n"
        result += "Matches found: " + str(len(matches)) + "\n\n"
        
        if not matches:
            result += "No matches found.\n"
            return result
        
        result += "MATCHES\n"
        result += "-" * 30 + "\n"
        
        for match in matches[:30]:
            line_content = match["content"]
            if len(line_content) > 80:
                line_content = line_content[:80] + "..."
            
            result += "Line " + str(match["line_num"]) + ":\n"
            result += "  " + line_content + "\n\n"
        
        if len(matches) > 30:
            result += "... and " + str(len(matches) - 30) + " more matches\n"
        
        return result
    
    def _get_stats(self, lines):
        total_lines = len(lines)
        
        total_chars = sum(len(line) for line in lines)
        avg_line_length = total_chars / total_lines if total_lines > 0 else 0
        
        line_lengths = [len(line) for line in lines]
        min_length = min(line_lengths) if line_lengths else 0
        max_length = max(line_lengths) if line_lengths else 0
        
        empty_lines = sum(1 for line in lines if not line.strip())
        
        unique_lines = len(set(lines))
        duplicate_lines = total_lines - unique_lines
        
        level_counts = {
            "error": 0,
            "warning": 0,
            "info": 0,
            "debug": 0,
            "other": 0
        }
        
        for line in lines:
            line_lower = line.lower()
            
            if "error" in line_lower or "err" in line_lower:
                level_counts["error"] += 1
            elif "warn" in line_lower:
                level_counts["warning"] += 1
            elif "info" in line_lower:
                level_counts["info"] += 1
            elif "debug" in line_lower:
                level_counts["debug"] += 1
            else:
                level_counts["other"] += 1
        
        result = "LOG STATISTICS\n"
        result += "=" * 50 + "\n\n"
        
        result += "BASIC STATS\n"
        result += "-" * 30 + "\n"
        result += "Total lines: " + str(total_lines) + "\n"
        result += "Total characters: " + str(total_chars) + "\n"
        result += "Average line length: " + str(round(avg_line_length, 1)) + " chars\n"
        result += "Min line length: " + str(min_length) + " chars\n"
        result += "Max line length: " + str(max_length) + " chars\n"
        result += "Empty lines: " + str(empty_lines) + "\n"
        result += "Unique lines: " + str(unique_lines) + "\n"
        result += "Duplicate lines: " + str(duplicate_lines) + "\n\n"
        
        result += "LOG LEVEL DISTRIBUTION\n"
        result += "-" * 30 + "\n"
        
        for level, count in level_counts.items():
            pct = (count / total_lines * 100) if total_lines > 0 else 0
            bar_len = int(pct / 2)
            bar = "#" * bar_len
            
            result += level.ljust(10) + ": " + str(count).rjust(6) + " (" + str(round(pct, 1)).rjust(5) + "%) " + bar + "\n"
        
        result += "\n"
        result += "SIZE ESTIMATE\n"
        result += "-" * 30 + "\n"
        
        size_bytes = total_chars
        if size_bytes < 1024:
            size_str = str(size_bytes) + " bytes"
        elif size_bytes < 1024 * 1024:
            size_str = str(round(size_bytes / 1024, 2)) + " KB"
        else:
            size_str = str(round(size_bytes / (1024 * 1024), 2)) + " MB"
        
        result += "Approximate size: " + size_str + "\n"
        
        return result