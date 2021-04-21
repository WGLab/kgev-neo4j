# kgev-neo4j

KGEV (Knowledge Graph Exploration and Visualization) is a web framework for expediting knowledge acquisition using Knowledge Graph.

## Abstract

**Background**: Knowledges graphs (KGs) serve as a convenient framework for structuring knowledge. A number of computational methods have been developed to generate KGs from biomedical literature and use them for downstream tasks such as link prediction and questioning and answering. However, there is a lack of computational tools or web frameworks to support the exploration and visualization of the KG themselves, which would facilitate interactive knowledge discovery and formulation of novel biological hypotheses. 

**Method**: We developed a web framework for Knowledge Graph Exploration and Visualization (KGEV), to construct and visualize KGs in five stages: triple extraction, triple filtration, metadata preparation, knowledge integration, and graph database presentation. The application has convenient user interface tools such as node and edge search and filtering, data source filtering, neighborhood retrieval, shortest path calculation, by querying a backend graph database. Unlike other KGs, our framework allows fast retrieval of relevant texts supporting the relationships in the KG, thus allowing human reviewers to judge the reliability of the knowledge extracted. 

**Results**: We demonstrated a case study of using the KGEV framework to perform research on COVID-19. The COVID-19 pandemic resulted in an explosion of relevant literature, making it challenging to make full use of the vast and heterogenous sources of information. We generated a COVID-19 KG with heterogenous information, including literature information from the CORD-19 dataset, as well as other existing knowledge from eight data sources. We showed the utility of KGEV in three intuitive case studies to explore and query knowledge on COVID-19. A demo of this web application can be accessed at http://covid19nlp.wglab.org. Finally, we also demonstrated a turn-key adaption of the KGEV framework to study clinical phenotypic presentation of human diseases, illustrating the versatility of the framework. 

**Conclusion**: In an era of literature explosion, the KGEV framework can be applied to many emerging diseases to support structured navigation of the vast amount of newly published biomedical literature and other existing biological knowledge in various databases. It can be also used as a general-purpose tool to explore and query gene-phenotype-disease-drug relationships interactively.

## Examples of web interface

**Figure**: Web application user interface. 1) The left panel is a graph view that shows the nodes and edges returned from a search. Nodes and edges are labelled and color-coded for an effective user experience. A node can be clicked on to return more information on the entity, such as its UMLS concept Unique Identifier (CUI), semantic group(s), and synonyms. Clicking an edge will bring up information on the triple, including the supporting texts, in the panel on the right, which the image demonstrates. 2) In addition to viewing the search results as a graph, one can use the list view to view the same nodes and edges in a table, which can be sorted. 3) The right panel will show information on the triple that was clicked on. The head, relationship, and tail of the triple are color-coded in the text for easy interpretation. Metadata information of the text can be seen by clicking “Paper details”. Covering over highlighted text shows more information about the entity. 4) The right panel also has a tab to do the actual search. One can select the type of search, the node to search for, whether or not to use fuzzy search, what node filters to use, as well as 5) what edge filters to use, the edge direction, what data sources to use, and how many supporting texts are required.

