# import utils.utilfunctions as ufuncs
import flet as ft
from abc import ABC, abstractmethod
from langchain.schema.runnable import Runnable, RunnablePassthrough
from LoggerConfig import setup_logger

logger = setup_logger(__file__)

class Config(ABC):
    def __init__(self, name: str) -> None:
        if not name.isidentifier():
            raise ValueError("Name must be a valid identifier (no special characters, spaces, etc.).")
        self.__name = name
        self.__memory = False
        self.config: Runnable = RunnablePassthrough()
    
    @property
    def name(self):
        return self.__name 
    
    def rename(self, new_name: str):
        if not isinstance(new_name, str):
            raise TypeError("Parameter new_name must be of type string")
        if not new_name.isidentifier():
            raise ValueError("new_name cannot contain special characters or spaces.")
        self.__name = new_name

    @abstractmethod
    def build_config(self):
        pass

    def run(self, prompt: str):
        if not self.config:
            raise ValueError("Configuration is not built yet. Call build_config() first.")
        self.config.invoke(prompt)
        return self.config.invoke(prompt)
    
    def invoke(self):
        #TODO: unimplement as of yet. As Config object does not need to be 
        return None


    def preview_pipeline(self, ):
        """Preview the chain of runnables for debugging and display purposes."""
        logger.debug(f"Pipeline for '{self.name}': {self.config}")
        return 


class PromptConfig(Config):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.__mutators: list[Runnable] = []
        self.__template: Runnable|None = None
        self.__suffixes: list[Runnable] = []
        self.__additional_runnables: list[Runnable] = []
        self.__memory: bool = False

    def add_mutator(self, mutator: Runnable):
        if not isinstance(mutator, Runnable):
            raise TypeError("Mutator must be an instance of Runnable.")
        self.__mutators.append(mutator)

    def add_template(self, template: Runnable):
        if not isinstance(template, Runnable):
            raise TypeError("Template must be an instance of Runnable.")
        self.__template = template

    def add_suffix(self, suffix: Runnable):
        if not isinstance(suffix, Runnable):
            raise TypeError("Suffix must be an instance of Runnable.")
        self.__suffixes.append(suffix)

    def build_config(self):
        
        # Build the pipeline
        self.config = RunnablePassthrough()  # Start fresh
        try:
            for mutator in self.__mutators:
                self.config = self.config | mutator

            if self.__template:
                self.config = self.config | self.__template

            for suffix in self.__suffixes:
                self.config = self.config | suffix
                
            for additional_runnable in self.__additional_runnables:
                self.config = self.config | additional_runnable
            logger.info("Config sucessfully built!")
            return self

        except Exception as e:
            logger.error(f"Build config unsucessful: {e}")
            return False

    def clear_pipeline(self):
        """Reset the configuration pipeline."""
        self.__mutators.clear()
        self.__template = None
        self.__suffixes.clear()
        self.config = RunnablePassthrough()

class PromptGuardConfig(Config):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class ResponseGuardConfig(Config):
    def __init__(self, name: str) -> None:
        super().__init__(name)

