# 📁 Complete File Structure for Vercel Deployment

## Your Project Structure Should Look Like This:

```
neural-pdf-ai/                          # Your project root folder
│
├── main.py                             # ✅ FastAPI application (Vercel-compatible)
├── rag_pipeline.py                     # ✅ RAG logic with PyMuPDF
├── requirements.txt                    # ✅ Python dependencies
├── vercel.json                         # ✅ Vercel configuration
├── .vercelignore                       # ✅ Files to exclude from deployment
├── .env                                # ⚠️  LOCAL ONLY - DO NOT COMMIT
├── .env.example                        # ✅ Template for environment variables
├── .gitignore                          # ✅ Git ignore file
├── README.md                           # ✅ Project documentation
├── VERCEL_DEPLOYMENT.md               # ✅ Deployment guide
│
└── templates/                          # ✅ HTML templates folder
    └── index.html                      # ✅ Ultra-modern AI interface
```

## ✅ Required Files (Must Have)

### 1. **main.py** - Backend Application
- FastAPI app with Mangum handler for serverless
- Session management
- Upload, ask, cleanup endpoints
- Uses temp directories for Vercel

### 2. **rag_pipeline.py** - RAG Logic
- PyMuPDFLoader for PDF processing
- HuggingFace embeddings
- ChromaDB vector store
- Gemini AI integration

### 3. **requirements.txt** - Dependencies
```txt
fastapi
uvicorn
python-multipart==0.0.20
jinja2==3.1.4
pydantic==2.10.4
mangum
langchain==0.1.17 
langchain-community==0.0.38 
langchain-core==0.1.53
langchain-text-splitters==0.0.1
langchain-google-genai==0.0.9
pymupdf
chromadb
sentence-transformers
python-dotenv==1.0.1
```

### 4. **vercel.json** - Vercel Config
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### 5. **templates/index.html** - Frontend
- Ultra-modern AI interface
- Cosmic animations
- Session management
- Auto-cleanup

### 6. **.env.example** - Environment Template
```env
# Google Gemini API Key
# Get your API key from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_api_key_here
```

### 7. **.gitignore** - Git Ignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Environment Variables
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Data directories
uploads/
data/

# Logs
*.log
```

## ⚠️ Files You Should NOT Have

### ❌ Do NOT include these:
- `uploads/` folder (created at runtime)
- `data/` folder (created at runtime)
- `__pycache__/` folders
- `.env` file (contains secrets!)
- `venv/` or `env/` folders
- `.DS_Store` or OS-specific files

## 📋 Step-by-Step Setup

### 1. Create Project Folder
```bash
mkdir neural-pdf-ai
cd neural-pdf-ai
```

### 2. Add All Required Files
Copy all the files I provided into this folder:
- main.py
- rag_pipeline.py
- requirements.txt
- vercel.json
- .vercelignore
- .env.example
- README.md
- VERCEL_DEPLOYMENT.md

### 3. Create templates Folder
```bash
mkdir templates
```

### 4. Add index.html
Copy the ultra-modern index.html into the templates folder

### 5. Create .env File (Local Testing)
```bash
cp .env.example .env
# Then edit .env and add your actual API key
```

### 6. Create .gitignore
```bash
# Create .gitignore with the content above
```

## 🔍 Verify Your Structure

Run this command in your project folder:
```bash
ls -la
```

You should see:
```
.env                    # Local only
.env.example           # ✅
.gitignore             # ✅
.vercelignore          # ✅
main.py                # ✅
rag_pipeline.py        # ✅
README.md              # ✅
requirements.txt       # ✅
templates/             # ✅ folder
vercel.json            # ✅
VERCEL_DEPLOYMENT.md   # ✅
```

Check templates folder:
```bash
ls templates/
```

Should show:
```
index.html             # ✅
```

## 🚀 Deploy to Vercel

### Option 1: GitHub → Vercel (Recommended)

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit - Neural PDF AI"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/neural-pdf-ai.git
git branch -M main
git push -u origin main
```

Then:
1. Go to https://vercel.com/new
2. Import your GitHub repo
3. Add environment variable: `GOOGLE_API_KEY`
4. Deploy!

### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Set environment variable when prompted
# GOOGLE_API_KEY=your_key_here

# Deploy to production
vercel --prod
```

## 📊 File Size Check

Before deploying, verify your files aren't too large:

```bash
# Check total project size
du -sh .

# Should be < 50MB (excluding venv, node_modules)
```

## ✅ Pre-Deployment Checklist

- [ ] All files in correct locations
- [ ] `templates/` folder exists with `index.html`
- [ ] `.env` is in `.gitignore` (NOT committed)
- [ ] `vercel.json` is present
- [ ] `requirements.txt` has all dependencies
- [ ] Tested locally with `uvicorn main:app --reload`
- [ ] Environment variable ready (GOOGLE_API_KEY)

## 🎯 Quick Test Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# Visit
http://127.0.0.1:8000
```

If it works locally, it will work on Vercel! 🎉

## 📝 Notes

- **templates/** folder MUST exist - Vercel looks for it
- **vercel.json** tells Vercel how to build your app
- **.vercelignore** excludes unnecessary files from deployment
- **mangum** in requirements.txt is REQUIRED for serverless
- Environment variables are set in Vercel Dashboard, not in .env

## 🆘 Troubleshooting

**"Module not found"**
→ Check requirements.txt has all dependencies

**"templates not found"**
→ Make sure templates/ folder exists and has index.html

**"GOOGLE_API_KEY not found"**
→ Add environment variable in Vercel Dashboard → Settings → Environment Variables

**Build fails**
→ Check vercel.json syntax
→ Verify all files are committed to GitHub

---

Your structure is now ready for deployment! 🚀
