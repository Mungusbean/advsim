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

    def predict(self, prompt: str|None):
        pass

    def get_metrics(self):
        pass

    def set_system_prompt(self, sys_prompt: str|None):
        pass

    def set_tools(self, tools):
        self.tools = tools

    def add_tools(self, tool):
        self.tools.append(tool)




    
        