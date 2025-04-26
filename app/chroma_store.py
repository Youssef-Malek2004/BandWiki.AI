from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import CHROMA_DIR, PRIMARY_TEXT_PATH, EMBEDDING_MODEL
from datetime import datetime
from pathlib import Path


def get_chroma_db():
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if not CHROMA_DIR.exists():
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)

        all_docs = []

        for band_file in Path(PRIMARY_TEXT_PATH).glob("*.txt"):
            band_slug = band_file.stem  # "ac_dc"
            band_name = band_slug.replace("_", " ").title()  # "Ac Dc"

            loader = TextLoader(str(band_file))
            docs = loader.load()

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)

            for chunk in chunks:
                chunk.metadata = {
                    "band": band_name,
                    "band_slug": band_slug,
                    "source": "Wikipedia",
                    "doc_type": "band_profile",
                    "date_added": datetime.utcnow().isoformat()
                }

            all_docs.extend(chunks)

        db = Chroma.from_documents(
            all_docs,
            embedding,
            persist_directory=str(CHROMA_DIR)
        )
    else:
        db = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding
        )

    return db