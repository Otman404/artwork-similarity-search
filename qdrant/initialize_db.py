
from config import QDRANT_URL, QDRANT_KEY, EMBEDDER, COLLECTION_NAME, IMAGES_DIR
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
from PIL import Image
from tqdm import tqdm
import os
import sys
# Add the parent directory to the system path to import the config.py file
sys.path.append(os.path.dirname("../"))


class Initialize:
    """
    Initialize Qdrant database and create a new collection
    """

    def __init__(self, qdrant_url, qdrant_key, encoder_name):
        """
        Initialize the QdrantClient with the given parameters

        :param qdrant_url: URL of the Qdrant database
        :type qdrant_url: str
        :param qdrant_key: API key for the Qdrant database
        :type qdrant_key: str
        :param encoder_name: Name of the model to use
        :type encoder_name: str
        """
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_key,
        )
        self.encoder = SentenceTransformer(encoder_name)

    def create_collection(self, collection_name):
        """
        Create a new collection in the Qdrant database

        :param collection_name: Name of the collection to create
        :type collection_name: str
        """

        self.qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=512, distance=Distance.COSINE),
        )

    def upsert_data(self, collection_name):
        """
        Insert or update image data in the specified Qdrant collection

        :param collection_name: Name of the collection to insert or update the data in
        :type collection_name: str
        """
        # Generate a PointStruct with an id, vector and metadata for each image in the IMAGES_DIR

        self.qdrant_client.upsert(
            collection_name=collection_name,
            wait=True,
            points=[
                # Generate a PointStruct with an id, vector and metadata for each image in the IMAGES_DIR
                PointStruct(
                            id=id, 
                            vector=self.encoder.encode(Image.open(os.path.join(IMAGES_DIR, img))).tolist(), 
                            payload={
                                'artist': ' '.join(img.split('_')[:-1]),  # Extract artist name from image file name
                                'image_name': img # Store image file name
                                } 
                                ) for id, img in tqdm(enumerate(os.listdir(IMAGES_DIR)))
                                ]
        )


if __name__ == '__main__':
    db_initialize = Initialize(QDRANT_URL, QDRANT_KEY, EMBEDDER)
    db_initialize.create_collection(COLLECTION_NAME)
    db_initialize.upsert_data(COLLECTION_NAME)
