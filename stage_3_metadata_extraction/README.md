# KGEV Stage 3: metadata extraction

`process_metadata.ipynb` extracts the metadata for all Documents/papers after Stage 2 (i.e. the documents/papers the processed triples are mapped to) and formats the information for Neo4j import.   

The code requires `metadata.csv` to be downloaded from CORD-19 (https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge) [1] and placed in the `data` directory at the root of this project. This file contains the CORD-19 metadata.    

The code also requires a .csv file called `journal_data.csv` to map journal names to the jounal's impact factor/other information, where one column contains the journal name and another column contains the journal impact factor/information.   

[1] Lu Wang L, Lo K, Chandrasekhar Y, Reas R, Yang J, Eide D, Funk K, Kinney R, Liu Z, Merrill W et al: CORD-19: The Covid-19 Open Research Dataset. ArXiv 2020.   