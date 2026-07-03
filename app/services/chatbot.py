from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import RedisChatMessageHistory

from app.config.settings import OPENAI_API_KEY, REDIS_URL
from app.tools.calculator import calculator
from app.tools.datetime_tool import current_datetime
from app.tools.web_search import web_search
from app.prompts.chat_prompt import PROMPT

# Initialize tools
tools = [calculator, current_datetime, web_search]
tools_map = {tool.name: tool for tool in tools}

# Initialize LLM
llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
llm_with_tools = llm.bind_tools(tools)

# Create chain
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", PROMPT()),
    MessagesPlaceholder(variable_name="history"),
    MessagesPlaceholder(variable_name="input")
])

chain = chat_prompt | llm_with_tools

def get_session_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(
        session_id,
        url=REDIS_URL,
        ttl=300
    )

runnable = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

def chat_with_bot(session_id: str, message: str) -> str:
    input_messages = [HumanMessage(content=message)]
    
    while True:
        response = runnable.invoke(
            {"input": input_messages},
            config={"configurable": {"session_id": session_id}}
        )
        
        if not response.tool_calls:
            return str(response.content)
            
        input_messages = []
        for tool_call in response.tool_calls:
            tool = tools_map.get(tool_call["name"])
            if tool:
                try:
                    tool_result = tool.invoke(tool_call["args"])
                except Exception as e:
                    tool_result = f"Error: {str(e)}"
            else:
                tool_result = f"Error: Tool {tool_call['name']} not found."
                
            input_messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call["id"]
                )
            )
