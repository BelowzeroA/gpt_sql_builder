import os

from builder.pipeline import SQLBuilderPipeline

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']


pipeline = SQLBuilderPipeline(
    open_ai_api_key=OPENAI_API_KEY,
    clickhouse_password=CLICKHOUSE_PASSWORD
)


def main():
    # query = "When did we get the maximum of daily visits on the website in 2023?"
    query = "When did we get the maximum of daily visits on the website in 2023?"
    # query = "What was the average CPC in Google Ads in May 2023?"
    # query = "Which platform had the highest CPC in 2023: Google or Bing?"
    sql = pipeline.run(query)
    print(sql)


if __name__ == "__main__":
    main()