"""
JSON Schema Generator Tool - Generate JSON schemas from JSON data.
"""

from .base_tool import BaseTool
import json


class JSONSchemaGeneratorTool(BaseTool):
    """Generate JSON schemas from JSON data or descriptions."""
    
    def __init__(self):
        super().__init__()
        self.name = "json_schema_generator"
        self.description = "Generate JSON Schema from JSON data, validate JSON against schemas, and create sample JSON from schemas."
        
        self.parameters = {
            "type": "object",
            "properties": {
                "json_data": {
                    "type": "string",
                    "description": "JSON data to generate schema from"
                },
                "operation": {
                    "type": "string",
                    "enum": ["generate", "validate", "sample", "format"],
                    "description": "Operation to perform",
                    "default": "generate"
                },
                "schema": {
                    "type": "string",
                    "description": "JSON Schema for validation"
                },
                "title": {
                    "type": "string",
                    "description": "Title for the generated schema"
                }
            },
            "required": ["json_data"]
        }
    
    def execute(self, json_data, operation="generate", schema=None, title=None):
        try:
            if not json_data or not json_data.strip():
                return "Please provide JSON data."
            
            if operation == "generate":
                return self._generate_schema(json_data, title)
            elif operation == "validate":
                return self._validate_json(json_data, schema)
            elif operation == "sample":
                return self._generate_sample(json_data)
            elif operation == "format":
                return self._format_json(json_data)
            else:
                return self._generate_schema(json_data, title)
                
        except Exception as e:
            return "JSON Schema error: " + str(e)
    
    def _parse_json(self, json_string):
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            return None
    
    def _generate_schema(self, json_data, title=None):
        parsed = self._parse_json(json_data)
        
        if parsed is None:
            return "Invalid JSON data. Please check the format."
        
        schema = self._infer_schema(parsed)
        
        if title:
            schema["title"] = title
        
        schema["$schema"] = "http://json-schema.org/draft-07/schema#"
        
        schema_str = json.dumps(schema, indent=2)
        
        result = "JSON SCHEMA GENERATOR\n"
        result += "=" * 50 + "\n\n"
        
        result += "INPUT JSON:\n"
        result += "-" * 30 + "\n"
        input_str = json.dumps(parsed, indent=2)
        if len(input_str) > 500:
            result += input_str[:500] + "\n... (truncated)\n"
        else:
            result += input_str + "\n"
        
        result += "\n"
        result += "GENERATED SCHEMA:\n"
        result += "-" * 30 + "\n"
        result += schema_str + "\n"
        
        result += "\n"
        result += "SCHEMA INFO:\n"
        result += "-" * 30 + "\n"
        result += "Root type: " + schema.get("type", "unknown") + "\n"
        
        if "properties" in schema:
            result += "Properties: " + str(len(schema["properties"])) + "\n"
            for prop in list(schema["properties"].keys())[:10]:
                prop_type = schema["properties"][prop].get("type", "unknown")
                result += "  - " + prop + ": " + prop_type + "\n"
        
        if "items" in schema:
            result += "Array item type: " + schema["items"].get("type", "unknown") + "\n"
        
        return result
    
    def _infer_schema(self, data):
        if data is None:
            return {"type": "null"}
        
        if isinstance(data, bool):
            return {"type": "boolean"}
        
        if isinstance(data, int):
            return {"type": "integer"}
        
        if isinstance(data, float):
            return {"type": "number"}
        
        if isinstance(data, str):
            schema = {"type": "string"}
            
            if self._is_email(data):
                schema["format"] = "email"
            elif self._is_date(data):
                schema["format"] = "date"
            elif self._is_datetime(data):
                schema["format"] = "date-time"
            elif self._is_uri(data):
                schema["format"] = "uri"
            elif self._is_uuid(data):
                schema["format"] = "uuid"
            
            return schema
        
        if isinstance(data, list):
            schema = {"type": "array"}
            
            if len(data) == 0:
                schema["items"] = {}
            elif len(data) == 1:
                schema["items"] = self._infer_schema(data[0])
            else:
                item_schemas = [self._infer_schema(item) for item in data[:10]]
                
                all_same = True
                first_type = item_schemas[0].get("type")
                for s in item_schemas[1:]:
                    if s.get("type") != first_type:
                        all_same = False
                        break
                
                if all_same:
                    if first_type == "object":
                        merged = self._merge_object_schemas(item_schemas)
                        schema["items"] = merged
                    else:
                        schema["items"] = item_schemas[0]
                else:
                    schema["items"] = {"oneOf": item_schemas}
            
            return schema
        
        if isinstance(data, dict):
            schema = {"type": "object", "properties": {}, "required": []}
            
            for key, value in data.items():
                schema["properties"][key] = self._infer_schema(value)
                schema["required"].append(key)
            
            if not schema["required"]:
                del schema["required"]
            
            return schema
        
        return {"type": "string"}
    
    def _merge_object_schemas(self, schemas):
        merged = {"type": "object", "properties": {}}
        
        for schema in schemas:
            if "properties" in schema:
                for key, value in schema["properties"].items():
                    if key not in merged["properties"]:
                        merged["properties"][key] = value
        
        return merged
    
    def _is_email(self, s):
        if "@" in s and "." in s:
            parts = s.split("@")
            if len(parts) == 2 and len(parts[0]) > 0 and "." in parts[1]:
                return True
        return False
    
    def _is_date(self, s):
        import re
        if re.match(r"^\d{4}-\d{2}-\d{2}$", s):
            return True
        return False
    
    def _is_datetime(self, s):
        import re
        if re.match(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}", s):
            return True
        return False
    
    def _is_uri(self, s):
        if s.startswith("http://") or s.startswith("https://"):
            return True
        return False
    
    def _is_uuid(self, s):
        import re
        if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", s.lower()):
            return True
        return False
    
    def _validate_json(self, json_data, schema):
        parsed_data = self._parse_json(json_data)
        
        if parsed_data is None:
            return "Invalid JSON data."
        
        if not schema:
            return "Please provide a JSON schema for validation."
        
        parsed_schema = self._parse_json(schema)
        
        if parsed_schema is None:
            return "Invalid JSON schema."
        
        errors = self._validate_against_schema(parsed_data, parsed_schema, "root")
        
        result = "JSON VALIDATION\n"
        result += "=" * 50 + "\n\n"
        
        if not errors:
            result += "STATUS: VALID\n\n"
            result += "The JSON data conforms to the schema.\n"
        else:
            result += "STATUS: INVALID\n\n"
            result += "Found " + str(len(errors)) + " error(s):\n"
            result += "-" * 30 + "\n"
            
            for i, error in enumerate(errors[:20]):
                result += str(i + 1) + ". " + error + "\n"
            
            if len(errors) > 20:
                result += "\n... and " + str(len(errors) - 20) + " more errors\n"
        
        return result
    
    def _validate_against_schema(self, data, schema, path):
        errors = []
        
        expected_type = schema.get("type")
        
        if expected_type:
            actual_type = self._get_json_type(data)
            
            if expected_type == "integer" and actual_type == "number":
                if not isinstance(data, int):
                    errors.append(path + ": expected integer, got float")
            elif expected_type != actual_type:
                errors.append(path + ": expected " + expected_type + ", got " + actual_type)
                return errors
        
        if expected_type == "object" and isinstance(data, dict):
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            
            for req in required:
                if req not in data:
                    errors.append(path + ": missing required property '" + req + "'")
            
            for key, value in data.items():
                if key in properties:
                    sub_errors = self._validate_against_schema(value, properties[key], path + "." + key)
                    errors.extend(sub_errors)
        
        if expected_type == "array" and isinstance(data, list):
            items_schema = schema.get("items", {})
            
            for i, item in enumerate(data):
                sub_errors = self._validate_against_schema(item, items_schema, path + "[" + str(i) + "]")
                errors.extend(sub_errors)
            
            min_items = schema.get("minItems")
            max_items = schema.get("maxItems")
            
            if min_items and len(data) < min_items:
                errors.append(path + ": array has " + str(len(data)) + " items, minimum is " + str(min_items))
            if max_items and len(data) > max_items:
                errors.append(path + ": array has " + str(len(data)) + " items, maximum is " + str(max_items))
        
        if expected_type == "string" and isinstance(data, str):
            min_length = schema.get("minLength")
            max_length = schema.get("maxLength")
            pattern = schema.get("pattern")
            
            if min_length and len(data) < min_length:
                errors.append(path + ": string length " + str(len(data)) + " is less than minimum " + str(min_length))
            if max_length and len(data) > max_length:
                errors.append(path + ": string length " + str(len(data)) + " exceeds maximum " + str(max_length))
            
            if pattern:
                import re
                if not re.match(pattern, data):
                    errors.append(path + ": string does not match pattern '" + pattern + "'")
        
        if expected_type in ["number", "integer"] and isinstance(data, (int, float)):
            minimum = schema.get("minimum")
            maximum = schema.get("maximum")
            
            if minimum is not None and data < minimum:
                errors.append(path + ": value " + str(data) + " is less than minimum " + str(minimum))
            if maximum is not None and data > maximum:
                errors.append(path + ": value " + str(data) + " exceeds maximum " + str(maximum))
        
        return errors
    
    def _get_json_type(self, data):
        if data is None:
            return "null"
        if isinstance(data, bool):
            return "boolean"
        if isinstance(data, int):
            return "integer"
        if isinstance(data, float):
            return "number"
        if isinstance(data, str):
            return "string"
        if isinstance(data, list):
            return "array"
        if isinstance(data, dict):
            return "object"
        return "unknown"
    
    def _generate_sample(self, schema_data):
        parsed_schema = self._parse_json(schema_data)
        
        if parsed_schema is None:
            return "Invalid JSON schema."
        
        sample = self._create_sample(parsed_schema)
        
        sample_str = json.dumps(sample, indent=2)
        
        result = "SAMPLE JSON GENERATOR\n"
        result += "=" * 50 + "\n\n"
        
        result += "FROM SCHEMA:\n"
        result += "-" * 30 + "\n"
        schema_str = json.dumps(parsed_schema, indent=2)
        if len(schema_str) > 500:
            result += schema_str[:500] + "\n... (truncated)\n"
        else:
            result += schema_str + "\n"
        
        result += "\n"
        result += "GENERATED SAMPLE:\n"
        result += "-" * 30 + "\n"
        result += sample_str + "\n"
        
        return result
    
    def _create_sample(self, schema):
        schema_type = schema.get("type", "string")
        
        if schema_type == "null":
            return None
        
        if schema_type == "boolean":
            return True
        
        if schema_type == "integer":
            minimum = schema.get("minimum", 0)
            maximum = schema.get("maximum", 100)
            return int((minimum + maximum) / 2)
        
        if schema_type == "number":
            minimum = schema.get("minimum", 0.0)
            maximum = schema.get("maximum", 100.0)
            return (minimum + maximum) / 2
        
        if schema_type == "string":
            fmt = schema.get("format")
            
            if fmt == "email":
                return "user@example.com"
            elif fmt == "date":
                return "2024-01-15"
            elif fmt == "date-time":
                return "2024-01-15T10:30:00Z"
            elif fmt == "uri":
                return "https://example.com"
            elif fmt == "uuid":
                return "550e8400-e29b-41d4-a716-446655440000"
            else:
                return "string_value"
        
        if schema_type == "array":
            items_schema = schema.get("items", {"type": "string"})
            min_items = schema.get("minItems", 1)
            
            sample_items = []
            for i in range(max(1, min_items)):
                sample_items.append(self._create_sample(items_schema))
            
            return sample_items
        
        if schema_type == "object":
            properties = schema.get("properties", {})
            
            sample_obj = {}
            for key, prop_schema in properties.items():
                sample_obj[key] = self._create_sample(prop_schema)
            
            return sample_obj
        
        return "value"
    
    def _format_json(self, json_data):
        parsed = self._parse_json(json_data)
        
        if parsed is None:
            return "Invalid JSON data. Could not parse."
        
        formatted = json.dumps(parsed, indent=2, sort_keys=False, ensure_ascii=False)
        minified = json.dumps(parsed, separators=(",", ":"))
        
        result = "JSON FORMATTER\n"
        result += "=" * 50 + "\n\n"
        
        result += "FORMATTED (Pretty):\n"
        result += "-" * 30 + "\n"
        result += formatted + "\n"
        
        result += "\n"
        result += "MINIFIED:\n"
        result += "-" * 30 + "\n"
        result += minified + "\n"
        
        result += "\n"
        result += "STATISTICS:\n"
        result += "-" * 30 + "\n"
        result += "Original length: " + str(len(json_data)) + " chars\n"
        result += "Formatted length: " + str(len(formatted)) + " chars\n"
        result += "Minified length: " + str(len(minified)) + " chars\n"
        result += "Savings (minified): " + str(len(formatted) - len(minified)) + " chars\n"
        
        return result