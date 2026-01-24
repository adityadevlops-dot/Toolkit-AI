"""
Data Visualization Tool - Generate text-based charts and visualizations.
"""

from .base_tool import BaseTool


class DataVisualizationTool(BaseTool):
    """Generate text-based charts and visualizations from data."""
    
    def __init__(self):
        super().__init__()
        self.name = "data_visualization"
        self.description = "Generate text-based charts including bar charts, line charts, histograms, and pie charts from data."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "data": {
                    "type": "string",
                    "description": "Data as comma-separated values or JSON"
                },
                "chart_type": {
                    "type": "string",
                    "enum": ["bar", "horizontal_bar", "line", "histogram", "pie", "scatter", "table"],
                    "description": "Type of chart to generate",
                    "default": "bar"
                },
                "title": {
                    "type": "string",
                    "description": "Chart title"
                },
                "labels": {
                    "type": "string",
                    "description": "Comma-separated labels for data points"
                },
                "width": {
                    "type": "integer",
                    "description": "Chart width in characters",
                    "default": 50
                }
            },
            "required": ["data"]
        }
    
    def execute(self, data, chart_type="bar", title=None, labels=None, width=50):
        try:
            if not data or not data.strip():
                return "Please provide data to visualize."
            
            parsed_data = self._parse_data(data)
            
            if parsed_data is None or len(parsed_data) == 0:
                return "Could not parse data. Use comma-separated numbers or JSON format."
            
            parsed_labels = None
            if labels:
                parsed_labels = [l.strip() for l in labels.split(",")]
            
            if chart_type == "bar":
                return self._bar_chart(parsed_data, title, parsed_labels, width)
            elif chart_type == "horizontal_bar":
                return self._horizontal_bar_chart(parsed_data, title, parsed_labels, width)
            elif chart_type == "line":
                return self._line_chart(parsed_data, title, parsed_labels, width)
            elif chart_type == "histogram":
                return self._histogram(parsed_data, title, width)
            elif chart_type == "pie":
                return self._pie_chart(parsed_data, title, parsed_labels)
            elif chart_type == "scatter":
                return self._scatter_plot(parsed_data, title, width)
            elif chart_type == "table":
                return self._table(parsed_data, title, parsed_labels)
            else:
                return self._bar_chart(parsed_data, title, parsed_labels, width)
                
        except Exception as e:
            return "Visualization error: " + str(e)
    
    def _parse_data(self, data):
        data = data.strip()
        
        if data.startswith("[") and data.endswith("]"):
            try:
                import json
                return json.loads(data)
            except Exception:
                pass
        
        if data.startswith("{") and data.endswith("}"):
            try:
                import json
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    return list(parsed.values())
            except Exception:
                pass
        
        try:
            values = []
            for item in data.split(","):
                item = item.strip()
                if item:
                    values.append(float(item))
            if values:
                return values
        except ValueError:
            pass
        
        try:
            values = []
            for item in data.split():
                item = item.strip()
                if item:
                    values.append(float(item))
            if values:
                return values
        except ValueError:
            pass
        
        return None
    
    def _bar_chart(self, data, title, labels, width):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "BAR CHART\n"
            result += "=" * 9 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        max_val = max(data)
        min_val = min(data)
        
        if max_val == min_val:
            max_val = min_val + 1
        
        height = 15
        
        chart_lines = []
        for row in range(height, 0, -1):
            threshold = min_val + (max_val - min_val) * (row / height)
            line = ""
            for val in data:
                if val >= threshold:
                    line += " ## "
                else:
                    line += "    "
            chart_lines.append(line)
        
        for line in chart_lines:
            result += line + "\n"
        
        result += "-" * (len(data) * 4) + "\n"
        
        if labels and len(labels) >= len(data):
            label_line = ""
            for i in range(len(data)):
                label = labels[i][:3].center(4)
                label_line += label
            result += label_line + "\n"
        else:
            label_line = ""
            for i in range(len(data)):
                label_line += str(i + 1).center(4)
            result += label_line + "\n"
        
        result += "\n"
        result += "Values: " + ", ".join(str(round(v, 2)) for v in data) + "\n"
        result += "Min: " + str(round(min_val, 2)) + " | Max: " + str(round(max_val, 2)) + "\n"
        result += "Sum: " + str(round(sum(data), 2)) + " | Avg: " + str(round(sum(data) / len(data), 2)) + "\n"
        
        return result
    
    def _horizontal_bar_chart(self, data, title, labels, width):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "HORIZONTAL BAR CHART\n"
            result += "=" * 20 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        max_val = max(data)
        if max_val == 0:
            max_val = 1
        
        max_label_len = 10
        if labels:
            max_label_len = max(len(str(l)[:15]) for l in labels[:len(data)])
            max_label_len = min(max_label_len, 15)
        
        bar_width = width - max_label_len - 15
        
        for i, val in enumerate(data):
            if labels and i < len(labels):
                label = str(labels[i])[:15].ljust(max_label_len)
            else:
                label = ("Item " + str(i + 1)).ljust(max_label_len)
            
            bar_len = int((val / max_val) * bar_width)
            bar = "#" * bar_len
            
            result += label + " | " + bar + " " + str(round(val, 2)) + "\n"
        
        result += "\n"
        result += "Total: " + str(round(sum(data), 2)) + "\n"
        
        return result
    
    def _line_chart(self, data, title, labels, width):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "LINE CHART\n"
            result += "=" * 10 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        if len(data) < 2:
            return result + "Need at least 2 data points for line chart."
        
        max_val = max(data)
        min_val = min(data)
        
        if max_val == min_val:
            max_val = min_val + 1
        
        height = 12
        chart_width = min(len(data), width)
        
        grid = []
        for row in range(height):
            grid.append([" "] * chart_width)
        
        for i, val in enumerate(data):
            if i >= chart_width:
                break
            
            normalized = (val - min_val) / (max_val - min_val)
            row = height - 1 - int(normalized * (height - 1))
            row = max(0, min(height - 1, row))
            grid[row][i] = "*"
        
        for i in range(len(data) - 1):
            if i >= chart_width - 1:
                break
            
            val1 = data[i]
            val2 = data[i + 1]
            
            norm1 = (val1 - min_val) / (max_val - min_val)
            norm2 = (val2 - min_val) / (max_val - min_val)
            
            row1 = height - 1 - int(norm1 * (height - 1))
            row2 = height - 1 - int(norm2 * (height - 1))
            
            if row1 != row2:
                step = 1 if row2 > row1 else -1
                for r in range(row1, row2, step):
                    if 0 <= r < height:
                        if grid[r][i] == " ":
                            grid[r][i] = "|"
        
        result += str(round(max_val, 1)).rjust(8) + " |\n"
        
        for row in grid:
            result += " " * 8 + " |" + "".join(row) + "\n"
        
        result += str(round(min_val, 1)).rjust(8) + " |" + "-" * chart_width + "\n"
        
        result += "\n"
        result += "Points: " + str(len(data)) + "\n"
        result += "Range: " + str(round(min_val, 2)) + " to " + str(round(max_val, 2)) + "\n"
        
        if len(data) >= 2:
            trend = data[-1] - data[0]
            if trend > 0:
                result += "Trend: Upward (+" + str(round(trend, 2)) + ")\n"
            elif trend < 0:
                result += "Trend: Downward (" + str(round(trend, 2)) + ")\n"
            else:
                result += "Trend: Flat\n"
        
        return result
    
    def _histogram(self, data, title, width):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "HISTOGRAM\n"
            result += "=" * 9 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        num_bins = min(10, len(set(data)))
        if num_bins < 2:
            num_bins = 2
        
        min_val = min(data)
        max_val = max(data)
        
        if max_val == min_val:
            max_val = min_val + 1
        
        bin_width = (max_val - min_val) / num_bins
        
        bins = [0] * num_bins
        
        for val in data:
            bin_idx = int((val - min_val) / bin_width)
            if bin_idx >= num_bins:
                bin_idx = num_bins - 1
            bins[bin_idx] += 1
        
        max_count = max(bins) if bins else 1
        if max_count == 0:
            max_count = 1
        
        bar_max_width = width - 25
        
        result += "Distribution:\n"
        result += "-" * 40 + "\n"
        
        for i, count in enumerate(bins):
            bin_start = min_val + i * bin_width
            bin_end = bin_start + bin_width
            
            range_str = str(round(bin_start, 1)) + "-" + str(round(bin_end, 1))
            range_str = range_str.ljust(15)
            
            bar_len = int((count / max_count) * bar_max_width)
            bar = "#" * bar_len
            
            result += range_str + " |" + bar + " " + str(count) + "\n"
        
        result += "\n"
        result += "Statistics:\n"
        result += "-" * 20 + "\n"
        result += "Count: " + str(len(data)) + "\n"
        result += "Min: " + str(round(min_val, 2)) + "\n"
        result += "Max: " + str(round(max_val, 2)) + "\n"
        result += "Mean: " + str(round(sum(data) / len(data), 2)) + "\n"
        
        sorted_data = sorted(data)
        mid = len(sorted_data) // 2
        if len(sorted_data) % 2 == 0:
            median = (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            median = sorted_data[mid]
        result += "Median: " + str(round(median, 2)) + "\n"
        
        return result
    
    def _pie_chart(self, data, title, labels):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "PIE CHART\n"
            result += "=" * 9 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        total = sum(data)
        if total == 0:
            return result + "Total is zero, cannot create pie chart."
        
        percentages = [(val / total) * 100 for val in data]
        
        symbols = ["#", "*", "@", "+", "=", "-", "~", "^", "&", "%"]
        
        result += "     ****\n"
        result += "   ********\n"
        result += "  **********\n"
        result += "  **********\n"
        result += "   ********\n"
        result += "     ****\n\n"
        
        result += "Legend:\n"
        result += "-" * 40 + "\n"
        
        for i, (val, pct) in enumerate(zip(data, percentages)):
            symbol = symbols[i % len(symbols)]
            
            if labels and i < len(labels):
                label = str(labels[i])[:20]
            else:
                label = "Item " + str(i + 1)
            
            bar_len = int(pct / 2)
            bar = symbol * bar_len
            
            result += symbol + " " + label.ljust(20) + ": " + str(round(val, 2)).rjust(10)
            result += " (" + str(round(pct, 1)) + "%)\n"
            result += "  " + bar + "\n"
        
        result += "\n"
        result += "Total: " + str(round(total, 2)) + "\n"
        
        return result
    
    def _scatter_plot(self, data, title, width):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "SCATTER PLOT\n"
            result += "=" * 12 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        if len(data) < 2:
            return result + "Need at least 2 data points."
        
        if len(data) % 2 != 0:
            data = data[:-1]
        
        x_vals = data[0::2]
        y_vals = data[1::2]
        
        if not x_vals or not y_vals:
            return result + "Could not parse x,y pairs from data."
        
        min_x = min(x_vals)
        max_x = max(x_vals)
        min_y = min(y_vals)
        max_y = max(y_vals)
        
        if max_x == min_x:
            max_x = min_x + 1
        if max_y == min_y:
            max_y = min_y + 1
        
        plot_width = 40
        plot_height = 15
        
        grid = []
        for row in range(plot_height):
            grid.append(["."] * plot_width)
        
        for x, y in zip(x_vals, y_vals):
            norm_x = (x - min_x) / (max_x - min_x)
            norm_y = (y - min_y) / (max_y - min_y)
            
            col = int(norm_x * (plot_width - 1))
            row = plot_height - 1 - int(norm_y * (plot_height - 1))
            
            col = max(0, min(plot_width - 1, col))
            row = max(0, min(plot_height - 1, row))
            
            grid[row][col] = "*"
        
        result += "Y\n"
        result += str(round(max_y, 1)).rjust(6) + " |"
        for row in grid:
            result += "".join(row) + "\n       |"
        result = result[:-8]
        result += str(round(min_y, 1)).rjust(6) + " |" + "-" * plot_width + " X\n"
        result += "        " + str(round(min_x, 1)).ljust(15) + str(round(max_x, 1)).rjust(20) + "\n"
        
        result += "\n"
        result += "Points: " + str(len(x_vals)) + "\n"
        result += "X range: " + str(round(min_x, 2)) + " to " + str(round(max_x, 2)) + "\n"
        result += "Y range: " + str(round(min_y, 2)) + " to " + str(round(max_y, 2)) + "\n"
        
        return result
    
    def _table(self, data, title, labels):
        result = ""
        
        if title:
            result += title + "\n"
            result += "=" * len(title) + "\n\n"
        else:
            result += "DATA TABLE\n"
            result += "=" * 10 + "\n\n"
        
        if not data:
            return result + "No data to display."
        
        result += "+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 10 + "+\n"
        result += "| " + "Index".ljust(6) + " | " + "Label".ljust(13) + " | " + "Value".ljust(8) + " |\n"
        result += "+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 10 + "+\n"
        
        for i, val in enumerate(data):
            idx = str(i + 1).ljust(6)
            
            if labels and i < len(labels):
                label = str(labels[i])[:13].ljust(13)
            else:
                label = ("Item " + str(i + 1)).ljust(13)
            
            val_str = str(round(val, 2)).ljust(8)
            
            result += "| " + idx + " | " + label + " | " + val_str + " |\n"
        
        result += "+" + "-" * 8 + "+" + "-" * 15 + "+" + "-" * 10 + "+\n"
        
        result += "\n"
        result += "Summary:\n"
        result += "  Count: " + str(len(data)) + "\n"
        result += "  Sum: " + str(round(sum(data), 2)) + "\n"
        result += "  Average: " + str(round(sum(data) / len(data), 2)) + "\n"
        result += "  Min: " + str(round(min(data), 2)) + "\n"
        result += "  Max: " + str(round(max(data), 2)) + "\n"
        
        return result