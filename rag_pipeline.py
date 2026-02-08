import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()

# OPTIMIZATION: Cache embeddings model (load once, reuse)


def build_vectorstore(pdf_path: str):
    """
    Load PDF, split into chunks, and create vector store - OPTIMIZED VERSION
    """
    try:
        # Load PDF using PyMuPDF
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()
        
        if not documents:
            raise ValueError("PDF appears to be empty or unreadable")

        # OPTIMIZATION: Larger chunks = fewer chunks to embed = faster
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = splitter.split_documents(documents)

        # OPTIMIZATION: Use cached embeddings model
        embeddings = GoogleGenerativeAIEmbeddings(
         model="models/embedding-001"
        )

        # Create vectorstore with optimized settings
        vectorstore = Chroma.from_documents(
          documents=chunks,
          embedding=embeddings
        )


        print(f"✅ Indexed {len(chunks)} chunks from PDF")
        return vectorstore
    
    except Exception as e:
        raise Exception(f"Error building vectorstore: {str(e)}")


def get_rag_chain(vectorstore):
    """
    Create RAG chain with retriever and LLM - STRICTLY PDF-only responses
    """
    try:
        # OPTIMIZATION: Reduced k from 5 to 4 for faster retrieval
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )

        # Using gemini-pro (most stable, 50 requests/day free)
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0.3,
            streaming=True,
            max_retries=2
        )

        # FIXED: Correct prompt format for LangChain 0.2.x
        # Must use {context} and {input} as variable names
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a PDF document assistant. Your ONLY job is to answer questions using EXCLUSIVELY the information provided in the context below.

CRITICAL RULES:
1. ONLY use information from the context below - NEVER use external knowledge
2. If the answer is NOT in the context, you MUST respond: "I don't have this information in the provided PDF."
3. Do NOT make assumptions or inferences beyond what's explicitly stated
4. Do NOT add information from your training data
5. Keep responses BRIEF - 1-3 sentences maximum (conversational style)
6. For counting questions (e.g., "how many times", "count", "number of"):
   - Count ALL occurrences in the provided context
   - Give the exact count number
   - Example: "The term appears 5 times in the document."

Context from PDF:
{context}"""),
            ("human", "{input}")
        ])

        # Create document chain
        document_chain = create_stuff_documents_chain(
            llm=llm,
            prompt=prompt
        )

        # Create retrieval chain
        rag_chain = create_retrieval_chain(
            retriever=retriever,
            combine_docs_chain=document_chain
        )

        return rag_chain
    
    except Exception as e:
        raise Exception(f"Error creating RAG chain: {str(e)}")