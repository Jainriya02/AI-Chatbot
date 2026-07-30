from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv(override=True)

CHROMA_PATH = "./chromadb"


def load_documents(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()


def split_documents(documents, chunk_size=300, chunk_overlap=30):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def create_vector_db():
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )


vectorstore = create_vector_db()

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)


def ask_rag(question):

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    return {
        "context": context,
        "documents": docs
    }