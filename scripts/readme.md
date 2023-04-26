# Data Preparation

## Setup
- Install the necessary packages listed in requirements.txt, e.g. `pip install --user -r requirements.txt`

## Configure
- Create a config file like `config.json`. The format should be a list of JSON objects, with each object specifying a configuration of local data path and target search service and index.

```
[
***REMOVED***{
***REMOVED***"data_path": "<path to data>",
***REMOVED***"location": "<azure region, e.g. 'westus2'>", 
***REMOVED***"subscription_id": "<subscription id>",
***REMOVED***"resource_group": "<resource group name>",
***REMOVED***"search_service_name": "<search service name to use or create>",
***REMOVED***"index_name": "<index name to use or create>",
***REMOVED***"chunk_size": 1024, // set to null to disable chunking before ingestion
***REMOVED***"token_overlap": 128 // number of tokens to overlap between chunks
***REMOVED***"semantic_config_name": "default"
***REMOVED***
]
```

## Create Indexes and Ingest Data
- Run the data preparation script, passing in your config file.

***REMOVED*** `python data_preparation.py --config config.json`

