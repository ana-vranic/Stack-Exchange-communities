import pandas as pd
import numpy as np
import sys

qfile=sys.argv[1] 
afile=sys.argv[2]
vfile = sys.argv[3]

csv1=sys.argv[4] #posted questions
csv2=sys.argv[5] #posted_answers 
csv3=sys.argv[6] #accepted answers
csv4=sys.argv[7] #votes file

questions = pd.read_csv(qfile)
answers = pd.read_csv(afile)
votes = pd.read_csv(vfile)

t0 = (questions['QTime'][0])

#print(qfile)
#print (t0)

post_q = questions[['QId', 'QUserId', 'QTime']]
post_q = post_q.rename(columns={'QUserId':'PostUserId', 'QTime':'Time'})
post_q['days'] = ((pd.to_datetime(post_q['Time']) - pd.to_datetime(t0)).dt.days)  
post_q.to_csv(csv1, index=False)

post_a = answers[['AId', 'AUserId', 'ATime', 'QId']]
post_a = post_a.rename(columns={'AUserId':'PostUserId', 'ATime':'Time'})

questions_answers = pd.merge(questions, answers, left_on='QId', right_on='QId')
qa = questions_answers[['QId', 'QUserId', 'AUserId', 'ATime']]
qa = qa.rename(columns={"QUserId":"PostUserId", "AUserId":"RespondUserId", 'ATime':'Time'})
qa['days'] = ((pd.to_datetime(qa['Time']) - pd.to_datetime(t0)).dt.days)  
qa.to_csv(csv2, index=False)

acc = questions[pd.notna(questions['QAcceptedAnswerId'])]
acc_answers = pd.merge(acc, answers, left_on='QAcceptedAnswerId', right_on="AId" )
acc_answers = acc_answers[['QId_x', 'QUserId', 'AUserId', 'ATime']]
acc_answers = acc_answers.rename(columns={'QId_x':"QId", "QUserId":"RespondUserId", "AUserId":"PostUserId", 'ATime':'Time'})
acc_answers['days'] = ((pd.to_datetime(acc_answers['Time']) - pd.to_datetime(t0)).dt.days) 

acc_answers.to_csv(csv3, index=False)

votes = votes[(votes['Vote']==2 ) | (votes['Vote']==3)]
votes_q = pd.merge(left = votes, right=post_q, left_on='PostId', right_on='QId', how='left').dropna()
votes_a = pd.merge(left = votes, right=post_a, left_on='PostId', right_on='AId', how='left').dropna()
votes_q = votes_q[['QId', 'PostUserId', 'Vote', 'VTime']]
votes_a = votes_a[['QId', 'PostUserId', 'Vote', 'VTime']]

votes = pd.concat([votes_q, votes_a])
votes = votes.rename(columns={'VTime':'Time'})
votes['days'] = ((pd.to_datetime(votes['Time']) - pd.to_datetime(t0)).dt.days) + 1
votes.dropna().to_csv(csv4, index=False)