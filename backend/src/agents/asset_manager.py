from typing import Any
from langchain.agents import create_agent , AgentState
from langchain.agents.middleware import before_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_core.runnables import RunnableConfig


from backend.src.clients import get_nvidia_client
from backend.src.utils.tools.asset_manager_tools import ask_db_manager

class AssetManager:

    def __init__(self):
        self.tools = [ask_db_manager]
        self.mem_limit = [trim_messages]
        self.llm = get_nvidia_client()
        self.sys_prompt = self._sys_prompt()
        self.agent = self._create_agent()



    def _sys_prompt(self) -> str:
        prompt =  "".join([
            'You are "THE-Ledger", a dedicated and intelligent Asset Manager and Personal Financial Expert.\n\n',
             
            "YOUR PERSONA:\n",
            "- Professional, concise, and helpful.\n",
            "- You interact naturally with the user.\n",
            
            "GOAL:\n",
            "Help the user with financial tracking and asset management using your database tool when necessary.\n\n",


            "TOOL USAGE RULES (CRITICAL):\n",
            "1. `ask_db_manager`: Use this tool ONLY when you need to fetch specific user's asset data (prices, quantities) not any personal from the database.\n",
            "2. **STOP CONDITION**: Once `ask_db_manager` returns information, you MUST stop calling tools. Use that information to answer the user immediately.\n",
            "3. NO TOOL NEEDED: If the user is just chatting or asking general questions, do NOT use the tool.\n\n",

            "ONE-SHOT EXAMPLE (Follow this flow):\n",
            "User: 'How much is my MacBook worth?'\n",
            "You: Call tool `ask_db_manager` with query 'MacBook value'\n",
            "Tool Output: 'MacBook Pro: $2000'\n",
            "You: 'Your MacBook Pro is currently valued at $2,000.' (STOP calling tools)\n\n",
            
            "BEHAVIOR:\n",
            "- If the tool returns an answer, rephrase it naturally for the user.\n",
            "- If the tool returns an error, apologize and state you cannot access the database right now.\n",
            "- Never expose tool names or internal mechanics."
        ])

        return prompt


    def _create_agent(self):
        "a method to create the agent"


        agent = create_agent(
            model= self.llm,
            system_prompt= self.sys_prompt,
            tools= self.tools,
            middleware=self.mem_limit,
            checkpointer=InMemorySaver()

        )

        return agent

    def run_query(self, user_query : str):
        "a method to invoke the agent and execute the user query"

        try:
            config: RunnableConfig = {"configurable": {"thread_id": "1"}}
            result = self.agent.invoke(
                {"messages": [{"role" : "user" , "content" : user_query}]},
                config=config
            )

           
            if result and "messages" in result:
                answer = result["messages"][-1].content
                return answer
            else:
                return None
        except Exception as e:
            print("damn shit happened")
            return None


@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Keep only the last few messages to fit context window."""
    messages = state["messages"]

    if len(messages) <= 5:
        return None  # No changes needed

    first_msg = messages[0]
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    new_messages = [first_msg] + recent_messages

    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *new_messages
        ]
    }