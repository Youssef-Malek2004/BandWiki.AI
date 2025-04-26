from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import CHROMA_DIR, PRIMARY_TEXT_PATH, EMBEDDING_MODEL


def get_chroma_db():
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    if not CHROMA_DIR.exists():
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        loader = TextLoader(str(PRIMARY_TEXT_PATH))
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        db = Chroma.from_documents(
            chunks,
            embedding,
            persist_directory=str(CHROMA_DIR)
        )
    else:
        db = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding
        )
    return db