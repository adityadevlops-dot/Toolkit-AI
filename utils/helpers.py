"""
Helper utility functions for the Multi-Tool LLM Agent.
"""

import re
import json
from datetime import datetime
from typing import Any, Dict, List, Optional


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Format datetime to readable string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def clean_json_string(text: str) -> str:
    """Extract JSON from text that might contain markdown code blocks."""
    # Remove markdown code blocks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_match:
        return json_match.group(1).strip()
    return text.strip()


def safe_json_parse(text: str) -> Optional[Dict]:
    """Safely parse JSON from text."""
    try:
        cleaned = clean_json_string(text)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def format_tool_result(tool_name: str, result: Any) -> str:
    """Format tool result for display."""
    return f"**🔧 {tool_name}**\n```\n{result}\n```"


def extract_code_blocks(text: str) -> List[str]:
    """Extract code blocks from markdown text."""
    pattern = r'```(?:\w+)?\s*([\s\S]*?)\s*```'
    matches = re.findall(pattern, text)
    return matches


def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove dangerous characters."""
    # Remove path separators and null bytes
    filename = filename.replace('/', '_').replace('\\', '_').replace('\0', '')
    # Keep only safe characters
    return re.sub(r'[^\w\-_\. ]', '', filename)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} TB"