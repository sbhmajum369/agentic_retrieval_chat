
""" Main src file """
import os 
import sys 
from pprint import pprint 
from enum import Enum 
from pathlib import Path
import shutil 
import json 

# SRC_DIR = Path(__file__).resolve().parent / "src"
# sys.path.insert(0, str(SRC_DIR))

# import pyarmor_runtime_000000
# print("PyArmor runtime OK")

from src.chat import agent 
from src.extraction import extract 


## Ollama model collections 
Gemma3_4B = "gemma3:4b" 
Qwen3_4B = "qwen3:4b"
Ministral3_3B = "ministral-3:3b"


class ModelsQA(str, Enum):
    SHORT_CONTEXT = Gemma3_4B 
    LONG_CONTEXT = Gemma3_4B 

class ModelsQueryAnalysis(str, Enum):
    DECOMPOSER = Qwen3_4B 
    DIRECTORY_SEARCH = Qwen3_4B 


def run_extraction(src_path, dest_dir, json_path, page_limit:int=100, target_pdf:str=""):
    """ Extract PDF data into JSON files and save metadata images 

        Option 1: Run all PDFs (default) 
        Option 2: Run a selected file (Enable this by providing a pdf file name in 'target_pdf') 
    """ 
    
    if target_pdf.strip():
        extracted_filenames = [] 
        extract.parse_pdf(src_path, dest_dir, page_limit=page_limit, target_file=target_pdf, save_page_markdown=False) 

        root_folder = os.path.join(dest_dir, target_pdf) 
        for file in os.listdir(root_folder):
            if file.lower().endswith(".json"):
                source_path = os.path.join(root_folder, file)

                try:
                    with open(source_path, "r", encoding="utf-8") as f:
                        data = json.load(f) 
                except json.JSONDecodeError:
                    print(f"Invalid JSON, skipped: {source_path}") 
                except Exception as e:
                    print(f"Error processing {source_path}: {e}") 
                
                if "ID" not in data:
                    print(f"\nSkipping (no 'ID'): {source_path}")
                    continue 

                file_id = str(data["ID"]) 
                new_filename = f"{file_id}.json" 
                extracted_filenames.append(new_filename) 
                
                target_path = os.path.join(json_path, new_filename) 

                if os.path.exists(target_path):
                    print(f"\nDuplicate ID, skipping: {file_id}")
                    continue 

                shutil.copy2(source_path, target_path)
                print(f"\nCopied: {source_path} -> {target_path}")  
    else:
        extracted_filenames = [] 
        extract.parse_pdf(src_path, dest_dir, page_limit=page_limit, save_page_markdown=False) 

        for root in os.listdir(dest_dir):
            root_folder = os.path.join(dest_dir, root) 

            for file in os.listdir(root_folder):
                if file.lower().endswith(".json"):
                    source_path = os.path.join(root_folder, file)

                    try:
                        with open(source_path, "r", encoding="utf-8") as f:
                            data = json.load(f) 
                    except json.JSONDecodeError:
                        print(f"Invalid JSON, skipped: {source_path}") 
                    except Exception as e:
                        print(f"Error processing {source_path}: {e}") 
                    
                    if "ID" not in data:
                        print(f"\nSkipping (no 'ID'): {source_path}")
                        continue 

                    file_id = str(data["ID"]) 
                    new_filename = f"{file_id}.json" 
                    extracted_filenames.append(new_filename) 
                    
                    target_path = os.path.join(json_path, new_filename) 

                    if os.path.exists(target_path):
                        print(f"\nDuplicate ID, skipping: {file_id}")
                        continue 

                    shutil.copy2(source_path, target_path)
                    print(f"\nCopied: {source_path} -> {target_path}") 
    
    # extract.parse_pdf(src_path, dest_dir, page_limit=10, target_file=target_pdf, save_page_markdown=False)
        
    print(f"{len(extracted_filenames)} files parsed and moved") 

    return extracted_filenames 

def run_chat(user_query:str, local_dir_path:str):
    """ AT the moment it's only 1-off search agent who will find any relevant information from the local file directory """
    local_agent = agent.ActiveSearchAgent(json_dir_path = local_dir_path) 
    
    final_response, org_detail_response, relevant_files, file_confidences, matched_src_text = local_agent.ask(user_query, models_qa = ModelsQA, models_query_analyzer = ModelsQueryAnalysis, response_smmarizer= Qwen3_4B) 
    
    ## Visualize original responses 
    # for doc in org_detail_response: 
    #     for file_name, agent_resp in doc.items():
    #         print(f"File: {file_name}") 
    #         print(f"Response >>> {agent_resp}\n")
    
    FOUND = False 
    print(f"\nFinal Response from each Doc =>\n") 
    for doc in final_response: 
        for file_name, agent_resp in doc.items():
            FOUND = True 
            print(f"File: {file_name}") 
            print(f"Response >>> {agent_resp}\n") 

    if FOUND:
        print(f"Final Relevant DOcs: {relevant_files}\n") 
        print("Original Relevant doc confidences:") 
        pprint(file_confidences, width=80, sort_dicts=False) 
        # print(f"Relevant Texts: {matched_src_text}") 
    else:
        print("No references or relevant data found in the current document folder!") 
    
    return 

## Trajectory 
## PDF -> JSON (run_extraction() -> run_chat()) 
""" Select between the 2 modes and run """

def main():
    pdf_src_path = os.path.abspath("sample_docs/pdf") 
    pdf_dest_dir = os.path.abspath("sample_docs/pdf_output") 
    json_path = os.path.abspath("sample_docs/JSON") 

    os.makedirs(pdf_dest_dir, exist_ok=True) 
    os.makedirs(json_path, exist_ok=True) 

    ## EXTRACTION module ## 
    extracted_file_names = run_extraction(pdf_src_path, pdf_dest_dir, json_path, page_limit=5) 

    ## CHAT module ## 
    # Samples:
    # "Find the main authors of all the research papers in the document collection." 
    # "What is (2 + 2^3 - 76) = ?"  => No answer 
    user_input = "Find the main authors of all the research papers in the document collection." 
    run_chat(user_input, json_path) 

    
    return 

if __name__ == '__main__':
    curr_dir = os.getcwd() 
    env_path = sys.path[0] 

    main()



