import chromadb
from typing import List

from utils.models import EscalationTopic
from utils.llm import get_embedding
from utils.constants import chromadir, escalation_topics_collection_name

from sarthakai.models import Chunk
from sarthakai.vector_search.chromadb_utils import add_chunks_to_chromadb_collection, search_chromadb

def create_escalation_topics_vectordb(escalation_topics : List[EscalationTopic]):
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collection = chromadb_client.get_or_create_collection(name=escalation_topics_collection_name)

    chunks = []
    for i, topic in enumerate(escalation_topics):
        print("Getting embedding for chunk", i)
        chunks.append(Chunk(text=topic.statement,
                            embedding=get_embedding(topic.statement),
                            #metadata={"count" : topic.count, "examples" : str(topic.examples)}
                            )
                    )
              
              
    add_chunks_to_chromadb_collection(chunks=chunks, collection=collection)


def vector_search_escalation_topics(user_message: str, embedding):
    return search_chromadb(chromadir=chromadir,
                           collection_name=escalation_topics_collection_name,
                           query=user_message,
                           embedding=embedding,
                           n_results=3)
