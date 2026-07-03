# AI Chatbot API

A production-ready, minimalist AI chatbot API built with FastAPI, LangChain, OpenAI, and Redis. It supports session-based temporary memory and automatic tool calling without overengineered frameworks.

## Features

- **Session-Based Memory**: Conversations are stored in Redis with an automatic 5-minute (300 seconds) TTL.
- **Tool Calling**: The LLM autonomously decides when to use tools.
- **Available Tools**:
  - **Calculator**: Performs basic math operations (+, -, *, /).
  - **Current Date & Time**: Fetches the current datetime.
  - **Web Search**: Searches the web using DuckDuckGo.

## Project Structure

```
app/
  config/
    settings.py
  prompts/
    chat_prompt.py
  services/
    chatbot.py
  tools/
    calculator.py
    datetime_tool.py
    web_search.py
  main.py
.env.example
requirements.txt
README.md
```

## Installation

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Copy the `.env.example` file to `.env` and configure your variables:

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
REDIS_URL=redis://localhost:6379/0
```

## How to Run Redis

If you have Docker installed, you can easily run a Redis instance:

```bash
docker run -d --name redis-stack -p 6379:6379 redis/redis-stack-server:latest
```
*(Alternatively, you can install Redis directly on your machine or use a managed Redis service).*

## How to Run FastAPI

Run the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Example API Request

```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "user_123",
           "message": "What is 25 + 18?"
         }'
```

## Example API Response

```json
{
  "response": "25 + 18 is 43."
}
```

## How Memory Works

The application uses `RedisChatMessageHistory` from the `langchain-redis` package to maintain short-term conversational context.
- Each unique `session_id` maps to a distinct conversation thread in Redis.
- A Time-To-Live (TTL) of 300 seconds (5 minutes) is enforced automatically.
- If a user interacts within 5 minutes, the history remains active. After 5 minutes of inactivity, Redis automatically purges the memory for that session.

## How Tool Calling Works

The chatbot uses modern LangChain tool calling (`bind_tools`). We avoid complex agent frameworks (like LangGraph or AgentExecutor) to keep the backend lightweight and readable.
- The user's input is passed to the language model.
- If the model decides a tool is necessary, it returns a `tool_calls` payload.
- Our service iteratively executes the invoked tools and feeds the results back to the model as `ToolMessage`s until the model issues a final response.
