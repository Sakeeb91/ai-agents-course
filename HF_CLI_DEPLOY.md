# 🚀 Deploy to Hugging Face via CLI

Quick guide to deploy your AI Agent Chat to Hugging Face Spaces using the command line.

## 📋 Prerequisites

1. **Hugging Face Account** - Sign up at https://huggingface.co
2. **Access Token** - Get from https://huggingface.co/settings/tokens

## 🔐 Step 1: Get Your Access Token

1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `cli-access` (or any name you want)
4. Type: Select "Write" permissions
5. Click "Generate token"
6. **Copy the token** (you'll only see it once!)

## 💻 Step 2: Login via CLI

Run this command and paste your token when prompted:

```bash
huggingface-cli login
```

Or set it directly:

```bash
export HUGGINGFACE_TOKEN="your_token_here"
huggingface-cli login --token $HUGGINGFACE_TOKEN
```

## 📦 Step 3: Create the Space

We need to create a Space on Hugging Face first. You have two options:

### Option A: Via Web (Easier)
1. Go to https://huggingface.co/new-space
2. **Owner**: Your username
3. **Space name**: `ai-agent-chat` (or your preferred name)
4. **License**: MIT
5. **Space SDK**: Select **Gradio**
6. **Visibility**: Public (or Private if you prefer)
7. Click "Create Space"

### Option B: Via CLI (Advanced)
```bash
huggingface-cli repo create ai-agent-chat --type space --space_sdk gradio
```

## 📤 Step 4: Upload Files

Once your Space is created, upload the files:

```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"

# Upload app.py
huggingface-cli upload YOUR_USERNAME/ai-agent-chat app.py app.py

# Upload requirements.txt
huggingface-cli upload YOUR_USERNAME/ai-agent-chat requirements.txt requirements.txt
```

Replace `YOUR_USERNAME` with your actual Hugging Face username!

## 🔑 Step 5: Add API Key as Secret

You need to add your Google API key as a secret. Do this via the web:

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/ai-agent-chat`
2. Click "Settings" tab
3. Scroll to "Repository secrets"
4. Click "New secret"
5. **Name**: `GOOGLE_API_KEY`
6. **Value**: `your-google-api-key-here`
7. Click "Save"

## ⏳ Step 6: Wait for Build

- Your Space will automatically build (takes 2-5 minutes)
- Check build status at: `https://huggingface.co/spaces/YOUR_USERNAME/ai-agent-chat`
- Once ready, your Space will have a URL like:
  ```
  https://YOUR_USERNAME-ai-agent-chat.hf.space
  ```

## 🎉 Step 7: Test Your Space!

Visit your Space URL and start chatting with your AI agent!

---

## 🛠️ Alternative: One-Command Deploy Script

I can create a script that does all the uploading for you. Just run:

```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"
chmod +x deploy_to_hf.sh
./deploy_to_hf.sh YOUR_USERNAME
```

Would you like me to create this script?

---

## 🔄 Updating Your Space

To update your Space after making changes:

```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"

# Update app.py
huggingface-cli upload YOUR_USERNAME/ai-agent-chat app.py app.py

# Or update multiple files
huggingface-cli upload YOUR_USERNAME/ai-agent-chat . --include="app.py,requirements.txt"
```

---

## 📚 Quick Reference

### Common Commands

```bash
# Login
huggingface-cli login

# Create space
huggingface-cli repo create SPACE_NAME --type space --space_sdk gradio

# Upload file
huggingface-cli upload USERNAME/SPACE_NAME local_file.py remote_file.py

# Upload directory
huggingface-cli upload USERNAME/SPACE_NAME . --include="*.py,*.txt"

# Check login status
huggingface-cli whoami

# Logout
huggingface-cli logout
```

### File Structure Needed

Your Space needs these files:
- ✅ `app.py` - Main Gradio application
- ✅ `requirements.txt` - Python dependencies
- ✅ Secret: `GOOGLE_API_KEY` (added via web interface)

---

## ❓ Troubleshooting

### "Not logged in"
```bash
huggingface-cli login
```

### "Space not found"
Make sure you created the Space first (via web or CLI)

### "Upload failed"
Check your username and Space name are correct:
```bash
huggingface-cli whoami  # Check your username
```

### "Build failed"
1. Check build logs in Space settings
2. Verify `requirements.txt` is correct
3. Check `app.py` has no syntax errors

---

## 🎯 Next Steps After Deployment

1. **Test thoroughly** - Try different queries
2. **Share the link** - Send to friends!
3. **Monitor usage** - Check logs in Space settings
4. **Upgrade if needed** - HF Spaces Pro for better performance
5. **Add features** - Customize the app further

---

**Ready to deploy? Let me know if you want me to create the automated deployment script!**
