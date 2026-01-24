"""
File Reader Tool - Read and analyze various file types.
"""

import os
import json
import csv
from pathlib import Path
from typing import Dict, Optional
from io import StringIO

from .base_tool import BaseTool
from config import Config


class FileReaderTool(BaseTool):
    """Read and analyze various file types (txt, pdf, docx, csv, json, etc.)."""
    
    def __init__(self):
        super().__init__()
        self.name = "file_reader"
        self.description = """Read and analyze files. Supports:
        - Text files (.txt, .md, .py, .js, .html, .css, etc.)
        - PDF documents (.pdf)
        - Word documents (.docx)
        - CSV files (.csv) - returns as formatted table
        - JSON files (.json) - returns parsed content
        Provide the file path or uploaded file name."""
        
        self.parameters = {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file or filename of uploaded file"
                },
                "operation": {
                    "type": "string",
                    "enum": ["read", "summary", "word_count", "search"],
                    "description": "Operation to perform (default: read)",
                    "default": "read"
                },
                "search_term": {
                    "type": "string",
                    "description": "Term to search for (when operation is 'search')"
                }
            },
            "required": ["file_path"]
        }
    
    def execute(self, file_path: str, operation: str = "read", search_term: str = None) -> str:
        """Execute file reading operation."""
        try:
            # Check in uploaded files folder first
            upload_path = Path(Config.UPLOAD_FOLDER) / file_path
            if upload_path.exists():
                file_path = str(upload_path)
            
            path = Path(file_path)
            
            if not path.exists():
                return f"❌ File not found: {file_path}"
            
            # Check file size
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > Config.MAX_FILE_SIZE_MB:
                return f"❌ File too large ({size_mb:.2f} MB). Maximum allowed: {Config.MAX_FILE_SIZE_MB} MB"
            
            # Read file based on extension
            extension = path.suffix.lower()
            content = self._read_file(path, extension)
            
            if content is None:
                return f"❌ Unsupported file type: {extension}"
            
            # Perform operation
            if operation == "read":
                return f"📄 **Contents of {path.name}:**\n\n{content}"
            elif operation == "summary":
                return self._generate_summary(content, path.name)
            elif operation == "word_count":
                return self._word_count(content, path.name)
            elif operation == "search" and search_term:
                return self._search_content(content, search_term, path.name)
            else:
                return f"📄 **Contents of {path.name}:**\n\n{content}"
                
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    def _read_file(self, path: Path, extension: str) -> Optional[str]:
        """Read file based on its extension."""
        
        # Text-based files
        text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', 
                         '.xml', '.yaml', '.yml', '.ini', '.cfg', '.log', '.sh', '.bat'}
        
        if extension in text_extensions:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        # CSV files
        elif extension == '.csv':
            return self._read_csv(path)
        
        # PDF files
        elif extension == '.pdf':
            return self._read_pdf(path)
        
        # Word documents
        elif extension == '.docx':
            return self._read_docx(path)
        
        # JSON files (pretty print)
        elif extension == '.json':
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return json.dumps(data, indent=2)
        
        return None
    
    def _read_csv(self, path: Path) -> str:
        """Read CSV file and format as table."""
        try:
            import pandas as pd
            df = pd.read_csv(path)
            return f"**CSV Data ({len(df)} rows, {len(df.columns)} columns):**\n\n{df.to_markdown(index=False)}"
        except ImportError:
            # Fallback without pandas
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                if not rows:
                    return "Empty CSV file"
                
                # Format as simple table
                output = []
                for i, row in enumerate(rows[:20]):  # Limit to first 20 rows
                    output.append(' | '.join(row))
                    if i == 0:
                        output.append('-' * 50)
                
                if len(rows) > 20:
                    output.append(f"\n... and {len(rows) - 20} more rows")
                
                return '\n'.join(output)
    
    def _read_pdf(self, path: Path) -> str:
        """Read PDF file."""
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(path)
            text = []
            for i, page in enumerate(reader.pages[:10]):  # Limit to first 10 pages
                text.append(f"--- Page {i+1} ---\n{page.extract_text()}")
            
            if len(reader.pages) > 10:
                text.append(f"\n... and {len(reader.pages) - 10} more pages")
            
            return '\n\n'.join(text)
        except ImportError:
            return "❌ PyPDF2 library not installed. Run: pip install PyPDF2"
    
    def _read_docx(self, path: Path) -> str:
        """Read Word document."""
        try:
            from docx import Document
            doc = Document(path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n\n'.join(paragraphs)
        except ImportError:
            return "❌ python-docx library not installed. Run: pip install python-docx"
    
    def _generate_summary(self, content: str, filename: str) -> str:
        """Generate basic summary statistics."""
        lines = content.split('\n')
        words = content.split()
        chars = len(content)
        
        return f"""📊 **Summary of {filename}:**
        
- **Lines:** {len(lines)}
- **Words:** {len(words)}
- **Characters:** {chars}
- **Average words per line:** {len(words) / max(len(lines), 1):.1f}

**First 200 characters:**
{content[:200]}..."""
    
    def _word_count(self, content: str, filename: str) -> str:
        """Count words in file."""
        words = content.split()
        return f"📊 **Word count for {filename}:** {len(words)} words"
    
    def _search_content(self, content: str, search_term: str, filename: str) -> str:
        """Search for term in content."""
        lines = content.split('\n')
        matches = []
        
        for i, line in enumerate(lines, 1):
            if search_term.lower() in line.lower():
                matches.append(f"Line {i}: {line.strip()}")
        
        if matches:
            return f"🔍 **Found {len(matches)} matches for '{search_term}' in {filename}:**\n\n" + '\n'.join(matches[:20])
        else:
            return f"🔍 No matches found for '{search_term}' in {filename}"