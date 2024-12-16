from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")
class SummarizeRequest(BaseModel):
    url: str



@app.get("/summarize", response_class=HTMLResponse)
async def summarize_page(url: str):
    try:
         # Load webpage content using LangChain's WebBaseLoader
        loader = WebBaseLoader(url)
        page_data = loader.load().pop().page_content


        # Initialize OpenAI LLM with LangChain
        llm = ChatOpenAI(model="gpt-4o", api_key=api_key)  # Replace with your API key


        prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the page of a website.
        You are an advanced summarization assistant. Your task is to read the content provided, 
            understand the key points, and generate a detailed summary. Ensure the following:

            1. Capture all essential topics, arguments, or details presented in the text.
            2. Structure the summary into clear paragraphs with headings if needed.
            3. Highlight any significant facts, statistics, or takeaways.
            4. Maintain a professional tone suitable for readers who need an in-depth understanding.    
        """
)

        chain_extract = prompt_extract | llm 
        res = chain_extract.invoke(input={'page_data':page_data})




        # Render the summary in a new page
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Summary</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; }}
                    h1 {{ color: #333; }}
                    p {{ line-height: 1.6; }}
                </style>
            </head>
            <body>
                <h1>Summary</h1>
                <p>{res.content}</p>
            </body>
            </html>
            """
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)