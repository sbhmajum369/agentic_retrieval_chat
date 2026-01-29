# Talk to PDF  



## Installation  

### Step 1 (python setup)  
Create `venv` and from inside it run *`dep_install_...`* following file for complete installation,  

* `python -m venv .venv`  
* `.venv/Scripts/activate.bat` OR `.venv/bin/activate`  
* For Linux OS: run `dep_install_windows.bat`  
   For Windows OS (>=10.0): run `dep_install_linux.sh`  

### Step 2 (ollama setup)  

* Install [Ollama](https://github.com/ollama/ollama)  
* Pull the model: `ollama pull llama3.2` (current list can be found at *main.py*)  


## Usage  

### Extraction  
Usage for extraction of data in a JSON from PDF (*coming soon*)  


### Chat  
After extracting the PDF data and metadata you can chat with the `.json` files using the **Chat** module.  
In general you can use any `.json` file for this functionality, you have to follow only the following schema structure.  

```json
{
  "Title": "JPEG INSPIRED DEEP LEARNING",
  "File_Name": "Squad_dataset.pdf",
  "Section 0": {
    "Text": "The Normans (Norman: Nourmands; ...",
  },
  "Section 1": {
    "Text": "The United Kingdom is the fourth largest exporter of goods ...",
    "Image_paths": [],
    "Image_captions": [],
    "Tables": [],
    "Table_captions": [],
    "Equations": {}
  },
}
```  


Start Ollama server:  
`ollama serve`  

In the `main.py`:  
1) Update you local JSON folder path  
2) Enter your query  
3) Select the models for *`ModelsQA`* and *`ModelsQueryAnalysis`*  
4) Run `python main.py`  

HuggingFace and Sentence-Transformer models will auto download the first time. Later you can run it totally OFFLINE.  


```python
json_path = "./sample_docs" 

user_query = "Summarize the information in 2410.07081v3_parsed.json" 

local_agent = agent.ActiveSearchAgent(json_dir_path=json_path) 

response, doc_list, sub_queries, matched_src_text = local_agent.ask(user_query, models_qa = ModelsQA, models_query_analyzer = ModelsQueryAnalysis) 

```


## Details  

It is a 2 Stage application.  

The **extraction** module extracts text, image, tables and other metadata from a PDF (preferably scientific paper) and saves the data. The `.json` file contains all the textual data and metadata including a summary of the paper. 

The **chat** module acts as an Agent and scans through the files, to find relevant text chunks and also generates answers for each query/meta-queries. The goal is to use it with a reasoning model for grounded information retrieval. (*more updates coming soon*)  

This was built with local GPU powered device usage in mind. Hence, "**max. each model parameter recommended is 4B**"  

At the moment Qwen3 and Gemma3 models perform relatively better at instruction following.  

Some complex queries can take much longer (~5-10 mins)  


### Sample Queries  

***Worked***:  
* What's (2^4 + 2^3 - 76 + 9) ?  
* Summarize the information in 2410.07081v3_parsed.json  
* summarize all the documents.  
* Which files mention JPEG compression in deep learning context?  
* Summarize these files: [arxiv_21345v2.json, 2410.07081v3_parsed.json]  
* Is there any reference to adversarial attacks on vision deep learning model?  
* If I used deep learning models without image compression, will my performance be better?  
* Do 2410.07081v3_parsed.json and squad_passage.json deals with JPEG compression?  

General Qs for any json file (SQUAD dataset),  
* In what country is Normandy located?  
* What century did the Normans first gain their separate identity?  
* By what main attribute are computational problems classified utilizing computational complexity theory?  


***Fails/Partially Correct***  
* Find all the github links. Find if the current document is a research paper.  
* What's (2 + 2^3 - 76) = (correct answer but wrong reference)  


## Local Hardware Requirements (baseline)  

**CPU RAM**: >=20GB  
**GPU VRAM**: 6-8GB (NVIDIA CUDA compatibile)  


________ 

Special Thanks to [@Qwen3](https://github.com/QwenLM/Qwen3) and [@gemma](https://github.com/google-deepmind/gemma) teams for building efficient and high-quality low-resource usage models. 

This version uses #HuggingFace and #Ollama for local OFFLINE usage.  



