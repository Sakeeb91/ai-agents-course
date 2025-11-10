# 🤖 AI Agent Web Chat

A beautiful web interface for chatting with your AI Agent powered by Google ADK and Gemini!

## 🚀 What's Running

✅ **Backend Server**: Flask API running on `http://localhost:8080`
✅ **Frontend**: Beautiful chat interface opened in your browser
✅ **AI Agent**: Google Gemini 2.5 Flash Lite with Google Search tool

## 📁 Files

- **index.html** - Beautiful gradient-themed chat interface
- **server.py** - Flask API backend that connects to the AI agent
- **README.md** - This file

## 🎨 Features

### Beautiful UI
- Gradient purple theme
- Smooth animations
- Loading indicators
- Auto-scrolling chat
- Responsive design

### AI Capabilities
- **Google Search**: Agent can search the web for current information
- **Smart Tool Usage**: Agent decides when to use search based on the query
- **Fast Responses**: Using Gemini 2.5 Flash Lite for speed
- **Grounded Answers**: Responses backed by real sources

## 💬 Try These Queries

- "What's the weather in Tokyo?"
- "Who won the latest World Cup?"
- "Tell me about quantum computing"
- "What are the latest tech news?"
- "Explain how AI agents work"

## 🔧 Technical Details

### Backend API Endpoints

**POST /api/chat**
```json
Request:
{
  "message": "Your question here"
}

Response:
{
  "response": "Agent's answer",
  "success": true
}
```

**GET /api/health**
```json
Response:
{
  "status": "healthy",
  "agent": "ready",
  "model": "gemini-2.5-flash-lite"
}
```

### Server Status

The server is running in the background. You can check its output:

```bash
# See recent server logs
tail -f server.log  # if you want to save logs

# Or check the background process
ps aux | grep server.py
```

## 🛑 Stopping the Server

To stop the server, find the process and kill it:

```bash
# Find the process
lsof -i :8080

# Kill it
kill -9 <PID>
```

Or press `CTRL+C` in the terminal where you started the server.

## 🔄 Restarting the Server

```bash
cd "/Users/sakeeb/Code repositories/kagglae agent course/web-chat"
python3 server.py
```

Then open `index.html` in your browser.

## 🎯 How It Works

1. **User types message** in the web interface
2. **JavaScript sends POST request** to Flask backend
3. **Flask receives request** and passes it to the AI agent
4. **Agent analyzes query** and decides if it needs Google Search
5. **If needed, agent searches** the web for current information
6. **Agent synthesizes response** combining search results and knowledge
7. **Flask returns response** to the frontend
8. **JavaScript displays answer** in the chat interface

## 🌟 Architecture

```
┌─────────────────┐
│  Web Browser    │
│  (index.html)   │
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│  Flask Server   │
│  (server.py)    │
│  Port 8080      │
└────────┬────────┘
         │ Python API
         ▼
┌─────────────────┐
│  Google ADK     │
│  InMemoryRunner │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────┐
│  Gemini Model   │────▶│ Google Search│
│  2.5-flash-lite │     │     Tool     │
└─────────────────┘     └──────────────┘
```

## 🔐 Security Note

- API key is embedded in `server.py` for development
- For production, use environment variables
- Never commit API keys to version control
- Consider adding authentication for public deployment

## 📊 Monitoring Requests

Watch the server terminal to see:
- Incoming messages
- Agent responses
- Any errors

Example output:
```
📨 Received: What's the weather in London?
💬 Response: The weather in London is currently 13°C with light rain...
```

## 🎓 What You Learned

- Building web interfaces for AI agents
- Creating REST APIs with Flask
- Connecting frontend JavaScript to backend Python
- Real-time chat UI with loading states
- Handling async agent queries in a web server

## 🚀 Next Steps

- Add message history persistence
- Add user authentication
- Deploy to a cloud service
- Add more tools to the agent
- Create multi-agent conversations

---

**Enjoy chatting with your AI Agent! 🤖✨**
