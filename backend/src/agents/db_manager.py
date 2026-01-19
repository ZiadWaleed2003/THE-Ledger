from typing import Any
from langchain.agents import create_agent , AgentState
from langchain.agents.middleware import before_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_core.runnables import RunnableConfig


from backend.src.clients import get_nvidia_client
from backend.src.utils.tools.db_manager_tools import search_assets_by_name_or_category, get_all_assets, get_asset_value_statistics

class DBManager:

    def __init__(self):
        self.tools = [search_assets_by_name_or_category, get_all_assets, get_asset_value_statistics]
        # self.mem_limit = [trim_messages]
        self.llm = get_nvidia_client()
        self.sys_prompt = self._sys_prompt()
        self.agent = self._create_agent()



    def _sys_prompt(self) -> str:
        prompt =  "".join([
            "You are the Database Manager, a specialized sub-agent responsible for precise retrieval of asset data.\n\n",
            
            "Your role is to strictly query the database using the provided tools to answer the user's request.\n",
            "You do not make assumptions. You rely solely on tool outputs.\n\n",
            
            "AVAILABLE TOOLS:\n",
            "- `search_assets_by_name_or_category`: Use for finding specific items (e.g., 'MacBook', 'Electronics').\n",
            "- `get_asset_value_statistics`: Use for max, min, or mean calculations.\n",
            "- `get_all_assets`: if the user didn't specify a specific name for an asset or category then use this tool to get all the stored assets and answer the user query from it.\n\n",
            
            "CHAIN OF THOUGHT REASONING:\n",
            "Before calling a tool, you must reason step-by-step:\n",
            "1. Analyze the user's request to identify the specific data point needed.\n",
            "2. Select the most appropriate tool for that specific data point.\n",
            "3. Explain why you selected that tool.\n\n",
            
            "OUTPUT GUIDELINES:\n",
            "- If a tool returns data, summarize it clearly.\n",
            "- If a tool returns 'No Assets found' or an error, report it faithfully.\n",
            "- Do not provide financial advice, only data."
        ])

        return prompt


    def _create_agent(self):
        "a method to create the agent"


        agent = create_agent(
            model= self.llm,
            system_prompt= self.sys_prompt,
            tools= self.tools,
            # middleware=self.mem_limit,
            # checkpointer=InMemorySaver()

        )

        return agent

    def run_query(self, user_query : str):
        "a method to invoke the agent and execute the user query"

        try:
            config: RunnableConfig = {"configurable": {"thread_id": "1"}}
            result = self.agent.invoke(
                {"messages": [{"role" : "user" , "content" : user_query}]},
                # config=config
            )

           
            if result and "messages" in result:
                answer = result["messages"][-1].content
                return answer
            else:
                return None
        except Exception as e:
            print("damn shit happened")
            return None
        

# @before_model
# def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
#     """Keep only the last few messages to fit context window."""
#     messages = state["messages"]

#     if len(messages) <= 5:
#         return None  # No changes needed

#     first_msg = messages[0]
#     recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
#     new_messages = [first_msg] + recent_messages

#     return {
#         "messages": [
#             RemoveMessage(id=REMOVE_ALL_MESSAGES),
#             *new_messages
#         ]
#     }