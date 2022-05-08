# -*- coding: utf-8 -*-
"""Dynamical Reputation Module

This module holds functions for calculating dynamical reputation
based on Stack Exchange interactions data.

Two types of dynamical reputation are included: popularity and engagement.
The type of reputation is specified as argument to ``merge_interactions`` function.

Two methods for calculating dynamical reputation are provided: linear and parallel.

Examples:

    Calculate popularity reputation using linear method::

        import time
        import dynamical_reputation as dr

        def prepare_data(net, name, ltlim, htlim, reputation):
            qa = pd.read_csv('interactions/%s/%s/%s_interactions_questions_answers.csv'%(net,name,name))
            comm = pd.read_csv('interactions/%s/%s/%s_interactions_comments.csv'%(net,name,name))
            acc = pd.read_csv('interactions/%s/%s/%s_interactions_acc_answers.csv'%(net,name,name))
            q = pd.read_csv('interactions/%s/%s/%s_interactions_post_questions.csv'%(net,name,name))
            data = dr.merge_interactions (qa, comm, acc, q,  ltlim, htlim, reputation)
            return data
        data = prepare_data('area51', '052012astronomy', 0, 180, 'pop')
        dr_a51_pop = dr.calculate_dynamical_reputation(data, beta=0.999, Ib=1, alpha=2, decay_per_day="True")

        data = prepare_data('area51', '052012astronomy', 0, 180, 'eng')
        dr_a51_eng = dr.calculate_dynamical_reputation(data, beta=0.999, Ib=1, alpha=2, decay_per_day = "True")

    Calculate popularity reputation using parallel method::
        import time
        import dynamical_reputation as dr

        def prepare_data(net, name, ltlim, htlim, reputation):
            qa = pd.read_csv('../Data/interactions/%s/%s/%s_interactions_questions_answers.csv'%(net,name,name))
            comm = pd.read_csv('../Data/interactions/%s/%s/%s_interactions_comments.csv'%(net,name,name))
            acc = pd.read_csv('../Data/interactions/%s/%s/%s_interactions_acc_answers.csv'%(net,name,name))
            q = pd.read_csv('../Data/interactions/%s/%s/%s_interactions_post_questions.csv'%(net,name,name))
            data = dr.merge_interactions (qa, comm, acc, q,  ltlim, htlim, reputation)
            return data

        data = prepare_data('launched', 'astronomy', 0, 1000, 'pop')
        astr_pop = dr.calculate_dynamical_reputation_paralel(data, beta=0.999, Ib=1, alpha=2, decay_per_day = "True")

"""

from functools import partial
from datetime import timedelta
from multiprocessing import Pool, cpu_count
import pandas as pd
import numpy as np

def calculate_dynamical_reputation(interactions, beta=0.999, Ib=1., alpha=2, decay_per_day = "True"):
    """Calculate time series of dynamical reputation for each user given a set of interactions.
    This is a linear method and does not use parallel computing.

    Args:
        interactions (DataFrame): Pandas dataframe of merged interactions.
        The type of merged interactions determines the type of reputation (popularity or engagement)
        beta (float, optional): Reputation decay parameter. Defaults to 0.999.
        Ib (float, optional): Basic reputational value of a single interaction. Defaults to 1.
        alpha (float, optional): Cumulation parameter. Defaults to 2.
        decay_per_day (str, optional): Perform decay in each day of inactivity? Defaults to "True".

    Returns:
        (DataFrame): DF with values of reputation for each user (row) each day (column)
    """

    TReputation = {} 
    users = interactions['UserId'].unique()
    day_max = max(interactions['days'])
    d_min = min(interactions['Time'])
    for u in users:
        dates = interactions[interactions['UserId']==u][['Time', 'days']]
        Ru = calculate_user_reputation(dates, d_min, day_max, beta=beta, Ib=Ib, alpha=alpha, decay_per_day = decay_per_day )
        TReputation[int(u)] = Ru
    df = pd.DataFrame(TReputation).T    
    return df

