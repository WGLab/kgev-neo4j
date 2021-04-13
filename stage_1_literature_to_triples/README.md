# KGEV Stage 1: literature to triples

`process_semrep_abstracts.py` processes SemRep output and converts it into a .csv file, `semrep_relationships.csv`, where each row in the .csv file is a relationship detected by SemRep. Run this script with `python3 process_semrep_abstracts.py [SEMREP_FOLDER] [OUTPUT_FOLDER]`, where `SEMREP_FOLDER` is a directory containing the output from SemRep (it can include multiple sub-directories if the data are in parts) and `OUTPUT_FOLDER` is the directory in which the .csv file will be created.
