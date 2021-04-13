import os, sys, csv
import pandas as pd

SEMREP_FOLDER = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]

def check_start_end(start, end, original_text, sentence, file):
    from_text = sentence[start:end]
    if original_text != from_text:
        print("text does not match original text")
        print(file)
        print(sentence)
        print(original_text, "|", from_text)
        print("start =", start)
        print("end =", end)
        print()


with open(os.path.join(OUTPUT_FOLDER, "semrep_relationships.csv"), "w", newline='') as output_file:
    
    columns = """paper_id, section_id, \
                subj_max_dist, subj_dist, subj_CUI, subj_preferred_name, subj_all_semantic_types, subj_semantic_type, \
                subj_gene_id, subj_gene_name, subj_original_text, subj_change_term, subj_degree_term, \
                subj_negated, subj_confidence_score, subj_start, subj_end, \
                relation_type, relation, relation_negated, relation_start, relation_end, relation_original_text, \
                obj_max_dist, obj_dist, obj_CUI, obj_preferred_name, obj_all_semantic_types, obj_semantic_type, \
                obj_gene_id, obj_gene_name, obj_original_text, obj_change_term, obj_degree_term, \
                obj_negated, obj_confidence_score, obj_start, obj_end, \
                sentence""".replace("\\", "").split(",")
    columns = [i.strip() for i in columns]
    wr = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
    wr.writerow(columns)

    for root, dirs, files in os.walk(SEMREP_FOLDER):
        sub_dir = root.split("/")[-1]

        for filename in files:

            semrep_path = os.path.join(SEMREP_FOLDER, sub_dir, filename)
            sentence = ""
            print(semrep_path)

            try:
                semrep_output = open(semrep_path, "r")
            except:
                print(semrep_path, "does not exist")
                continue

            paper_id = filename
            section_id = 'abstract'

            # for each text/entity/relationship
            for line in semrep_output:

                # whitespace line
                if not line.strip():
                    continue

                info = line.strip().split("|")

                if len(info) < 6:
                    print("Unexpected line: not enough fields")
                    print(semrep_path)
                    print(line)
                    print()
                    continue

                info_type = info[5]

                if info_type == "relation":

                    # the sentence text was not properly formatted
                    if not sentence:
                        continue

                    info = line.strip().split("|")
                    if len(info) != 41:
                        print("Unexpected line: relation not formatted properly")
                        print(semrep_path)
                        print(line)
                        print()
                        continue

                    offset = sentence_start

                    # subject information
                    subj_max_dist = info[6]
                    subj_dist = info[7]
                    subj_CUI = info[8]
                    subj_preferred_name = info[9]
                    subj_all_semantic_types = info[10]
                    subj_semantic_type = info[11]
                    subj_gene_id = info[12]
                    subj_gene_name = info[13]
                    subj_original_text = info[14].replace("�", " ")
                    subj_change_term = info[15]
                    subj_degree_term = info[16]
                    subj_negated = info[17]
                    subj_confidence_score = info[18]
                    subj_start = int(info[19]) - offset
                    subj_end = int(info[20]) - offset

                    check_start_end(subj_start, subj_end, subj_original_text, sentence, semrep_path)

                    # relationship information
                    relation_type = info[21]
                    relation = info[22]
                    relation_negated = info[23]
                    relation_start = int(info[24]) - offset
                    relation_end = int(info[25]) - offset
                    relation_original_text = sentence[relation_start:relation_end]

                    # object information
                    obj_max_dist = info[26]
                    obj_dist = info[27]
                    obj_CUI = info[28]
                    obj_preferred_name = info[29]
                    obj_all_semantic_types = info[30]
                    obj_semantic_type = info[31]
                    obj_gene_id = info[32]
                    obj_gene_name = info[33]
                    obj_original_text = info[34].replace("�", " ")
                    obj_change_term = info[35]
                    obj_degree_term = info[36]
                    obj_negated = info[37]
                    obj_confidence_score = info[38]
                    obj_start = int(info[39]) - offset
                    obj_end = int(info[40]) - offset

                    check_start_end(obj_start, obj_end, obj_original_text, sentence, semrep_path)

                    new_data = [paper_id, section_id, \
                                subj_max_dist, subj_dist, subj_CUI, subj_preferred_name, subj_all_semantic_types, subj_semantic_type, \
                                subj_gene_id, subj_gene_name, subj_original_text, subj_change_term, subj_degree_term, \
                                subj_negated, subj_confidence_score, subj_start, subj_end, \
                                relation_type, relation, relation_negated, relation_start, relation_end, relation_original_text, \
                                obj_max_dist, obj_dist, obj_CUI, obj_preferred_name, obj_all_semantic_types, obj_semantic_type, \
                                obj_gene_id, obj_gene_name, obj_original_text, obj_change_term, obj_degree_term, \
                                obj_negated, obj_confidence_score, obj_start, obj_end, \
                                sentence]
                    wr.writerow(new_data)

                elif info_type == "entity":
                    pass
                elif info_type == "text":
                    sentence = ''
                    info = line.strip().split("|")
                    if len(info) != 9:
                        print("Unexpected line: text not formatted properly")
                        print(semrep_path)
                        print(line)
                        print()
                        continue
                    sentence = info[8] 
                    sentence_start = int(info[6])
                else:
                    print("Unexpected line: info type", info_type, "not recognized")
                    print(semrep_path)
                    print(line)
                    print()
                    continue
                
            semrep_output.close()