# 🚀 Gradio Deployment Guide

Your AI Agent Chat is now available as a Gradio app! You can run it locally or deploy to Hugging Face Spaces.

## 📁 Files Created

- **app.py** - Main Gradio application (deployment-ready)
- **gradio_app.py** - Local development version
- **requirements.txt** - Python dependencies

## 💻 Run Locally

### Option 1: Quick Start
```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"
python3 gradio_app.py
```

The app will open automatically at: http://localhost:7860

### Option 2: With Public URL (Share Link)
Edit `gradio_app.py` and change:
```python
demo.launch(share=False)  # Change to share=True
```

This creates a temporary public URL you can share with anyone!

## 🌐 Deploy to Hugging Face Spaces (FREE!)

### Step 1: Create a Hugging Face Account
1. Go to https://huggingface.co
2. Sign up for a free account

### Step 2: Create a New Space
1. Click on your profile → "New Space"
2. **Space name**: ai-agent-chat (or any name you want)
3. **License**: Choose MIT or Apache 2.0
4. **Space SDK**: Select **Gradio**
5. Click "Create Space"

### Step 3: Upload Files
You have two options:

#### Option A: Git (Recommended)
```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"
git init
git add app.py requirements.txt
git commit -m "Initial commit"
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/ai-agent-chat
git push hf main
```

#### Option B: Web Upload
1. In your Space, click "Files" → "Upload files"
2. Upload:
   - `app.py`
   - `requirements.txt`
3. Click "Commit changes to main"

### Step 4: Add Your API Key as a Secret
1. In your Space, go to "Settings" tab
2. Scroll to "Repository secrets"
3. Click "New secret"
4. Name: `GOOGLE_API_KEY`
5. Value: `your-google-api-key-here`
6. Click "Save"

### Step 5: Wait for Build
- Your Space will automatically build (takes 2-5 minutes)
- Once ready, you'll have a public URL like:
  `https://huggingface.co/spaces/YOUR_USERNAME/ai-agent-chat`

## 🎨 Gradio Features

### Beautiful Chat Interface
- 💬 Chat bubble design
- 🤖 Robot avatar for AI agent
- 📱 Mobile responsive
- 🎨 Purple gradient theme

### Built-in Features
- 📋 Copy messages
- 🗑️ Clear chat button
- 💡 Example prompts
- ℹ️ Expandable info section

### Markdown Support
- **Bold** and *italic* text
- Code blocks with syntax highlighting
- Lists and tables
- Links and more

## 🔧 Customization

### Change Theme
Edit `app.py`:
```python
theme=gr.themes.Soft(
    primary_hue="blue",      # Try: blue, green, red, orange
    secondary_hue="cyan",    # Try: cyan, teal, lime
)
```

### Add More Examples
Edit `app.py`:
```python
gr.Examples(
    examples=[
        "Your custom example here",
        "Another example",
    ],
    inputs=msg,
)
```

### Change Model
Edit `app.py`:
```python
root_agent = Agent(
    model="gemini-2.0-pro",  # Try: gemini-2.0-pro, gemini-2.5-flash
    ...
)
```

## 📊 Gradio vs Flask Comparison

| Feature | Gradio | Flask (Your Web App) |
|---------|--------|---------------------|
| Setup Time | ⚡ 5 minutes | 🕐 15 minutes |
| Deployment | ☁️ One-click (HF Spaces) | 🔧 Manual (VPS/Cloud) |
| Cost | 💚 Free on HF | 💰 Server costs |
| Interface | 🎨 Auto-generated | 🛠️ Custom HTML/CSS |
| Share Link | ✅ Built-in | ❌ Need ngrok/etc |
| Customization | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Full control |
| Mobile Support | ✅ Auto | ✅ Custom |

## 🎯 Best Use Cases

### Use Gradio When:
- ✅ You want quick deployment
- ✅ You need a public demo
- ✅ You want free hosting
- ✅ You're prototyping
- ✅ You don't need custom branding

### Use Flask When:
- ✅ You need full UI control
- ✅ You want custom branding
- ✅ You're building a product
- ✅ You need complex frontend features
- ✅ You want to integrate with existing web app

## 🚀 Next Steps

### 1. Test Locally
```bash
python3 gradio_app.py
```

### 2. Deploy to Hugging Face Spaces
Follow the deployment steps above

### 3. Share Your Space
Once deployed, share your URL with friends!

### 4. Add Features
- Add more tools to the agent
- Customize the theme
- Add authentication
- Track usage analytics

## 🔒 Security Notes

### For Production:
1. **Never commit API keys** - Use environment variables
2. **Use Secrets** - On HF Spaces, always use repository secrets
3. **Rate Limiting** - Consider adding rate limits for public spaces
4. **Monitoring** - Check usage and costs regularly

### Update API Key on HF Spaces:
1. Go to Space Settings
2. Update the `GOOGLE_API_KEY` secret
3. Restart the Space

## 💡 Pro Tips

### 1. Enable Queue
For better handling of concurrent users:
```python
demo.launch(
    share=False,
    enable_queue=True,
)
```

### 2. Add Analytics
Track usage with Gradio analytics:
```python
demo.launch(
    analytics_enabled=True,
)
```

### 3. Custom Domain
On Hugging Face Spaces Pro, you can use custom domains!

### 4. Monetization
Enable paid access on HF Spaces Pro to monetize your agent.

## 📚 Resources

- [Gradio Documentation](https://gradio.app/docs)
- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Gradio Themes Gallery](https://gradio.app/guides/theming-guide)

## 🆘 Troubleshooting

### Space Build Fails
- Check requirements.txt has correct package names
- Verify Python version compatibility
- Check build logs in Space settings

### API Key Not Working
- Verify secret name is exactly `GOOGLE_API_KEY`
- Check the key is valid on Google AI Studio
- Restart the Space after adding secrets

### Slow Performance
- Consider upgrading to HF Spaces Pro
- Use a faster Gemini model (flash vs pro)
- Reduce search tool usage

### Memory Issues
- HF Spaces free tier has limited RAM
- Use lighter models
- Clear session state periodically

---

**Your Gradio app is ready to deploy! 🎉**

Choose your deployment method and share your AI agent with the world!
