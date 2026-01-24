"""
Tools package - All tools for the Multi-Tool LLM Agent.
"""

from .base_tool import BaseTool
from .calculator import CalculatorTool
from .web_search import WebSearchTool
from .file_reader import FileReaderTool
from .weather import WeatherTool
from .wikipedia import WikipediaTool
from .url_reader import URLReaderTool
from .code_executor import CodeExecutorTool
from .text_summarizer import TextSummarizerTool
from .semantic_qa import SemanticQATool
from .intent_classifier import IntentClassifierTool
from .prompt_optimizer import PromptOptimizerTool
from .code_generator import CodeGeneratorTool
from .code_debugger import CodeDebuggerTool
from .regex_tool import RegexTool
from .api_tester import APITesterTool
from .dependency_analyzer import DependencyAnalyzerTool
from .csv_analyzer import CSVAnalyzerTool
from .data_visualizer import DataVisualizationTool
from .json_schema_generator import JSONSchemaGeneratorTool
from .log_analyzer import LogAnalyzerTool
from .translator import TranslatorTool
from .unit_currency_converter import UnitCurrencyConverterTool
from .datetime_reasoner import DateTimeReasonerTool
from .email_writer import EmailWriterTool
from .task_planner import TaskPlannerTool


AVAILABLE_TOOLS = {
    "calculator": CalculatorTool,
    "web_search": WebSearchTool,
    "file_reader": FileReaderTool,
    "weather": WeatherTool,
    "wikipedia": WikipediaTool,
    "url_reader": URLReaderTool,
    "code_executor": CodeExecutorTool,
    "text_summarizer": TextSummarizerTool,
    "semantic_qa": SemanticQATool,
    "intent_classifier": IntentClassifierTool,
    "prompt_optimizer": PromptOptimizerTool,
    "code_generator": CodeGeneratorTool,
    "code_debugger": CodeDebuggerTool,
    "regex_tool": RegexTool,
    "api_tester": APITesterTool,
    "dependency_analyzer": DependencyAnalyzerTool,
    "csv_analyzer": CSVAnalyzerTool,
    "data_visualization": DataVisualizationTool,
    "json_schema_generator": JSONSchemaGeneratorTool,
    "log_analyzer": LogAnalyzerTool,
    "translator": TranslatorTool,
    "unit_currency_converter": UnitCurrencyConverterTool,
    "datetime_reasoner": DateTimeReasonerTool,
    "email_writer": EmailWriterTool,
    "task_planner": TaskPlannerTool,
}


def get_all_tools():
    return [tool_class() for tool_class in AVAILABLE_TOOLS.values()]


def get_tool_by_name(name):
    tool_class = AVAILABLE_TOOLS.get(name)
    if tool_class:
        return tool_class()
    return None