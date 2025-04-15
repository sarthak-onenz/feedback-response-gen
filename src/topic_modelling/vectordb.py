import json
import chromadb
from typing import List

from utils.models import Topic
from utils.llm import get_embedding
from utils.constants import chromadir, topics_collection_name

from sarthakai.models import Chunk
from sarthakai.vector_search.chromadb_utils import add_chunks_to_chromadb_collection, search_chromadb

def create_topics_vectordb(topics : List[Topic]):
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collection = chromadb_client.get_or_create_collection(name=topics_collection_name)

    chunks = []
    for i, topic in enumerate(topics):
        chunks.append(Chunk(text=topic.topic_name,
                            embedding=topic.embedding or get_embedding(topic.topic_name),
                            metadata={"count" : topic.count, "examples" : json.dumps(topic.examples)}
                            )
                    )
    add_chunks_to_chromadb_collection(chunks=chunks, collection=collection)

def vector_search_topics(user_message: str, embedding):
    return search_chromadb(chromadir=chromadir,
                           collection_name=topics_collection_name,
                           query=user_message,
                           embedding=embedding,
                           n_results=16)
