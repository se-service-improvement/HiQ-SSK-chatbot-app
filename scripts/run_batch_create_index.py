import copy
import json
import os
import subprocess
import tqdm
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()  

FORM_RECOGNIZER_KEY = os.getenv("FORM_RECOGNIZER_KEY")

with open("./config.json", "r") as f:
***REMOVED***config = json.loads(f.read())

# this is an example, 
# it address how to handle subfolders 
# it also provide option wether to use form recognizer
run_config_by_data_path_3_small_512_512 = {
***REMOVED***"aks": "aks_embed_003_small_512_512_index",
***REMOVED***"azure-docs": {
***REMOVED***"index": "azure_embed_003_small_512_512_index",
***REMOVED***"subfolder": "azure-docs",
***REMOVED***,
***REMOVED***"test_loranorm": {
***REMOVED***"index": "test_loranorm_embed_003_small_512_512_index",
***REMOVED***"form-rec-use-layout": False,
***REMOVED***,
***REMOVED***
}

for key, cfg in tqdm.tqdm(run_config_by_data_path_3_small_512_512.items()):
***REMOVED***# folder is where data is saved
***REMOVED***folder = os.path.join("/index_data", key)
***REMOVED***
***REMOVED***if isinstance(cfg, str):
***REMOVED***index = cfg
***REMOVED***form_rec_use_layout = True
***REMOVED***else:
***REMOVED***index = cfg["index"]
***REMOVED***form_rec_use_layout = cfg.get("form-rec-use-layout", True)
***REMOVED***if "subfolder" in cfg:
***REMOVED******REMOVED***folder = os.path.join(folder, cfg["subfolder"])


***REMOVED***config_key = copy.deepcopy(config[0])
***REMOVED***config_key["data_path"] = os.path.abspath(folder)
***REMOVED***config_key["index_name"] = index

***REMOVED***print(config_key["data_path"])
***REMOVED***with open(f"./config.{key}.json", "w") as f:
***REMOVED***f.write(json.dumps([config_key]))
***REMOVED***
***REMOVED***command = [
***REMOVED***"python",
***REMOVED***"data_preparation.py",
***REMOVED***"--config",
***REMOVED***f"config.{key}.json",
***REMOVED***"--embedding-model-endpoint",
***REMOVED***'"EMBEDDING_MODEL_ENDPOINT"',
***REMOVED***"--form-rec-resource",
***REMOVED***"test-tprompt",
***REMOVED***"--form-rec-key",
***REMOVED***FORM_RECOGNIZER_KEY,
***REMOVED***] + (["--form-rec-use-layout"] if form_rec_use_layout else []) + [
***REMOVED***"--njobs=8",
***REMOVED***]
***REMOVED***str_command = " ".join(command)
***REMOVED***proc = subprocess.run(str_command, capture_output=True)
***REMOVED***if proc.returncode != 0:
***REMOVED***print("Error running", command)
***REMOVED***print(proc.stderr)
***REMOVED***print(proc.stdout)






