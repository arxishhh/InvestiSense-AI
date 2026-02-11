from typing import List,Dict, Callable, Any
from pydantic import BaseModel
from langchain_core.tools import StructuredTool

class ToolRegistry:
    def __init__(self):
        self.all_tools : Dict[str, StructuredTool] = {}

    def format_proofs(self,proofs : List[Dict[str,Any]],is_dict : bool = False):
        pass

    def getAllTools(self) -> List[StructuredTool]:
        return self.all_tools

    def registerTool(self,func_name :Callable,description : str,name : str, args_schema : BaseModel):
        
        tool = StructuredTool.from_function(
            name = name,
            func = func_name,
            description=description,
            args_schema=args_schema
        )
        self.all_tools[name] = tool

        return tool