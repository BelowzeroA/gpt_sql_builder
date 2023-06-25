import os

import pandas as pd

from builder.pipeline import SQLBuilderPipeline

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
CLICKHOUSE_PASSWORD = os.environ['CLICKHOUSE_PASSWORD']


def _is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def check_results(result, gold_label):
    if isinstance(result, list):
        value = result[0]
    else:
        value = result

    if _is_float(gold_label):
        return abs(float(value) - float(gold_label)) < 1e-4

    return value == gold_label


def main():
    df = pd.read_csv("data/test_queries.csv")
    pipeline = SQLBuilderPipeline(OPENAI_API_KEY, CLICKHOUSE_PASSWORD)
    matches = 0
    for i, row in df.iterrows():
        query = row["query"]
        result = pipeline.run(query)
        gold_label = row["result"]
        if check_results(result['data'], gold_label):
            matches += 1
    accuracy = matches / len(df)
    print(f"Accuracy: {accuracy}")


if __name__ == "__main__":
    main()