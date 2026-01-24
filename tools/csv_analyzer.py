"""
CSV Analyzer Tool - Analyze CSV data with statistics and insights.
"""

from .base_tool import BaseTool


class CSVAnalyzerTool(BaseTool):
    """Analyze CSV data with statistics, preview, and insights."""
    
    def __init__(self):
        super().__init__()
        self.name = "csv_analyzer"
        self.description = "Analyze CSV data with statistics, column info, preview, filtering, and missing value detection."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "csv_data": {
                    "type": "string",
                    "description": "CSV content as string or file path"
                },
                "operation": {
                    "type": "string",
                    "enum": ["summary", "statistics", "columns", "preview", "missing", "filter", "groupby"],
                    "description": "Operation to perform",
                    "default": "summary"
                },
                "column": {
                    "type": "string",
                    "description": "Column name for specific operations"
                },
                "filter_expr": {
                    "type": "string",
                    "description": "Filter expression"
                },
                "rows": {
                    "type": "integer",
                    "description": "Number of rows for preview",
                    "default": 5
                }
            },
            "required": ["csv_data"]
        }
    
    def execute(self, csv_data, operation="summary", column=None, filter_expr=None, rows=5):
        try:
            if not csv_data or not csv_data.strip():
                return "Please provide CSV data."
            
            data = self._parse_csv(csv_data)
            
            if data is None:
                return "Could not parse CSV data. Please check the format."
            
            if len(data["rows"]) == 0:
                return "CSV has no data rows."
            
            if operation == "summary":
                return self._get_summary(data)
            elif operation == "statistics":
                return self._get_statistics(data, column)
            elif operation == "columns":
                return self._get_columns(data)
            elif operation == "preview":
                return self._get_preview(data, rows)
            elif operation == "missing":
                return self._get_missing(data)
            elif operation == "filter":
                return self._filter_data(data, filter_expr, rows)
            elif operation == "groupby":
                return self._group_by(data, column)
            else:
                return self._get_summary(data)
                
        except Exception as e:
            return "CSV analysis error: " + str(e)
    
    def _parse_csv(self, csv_data):
        import csv
        import io
        from pathlib import Path
        
        content = None
        
        try:
            path = Path(csv_data.strip())
            if path.exists() and path.is_file():
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
        except Exception:
            pass
        
        if content is None:
            content = csv_data
        
        for delimiter in [",", ";", "\t", "|"]:
            try:
                reader = csv.reader(io.StringIO(content), delimiter=delimiter)
                rows = list(reader)
                
                if len(rows) < 1:
                    continue
                
                headers = rows[0]
                data_rows = rows[1:]
                
                if len(headers) > 1 or (len(headers) == 1 and len(data_rows) > 0):
                    return {
                        "headers": headers,
                        "rows": data_rows,
                        "delimiter": delimiter
                    }
            except Exception:
                continue
        
        return None
    
    def _get_summary(self, data):
        headers = data["headers"]
        rows = data["rows"]
        
        row_count = len(rows)
        col_count = len(headers)
        
        numeric_cols = []
        text_cols = []
        
        for i, header in enumerate(headers):
            is_numeric = True
            for row in rows[:100]:
                if i < len(row):
                    val = row[i].strip()
                    if val:
                        try:
                            float(val.replace(",", ""))
                        except ValueError:
                            is_numeric = False
                            break
            
            if is_numeric:
                numeric_cols.append(header)
            else:
                text_cols.append(header)
        
        missing_count = 0
        for row in rows:
            for val in row:
                if not val.strip():
                    missing_count += 1
        
        total_cells = row_count * col_count
        missing_pct = (missing_count / total_cells * 100) if total_cells > 0 else 0
        
        result = "CSV ANALYSIS SUMMARY\n"
        result += "=" * 50 + "\n\n"
        
        result += "BASIC INFO\n"
        result += "-" * 30 + "\n"
        result += "Rows: " + str(row_count) + "\n"
        result += "Columns: " + str(col_count) + "\n"
        result += "Total cells: " + str(total_cells) + "\n"
        result += "Missing values: " + str(missing_count) + " (" + str(round(missing_pct, 2)) + "%)\n\n"
        
        result += "COLUMNS\n"
        result += "-" * 30 + "\n"
        
        col_list = ", ".join(headers[:10])
        if len(headers) > 10:
            col_list += " ... and " + str(len(headers) - 10) + " more"
        result += col_list + "\n\n"
        
        result += "COLUMN TYPES\n"
        result += "-" * 30 + "\n"
        result += "Numeric columns (" + str(len(numeric_cols)) + "): "
        if numeric_cols:
            result += ", ".join(numeric_cols[:5])
            if len(numeric_cols) > 5:
                result += " ..."
        else:
            result += "None"
        result += "\n"
        
        result += "Text columns (" + str(len(text_cols)) + "): "
        if text_cols:
            result += ", ".join(text_cols[:5])
            if len(text_cols) > 5:
                result += " ..."
        else:
            result += "None"
        result += "\n\n"
        
        result += "SAMPLE DATA (first 3 rows)\n"
        result += "-" * 30 + "\n"
        
        header_line = " | ".join(h[:15] for h in headers[:6])
        if len(headers) > 6:
            header_line += " | ..."
        result += header_line + "\n"
        result += "-" * len(header_line) + "\n"
        
        for row in rows[:3]:
            row_line = " | ".join(str(v)[:15] for v in row[:6])
            if len(row) > 6:
                row_line += " | ..."
            result += row_line + "\n"
        
        return result
    
    def _get_statistics(self, data, column=None):
        headers = data["headers"]
        rows = data["rows"]
        
        if column:
            if column not in headers:
                return "Column '" + column + "' not found. Available: " + ", ".join(headers[:10])
            
            col_idx = headers.index(column)
            values = []
            
            for row in rows:
                if col_idx < len(row):
                    val = row[col_idx].strip()
                    if val:
                        try:
                            values.append(float(val.replace(",", "")))
                        except ValueError:
                            pass
            
            if not values:
                unique_vals = set()
                for row in rows:
                    if col_idx < len(row):
                        val = row[col_idx].strip()
                        if val:
                            unique_vals.add(val)
                
                result = "COLUMN STATISTICS: " + column + "\n"
                result += "=" * 50 + "\n\n"
                result += "Type: Text/Categorical\n"
                result += "Unique values: " + str(len(unique_vals)) + "\n\n"
                
                result += "Top values:\n"
                val_counts = {}
                for row in rows:
                    if col_idx < len(row):
                        val = row[col_idx].strip()
                        if val:
                            val_counts[val] = val_counts.get(val, 0) + 1
                
                sorted_vals = sorted(val_counts.items(), key=lambda x: x[1], reverse=True)
                for val, count in sorted_vals[:10]:
                    result += "  " + val[:30] + ": " + str(count) + "\n"
                
                return result
            
            count = len(values)
            mean = sum(values) / count
            sorted_vals = sorted(values)
            
            if count % 2 == 0:
                median = (sorted_vals[count // 2 - 1] + sorted_vals[count // 2]) / 2
            else:
                median = sorted_vals[count // 2]
            
            min_val = min(values)
            max_val = max(values)
            
            variance = sum((x - mean) ** 2 for x in values) / count
            std_dev = variance ** 0.5
            
            q1_idx = int(count * 0.25)
            q3_idx = int(count * 0.75)
            q1 = sorted_vals[q1_idx]
            q3 = sorted_vals[q3_idx]
            
            result = "COLUMN STATISTICS: " + column + "\n"
            result += "=" * 50 + "\n\n"
            result += "Type: Numeric\n\n"
            result += "Count: " + str(count) + "\n"
            result += "Mean: " + str(round(mean, 4)) + "\n"
            result += "Median: " + str(round(median, 4)) + "\n"
            result += "Std Dev: " + str(round(std_dev, 4)) + "\n"
            result += "Min: " + str(round(min_val, 4)) + "\n"
            result += "Max: " + str(round(max_val, 4)) + "\n"
            result += "25th percentile: " + str(round(q1, 4)) + "\n"
            result += "75th percentile: " + str(round(q3, 4)) + "\n"
            result += "Range: " + str(round(max_val - min_val, 4)) + "\n"
            
            return result
        
        else:
            result = "STATISTICS FOR ALL NUMERIC COLUMNS\n"
            result += "=" * 50 + "\n\n"
            
            for i, header in enumerate(headers):
                values = []
                for row in rows:
                    if i < len(row):
                        val = row[i].strip()
                        if val:
                            try:
                                values.append(float(val.replace(",", "")))
                            except ValueError:
                                pass
                
                if len(values) >= 2:
                    count = len(values)
                    mean = sum(values) / count
                    min_val = min(values)
                    max_val = max(values)
                    
                    result += header + ":\n"
                    result += "  Count: " + str(count)
                    result += ", Mean: " + str(round(mean, 2))
                    result += ", Min: " + str(round(min_val, 2))
                    result += ", Max: " + str(round(max_val, 2)) + "\n\n"
            
            return result
    
    def _get_columns(self, data):
        headers = data["headers"]
        rows = data["rows"]
        
        result = "COLUMN INFORMATION\n"
        result += "=" * 50 + "\n\n"
        result += "Total columns: " + str(len(headers)) + "\n\n"
        
        for i, header in enumerate(headers):
            non_null = 0
            null_count = 0
            unique_vals = set()
            
            for row in rows:
                if i < len(row):
                    val = row[i].strip()
                    if val:
                        non_null += 1
                        unique_vals.add(val)
                    else:
                        null_count += 1
                else:
                    null_count += 1
            
            is_numeric = True
            for row in rows[:50]:
                if i < len(row):
                    val = row[i].strip()
                    if val:
                        try:
                            float(val.replace(",", ""))
                        except ValueError:
                            is_numeric = False
                            break
            
            col_type = "Numeric" if is_numeric else "Text"
            
            result += str(i + 1) + ". " + header + "\n"
            result += "   Type: " + col_type + "\n"
            result += "   Non-null: " + str(non_null) + "\n"
            result += "   Null: " + str(null_count) + "\n"
            result += "   Unique: " + str(len(unique_vals)) + "\n\n"
        
        return result
    
    def _get_preview(self, data, rows=5):
        headers = data["headers"]
        data_rows = data["rows"]
        
        rows = min(rows, len(data_rows), 20)
        
        result = "DATA PREVIEW\n"
        result += "=" * 50 + "\n\n"
        result += "Showing " + str(rows) + " of " + str(len(data_rows)) + " rows\n\n"
        
        col_widths = []
        for i, header in enumerate(headers[:8]):
            max_width = len(header)
            for row in data_rows[:rows]:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])[:20]))
            col_widths.append(min(max_width, 20))
        
        header_line = ""
        for i, header in enumerate(headers[:8]):
            header_line += header[:col_widths[i]].ljust(col_widths[i]) + " | "
        if len(headers) > 8:
            header_line += "..."
        result += header_line + "\n"
        result += "-" * len(header_line) + "\n"
        
        for row in data_rows[:rows]:
            row_line = ""
            for i in range(min(len(headers), 8)):
                if i < len(row):
                    val = str(row[i])[:col_widths[i]]
                else:
                    val = ""
                row_line += val.ljust(col_widths[i]) + " | "
            if len(row) > 8:
                row_line += "..."
            result += row_line + "\n"
        
        if len(data_rows) > rows:
            result += "\n... " + str(len(data_rows) - rows) + " more rows\n"
        
        return result
    
    def _get_missing(self, data):
        headers = data["headers"]
        rows = data["rows"]
        
        result = "MISSING VALUE ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        
        missing_by_col = []
        
        for i, header in enumerate(headers):
            missing = 0
            total = len(rows)
            
            for row in rows:
                if i >= len(row) or not row[i].strip():
                    missing += 1
            
            if missing > 0:
                pct = (missing / total) * 100
                missing_by_col.append((header, missing, pct))
        
        if not missing_by_col:
            result += "No missing values found!\n"
            return result
        
        total_missing = sum(m[1] for m in missing_by_col)
        total_cells = len(headers) * len(rows)
        
        result += "OVERVIEW\n"
        result += "-" * 30 + "\n"
        result += "Total missing: " + str(total_missing) + " / " + str(total_cells) + "\n"
        result += "Columns with missing: " + str(len(missing_by_col)) + " / " + str(len(headers)) + "\n\n"
        
        result += "MISSING BY COLUMN\n"
        result += "-" * 30 + "\n"
        
        missing_by_col.sort(key=lambda x: x[1], reverse=True)
        
        for header, count, pct in missing_by_col:
            bar_len = int(pct / 5)
            bar = "#" * bar_len
            result += header[:20].ljust(20) + ": " + str(count) + " (" + str(round(pct, 1)) + "%) " + bar + "\n"
        
        return result
    
    def _filter_data(self, data, filter_expr, rows=10):
        if not filter_expr:
            return "Please provide a filter expression. Example: column_name > 100"
        
        headers = data["headers"]
        data_rows = data["rows"]
        
        result = "FILTERED DATA\n"
        result += "=" * 50 + "\n\n"
        result += "Filter: " + filter_expr + "\n\n"
        
        parts = None
        operator = None
        
        for op in [">=", "<=", "!=", "==", ">", "<", "="]:
            if op in filter_expr:
                parts = filter_expr.split(op, 1)
                operator = op
                break
        
        if not parts or len(parts) != 2:
            return "Invalid filter expression. Use: column_name operator value"
        
        col_name = parts[0].strip()
        filter_val = parts[1].strip().strip("'\"")
        
        if col_name not in headers:
            return "Column '" + col_name + "' not found. Available: " + ", ".join(headers[:10])
        
        col_idx = headers.index(col_name)
        
        filtered_rows = []
        
        for row in data_rows:
            if col_idx >= len(row):
                continue
            
            cell_val = row[col_idx].strip()
            
            try:
                cell_num = float(cell_val.replace(",", ""))
                filter_num = float(filter_val.replace(",", ""))
                
                match = False
                if operator in ["=", "=="]:
                    match = cell_num == filter_num
                elif operator == "!=":
                    match = cell_num != filter_num
                elif operator == ">":
                    match = cell_num > filter_num
                elif operator == "<":
                    match = cell_num < filter_num
                elif operator == ">=":
                    match = cell_num >= filter_num
                elif operator == "<=":
                    match = cell_num <= filter_num
                
                if match:
                    filtered_rows.append(row)
                    
            except ValueError:
                if operator in ["=", "=="]:
                    if cell_val.lower() == filter_val.lower():
                        filtered_rows.append(row)
                elif operator == "!=":
                    if cell_val.lower() != filter_val.lower():
                        filtered_rows.append(row)
        
        result += "Matching rows: " + str(len(filtered_rows)) + " / " + str(len(data_rows)) + "\n\n"
        
        if filtered_rows:
            rows = min(rows, len(filtered_rows))
            
            header_line = " | ".join(h[:15] for h in headers[:6])
            result += header_line + "\n"
            result += "-" * len(header_line) + "\n"
            
            for row in filtered_rows[:rows]:
                row_line = " | ".join(str(v)[:15] for v in row[:6])
                result += row_line + "\n"
            
            if len(filtered_rows) > rows:
                result += "\n... " + str(len(filtered_rows) - rows) + " more rows\n"
        else:
            result += "No matching rows found.\n"
        
        return result
    
    def _group_by(self, data, column):
        if not column:
            return "Please specify a column to group by."
        
        headers = data["headers"]
        rows = data["rows"]
        
        if column not in headers:
            return "Column '" + column + "' not found. Available: " + ", ".join(headers[:10])
        
        col_idx = headers.index(column)
        
        groups = {}
        
        for row in rows:
            if col_idx < len(row):
                key = row[col_idx].strip()
                if not key:
                    key = "(empty)"
            else:
                key = "(empty)"
            
            if key not in groups:
                groups[key] = 0
            groups[key] += 1
        
        result = "GROUP BY ANALYSIS\n"
        result += "=" * 50 + "\n\n"
        result += "Grouped by: " + column + "\n"
        result += "Unique groups: " + str(len(groups)) + "\n\n"
        
        sorted_groups = sorted(groups.items(), key=lambda x: x[1], reverse=True)
        
        result += "GROUP COUNTS\n"
        result += "-" * 30 + "\n"
        
        for key, count in sorted_groups[:20]:
            pct = (count / len(rows)) * 100
            bar_len = int(pct / 2)
            bar = "#" * bar_len
            result += key[:25].ljust(25) + ": " + str(count) + " (" + str(round(pct, 1)) + "%) " + bar + "\n"
        
        if len(sorted_groups) > 20:
            result += "\n... " + str(len(sorted_groups) - 20) + " more groups\n"
        
        return result