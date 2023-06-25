import json
import os
from typing import Any

from builder.file_utils import load_list_from_file

PROMPTS_DIR = "./prompts"
master_prompt = load_list_from_file(os.path.join(PROMPTS_DIR, "master_prompt.txt"))


class GPTPromptManager:
    """Helper class to manage GPT prompts and processes GPT responses"""
    def __init__(self):
        self.prompts = self._load_prompts()

    @staticmethod
    def _load_prompts():
        prompts = {}
        for file in os.listdir(PROMPTS_DIR):
            full_path = os.path.join(PROMPTS_DIR, file)
            basename = os.path.splitext(file)[0]
            prompts[basename] = load_list_from_file(full_path)
        return prompts

    @staticmethod
    def _fill_parameter(prompt_lines: list, param_key: str, param_value):
        result_lines = []
        param_key = f"[{param_key}]"
        for line in prompt_lines:
            if param_key in line:
                if isinstance(param_value, list):
                    result_lines.extend(param_value)
                else:
                    result_lines.append(line.replace(param_key, param_value))
            else:
                result_lines.append(line)
        return result_lines

    def compose_prompt(self, state: str, parameters: dict):
        prompt = self.prompts[state]
        for param_key in parameters:
            formatter = f"_format_parameter_{param_key}"
            if hasattr(self, formatter):
                param_value = getattr(self, formatter)(parameters[param_key])
            else:
                param_value = parameters[param_key]
            prompt = self._fill_parameter(prompt, param_key, param_value)

        return "\n".join(master_prompt), "\n".join(prompt)

    def get_prompt(self, state: str, parameters: dict):
        if state not in self.prompts:
            raise ValueError("Unknown state: " + state)
        return self.compose_prompt(state, parameters)

    @staticmethod
    def _format_parameter_tables(tables: list) -> str:
        result = []
        for table in tables:
            result.append(f"Table '{table['name']}':")
            for column in table['columns']:
                result.append(f"    {column['name']}: {column['type']}")
            result.append("")
        return "\n".join(result)

    def _format_parameter_query_result(self, result: Any) -> str:
        return json.dumps(result, indent=4)

    def parse_response(self, operation, response: str) -> Any:
        parser = f"_parse_response_{operation}"
        if hasattr(self, parser):
            parser_func = getattr(self, parser)
        else:
            raise ValueError(f"No parser for {operation} operation")
        return parser_func(response)

    @staticmethod
    def _parse_response_build_sql(response: str) -> Any:
        return response.strip()

    @staticmethod
    def _parse_response_describe_result(response: str) -> Any:
        return response.strip()

    @staticmethod
    def _parse_response_select_table(response: str) -> Any:
        parts = response.split(":")
        if len(parts) != 2:
            raise ValueError("Wrong response format")
        return parts[1].strip()
