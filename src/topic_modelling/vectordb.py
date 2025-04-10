import chromadb
from typing import List
from slugify import slugify

from utils.models import Topic
from utils.llm import get_embedding
from utils.constants import chromadir, topics_collection_name

from sarthakai.models import Chunk
from sarthakai.vector_search.chromadb_utils import get_or_create_chromadb_collection, add_chunks_to_chromadb_collection

def create_topics_vectordb(topics : List[Topic]):
    chromadb_client = chromadb.PersistentClient(path=chromadir)
    collection_name = slugify(topics_collection_name)
    collection = chromadb_client.get_or_create_collection(name=topics_collection_name)

    chunks = [Chunk(text=topic.topic_name, embedding=get_embedding(topic.topic_name), metadata={"count" : topic.count, "examples" : str(topic.examples)}) for topic in topics]
    add_chunks_to_chromadb_collection(chunks=chunks, collection=collection)