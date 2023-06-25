import clickhouse_connect


DB_HOST = 'rpfd7cscze.eu-west-1.aws.clickhouse.cloud'
PORT = 443
USER = 'default'


class ClickhouseConnector:

    def __init__(self, password: str):
        self.client = clickhouse_connect.get_client(
            host=DB_HOST,
            port=PORT,
            username=USER,
            password=password
        )

    def get_table_descriptions(self):
        result = self.client.command('Show tables')
        tables = result.split('\n')
        descriptions = []
        for table in tables:
            result = self.client.command(f'DESCRIBE TABLE {table}')
            fields_num = len(result) // 6
            table_descr = {"name": table, "columns": []}
            for i in range(fields_num):
                field_description = {
                    "name": result[i * 6].strip("\n"),
                    "type": result[i * 6 + 1]
                }
                table_descr["columns"].append(field_description)
            descriptions.append(table_descr)
        return descriptions

    def command(self, query: str):
        result = self.client.command(query)
        return result
