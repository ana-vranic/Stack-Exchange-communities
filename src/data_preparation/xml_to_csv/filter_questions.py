import pandas as pd
import xml.etree.ElementTree as etree
import sys


def filter_first_N_days(dataframe_q, dataframe, Ndays):
    dataframe_q["QTime"] = pd.to_datetime(dataframe_q['QTime']) 
    t0 = dataframe_q[dataframe_q['QId']=="1"]["QTime"].item()
    tmax = t0 + pd.Timedelta(days=Ndays)

    return t0, tmax



#filter questions
#file = '../astronomy/Posts.xml'

xml_file = sys.argv[1] #'../data/launched/astronomy/Posts.xml'
csv_file = sys.argv[2] #'./launched/astronomy/astronomy_questions.csv'
tree = etree.parse(xml_file)
root = tree.getroot()

columns = ["QId", "QUserId", "QTags", "QTime", "QAcceptedAnswerId", "QScore", "QViewCount", "QAnswerCount", "QCommentCount"]
#dataframe = pd.DataFrame(columns = columns)
dictn = {}
i=0
for node in root: 
    OID=node.get("OwnerUserId")
    PST = node.get("PostTypeId")
    if PST=="1":
        ID = node.get("Id")
        Tags = node.get("Tags")
        Time=node.get("CreationDate")
        AAId=node.get("AcceptedAnswerId")
        Score=node.get("Score")
        VCount=node.get("ViewCount")
        ACount=node.get("AnswerCount")
        CCount=node.get("CommentCount")
        dictn[i] = {"QId": ID, "QUserId": OID, "QTags": Tags, "QTime": Time, "QAcceptedAnswerId":AAId, "QScore":Score, "QViewCount":VCount, "QAnswerCount":ACount, "QCommentCount":CCount}
        i+=1


dataframe = pd.DataFrame.from_dict(dictn, "index")


#filter first 180 days 
#dataframe["QTime"] = pd.to_datetime(dataframe['QTime']) 
##t0 = dataframe[dataframe['QId']=="1"]["QTime"].item()
#tmax = t0 + pd.Timedelta(days=180)
#dataframe = dataframe[(dataframe['QTime']>=t0)]

t0, tmax = filter_first_N_days(dataframe, dataframe, 180)
dataframe = dataframe[(dataframe['QTime']>=t0) & (dataframe['QTime']<tmax)]

dataframe.to_csv(csv_file, index=False)
