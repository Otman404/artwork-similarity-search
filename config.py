import os
import streamlit as st



CODE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CODE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
IMAGES_DIR = os.path.join(CODE_DIR ,'data', 'artwork_data','images','combined')
KAGGLE_USERNAME = st.secrets['Kaggle']['KAGGLE_USERNAME']
KAGGLE_KEY = st.secrets['Kaggle']['KAGGLE_KEY']

COLLECTION_NAME = st.secrets['Database']['COLLECTION_NAME']

EMBEDDER = st.secrets['Database']['EMBEDDER_NAME']
QDRANT_URL = st.secrets['Database']['QDRANT_URL']
QDRANT_KEY = st.secrets['Database']['QDRANT_KEY']

GCP_CREDS = st.secrets["gcp_service_account"]