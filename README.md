# 🤖 AI Notes Q&A - RAG Application

A secure, session-based RAG (Retrieval-Augmented Generation) application that allows you to upload PDF documents and ask questions using AI. Built with FastAPI, LangChain, and Google's Gemini 2.5 Flash Lite.

## 🔒 Privacy & Security Features

### ✅ PDF-Only Responses
- **Strictly PDF-based answers** - AI uses ONLY information from your uploaded PDF
- **No external knowledge** - AI will not use information from its training data
- **Explicit "I don't know"** - If information isn't in the PDF, AI clearly states it

### 🗑️ Automatic Data Deletion
- **Session-based storage** - Each user gets a unique session ID
- **Auto-cleanup on close** - When you close the browser window/tab, your PDF and data are automatically deleted
- **No data persistence** - Your documents are never stored permanently
- **Server shutdown cleanup** - All sessions are cleaned when server restarts

## ✨ Features

### User Interface
- 🎨 **Modern Gradient Design** - Beautiful purple gradient theme with glass morphism effects
- 📱 **Responsive Layout** - Works perfectly on desktop, tablet, and mobile devices
- 🎭 **Smooth Animations** - Typing indicators, fade-ins, and loading states
- 🎯 **Intuitive Workflow** - Clear step-by-step process (Upload → Ask → Answer)
- 📊 **Real-time Feedback** - Live status updates and error handling

### Core Functionality
- 📄 **PDF Upload & Processing** - Drag-and-drop file upload with validation
- 🔍 **Smart Chunking** - Intelligent text splitting for optimal retrieval
- 🧠 **Vector Search** - Semantic search using embeddings
- 💬 **Streaming Responses** - Real-time AI answer streaming
- 🔐 **Session Management** - Unique session per user for data isolation

### Technical Features
- ⚡ **FastAPI Backend** - High-performance async API
- 🔗 **LangChain Integration** - Production-grade RAG pipeline
- 🎯 **Accurate Retrieval** - Top-3 similarity search for best context
- 🛡️ **Error Handling** - Comprehensive validation and user-friendly errors
- 🔐 **File Validation** - Type checking and size limits (10MB max)

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone or download the project**
   ```bash
   cd ai-notes-qa
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open in browser**
   
   Navigate to: `http://127.0.0.1:8000`

## 📖 Usage Guide

### 1. Upload a PDF
- When you open the page, a unique session is automatically created
- Click the upload area or drag and drop a PDF file
- Maximum file size: 10MB
- Wait for the indexing process to complete (green checkmark appears)

### 2. Ask Questions
- Type your question in the text area
- Questions can be about any content in the uploaded PDF
- Click "Ask AI" and watch the answer stream in real-time

### 3. Get Answers
- AI provides concise answers (2-4 sentences maximum)
- **Answers are based ONLY on the PDF content** - no external knowledge used
- If information isn't found, AI will respond: "I don't have this information in the provided PDF."

### 4. Automatic Cleanup
- When you close the browser tab/window, your session data is automatically deleted
- This includes: uploaded PDF file, vector embeddings, and session information
- You can safely close the window knowing your data won't persist

### Example Questions
- "What are the main topics covered in this document?"
- "Summarize the key findings from chapter 3"
- "What conclusions does the author make?"
- "Explain the methodology used in this research"
- **"How many times is 'machine learning' mentioned?"** ← NEW
- **"Count the number of references to AI"** ← NEW
- **"What's the total number of chapters?"** ← NEW

## 🏗️ Project Structure

```
ai-notes-qa/
├── main.py                 # FastAPI application with session management
├── rag_pipeline.py         # RAG logic (vectorstore, retrieval, LLM)
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Environment variables template
├── templates/
│   └── index.html         # Frontend UI with auto-cleanup
├── uploads/               # Temporary session-based PDF storage
└── data/
    └── chroma_*/         # Session-specific vector databases
```

## 🔧 How It Works

