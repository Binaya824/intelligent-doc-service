from typing import List
from langchain_community.embeddings import DeepInfraEmbeddings

from app.core.config import settings
from app.schemas.document import PageData
from app.utils.chunking import chunk_page
from app.db.vector_db import QdrantService
import logging
from time import sleep
from qdrant_client.models import PointStruct
from app.agents.assistant_agent import AssistantAgent

logger = logging.getLogger(__name__)
class AssistantService:
    def __init__(self):
        self.embeddings = DeepInfraEmbeddings(
            model_id=settings.EMBEDDINGS_MODEL,
            deepinfra_api_token=settings.API_KEY,
        )
        self.qdrant_service = QdrantService()
        self.qdrant_client = self.qdrant_service.get_client()
        self.assistant_agent = AssistantAgent()
        
        
    def safe_upsert(self, collection_name, points, retries=3, delay=2):
        try:
            # Attempt the upsert
            self.qdrant_client.upsert(collection_name=collection_name, points=points)
            logger.info(f"Successfully upserted into collection {collection_name}")
        except Exception as e:
            if retries > 0:
                # Log error and retry
                logger.error(f"Error while upserting. Retrying... {retries} attempts left. Error: {e}")
                sleep(delay)
                # Recursively retry the upsert
                self.safe_upsert(collection_name, points, retries-1, delay)
            else:
                # Log error after exhausting retries
                logger.error(f"Error in posting chunks after {retries} retries: {e}")
                raise e

    def create_embeddings(
        self,
        collection_name: str,
        pages: List[PageData],
        batch_size: int = 32,
    ):
        """
        Embed chunks in batches.
        This method is SYNC by design (LangChain client is sync).
        """
        
        self.qdrant_service.ensure_collection(name=collection_name)
        
        point_id = 0
        total_chunk = 0
        points = []
        
        for page_index , data in enumerate(pages):
            chunks = chunk_page(data)
            total_chunk += len(chunks)
            
            for i , chunk in enumerate(chunks):
                print(f"Embedding Page {data["page"]} Chunk {i+1}/{len(chunks)} data: {chunk.text[:30]}...")
                vec_chunk = self.embeddings.embed_documents([chunk.text])[0]
                print(f"\n--- Chunk {i + 1} on Page {page_index} --- Point ---{point_id}")
                print(len(vec_chunk))
                payload = {
                        "page": page_index,
                        "chunk_index": i,
                        "text": chunk.text,
                        "is_last": True if (point_id == total_chunk-1) and (page_index == len(pages)-1) else False
                    }
                print("payload  *******" , payload)
                point = PointStruct(id=point_id, vector=vec_chunk, payload=payload)
                points.append(point)
                if len(points) >= batch_size:
                    self.safe_upsert(collection_name, points)
                    points = []
                point_id+=1
            
        if points:
            self.safe_upsert(collection_name, points)
            points = [] 

        point_id = 0
        
        
    def rag_query(self, collection_name, query):
        """
        Perform a RAG query on the specified collection.
        """
        logger.info(f"Performing RAG query on collection {collection_name} with query: {query}")
        query_vector = self.embeddings.embed_documents([query])[0]
        search_result = self.qdrant_service.get_client().query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=4,  # Adjust the limit as needed
            score_threshold=0.3
        )
        print(f"Top matches from document '{collection_name}':")
        print(f"Query: {query}")
        print(f"results:" , len(search_result.points) , search_result.points)
        
        neighbors = set()  # use set to avoid duplicates

        # Step 1: Print search results and collect neighbor IDs
        for i, result in enumerate(search_result.points):
            # print("-" * 50)
            # print(f"🔹 Search Result {i}")
            # print(f"Score: {result.score}")
            # print(f"Page: {result.payload.get('page')}")
            # print(f"Chunk Index: {result.payload.get('chunk_index')}")
            # print(f"Text:\n{result.payload.get('text')}")

            # Add neighbor IDs based on position
            if result.id == 0:
                neighbors.add(result.id + 1)
            elif result.payload.get("is_last"):
                neighbors.add(result.id - 1)
            else:
                neighbors.update([result.id - 1, result.id + 1])

        # Step 2: Fetch neighbors
        neighbors_vec = self.qdrant_service.get_client().retrieve(
            collection_name=collection_name,
            ids=list(neighbors)
        )

        # Step 3: Combine original results and neighbors, sort by ID
        all_results = list(search_result.points) + list(neighbors_vec)
        all_results_sorted = sorted(all_results, key=lambda p: p.id)

        # Step 4: Print and build final text list
        sorted_texts = []
        print("\n🔁 Combined and Sorted Chunks by Point ID")
        for i, result in enumerate(all_results_sorted):
            print("-" * 50)
            print(f"Point ID: {result.id}")
            print(f"Page: {result.payload.get('page')}, Chunk Index: {result.payload.get('chunk_index')}")
            print(f"Text:\n{result.payload.get('text')}")
            sorted_texts.append(result.payload.get("text"))

        # Optional: Use `sorted_texts` further
        print("\n✅ Final Texts List (Sorted by ID):" , len(sorted_texts))
        print(sorted_texts)
        response = self.assistant_agent.send_message(sorted_texts, query)
        return response