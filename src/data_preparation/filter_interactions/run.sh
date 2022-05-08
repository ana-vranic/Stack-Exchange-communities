#!/bin/bash

for name in "astronomy" "052012astronomy" "economics" "052012economics" "literature" "052012-literature" "physics" "052012-theoretical-physics"

do
    echo
    echo "${name}"
    loc="../../../data/raw_data/${name}"

    questions="${loc}/${name}_questions.csv"
    answers="${loc}/${name}_answers.csv"
    votes="${loc}/${name}_votes.csv"
    users="${loc}/${name}_users.csv"
    comments="${loc}/${name}_comments.csv"


    csv_loc="../../../data/interactions/${name}"
    [ ! -d ${csv_loc} ] && mkdir -p ${csv_loc}
    

    i1="${csv_loc}/${name}_interactions_post_questions.csv"
    i2="${csv_loc}/${name}_interactions_questions_answers.csv"
    i3="${csv_loc}/${name}_interactions_acc_answers.csv"
    i4="${csv_loc}/${name}_interactions_votes.csv"

    python interactions.py ${questions} ${answers} ${votes} ${i1} ${i2} ${i3} ${i4}

    i1="${csv_loc}/${name}_interactions_comments_questions.csv"
    i2="${csv_loc}/${name}_interactions_comments_answers.csv"
    i3="${csv_loc}/${name}_interactions_comments.csv"
   

    python comments.py ${questions} ${answers} ${comments} ${users} ${i1} ${i2} ${i3}

done

