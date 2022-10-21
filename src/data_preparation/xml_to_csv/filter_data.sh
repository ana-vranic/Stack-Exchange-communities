#!/bin/bash

for name in "astronomy" "052012astronomy" "economics" "052012economics" "literature" "052012-literature" "physics" "052012-theoretical-physics"
do
   echo
   echo "${name}"
   
    xml_loc="../../../data/raw_xml_data/${name}"
    csv_loc="../../../data/raw_data/${name}"
   
    [ ! -d ${csv_loc} ] && mkdir -p ${csv_loc}
    q_file="${csv_loc}/${name}_questions.csv"
    
    xml_file="${xml_loc}/posts.xml"
    csv_file="${csv_loc}/${name}_questions.csv"  
    python filter_questions.py ${xml_file} ${csv_file}

    xml_file="${xml_loc}/posts.xml"
    csv_file="${csv_loc}/${name}_answers.csv"  
    python filter_answers.py ${xml_file} ${csv_file} ${q_file}

    xml_file="${xml_loc}/comments.xml"
    csv_file="${csv_loc}/${name}_comments.csv"  
    python filter_comments.py ${xml_file} ${csv_file} ${q_file}
    
    xml_file="${xml_loc}/votes.xml"
    csv_file="${csv_loc}/${name}_votes.csv"  
    python filter_votes.py ${xml_file} ${csv_file} ${q_file}

    xml_file="${xml_loc}/users.xml"
    csv_file="${csv_loc}/${name}_users.csv"  
    python filter_users.py ${xml_file} ${csv_file} ${q_file}

    a_file="${csv_loc}/${name}_answers.csv"  
    csv_file="${csv_loc}/${name}_acc_answers.csv"  
    python filter_acc_answers.py  ${q_file} ${a_file} ${csv_file}
  
done
