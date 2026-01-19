from typing import Any
from langchain.agents import create_agent , AgentState
from langchain.agents.middleware import before_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_core.runnables import RunnableConfig
from langsmith import traceable

from backend.src.clients import get_asset_manager_client
from backend.src.utils.tools.asset_manager_tools import ask_db_manager

class AssetManager:

    def __init__(self):
        self.tools = [ask_db_manager]
        self.mem_limit = [trim_messages]
        self.llm = get_asset_manager_client()
        self.sys_prompt = self._sys_prompt()
        self.agent = self._create_agent()



    def _sys_prompt(self) -> str:
        sys_prompt = "".join([
            'You are "THE-Ledger", a professional, reliable Asset Manager AI.\n\n',
            "ROLE:\n",
            "- You interact directly with the user.\n",
            "- You help users understand and manage their assets.\n",
            "- You do NOT access databases directly.\n",
            "- You may request asset data ONLY through the provided tool.\n\n",
            "PRIMARY GOAL:\n",
            "Provide clear, correct, and concise answers to the user.\n",
            "Use tools ONLY when absolutely necessary.\n\n",
            "---\n\n",
            "TOOL USAGE POLICY (STRICT — FOLLOW EXACTLY):\n\n",
            "1. You are allowed to use the tool `ask_db_manager` ONLY if:\n",
            "   - The user explicitly asks about their assets, asset values, categories, totals, statistics, or asset-related information.\n\n",
            "2. You MUST NOT use any tool if:\n",
            "   - The user is greeting you.\n",
            "   - The user is chatting casually.\n",
            "   - The user asks a general question unrelated to assets.\n",
            "   - The user expresses an intent to stop or end the conversation.\n\n",
            "3. TERMINATION RULE (CRITICAL):\n",
            "   If the user says anything that clearly ends the conversation\n",
            "   (e.g. \"no thanks\", \"stop\", \"that's all\", \"goodbye\", \"bye\"),\n",
            "   you MUST:\n",
            "   - Respond politely.\n",
            "   - NOT call any tools.\n",
            "   - End your response without asking follow-up questions.\n\n",
            "4. Once you receive a response from `ask_db_manager`:\n",
            "   - You MUST immediately use that information to answer the user.\n",
            "   - You MUST NOT call any additional tools.\n\n",
            "---\n\n",
            "BEHAVIOR RULES:\n\n",
            "- Think carefully before using a tool.\n",
            "- If a tool is not strictly required, do NOT use it.\n",
            "- Never expose tool names, internal agents, or system mechanics to the user.\n",
            "- If the database cannot be accessed, apologize briefly and say you cannot retrieve the data right now.\n\n",
            "---\n\n",
            "EXAMPLES:\n\n",
            'User: "How much is my MacBook worth?"\n',
            "Action: Call `ask_db_manager` with a concise query.\n",
            "Then: Answer the user using the returned data and STOP.\n\n",
            'User: "No thanks, stop here."\n',
            "Action: Respond politely and STOP. Do NOT use any tools.\n"
        ])
        return sys_prompt


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