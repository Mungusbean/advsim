from langchain_core.runnables import RunnableLambda, Runnable
from abc import ABC, abstractmethod

class BaseAttackModule(Runnable, ABC):
    """_summary_

    Args:
        Runnable (_type_): BaseAttackModule is a wrapper of LangChain's Runnable base,
        allowing uses to define the "invoke" method in it's children class.
    """
    def __init__(self, name: str|None, description: str|None) -> None:
        self.name = name
        self.description = description 
        super().__init__()



    