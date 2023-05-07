from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

class VectorSearch:
    """
    A class for performing vector searches on a Qdrant collection using embeddings.
    """

    def __init__(self, encoder_name, qdrant_url, qdrant_key, collection_name):
        """
        Initializes the VectorSearch object with a SentenceTransformer encoder, Qdrant client, and collection name.
        
        :param encoder_name: The name of the encoder to use for encoding text and images into embeddings.
        :param qdrant_url: The URL of the Qdrant instance to connect to.
        :param qdrant_key: The API key for the Qdrant instance.
        :param collection_name: The name of the Qdrant collection to search.
        """
        self.encoder = SentenceTransformer(encoder_name)  # initialize the SentenceTransformer encoder
        self.qdrant_client = QdrantClient(
                url=qdrant_url, 
                api_key=qdrant_key,
            )  # initialize the Qdrant client with the given URL and API key
        self.collection_name = collection_name 

    
    def search(self, query, k):
        """
        Performs a search on the Qdrant collection using the encoded query vector and returns a list of hit payloads.
        
        :param query: The query that can be either a text or an image to encode and search for in the collection.
        :param k: The number of hits to return from the search.
        :return: A list of hit payloads containing information about the images associated with the hits.
        """
        hits = self.qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=self.encoder.encode(query).tolist(),
            limit=k
        )  # search the Qdrant collection using the encoded query vector and return the top k hits
        for hit in hits:
            print(hit.payload, "score:", hit.score)  # print the payload and score for each hit to the console

        return [hit.payload for hit in hits]  # return a list of hit payloads containing information about the images
