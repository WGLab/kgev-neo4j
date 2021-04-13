# KGEV Stage 2: triple processing

`process_semrep_triples.ipynb` processes the SemRep triples by doing entity and relationships standardization and triple filtering. It also formats the Text entities/nodes and Text-Document relationships for Neo4j Import.  

The code requires `SemanticTypes_2018AB.txt` and `SemGroups_2018.txt` to be downloaded from https://metamap.nlm.nih.gov/SemanticTypesAndGroups.shtml [1] and placed in the `semantic_type_files` directory. These two files are used to map semtype abbreciations to their respective semantic group.  

Also, `Disease_COVID-19.txt` and `Virus_SARS-CoV-2.txt` should be downloaded from https://github.com/Aitslab/corona/tree/master/dictionaries [2] and placed in the `covid_19_dictionaries` directory. These two files are used to standard COVID-19-related entities.  

[1] Aronson AR: Effective mapping of biomedical text to the UMLS Metathesaurus: the MetaMap program. Proc AMIA Symp 2001:17-21.  

[2] Kazemi Rashed S, Frid J, Aits S: English dictionaries, gold and silver standard corpora for biomedical natural language processing related to SARS-CoV-2 and COVID-19. In.; 2020: arXiv:2003.09865.  