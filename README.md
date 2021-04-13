# kgev-neo4j  

### KGEV pipeline  
The different stages of the pipeline are represented by the different sub-directories. Separate README files are in each sub-directory to explain each stage of the pipeline.    

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

Then run the following lines in the terminal (replacing [NEO4J_USERNAME and [NEO4J_PASSWORD] with their true values). This creates a Docker container called `kgev-neo4jj` that runs Neo4j.   

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
To run the frontend of the KGEV web applcation use the [genomicslab/kgev-frontend](https://hub.docker.com/repository/docker/genomicslab/kgev-frontend) Docker container.  
Similarly, to run the backend of the KGEV web applcation use the [genomicslab/kgev-backend](https://hub.docker.com/repository/docker/genomicslab/kgev-backend) Docker container.  


