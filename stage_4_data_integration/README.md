# KGEV Stage 4: data integration

`format_gene_mapping.ipynb` created a .csv file `interaction_data/gene_mapping.csv` that helps map between different gene IDs. It uses gene information from HGNC (https://www.genenames.org/download/custom/) [1] and UMLS (HGNC to CUI using `MRCONSO.RRF`, which can be downloaded here: https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html) [2] for the mapping.  

`process_data_sources.ipynb` formats the data sources so it can be integrated with the SemRep triples. Specifically it maps entity IDs to CUI. The code requires:  
`curated_gene_disease_associations.tsv` downloaded from DisGeNET (https://www.disgenet.org/downloads) [3],  
`drug_gene_interactions.tsv` downloaded from DGIdb (https://www.dgidb.org/downloads) [4],  
`9606.protein.links.v11.0.txt` and `9606.protein.info.v11.0.txt` downloaded from STRING (https://string-db.org/cgi/download?sessionId=%24input-%3E%7BsessionId%7D&species_text=Homo+sapiens) [5],  
`uniprot-filtered-organism__Homo+sapiens+(Human)+[9606]_+AND+review--.tab` downloaded from UniProt (https://www.uniprot.org/uniprot/?query=*&fil=organism%3A%22Homo+sapiens+%28Human%29+%5B9606%5D%22+AND+reviewed%3Ayes) [6],  
`genes_to_phenotype.txt` and `phenotype_annotation.tab` downloaded from HPO (https://hpo.jax.org/app/download/annotation) [7]. Additionally, the file `doid_formatted.tsv` is required to map OMIM to CUI. The file was created by inputting `doid.obo` from Disease Ontology (http://www.obofoundry.org/ontology/doid.html) into a tool that converts .obo to .tsv (https://github.com/macarthur-lab/obo_parser).    
All these files should be placed in the `integration_data` directory.  

`integrate_data_source.ipynb` integrates the additional data sources with the SemRep triples.    

[1] Tweedie S, Braschi B, Gray K, Jones TEM, Seal RL, Yates B, Bruford EA: Genenames.org: the HGNC and VGNC resources in 2021. Nucleic Acids Res 2021, 49(D1):D939-D946.  

[2] Bodenreider O: The Unified Medical Language System (UMLS): integrating biomedical terminology. Nucleic Acids Res 2004, 32(Database issue):D267-270.  
 
[3] Piñero J, Bravo À, Queralt-Rosinach N, Gutiérrez-Sacristán A, Deu-Pons J, Centeno E, García-García J, Sanz F, Furlong LI: DisGeNET: a comprehensive platform integrating information on human disease-associated genes and variants. Nucleic Acids Res 2017, 45(D1):D833-D839.  

[4] Cotto KC, Wagner AH, Feng YY, Kiwala S, Coffman AC, Spies G, Wollam A, Spies NC, Griffith OL, Griffith M: DGIdb 3.0: a redesign and expansion of the drug-gene interaction database. Nucleic Acids Res 2018, 46(D1):D1068-D1073.  

[5] Szklarczyk D, Gable AL, Lyon D, Junge A, Wyder S, Huerta-Cepas J, Simonovic M, Doncheva NT, Morris JH, Bork P et al: STRING v11: protein-protein association networks with increased coverage, supporting functional discovery in genome-wide experimental datasets. Nucleic Acids Res 2019, 47(D1):D607-D613.  

[6] Consortium U: UniProt: a worldwide hub of protein knowledge. Nucleic Acids Res 2019, 47(D1):D506-D515.   

[7] Robinson PN, Köhler S, Bauer S, Seelow D, Horn D, Mundlos S: The Human Phenotype Ontology: a tool for annotating and analyzing human hereditary disease. Am J Hum Genet 2008, 83(5):610-615.  