from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

model = init_chat_model("google_genai:gemini-2.5-flash", temperature=0)
response = model.invoke("Say hello in one sentence.")
print(response.content)
