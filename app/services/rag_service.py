import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

DB_DIR = "./chroma_db"
KB_DIR = "./knowledge_base"

def init_rag():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("Skipping RAG init: No valid Gemini API key.")
        return

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    if not os.path.exists(DB_DIR):
        print("Initializing ChromaDB from knowledge base...")
        if not os.path.exists(KB_DIR) or len(os.listdir(KB_DIR)) == 0:
            print("Knowledge base directory is empty. Cannot initialize RAG.")
            return

        loader = PyPDFDirectoryLoader(KB_DIR)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)
        
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=DB_DIR)
        print("ChromaDB initialized.")
    else:
        print("ChromaDB already exists.")

def ask_security_question(question: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        return "Please configure your GEMINI_API_KEY in the .env file to use the AI chatbot."

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")
    
    if not os.path.exists(DB_DIR):
        return "Knowledge base not initialized. Please add PDFs to the knowledge_base folder and restart."

    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    retriever = vectorstore.as_retriever()
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
    
    system_prompt = (
        "You are an AI School Security Assistant. Use the given context to answer the question. "
        "If you don't know the answer, say you don't know. "
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    response = rag_chain.invoke({"input": question})
    return response["answer"]
