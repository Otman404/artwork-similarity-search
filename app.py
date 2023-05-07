import streamlit as st
import io
from qdrant.vector_searcher import VectorSearch
from config import QDRANT_URL, QDRANT_KEY, EMBEDDER, COLLECTION_NAME
from PIL import Image
from data.from_gcp_bucket import GCP
import requests
from io import BytesIO

st.set_page_config(
    page_title="Artwork Search", layout="centered", page_icon="./images/icon.png"
)


vectorsearch = VectorSearch(encoder_name=st.secrets['Database']['EMBEDDER_NAME'], qdrant_url=st.secrets['Database']['QDRANT_URL'],
                            qdrant_key=st.secrets['Database']['QDRANT_KEY'], collection_name=st.secrets['Database']['COLLECTION_NAME'])
gcp = GCP()

st.sidebar.image("images/header_sidebar.png")
st.sidebar.title("Vector Search Engine")
st.sidebar.caption("Easily find similar artworks.")


st.sidebar.markdown("This app uses the CLIP model to encode images and stores the embeddings in a vector database called [Qdrant](https://qdrant.tech/). Check out their documentation [here](https://qdrant.tech/documentation/), ", unsafe_allow_html=True)


st.sidebar.markdown("Source code can be found [here]( https://github.com/Otman404/artwork-similarity-search)")
st.sidebar.markdown("Made by [Otmane Boughaba](https://www.linkedin.com/in/otmaneboughaba/)")


st.image("images/header.png")
search_option = st.selectbox(
    'How would you like to search for similar artworks?',
    ('Image search', 'Text search'))


image_bytes = None
artwork_desc = ""

if search_option == 'Image search':
    st.markdown('### Search for artworks similar to the uploaded image.')
    uploaded_file = st.file_uploader("Upload image", type=[
                                     "png", "jpeg", "jpg"], accept_multiple_files=False, key=None, help="upload image")
    if uploaded_file:
        # To read file as bytes
        image_bytes = uploaded_file.getvalue()
        st.image(image_bytes, width=400)
else:
    artwork_desc = st.text_input("Describe the artwork")

if image_bytes or artwork_desc:
    artists_data = gcp.get_artists_data()

    k = st.slider(label='Choose how many similar images to get',
                  min_value=1, max_value=10, step=1, value=3)

    if st.button('Search'):

        if not image_bytes and not artwork_desc:
            st.write("error")

        elif image_bytes:
            with st.spinner('Searching the vector database for similar artworks'):
                search_result = vectorsearch.search(
                    Image.open(io.BytesIO(image_bytes)), k)
        elif artwork_desc:
            with st.spinner("Searching for atwork that matches your description..."):
                search_result = vectorsearch.search(artwork_desc, k)

        artists_data = gcp.get_artists_data()

        
        st.title("Image search result")
        for id, r in enumerate(search_result):
            st.subheader(f"{r['artist']}")
            st.markdown(
                f"{artists_data[r['artist']]['nationality']} - (*{artists_data[r['artist']]['years']}*)")
            st.markdown(f"Genre: {artists_data[r['artist']]['genre']}")
            st.write(artists_data[r['artist']]['bio'])
            st.markdown(
                f"[*Learn more*]({artists_data[r['artist']]['wikipedia']})")
            st.image(gcp.get_image_url(
                r['image_name']), caption=r['artist'], width=400)
            with st.expander(f"See artworks from {r['artist']}"):
                c1, c2, c3, c4 = st.columns(4)
                for img_url, c in zip(gcp.get_artist_artwork(r['artist'] ,4), [c1,c2,c3,c4]):
                    r = requests.get(img_url)
                    image = Image.open(BytesIO(r.content)).resize((400,400), Image.LANCZOS)
                    c.image(image)
            st.divider()