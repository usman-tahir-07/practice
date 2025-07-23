from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import time

load_dotenv()

# loader_stime = time.time()
# loader = PyPDFLoader("Dopamine Nation.pdf")
# doc = loader.load()
# loader_etime = time.time()
# print("Loading Time: ",loader_etime-loader_stime)

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size = 1000,
#     chunk_overlap = 30
# )
# chunked_doc = splitter.split_documents(doc)

google_embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

chroma_stime = time.time()
pc = Pinecone()
index_name = "practice"
if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
index = pc.Index(index_name)
vector_store = PineconeVectorStore(index=index, embedding=google_embedding)
# vector_store.add_documents(chunked_doc)
chroma_etime = time.time()
print("Pinecone time: ",chroma_etime-chroma_stime)

ss_stime = time.time()
results = vector_store.similarity_search(query="What is pleasure",k=3)
for result in results:
    print(result)
ss_etime = time.time()
print("Similarity search time: ",ss_etime-ss_stime)

# prompt = PromptTemplate.from_template(
#     "Can u tell me the meaning of the {name}"
# )

# ai_model = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash"
# )
# chain = prompt | ai_model | StrOutputParser()
# start_time = time.time()
# ans = chain.invoke({"name":"Usman"})
# end_time = time.time()
# print(ans)
# print("Time: ",end_time-start_time)