import os
import toml


home = os.path.expanduser("~")


secrets_path = os.path.join(home, '.streamlit', 'secrets.toml')

config = toml.load(secrets_path)

CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
IMAGES_DIR = os.path.join(CODE_DIR ,'data', 'artwork_data','images','combined')
KAGGLE_USERNAME = config['Kaggle']['KAGGLE_USERNAME']
KAGGLE_KEY = config['Kaggle']['KAGGLE_KEY']

COLLECTION_NAME = config['Database']['COLLECTION_NAME']

EMBEDDER = config['Database']['EMBEDDER_NAME']
QDRANT_URL = config['Database']['QDRANT_URL']
QDRANT_KEY = config['Database']['QDRANT_KEY']

