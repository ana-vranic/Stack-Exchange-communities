import pandas as pd
import xml.etree.ElementTree as etree
import sys

def filter_first_N_days(dataframe_q, Ndays):
    dataframe_q["QTime"] = pd.to_datetime(dataframe_q['QTime']) 
    t0 = dataframe_q[dataframe_q['QId']==1]["QTime"].item()
    tmax = t0 + pd.Timedelta(days=Ndays)

    return t0, tmax


xml_file = sys.argv[1] #'../data/launched/astronomy/Users.xml'
csv_file = sys.argv[2] #'./launched/astronomy/astronomy_users.csv'
q_file = sys.argv[3]


tree = etree.parse(xml_file)
root = tree.getroot()

columns = ["PostId", "Vote","VTime"]
dictn={}
i=0
#dataframe = pd.DataFrame(columns = columns)
for node in root: 
    
    ID=node.get("PostId")
    V = node.get("VoteTypeId")
    time=node.get("CreationDate")
    dictn[i] = { "PostId": ID, "Vote": V, "VTime": time
            }
    
    i+=1
dataframe = pd.DataFrame.from_dict(dictn, "index")

questions = pd.read_csv(q_file)
t0, tmax = filter_first_N_days(questions, 180)
dataframe["VTime"] = pd.to_datetime(dataframe['VTime']) 

dataframe = dataframe[(dataframe['VTime']>=t0) & (dataframe['VTime']<tmax)]

dataframe.to_csv(csv_file, index=False)
