import pandas as pd
import sys
qfile = sys.argv[1] #'launched/astronomy/astronomy_questions.csv'
afile = sys.argv[2] #'launched/astronomy/astronomy_answers.csv'
csv_file=sys.argv[3]

a = pd.read_csv(afile)
q = pd.read_csv(qfile)

acc = q[pd.notna(q['QAcceptedAnswerId'])]

df = pd.merge(acc, a, left_on='QAcceptedAnswerId', right_on="AId" ).drop_duplicates()

df.to_csv(csv_file, index=None)
