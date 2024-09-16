import pandas as pd
from langchain_core.runnables.base import RunnableSequence
from datasets import Dataset


def populate_eval_dataset(df_eval_qs: pd.DataFrame, chain: RunnableSequence) -> Dataset:
    data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}
    
    for idx, row in df_eval_qs.iterrows():
        res = chain.invoke({'input': row['question']})
        
        data["question"].append(row['question'])
        data["ground_truth"].append(row['ground_truth'])
        data["answer"].append(res['answer'])
        data["contexts"].append([doc.page_content for doc in res['context']])
    
    dataset = Dataset.from_dict(data)

    return dataset