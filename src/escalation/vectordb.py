import chromadb
from typing import List
from slugify import slugify

from utils.models import EscalationTopic
from utils.llm import get_embedding
from utils.constants import chromadir, escalation_topics_collection_name

from sarthakai.models import Chunk
from sarthakai.vector_search.chromadb_utils import add_chunks_to_chromadb_collection, search_chromadb

def create_escalation_topics_vectordb(escalation_topics : List[EscalationTopic]):
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collection_name = slugify(escalation_topics_collection_name)
    collection = chromadb_client.get_or_create_collection(name=collection_name)

    chunks = [Chunk(text=topic.statement,
                    embedding=get_embedding(topic.statement),
                    #metadata={"count" : topic.count, "examples" : str(topic.examples)}
                    )
              for topic in escalation_topics
              ]
    add_chunks_to_chromadb_collection(chunks=chunks, collection=collection)


def vector_search_escalation_topics(user_message: str):
    return search_chromadb(chromadir=chromadir,
                           collection_name=escalation_topics_collection_name,
                           query=user_message,
                           n_results=3)
