
from google.oauth2 import service_account
from google.cloud import storage
import streamlit as st
from datetime import datetime, timedelta
from urllib.request import urlopen
import cloudpickle as cp
import itertools


class GCP:
    def __init__(self, bucket_name="artwork-images-streamlit", path_prefix="artwork_data/"):
        """
        Initializes a GCP object with the given bucket name and path prefix.

        :param bucket_name: str, the name of the GCP bucket.
        :param path_prefix: str, the prefix path for the GCP files.
        """
        self.credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        self.storage_client = storage.Client(credentials=self.credentials)
        self.bucket_name = bucket_name
        self.bucket = self.storage_client.bucket(self.bucket_name)
        self.path_prefix = path_prefix

    def list_files(self, prefix=''):
        """
        Lists all the files in the bucket.

        :return: list of str, the names of the files in the bucket.
        """
        file_list = self.storage_client.list_blobs(self.bucket_name, prefix=self.path_prefix+prefix)
        file_list = [file.name for file in file_list]

        return file_list

    def get_image_url(self, image_name, expire_in=datetime.today() + timedelta(1)):
        """
        Returns a public URL for a single image in the bucket.

        :param image_name: str, the name of the image to retrieve the URL for.
        :param expire_in: datetime, optional argument to specify when the URL should expire.
                        The default is to expire after 1 day.
        :return: str, a URL for the requested image.
        """

        image_path = self.path_prefix + "images/" + \
            '_'.join(image_name.split('_')[:-1]) + "/" + image_name
        url = self.bucket.blob(image_path).generate_signed_url(expire_in)

        return url

    def get_artists_data(self, filename="artists_data.pkl", expire_in=datetime.today() + timedelta(1)):
        """
        Returns a dict with artists data.
        
        :param filename: str, the name of the file containing the artists data.
        :param expire_in: datetime, optional argument to specify when the URL should expire.
                        The default is to expire after 1 day.
        :return: dict, the artists data from the file.
        """
        file_path = self.path_prefix + filename
        url = self.bucket.blob(file_path).generate_signed_url(expire_in)
        data = cp.load(urlopen(url))
        return data


    def get_artist_artwork(self, artist, n, expire_in=datetime.today() + timedelta(1)):
        """
        Retrieves a list of n signed URLs for artwork images by the specified artist from Google Cloud Storage.

        :param artist: str, the name of the artist whose artworks are being retrieved.
        :param n: int, the number of artworks to retrieve.
        :param expire_in: datetime, optional argument to specify when the URL should expire.
                        The default is to expire after 1 day.
        :return: List[str], a list of signed URLs to the retrieved artworks.
        """
        file_path_prefix = self.path_prefix + "images/" + artist.replace(' ', '_')
        result = self.storage_client.list_blobs(self.bucket_name, prefix=file_path_prefix)
        url_list = []
        for image_path in itertools.islice(result, n):
            url_list.append(self.bucket.blob(image_path.name).generate_signed_url(expire_in))
        return url_list