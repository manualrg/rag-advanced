import hashlib
from typing import List

import pandas as pd
from langchain_core.runnables.base import RunnableSequence
from datasets import Dataset
import langfuse

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



def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()


def trace_evaluation(
    client_langfuse: langfuse.client.LangfuseClient,
    trace_name: str,
    dataset: pd.DataFrame,
    metrics: List[str],
    *args,
    **kwargs
):
    
    lst_traces_id = []
    for idx, row in dataset.iterrows():
    
        question = row['question']
        contexts = row['contexts'].tolist()
        answer = row['answer']
        ground_truth = row['ground_truth']
        id_trace = hash_string(question + answer)
        lst_traces_id.append(id_trace)
        
        trace = client_langfuse.trace(  # https://langfuse.com/docs/sdk/python/low-level-sdk#span
            name = trace_name,
            id=id_trace,
            *args,
            **kwargs
        )
        
        trace.span(
            name = "retrieval",
            input={'question': question},
            output={'contexts': contexts}
        )
        trace.span(
            name = "generation",
            input={'question': question, 'contexts': contexts},
            output={'answer': answer},
            metadata={"ground_truth": ground_truth}
        )
        
        for metric_name in metrics:
            client_langfuse.score(
                        name=metric_name,
                        value=row[metric_name],
                        trace_id=id_trace
                    )

    # await that Langfuse SDK has processed all events before trying to retrieve it in the next step
    client_langfuse.flush()

    dataset_with_traces_id = dataset.copy().assign(id_trace=lst_traces_id)
    return  dataset_with_traces_id
