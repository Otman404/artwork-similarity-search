import os
import sys
# sys.path.insert(0, '../')
sys.path.append(os.path.dirname("../"))
from config import KAGGLE_USERNAME, KAGGLE_KEY, DATA_DIR
os.environ['KAGGLE_USERNAME'] = KAGGLE_USERNAME
os.environ['KAGGLE_KEY'] = KAGGLE_KEY
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi


DATASET_NAME = "ikarus777/best-artworks-of-all-time"
DOWNLOAD_PATH = "artwork_data/"

class Dataset:
    """
    A class to download and extract files from a Kaggle dataset.
    """
    def __init__(self, dataset_name):
        """
        Initialize the dataset instance.

        Args:
            dataset_name (str): The name of the Kaggle dataset to download.
        """
        self.api = KaggleApi()
        self.api.authenticate()
        self.dataset = dataset_name

    def download(self):
        """
        Download files from the Kaggle dataset and extract them.

        Returns:
            None
        """

        if os.path.isdir(DOWNLOAD_PATH):
            print(f'{DOWNLOAD_PATH} already exists. Skipping download.')
            return           
        print(f"Downloading {self.dataset}...")
        self.api.dataset_download_files(self.dataset, path=DOWNLOAD_PATH, unzip=True)
        print("Downloaded.")

    # def unzip(self, download_path):
    #     print("Extracting data...")
    #     zf = ZipFile(self.dataset.split('/')[1]+'.zip')
    #     zf.extractall(path=download_path)
    #     zf.close()
    #     print("Done.")


if __name__ == "__main__":
    data = Dataset(DATASET_NAME)
    data.download()
    # data.unzip(DOWNLOAD_PATH)