def calculate_dynamical_reputation_paralel(interactions, beta = 0.999, Ib=1., alpha = 2, decay_per_day = 'True'):
    """Calculate time series of dynamical reputation for each user given a set of interactions.
    This is a linear method and does not use parallel computing.

    Args:
        interactions (Pandas DataFrame): Pandas dataframe of merged interactions.
        The type of merged interactions determines the type of reputation (popularity or engagement)
        beta (float, optional): Reputation decay parameter. Defaults to 0.999.
        Ib (float, optional): Basic reputational value of a single interaction. Defaults to 1.
        alpha (float, optional): Cumulation parameter. Defaults to 2.
        decay_per_day (str, optional): Perform decay in each day of inactivity? Defaults to "True".

    Returns:
        (DataFrame): DF with values of reputation for each user (row) each day (column)
    """
    TReputation = {}
    users = interactions['UserId'].unique()
    day_max = max(interactions['days'])
    d_min = min(interactions['Time'])
    data = [(u, interactions[interactions['UserId']==u][['Time', 'days']]) for u in users ]
    pool = Pool(cpu_count())
    func = partial(mpi_run, d_min, day_max, beta, Ib, alpha, decay_per_day)
    results = pool.map(func, data)
    for u, rep in results:
        TReputation[int(u)]=rep
    df = pd.DataFrame(TReputation).T
    del data
    return df

def mpi_run(d_min, day_max, beta, Ib, alpha, decay_per_day, data ):
    """Multiprocessing instance run of ``calculate_user_reputation`` function.

    Args:
        d_min (datetime): Date-time stamp of the first interaction: 'YYYY-MM-DDTHH:MM:SS.SSS'
        day_max (int): Upper limit for days after first interaction which are counted.
        beta (float): Reputation decay parameter.
        Ib (float): Basic reputational value of a single interaction. 
        alpha (float): Cumulation parameter.
        decay_per_day (str): Perform decay in each day of inactivity? 'True' or 'False'
        data (Pandas DataFrame / dictionary ???): Sorted interactions for a single user

    Returns:
        (tuple): A tuple of user ID and dictionary of user's reputation 
    """
    u, dates = data[0], data[1]
    Ru = calculate_user_reputation(dates, d_min, day_max, beta=beta, Ib=Ib, alpha=alpha, decay_per_day = decay_per_day )
    return u, Ru

def calculate_user_reputation(dates, d_min, day_max, beta=0.999, Ib=1, alpha=2, decay_per_day = "True" ): 
    """Returns a dictionary of user's reputational values for each day

    Args:
        dates (DataFrame): Pandas DataFrame with timestamp and day columns.
        Each row is a single interaction by the same user.
        d_min (datetime): Date-time stamp of the first interaction: 'YYYY-MM-DDTHH:MM:SS.SSS'
        day_max (int): Upper limit for days after first interaction which are counted.
        beta (float, optional): Reputation decay parameter. Defaults to 0.999.
        Ib (float, optional): Basic reputational value of a single interaction. Defaults to 1.
        alpha (float, optional): Cumulation parameter. Defaults to 2.
        decay_per_day (str, optional): Perform decay in each day of inactivity? Defaults to "True".

    Returns:
        (dict): A dictionary of user's reputational values for each day
    """
    dates = dates.sort_values(by='Time')
    Ru = {}
    first_day = dates.iloc[0].days
    first_date = dates.iloc[0].Time
    if first_day > 0:
        for day in range(first_day):
            Ru[day] = 0.
    A = 1
    Ru[first_day] = Ib + Ib*alpha*(1.-1./(A+1))
    last_day = first_day
    last_activity_date = first_date
    last_activity_day = first_day
    for i in range(1,len(dates)):
        curr_day = dates.iloc[i].days
        curr_activity_date = dates.iloc[i].Time
        if curr_day > (last_day+1):
            for i in range(curr_day-last_day - 1):
                inactive_date = pd.to_datetime(d_min) + timedelta(days=int(last_day)+2)
                update_reputation_inactive(Ru, inactive_date, last_activity_date, last_activity_day,  last_day, beta=beta, decay_per_day = decay_per_day)
                last_day = last_day + 1
                A = 0
        A+=1
        update_reputation(Ru, A, curr_activity_date, last_activity_date, last_day, last_activity_day, curr_day, beta=beta,  Ib=Ib, alpha=alpha, decay_per_day=decay_per_day)
        last_activity_date = curr_activity_date
        last_activity_day = curr_day
        last_day = curr_day
    rest_days = day_max - last_day
    for i in range(rest_days):
        inactive_date = pd.to_datetime(d_min) + timedelta(days=int(last_day)+2)
        update_reputation_inactive(Ru, inactive_date, last_activity_date, last_activity_day,  last_day, beta=beta, decay_per_day = decay_per_day)
        last_day = last_day + 1
    return Ru