![image](https://user-images.githubusercontent.com/5926328/114648025-14128c80-9cac-11eb-9f1c-e82df10bb753.png)

**Figure**: Use KGEV to study human disease phenotypes. The entire HPO database of disease-phenotype relationships was stored in a new Neo4j database. Just by swapping the database, one can use the same user interface to query the KG, but on a different set of data. The figure shows an example of finding the shortest path between polydactyly, syndactyl, and cleft palate phenotypes to determine diseases that share at least two of the three phenotypes.

![image](https://user-images.githubusercontent.com/5926328/114648128-4a500c00-9cac-11eb-9164-af74c22958a4.png)



### KGEV pipeline  
The different stages of the pipeline are represented by the different sub-directories. Separate README files are in each sub-directory to explain each stage of the pipeline.    

Instead of running Stage 1 to extract triples from literature (i.e. applying SemRep on CORD-19 abstracts), you can download [semrep_relationships.csv](https://drive.google.com/file/d/1OpqYHsc6GaNLiQh-n9aSkSJ112MJktfU/view?usp=sharing) and place it in a sub-directory called `data` directly within the root directory of this project. `semrep_relationships.csv` is the file that is outputted from Stage 1 of the KGEV pipeline.   

### Setting up the Neo4j database

On the server you want to run Neo4j on, make sure Docker is installed. Once this is done, navigate to your home directory on the server. Run the following bash commands to create the relevant folders for running Neo4j.    
```
mkdir neo4j  
mkdir neo4j/data 
mkdir neo4j/logs
mkdir neo4j/import
mkdir neo4j/plugins
``` 

Move the .csv files outputted by the KGEV pipeline in the `NEO4J_OUTPUT_DIR` into neo4j/import.  

Then run the following lines in the terminal (replacing [NEO4J_USERNAME and [NEO4J_PASSWORD] with their true values). This creates a Docker container called `kgev-neo4j` that runs Neo4j.   

```
docker run \
    --name kgev-neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --user=$(id -u):$(id -g) \
    --env NEO4J_AUTH=[NEO4J_USERNAME]/[NEO4J_PASSWORD] \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS='["apoc"]' \
    -it \
    neo4j:latest \
    -c /bin/bash
```

Once this container is running, enter the container by running the command `docker exec -it kgev-neo4j bash`. This opens a terminal within the container. Now, run the following commands.  
```
cd import 
../bin/neo4j-admin import \
     --nodes=nodes.csv \
     --nodes=metadata.csv \
     --nodes=text_nodes.csv \
     --relationships=edges.csv \
     --relationships=text_edges.csv \
     --multiline-fields=true
```

This should import the files we copied into the `import` folder earlier into the Neo4j database.

Now, stop the container using `docker stop kgev-neo4j` and delete it using `docker rm kgev-neo4j`. Now, we want to recreate the container so that it runs the database. Run the following lines (replacing [NEO4J_USERNAME and [NEO4J_PASSWORD] with their true values).  

```
docker run \
    --name kgev-neo4j \
    -p7474:7474 -p7687:7687 \
    -d \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    --user=$(id -u):$(id -g) \
    --env NEO4J_AUTH=[NEO4J_USERNAME]/[NEO4J_PASSWORD] \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4JLABS_PLUGINS='["apoc"]' \
    neo4j:latest
```

Now, we want to complete our setup of the database. Enter the container again using  
`docker exec -it kgev-neo4j bash`  
and enter the Cypher shell (Cypher is a query language for Neo4j) by running  
`cypher-shell -u [NEO4J_USERNAME] -p [NEO4J_PASSWORD]`  
(replacing [NEO4J_USERNAME and [NEO4J_PASSWORD] with their true values).  

Within the Cypher shell, run    
```
MATCH (n:Item)
CALL apoc.neighbors.athop.count(n, '>', 1)
YIELD value AS v1
CALL apoc.neighbors.athop.count(n, '<', 1)
YIELD value AS v2
SET n.degree = v1 + v2;
```
to add the degree information for each node.  

Then, also within the Cypher shell, run  
```
CALL db.index.fulltext.createNodeIndex('items', ["Item"], ['id', 'identifier']);  
```
to optimize searching by creating a full-text index over the nodes. Now you can exit using `:exit` and then exit the container (ctrl+c).  

The Neo4J database should be completely up and running now.  


### Setting up the Frontend and the Backend
To run the frontend of the KGEV web applcation use the [genomicslab/kgev-frontend](https://hub.docker.com/r/genomicslab/kgev-frontend) Docker container.  
Similarly, to run the backend of the KGEV web applcation use the [genomicslab/kgev-backend](https://hub.docker.com/r/genomicslab/kgev-backend) Docker container.  


