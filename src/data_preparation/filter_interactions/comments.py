import pandas as pd
import numpy as np
import sys

qfile=sys.argv[1]
afile=sys.argv[2]
cfile=sys.argv[3]
ufile=sys.argv[4]

csv1=sys.argv[5]
csv2=sys.argv[6]
csv3=sys.argv[7]

questions = pd.read_csv(qfile)
answers = pd.read_csv(afile)
comments = pd.read_csv(cfile)
users = pd.read_csv(ufile)

t0 = (questions['QTime'][0])
#first we check if @UserName is mentioned in the text of the comment, so we can map CommentUserId - @UserName,  
users['@UserName']=users['@UserName'].apply(lambda x: str(x).replace(" ","").strip(";:,."))
p = users.groupby('@UserName')['@UserId'].count()
p = p.reset_index()
p = p.rename(columns={'@UserId':'N'})
merge = pd.merge(left = users, right = p, left_on='@UserName', right_on= '@UserName')
users = merge[merge['N']==1]

#find UserId 
comments = pd.merge(left = comments, right = users, how = 'left', left_on = '@UserName', right_on = '@UserName')


merge_questions = pd.merge(left=comments, right=questions, left_on='PId', right_on='QId')
merge_questions.loc[pd.isna(merge_questions['@UserId']), 'Id'] = merge_questions['QUserId']  
merge_questions.loc[pd.notna(merge_questions['@UserId']), 'Id'] = merge_questions['@UserId'] 

merge_qa = pd.merge(left=answers, right=questions, how='left', left_on='QId', right_on='QId')
merge_answers = pd.merge(left=comments, right = merge_qa, left_on='PId', right_on='AId')
merge_answers.loc[pd.isna(merge_answers['@UserId']), 'Id'] = merge_answers['AUserId']  
merge_answers.loc[pd.notna(merge_answers['@UserId']), 'Id'] = merge_answers['@UserId'] 


cq = merge_questions
ca = merge_answers

# comments and questions
cqt = cq[['Id', 'CUserId', 'QId', 'CTime']]
cqt = cqt.rename(columns={"Id": "PostUserId", "CUserId":"RespondUserId", 'CTime':"Time"})
cqt['days'] = ((pd.to_datetime(cqt['Time']) - pd.to_datetime(t0)).dt.days)  
cqt.to_csv(csv1, index=False)

#comments and answers
cat = ca[['Id', 'CUserId', 'QId', 'CTime']]
cat = cat.rename(columns={"Id": "PostUserId", "CUserId":"RespondUserId", 'CTime':"Time"})
cat['days'] = ((pd.to_datetime(cat['Time']) - pd.to_datetime(t0)).dt.days)  
cat.to_csv(csv2, index=False)

#comments on questions ans answers
comments = pd.concat([cqt,cat])
comments.to_csv(csv3, index=False)
