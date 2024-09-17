class LLMBlock:
    """_summary_
    """
    def __init__(self, LLM, memory, tools) -> None:
        self.LLM = LLM
        self.memory = memory
        self._use_memory = True
        self.tools = tools

    @property
    def use_memory(self):
        return self._use_memory
    
    @use_memory.setter
    def use_memory(self, state: bool):
        self._use_memory = state

    # tools have to be pipelines into this
    def predict(self, prompt: str|None) -> str:
        if not self.use_memory: return self.LLM._call(prompt)
        else:
            return self.LLM.predict(prompt)

    def get_metrics(self) -> dict:
        return dict()

    def set_system_prompt(self, sys_prompt: str|None) -> None:
        pass

    def set_tools(self, tools) -> None:
        self.tools = tools

    def add_tools(self, tool)  -> None:
        self.tools.append(tool)




    
        