### Session Management
1. **Session Creation**: When a user visits the page, a unique UUID session ID is generated
2. **File Upload**: PDF is saved as `uploads/{session_id}_{filename}.pdf`
3. **Vector Store**: Created in `data/chroma_{session_id}/` directory
4. **Question Answering**: Uses session-specific RAG chain to answer questions

### Automatic Cleanup
1. **Window Close Detection**: JavaScript `beforeunload` and `unload` events trigger cleanup
2. **Beacon API**: Reliable cleanup signal sent even if window is closing
3. **Server-side Cleanup**: Deletes PDF file and vector database for the session
4. **Shutdown Cleanup**: All sessions cleaned when server stops

### PDF-Only Response System
The AI is configured with strict rules:
- Only use information from the provided PDF context
- Never use external knowledge or training data
- Explicitly state when information is not found
- Provide concise answers (2-4 sentences)

## 🔧 Configuration

### RAG Pipeline Settings

In `rag_pipeline.py`, you can adjust:

```python
# Text chunking
chunk_size=500          # Characters per chunk
chunk_overlap=100       # Overlap between chunks

# Retrieval
search_kwargs={"k": 3}  # Number of chunks to retrieve

# LLM settings
temperature=0           # Deterministic responses
streaming=True         # Enable response streaming
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Render main UI |
| `/create-session` | POST | Create a new session ID |
| `/upload` | POST | Upload and index PDF (requires session_id) |
| `/ask` | POST | Ask a question (requires session_id) |
| `/status/{session_id}` | GET | Check if PDF is loaded |
| `/cleanup/{session_id}` | DELETE | Manual cleanup (auto-called on window close) |

## 🎯 Key Improvements

### Security & Privacy
- ✅ Session-based isolation (each user has separate data)
- ✅ Automatic data deletion on window close
- ✅ No permanent data storage
- ✅ PDF-only responses (no external knowledge)

### Code Quality
- ✅ Session management with UUID
- ✅ Automatic cleanup with atexit hooks
- ✅ Navigator.sendBeacon for reliable cleanup
- ✅ Comprehensive error handling
- ✅ Better async/await patterns

### User Experience
- ✅ Clear privacy notice in footer
- ✅ Visual indicator that answers are PDF-only
- ✅ Session-transparent to user
- ✅ Automatic session creation
- ✅ No manual cleanup needed

## 🐛 Troubleshooting

### Common Issues

**"Please upload a PDF first"**
- Make sure you've uploaded and indexed a PDF before asking questions
- Check if the green status badge appears after upload
- If page was refreshed, you'll need to upload the PDF again

**Answers say "I don't have this information"**
- The information is genuinely not in your PDF
- Try rephrasing your question
- Check if you're asking about the right document

**Upload fails**
- Check file size (must be under 10MB)
- Ensure file is a valid PDF
- Check your internet connection

**Session cleanup not working**
- Modern browsers support this feature reliably
- Data is also cleaned on server restart
- For manual cleanup, refresh the page

## 📝 Future Enhancements

Potential improvements for future versions:
- 📚 Multi-document support per session
- 🔍 Page number citations
- 📥 Export Q&A history
- 🌙 Dark mode toggle
- 🔄 Question suggestions based on PDF content
- 📊 Session analytics dashboard
- ⏱️ Session timeout (auto-cleanup after inactivity)

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [LangChain](https://langchain.com/) - RAG orchestration
- [Google Gemini](https://deepmind.google/technologies/gemini/) - LLM
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Sentence Transformers](https://www.sbert.net/) - Embeddings
- [Tailwind CSS](https://tailwindcss.com/) - Styling

## 📄 License

This project is open source and available for educational purposes.

## 🔐 Privacy Statement

This application:
- Does NOT store your PDFs permanently
- Does NOT use your data for training
- Does NOT share your data with third parties
- Automatically DELETES all data when you close the window
- Uses session-based storage that expires

Your privacy is our priority! 🛡️

---

**Happy questioning! 🎉**

For questions or issues, feel free to reach out or open an issue on the repository.
