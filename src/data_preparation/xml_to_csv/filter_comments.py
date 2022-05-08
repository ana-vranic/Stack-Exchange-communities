import pandas as pd
import xml.etree.ElementTree as etree
import sys


def filter_first_N_days(dataframe_q, dataframe, Ndays):
    dataframe_q["QTime"] = pd.to_datetime(dataframe_q['QTime']) 
    t0 = dataframe_q[dataframe_q['QId']==1]["QTime"].item()
    tmax = t0 + pd.Timedelta(days=Ndays)
    return t0, tmax


xml_file = sys.argv[1] #'../data/launched/astronomy/Comments.xml'
csv_file = sys.argv[2] #'./launched/astronomy/astronomy_comments.csv'
q_file = sys.argv[3]

tree = etree.parse(xml_file)
root = tree.getroot()

dictn = {}
i=0

for node in root: 
    OID=node.get("UserId")
    #if OID is not None:
    ID = node.get("Id")
    PID = node.get("PostId")
    Time=node.get("CreationDate")
    Score=node.get("Score")
    text = node.get("Text")
    if "@" in text:
        t = text.split('@')[1].split(" ")[0].strip(";:,.")
    else:
        t = " "
    dictn[i] = {"CId": ID, "CUserId":OID, "PId":PID, "@UserName":t, "CTime":Time, 'CScore':Score}
    i+=1
   
dataframe = pd.DataFrame.from_dict(dictn, "index") 


questions = pd.read_csv(q_file)
t0, tmax = filter_first_N_days(questions, dataframe, 180)
dataframe["CTime"] = pd.to_datetime(dataframe['CTime']) 

dataframe = dataframe[(dataframe['CTime']>=t0) & (dataframe['CTime']<tmax)]

dataframe.to_csv(csv_file, index=False)
