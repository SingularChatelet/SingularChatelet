#!/bin/env python3
# execute this from repo root

import subprocess
import shlex

print("data from site : http://www.cs.cmu.edu/~ark/QA-data/")
print("but need to be downloaded to ./data/Question_Answer_Dataset_v1.2/")

files = [
    "./data/Question_Answer_Dataset_v1.2/S08/question_answer_pairs.txt",
    "./data/Question_Answer_Dataset_v1.2/S09/question_answer_pairs.txt",
    "./data/Question_Answer_Dataset_v1.2/S10/question_answer_pairs.txt"
]

tmp_file = "./tmp_txt"

output_file = "./data/chatterbot/english/knowledge.txt"

new_corpus = """categories:
- general knowledge
conversations:
"""

fd = open(output_file, "w")
fd.close()

for file in files:
    print(f"open file {file}...")
    subprocess.run(shlex.split(f'strings {file} > {tmp_file}'))
    with open(tmp_file, "r") as fd:
        for line in fd.readlines()[1:]:
            parsed = line.split('\t')
            if len(parsed) != 6:
                continue
            question, answer = parsed[1].strip(' '), parsed[2].strip(' ')
            if "NULL" in (question, answer) or "" in (question, answer):
                continue
            new_corpus += "- - "
            new_corpus += parsed[1].strip(";!?.")
            new_corpus += "\n  - "
            new_corpus += parsed[2]
            new_corpus += "\n"
    print(f"file parsed will be added to {output_file}")
    with open(output_file, "a") as fd_out:
        fd_out.write(new_corpus)
    new_corpus = ""

print("end of all")