def update_reputation_inactive(R, inactive_date, last_activity_date, last_activity_day, last_day, beta=0.999, decay_per_day = 'True'):
    """Performs the decay of user's reputation during a period of inactivity.

    Args:
        R (dict): Dictionary of user's reputation which will be updated.
        inactive_date (datetime): Date-time stamp designating when the period of inactivity ends
        last_activity_date (datetime): Date-time stamp designating when the last recorded activity of user
        last_activity_day (int): Day in which last activity was recorded
        last_day (int): Last day for which reputation was previously updated
        beta (float, optional): Reputation decay parameter. Defaults to 0.999.
        decay_per_day (str, optional): Perform decay in each day of inactivity? Defaults to "True".
    """
    dt = ( pd.to_datetime(inactive_date) - pd.to_datetime(last_activity_date))/np.timedelta64(1,'D')
    if decay_per_day=='True':
        D = R[last_day]*np.power(beta, dt)
    else:
        D = R[last_activity_day]*np.power(beta, dt)  
    R[last_day+1] = D

def update_reputation(R, A, curr_date, last_activity_date, last_day, last_activity_day, curr_day, beta=0.999,  Ib=1, alpha=2, decay_per_day='True'):
    """Performs the decay of user's reputation during a period of inactivity.

    Args:
        R (dict): Dictionary of user's reputation which will be updated.
        A (int): Count of consecutive interactions within time-window frame
        curr_date (datetime): Date-time stamp of current activity when update function was called
        last_activity_date (datetime): Date-time stamp designating previous activity of the user
        last_activity_day (int): Day in which last activity was recorded
        last_day (int): Last day for which reputation was previously updated
        beta (float, optional): Reputation decay parameter. Defaults to 0.999.
        decay_per_day (str, optional): Perform decay in each day of inactivity? Defaults to "True".
    """
    dt = ( pd.to_datetime(curr_date) - pd.to_datetime(last_activity_date))/np.timedelta64(1,'D')
    In = Ib + Ib*alpha*(1.-1./(A+1))
    if (decay_per_day=='False') and (A==1):
        D = R[last_activity_day]*np.power(beta, dt)
    else:
        D = R[last_day]*np.power(beta, dt)
    y = R.get(curr_day, 0.)
    y = In+D
    R[curr_day] = y


def merge_interactions (qa, comm, acc, q,  ltlim, htlim, reputation):
    """Merged different interaction dataframes into one.
    Merges different interactions depending on type of reputation that needs to be calculated afterwards.

    Args:
        qa (DataFrame): Dataframe with posts (questions and answers)
        comm (DataFrame)): Dataframe with comments
        acc (DataFrame)): Dataframe with accepted answers
        q (DataFrame)): DataFrame with questions only
        ltlim (int): Lower time limit in days. 
        htlim (int): Upper time limit in days.
        reputation (str): "pop" for popularity reputation or "eng for engagement reputation"

    Returns:
        (DataFrame): Dataframe with three columns: user ID, time-stamp and day of interaction.
    """    
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
