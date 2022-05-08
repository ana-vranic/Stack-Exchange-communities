import pandas as pd

def merge_interactions (qa, comm, acc, q,  ltlim, htlim, reputation):

    i1 = qa[(qa['days']<htlim)&(qa['days']>=ltlim)]
    i1 = i1[i1['PostUserId']!=i1['RespondUserId']]
    
    a1 = acc[(acc['days']<htlim)&(acc['days']>=ltlim)]
    a1 = a1[a1['PostUserId']!=a1['RespondUserId']]
    
    c1 = comm[(comm['days']<htlim)&(comm['days']>=ltlim)]
    c1 = c1[c1['PostUserId']!=c1['RespondUserId']]
    

    if reputation=='pop':
        it = pd.concat([ i1[['PostUserId', 'Time', 'days']], 
                         a1[['PostUserId', 'Time', 'days']], 
                         c1[['PostUserId', 'Time', 'days']],])
        it = it.rename(columns={'PostUserId':'UserId'})  
        return it.dropna().sort_values(by='Time')

    if reputation=='eng':
        q1 = q[(q['days']<htlim)&(q['days']>=ltlim)]

        it = pd.concat([ i1[['RespondUserId', 'Time', 'days']], 
                         a1[['RespondUserId', 'Time', 'days']], 
                         c1[['RespondUserId', 'Time', 'days']],])
        it = it.rename(columns={'RespondUserId':'UserId'})  
        q1 = q1.rename(columns={'PostUserId':'UserId'})
        f = pd.concat([  it[['UserId', 'Time', 'days']], 
                         q1[['UserId', 'Time', 'days']]])
        
        return f.dropna().sort_values(by='Time')

def prepare_data(name, ltlim, htlim, reputation, path):
    #path = "data/interactions/%s/"%name
    qa = pd.read_csv(path+'%s_interactions_questions_answers.csv'%(name))
    comm = pd.read_csv(path+'/%s_interactions_comments.csv'%(name))
    acc = pd.read_csv(path+'/%s_interactions_acc_answers.csv'%(name))
    q = pd.read_csv(path+'/%s_interactions_post_questions.csv'%(name))

    data = merge_interactions (qa, comm, acc, q,  ltlim, htlim, reputation)
    return data

def Nusers_sw(data, end, step):
    # users in the sliding window
    nusers = []
    for lday in range(end-step):
        i = data[(data['days']>=lday) & (data['days']<lday+step)]['UserId'].unique()
        nusers.append((lday+step, len(i)))
    x, y = zip(*nusers)
    return x, y


##################################################################
#calculate first and last activity of user

def activity_times(interactions):
    
    conversations = {}

    for i in range(len(interactions)):
        l = interactions.iloc[i]
        u = l['UserId'];  d = l['Time']
        key = u
        curr_u = conversations.get(key, [])
        curr_u.append(d)
        conversations[key] = curr_u
    return conversations

def cal_first_activity(users_activity):
    
    last_activity = {}
    for user, t in users_activity.items():
       
        times = sorted([ pd.to_datetime(t[i]) for i in range(len(t))], reverse=False)
        last_activity[user] = min(times)
        
    return last_activity

def cal_last_activity(users_activity):
    
    last_activity = {}
    for user, t in users_activity.items():
       
        times = sorted([ pd.to_datetime(t[i]) for i in range(len(t))], reverse=False)
        last_activity[user] = max(times)
        
    return last_activity

def get_first_last_activity(name, ltlim, htlim, path):
    df = prepare_data(name, ltlim, htlim, 'eng', path)
    t0 = df['Time'].min()

    activity = activity_times(df) #make dictionaries with users activity
    first_activity = cal_first_activity(activity) #first activity
    last_activity = cal_last_activity(activity) #last activity

    #finaly fill 
    def fill_first_time(x):
        return (pd.to_datetime(first_activity[x])-pd.to_datetime(t0) ).days

    def fill_last_time(x):
        return (pd.to_datetime(last_activity[x])-pd.to_datetime(t0) ).days
        
    df['first_time'] = df['UserId'].apply(fill_first_time)
    df['last_time'] = df['UserId'].apply(fill_last_time)

    return df

###################################################################################

#from dataframe [UserId, Time, first_time, last_time] we can calculate following:

#total number of users in the sliding window

def active_users(df, window): 
    
    """
    calculates number of active users in rolling window from dataframe (userId,activity times)
    """
    
    tmax = df['days'].max()
    res = []
    for t in range(tmax-window):
        
        subset = df[(df['days']>=t)&(df['days']<t+window)]['UserId'].unique()
        
        res.append((t+window, len(subset)))
        
    return res

def last_time_active_users(df, window): 
    
    """
    calculates number of users who become inactive in rolling window from dataframe (userId and activity times, last time)
    """
    
    tmax = 180
    res = []
    for t in range(tmax-window):
        subset1 = df[(df['days']>=t)&(df['days']<t+window)]
        subset = df[(df['last_time']>=t)&(df['last_time']<t+window)]['UserId'].unique()

        res.append((t+window, len(subset)))#/len(subset1['UserId'].unique())))
        
    return res

def first_time_active_users(df, window): 
    
    """
    calculates number of users who become inactive in rolling window from dataframe (userId and activity times, last time)
    """
    
    tmax = 180
    res = []
    for t in range(tmax-window):
        subset1 = df[(df['days']>=t)&(df['days']<t+window)]
        subset = df[(df['first_time']>=t)&(df['first_time']<t+window)]['UserId'].unique()
        #if len(subset1)>0:

        res.append((t+window, len(subset)))#/len(subset1['UserId'].unique())))
        
    return res

def users_who_stay_active(df, window): 
    
    """
    calculates number of users who stay in rolling window from dataframe (userId and activity times, last time)
    """
    
    tmax = 180
    res = []
    for t in range( tmax-window):
        subset1 = df[(df['days']>=t)&(df['days']<t+window)]
        subset = subset1[(subset1['last_time']>t+window)]['UserId'].unique()
        #print(t+window)
        #print(subset)
        #if len(subset1)>0:
        res.append((t+window, len(subset)))#/len(subset1['UserId'].unique())))
        
    return res

def users_who_were_active(df, window): 
    
    """
    calculates number of users who stay in rolling window from dataframe (userId and activity times, last time)
    """
    
    tmax = 180
    res = []
    for t in range(tmax-window):
        subset1 = df[(df['days']>=t)&(df['days']<t+window)]
        subset = subset1[(subset1['first_time']<t)]['UserId'].unique()
        #if len(subset1)>0:
        res.append((t+window, len(subset)))#/len(subset1['UserId'].unique())))
        
    return res

def users_who_were_stay_active(df, window):
    tmax = 180
    res = []
    for t in range( tmax-window):
        subset1 = df[(df['days']>=t)&(df['days']<t+window)]

        stay = list(subset1[(subset1['last_time']>t+window)]['UserId'].unique())
        were = list(subset1[(subset1['first_time']<t)]['UserId'].unique())
        #print(len(stay), len(were))
        #print(len(stay+were))
        s = set(stay+were)

        #print(t+window)
        #print(subset)
        #if len(subset1)>0:
        res.append((t+window, len(s)))#/len(subset1['UserId'].unique())))
        
    return res

