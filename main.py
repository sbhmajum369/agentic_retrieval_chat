
import os 
import sys 
from pprint import pprint 
from enum import Enum 
from pathlib import Path

import pyarmor_runtime_000000
print("PyArmor runtime OK")

from src.chat import agent 


## Ollama model collections 
Gemma3_4B = "gemma3:4b" 
Gemma3_1B = "gemma3:1b" 
Qwen3_4B = "qwen3:4b"
Ministral3_3B = "ministral-3:3b"


class ModelsQA(str, Enum):
    SHORT_CONTEXT = Qwen3_4B 
    LONG_CONTEXT = Gemma3_4B 

class ModelsQueryAnalysis(str, Enum):
    DECOMPOSER = Qwen3_4B 
    DIRECTORY_SEARCH = Qwen3_4B 


def main():
    json_path = "./sample_docs" 

    user_query = "Who is Rollo?" 
    
    local_agent = agent.ActiveSearchAgent(json_dir_path=json_path) 
    
    response, doc_list, sub_queries, matched_src_text = local_agent.ask(user_query, models_qa = ModelsQA, models_query_analyzer = ModelsQueryAnalysis) 

    print(f"\nMatched Passages from each Doc =>") 
    for doc in response: 
        for file_name, agent_resp in doc.items():
            print(f"\nFile: {file_name}")
            print(f"Response >>> {agent_resp}\n") 
            
    
    print(f"Relevant DOcs: {doc_list}") 
    print(f"Relevant Queries: {sub_queries}") 

    
    return 

if __name__ == '__main__':
    curr_dir = os.getcwd() 
    env_path = sys.path[0] 

    main()
    
