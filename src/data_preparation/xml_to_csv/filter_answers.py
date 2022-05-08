import pandas as pd
import xml.etree.ElementTree as etree
import sys

def filter_first_N_days(dataframe_q, Ndays):
    dataframe_q["QTime"] = pd.to_datetime(dataframe_q['QTime']) 

    t0 = dataframe_q[dataframe_q['QId']==1]["QTime"].item()
    print(t0)
    
    tmax = t0 + pd.Timedelta(days=Ndays)
    print(t0, tmax)
    return t0, tmax

#filter answers

xml_file = sys.argv[1] #'../data/launched/astronomy/Posts.xml'
csv_file = sys.argv[2] #'./launched/astronomy/astronomy_answers.csv'
q_file = sys.argv[3] # questions csv

tree = etree.parse(xml_file)
root = tree.getroot()

#columns = ["AId", "AUserId", "QId", "ATime", "AScore", "ACommentCount"]
#dataframe = pd.DataFrame(columns = columns)
dictn = {}
i=0
for node in root: 
    OID=node.get("OwnerUserId")
    #if OID is not None:
    PST = node.get("PostTypeId")
    if PST=="2":
        ID = node.get("Id")
        PID = node.get("ParentId")
        Time=node.get("CreationDate")
        Score=node.get("Score")
        CCount=node.get("CommentCount")
        dictn [i] = {"AId": ID, "AUserId": OID, "QId": PID, "ATime":Time, "AScore":Score, "ACommentCount":CCount}
        i+=1

dataframe = pd.DataFrame.from_dict(dictn, "index")


questions = pd.read_csv(q_file)
t0, tmax = filter_first_N_days(questions, 180)
dataframe["ATime"] = pd.to_datetime(dataframe['ATime']) 

dataframe = dataframe[(dataframe['ATime']>=t0) & (dataframe['ATime']<tmax)]

dataframe.to_csv(csv_file, index=False)
