from src.agents.service import build_tools
from typing import Dict, List,Any


tools = build_tools()


def tool_call_loop(tool_calls : List[Dict[str,Any]]):
    
    AllTools = tools.get('AllTools')
    
    proofs = []
    message = ""
    for tool_call in tool_calls:
        tool_name = tool_call.get('name',"")
        if tool_name:
            tool = AllTools.get(tool_name,None)
            if tool:
                response = tool.invoke(tool_call.get('args'))
                proofs = proofs+response.get('proofs')
                message = message +response.get('message') + " | "
    
    
    return {
        'proofs' : proofs,
        'message' : message
    }



            

if __name__ == "__main__":
    tool_call_loop({'name': 'tickerResolver',
  'args': {'company_names': ['Apple','Microsoft','Google']},
  'id': 'fc_df2f8e2b-6a1c-41bd-8d7b-9db940144107',
  'type': 'tool_call'})