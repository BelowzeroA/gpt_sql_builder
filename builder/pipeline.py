# Run: streamlit run gpt_sql_builder/streamlit_app.py
from typing import Any

from builder.db_plugin import ClickhouseConnector
from builder.gpt_api import GPTApi
from builder.gpt_prompt_manager import GPTPromptManager

OPERATION_BUILD_SQL = "build_sql"
OPERATION_SELECT_TABLE = "select_table"
OPERATION_DESCRIBE_RESULT = "describe_result"


class SQLBuilderPipeline:
    """
    The main pipeline class that orchestrates the natural language query processing
    """
    def __init__(self, open_ai_api_key: str, clickhouse_password: str):
        self.api = GPTApi(open_ai_api_key)
        self.prompt_manager = GPTPromptManager()
        self.db_plugin = ClickhouseConnector(clickhouse_password)

    def select_table(self, query: str, tables: list) -> str:
        """Selects the table from the list of tables that matches the query"""
        params = {"query": query, "tables": tables}
        system_prompt, prompt = self.prompt_manager.get_prompt(
            OPERATION_SELECT_TABLE,
            parameters=params
        )
        response = self.api.generate(
            system_prompt,
            prompt,
            model="gpt-3.5-turbo",
            # model="gpt-4",
            max_tokens=20
        )

        table = self.prompt_manager.parse_response(
            OPERATION_SELECT_TABLE,
            response=response
        )

        return table

    def build_sql(self, query: str, tables: list) -> str:
        """Builds SQL query from the natural language query"""
        params = {"query": query, "tables": tables}
        system_prompt, prompt = self.prompt_manager.get_prompt(
            OPERATION_BUILD_SQL,
            parameters=params
        )
        response = self.api.generate(
            system_prompt,
            prompt,
            # model="gpt-3.5-turbo",
            model="gpt-4",
            max_tokens=150
        )

        sql = self.prompt_manager.parse_response(
            OPERATION_BUILD_SQL,
            response=response
        )

        return sql

    def describe_result(self, query: str, sql: str, query_result: Any) -> str:
        """Generates a description of the query result"""
        params = {"query": query, "query_result": query_result, "sql": sql}
        system_prompt, prompt = self.prompt_manager.get_prompt(
            OPERATION_DESCRIBE_RESULT,
            parameters=params
        )
        response = self.api.generate(
            system_prompt,
            prompt,
            model="gpt-3.5-turbo",
            # model="gpt-4",
            max_tokens=40
        )

        description = self.prompt_manager.parse_response(
            OPERATION_DESCRIBE_RESULT,
            response=response
        )

        return description

    def run(self, query: str) -> str:
        """Main pipeline method that orchestrates the query processing"""
        result = {}
        table_descriptions = self.db_plugin.get_table_descriptions()
        # main_table = self.select_table(query, table_descriptions)
        sql = self.build_sql(query, table_descriptions)
        result["sql"] = sql
        query_result = self.db_plugin.command(sql)
        result["data"] = query_result
        result["description"] = self.describe_result(query, sql, query_result)
        return result
