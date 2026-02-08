# 🚀 Vercel Deployment Guide

## Prerequisites
- Vercel account ([Sign up here](https://vercel.com/signup))
- GitHub/GitLab/Bitbucket account (for connecting your repository)
- Google Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

## Deployment Steps

### 1. Prepare Your Repository

Make sure your project has these files:
- `main.py` - FastAPI application
- `rag_pipeline.py` - RAG logic
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel configuration
- `.vercelignore` - Files to exclude from deployment
- `templates/index.html` - Frontend UI
- `.env.example` - Environment variable template

### 2. Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit for Vercel deployment"

# Create repository on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. Deploy to Vercel

#### Option A: Using Vercel Dashboard (Recommended)

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Other
   - **Build Command**: (leave empty)
   - **Output Directory**: (leave empty)
   - **Install Command**: `pip install -r requirements.txt`

5. **Add Environment Variable**:
   - Click "Environment Variables"
   - Add: `GOOGLE_API_KEY` = `your_actual_api_key_here`
   - Make sure to add it for all environments (Production, Preview, Development)

6. Click "Deploy"

#### Option B: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts and set environment variable when asked
# GOOGLE_API_KEY=your_actual_api_key_here

# Deploy to production
vercel --prod
```

### 4. Configure Environment Variables (Post-Deployment)

If you didn't add environment variables during setup:

1. Go to your project in Vercel Dashboard
2. Click "Settings" → "Environment Variables"
3. Add:
   - **Key**: `GOOGLE_API_KEY`
   - **Value**: Your Google Gemini API key
   - **Environment**: Production, Preview, Development (select all)
4. Click "Save"
5. Redeploy the project for changes to take effect

## ⚠️ Important Vercel Limitations

### 1. **Serverless Function Timeout**
- **Free Plan**: 10 seconds max execution time
- **Pro Plan**: 60 seconds max execution time
- **Solution**: Use smaller PDFs or upgrade to Pro plan

### 2. **Memory Limitations**
- **Free Plan**: 1024 MB (1 GB) memory
- **Pro Plan**: 3008 MB (3 GB) memory
- **Impact**: Large PDFs may cause memory issues
- **Solution**: Limit PDF size to 5-10 MB

### 3. **Cold Starts**
- **Issue**: First request after inactivity takes longer (10-30 seconds)
- **Impact**: Session data stored in memory is lost between cold starts
- **Mitigation**: Consider using external storage (see Advanced Setup below)

### 4. **No Persistent File Storage**
- **Issue**: Files stored in `/tmp` are deleted after function execution
- **Current Setup**: Uses temp directory for session-based storage
- **Impact**: Data is automatically cleaned, which is good for privacy
- **Limitation**: Sessions don't persist across cold starts

## 🔧 Configuration Files Explained

### `vercel.json`
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

### Key Changes for Vercel

1. **Mangum Handler**: Added `handler = Mangum(app)` to make FastAPI work with serverless
2. **Temp Directory**: Uses `tempfile.gettempdir()` instead of local directories
3. **Model**: Changed to `gemini-1.5-flash` (compatible with your langchain version)
4. **PyMuPDF**: Using `PyMuPDFLoader` instead of `PyPDFLoader`

## 📊 Recommended Settings for Production

### File Size Limits
```python
# In main.py - already set
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB (safe for Vercel)
```

### Chunk Settings
```python
# In rag_pipeline.py - already configured
chunk_size = 500  # Good balance for speed/accuracy
chunk_overlap = 100  # Ensures context continuity
```

## 🐛 Troubleshooting

### Build Fails
**Error**: `Module not found`
- **Solution**: Check `requirements.txt` has all dependencies
- Run locally first: `pip install -r requirements.txt`

### Timeout Errors
**Error**: `Function execution timeout`
- **Solution**: 
  - Use smaller PDFs (< 5MB)
  - Upgrade to Vercel Pro
  - Reduce chunk size in `rag_pipeline.py`

### Memory Errors
**Error**: `Memory limit exceeded`
- **Solution**:
  - Reduce PDF size
  - Reduce number of chunks retrieved (change `k=3` to `k=1`)
  - Upgrade to Pro plan

### Environment Variable Issues
**Error**: `GOOGLE_API_KEY not found`
- **Solution**:
  - Add environment variable in Vercel Dashboard
  - Redeploy after adding
  - Check variable is set for correct environment

### Cold Start Issues
**Symptom**: First request very slow
- **Expected**: This is normal for serverless
- **Solution**: Consider keeping function "warm" with periodic pings
- **Alternative**: Use Vercel Pro for better cold start performance

## 🎯 Testing Your Deployment

After deployment:

1. Visit your Vercel URL (e.g., `https://your-app.vercel.app`)
2. Upload a small test PDF (< 2MB)
3. Ask a simple question
4. Verify answer is based only on PDF content

## 📈 Monitoring

### Vercel Dashboard
- View function logs: Project → "Deployments" → Click deployment → "Logs"
- Monitor usage: Project → "Analytics"
- Check errors: Project → "Settings" → "Functions"

### Check Function Performance
```bash
# View recent logs
vercel logs YOUR_PROJECT_URL
```

## 🔒 Security Best Practices

1. **Never commit `.env` file**
2. **Use environment variables** for API keys
3. **Set appropriate CORS** if needed
4. **Enable Vercel Authentication** for private use
5. **Monitor API usage** to avoid quota exhaustion

## 💡 Advanced Setup (Optional)

### For Persistent Storage

If you need sessions to persist across cold starts, consider:

1. **Upstash Redis** (free tier available)
   - Store session metadata
   - Fast key-value storage
   
2. **Vercel KV** (requires Pro plan)
   - Native Vercel key-value store
   - Automatic scaling

3. **Supabase Storage** (free tier available)
   - Store uploaded PDFs
   - PostgreSQL database for session data

### Example: Using Vercel KV

```python
# Install
pip install vercel-kv

# In main.py
from vercel_kv import kv

# Store session
await kv.set(f"session:{session_id}", session_data)

# Retrieve session
session_data = await kv.get(f"session:{session_id}")
```

## 🎉 Your App is Live!

Once deployed, your URL will be:
`https://your-app-name.vercel.app`

Share it with users and start asking questions from PDFs!

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- Vercel Community: https://github.com/vercel/vercel/discussions
- FastAPI on Vercel: https://vercel.com/guides/deploying-fastapi-with-vercel

---

**Note**: For production use with high traffic, consider upgrading to Vercel Pro plan for better performance, longer timeouts, and more memory.
