# 🚀 Quick Deploy to Hugging Face Spaces

## One-Command Deployment!

I've created an automated deployment script for you. Here's how to use it:

---

## 📋 Before You Start

### 1. Create Hugging Face Account
If you don't have one: https://huggingface.co/join

### 2. Get Your Access Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `cli-access`
4. Type: Select **Write** permissions
5. Click "Generate token"
6. **Copy the token** (you won't see it again!)

### 3. Login to Hugging Face CLI
```bash
huggingface-cli login
```
Paste your token when prompted.

---

## 🎯 Deploy Your App (3 Steps!)

### Step 1: Navigate to the Directory
```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"
```

### Step 2: Run the Deployment Script
```bash
./deploy_to_hf.sh YOUR_HF_USERNAME
```
Replace `YOUR_HF_USERNAME` with your actual Hugging Face username!

**Example:**
```bash
./deploy_to_hf.sh sakeeb
```

### Step 3: Add Your API Key (Web)
After the script finishes, it will give you a link. Click it and:

1. Go to the Settings tab
2. Scroll to "Repository secrets"
3. Click "New secret"
4. **Name**: `GOOGLE_API_KEY`
5. **Value**: `your-google-api-key-here`
6. Click "Save"

---

## ✅ That's It!

Your Space will build automatically (2-5 minutes) and be available at:
```
https://YOUR_USERNAME-ai-agent-chat.hf.space
```

---

## 🎬 What the Script Does

The deployment script automatically:
- ✅ Checks you're logged in
- ✅ Verifies required files exist
- ✅ Creates the Space (if it doesn't exist)
- ✅ Uploads `app.py`
- ✅ Uploads `requirements.txt`
- ✅ Opens the Space in your browser
- ✅ Shows you the next steps

---

## 🔄 Update Your Deployed Space

Made changes and want to update? Just run the script again:

```bash
./deploy_to_hf.sh YOUR_HF_USERNAME
```

It will upload the latest versions of your files!

---

## 🛠️ Manual Commands (If You Prefer)

### Login
```bash
huggingface-cli login
```

### Create Space
```bash
huggingface-cli repo create ai-agent-chat --type space --space_sdk gradio
```

### Upload Files
```bash
# Upload app.py
huggingface-cli upload spaces/YOUR_USERNAME/ai-agent-chat app.py app.py

# Upload requirements.txt
huggingface-cli upload spaces/YOUR_USERNAME/ai-agent-chat requirements.txt requirements.txt
```

---

## 📊 Check Deployment Status

Visit your Space to see build logs:
```
https://huggingface.co/spaces/YOUR_USERNAME/ai-agent-chat
```

---

## ❓ Troubleshooting

### "Permission denied" when running script
```bash
chmod +x deploy_to_hf.sh
./deploy_to_hf.sh YOUR_USERNAME
```

### "Not logged in"
```bash
huggingface-cli login
```
Then paste your access token

### "Space not found" when uploading
Make sure you created the Space first. The script will ask if you want to create it.

### Build Failed
1. Check build logs in your Space's "Logs" tab
2. Verify `GOOGLE_API_KEY` secret is added
3. Check Python version compatibility (should work on HF's Python 3.10+)

---

## 🎉 Success!

Once deployed, you'll have:
- 🌐 Public URL for your AI agent chat
- 💬 Beautiful Gradio interface
- 🔍 Google Search integration
- ⚡ Fast Gemini 2.5 Flash Lite responses
- 🎨 Purple gradient theme

---

## 🚀 Next Steps

After successful deployment:

1. **Test it thoroughly** - Ask different questions
2. **Share the link** - Send to friends and colleagues
3. **Monitor usage** - Check logs in Space settings
4. **Customize further** - Edit `app.py` and redeploy
5. **Upgrade if needed** - HF Spaces Pro for better performance

---

## 📝 Files You're Deploying

- **app.py** - Full Gradio interface with your AI agent
- **requirements.txt** - Just `google-adk` and `gradio`
- **Secret**: GOOGLE_API_KEY (added via web)

---

**Ready to deploy? Run the command and watch the magic happen! ✨**

```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course"
./deploy_to_hf.sh YOUR_HF_USERNAME
```
