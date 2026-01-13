from langchain.agents import create_agent


from src.clients import get_nvidia_client


class AssetManager:

    def __init__(self):

        self.llm = get_nvidia_client()
        self.sys_prompt = self._sys_prompt()
        



    def _sys_prompt(self)-> str:

        sys_prompt = "".join([
            "",
            "",
            ""
        ])

        return sys_prompt
