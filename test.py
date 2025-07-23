from langchain_google_genai import GoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import time

load_dotenv()

stime = time.time()
# groq_model = ChatGroq(
#     name="llama-3.1-8b-instant"
# )

model = GoogleGenerativeAI(
    model = "gemini-2.5-flash-lite-preview-06-17"
)
ans = model.invoke("hi")
etime = time.time()
print(ans)
print("Time: ",etime-stime)