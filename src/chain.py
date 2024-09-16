
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence

def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def rag_basic_with_sources(llm, retriever) -> RunnableSequence:
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Keep the answer concrete and use only infomration from the context"
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )



    # This Runnable takes a dict with keys 'input' and 'context',
    # formats them into a prompt, and generates a response.
    rag_chain_from_docs = (
        {
            "input": lambda x: x["input"],  # input query
            "context": lambda x: format_docs(x["context"]),  # context
        }
        | prompt  # format query and context into prompt
        | llm  # generate response
        | StrOutputParser()  # coerce to string
    )

    # Pass input query to retriever
    retrieve_docs = (lambda x: x["input"]) | retriever

    # Below, we chain `.assign` calls. This takes a dict and successively
    # adds keys-- "context" and "answer"-- where the value for each key
    # is determined by a Runnable. The Runnable operates on all existing
    # keys in the dict.
    chain = (RunnablePassthrough
            .assign(context=retrieve_docs)
            .assign(answer=rag_chain_from_docs)
    )

    return chain