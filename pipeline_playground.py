from builder.pipeline import SQLBuilderPipeline

OPENAI_API_KEY = "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"
CLICKHOUSE_PASSWORD = "4a_v433uwivSV"


pipeline = SQLBuilderPipeline(
    open_ai_api_key=OPENAI_API_KEY,
    clickhouse_password=CLICKHOUSE_PASSWORD
)


def main():
    # query = "When did we get the maximum of daily visits on the website in 2023?"
    query = "When did we get the maximum of daily visits on the website in 2023?"
    sql = pipeline.run(query)
    print(sql)


if __name__ == "__main__":
    main()