from typing import List, Dict 


def format_history(history: List[Dict[str,str]]) -> str:
    formatted = ""
    history = history[-10:]

    for message in history:
        role = message.get('role','')
        content = message.get('content','')
        formatted += f"{role.upper()} : {content}\n"

    return formatted