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

i=0
dict = {}
for node in root: 
    UId=node.get("Id")
    
    #if OID is not None:
    Name = node.get("DisplayName")#.replace(" ", "")#.strip(";:,.")
    R=node.get("Reputation")
    V=node.get("Views")
    Up=node.get("UpVotes")
    Down=node.get("DownVotes")
    Time=node.get("CreationDate")
    Age=node.get("Age")
    Location=node.get("Location")
    LastAccess=node.get("LastAccessDate")
    #AccountId=node.get("AccountId")

    dict[i] = {"@UserId": UId, "@UserName": Name, "Age": Age, "Location":Location, 'UserCreationDate': Time, 
            "Reputation": R, "Views": V, "UpVotes":Up, "DownVotes": Down, "LastAccess": LastAccess, }#"AccountId":AccountId }
    #account id doesnt exist for area 51  
    i+=1
    

dataframe = pd.DataFrame.from_dict(dict, "index")    
questions = pd.read_csv(q_file)
t0, tmax = filter_first_N_days(questions, 180)
dataframe["UserCreationDate"] = pd.to_datetime(dataframe['UserCreationDate']) 

dataframe = dataframe[(dataframe['UserCreationDate']<tmax)]
dataframe.to_csv(csv_file, index=False)
