import pandas as pd
import networkx as nx
import csv
import numpy as np
import h5py
from multiprocessing import Pool, cpu_count
import sys
import os
from core_periphery_sbm import core_periphery as cp
from core_periphery_sbm import network_helper as nh
from core_periphery_sbm import model_fit as mf


def merge_interactions(interactions, acc, comm, ltlim, htlim, tip='qa'):
    """
    Merges different interactions dataframes, depending on the type of interactions. 
    interactions(Dataframe): Dataframe with questions-answers interactions
    acc(Dataframe): Dataframe with accepted answers interactions
    comm(Dataframe): Dataframe with comments interactions
    ltlim (int): Lower time limit in days
    htlim (int): Upper time limit in days
    tip(str):  'qa': only interactions+acc are used
    		'comm': only comments are used
    		'qa+comm': all interactions are used
    		
    Returns:
    	(Dataframe): Dataframe with three columns: ('PostUserId', 'RespondUserId', question id, day of interaction)
    """
    
    if tip=='qa':
        
        i1 = interactions[(interactions['days']<htlim)&(interactions['days']>=ltlim)]
        a1 = acc[(acc['days']<htlim)&(acc['days']>=ltlim)]
        
        it = pd.concat([ i1[['PostUserId', 'RespondUserId', 'QId', 'days']], a1[['PostUserId', 'RespondUserId', 'QId', 'days']],])
        it = it[it['PostUserId']!=it['RespondUserId']]
        
        return it.dropna()
    else:
        if tip=='comments':
            
            c = comm[(comm['days']<htlim)&(comm['days']>=ltlim)]
            it = pd.concat([ c[['PostUserId', 'RespondUserId', 'QId', 'days']],])
            #it = it[it['PostUserId']!=it['RespondUserId']]
            
            return it.dropna()
        else:
            if tip=='qa_comm':
                
                i1 = interactions[(interactions['days']<htlim)&(interactions['days']>=ltlim)]
                a1 = acc[(acc['days']<htlim)&(acc['days']>=ltlim)]
                c = comm[(comm['days']<htlim)&(comm['days']>=ltlim)]
                
                it = pd.concat([ i1[['PostUserId', 'RespondUserId', 'QId', 'days']], a1[['PostUserId', 'RespondUserId', 'QId', 'days']], c[['PostUserId', 'RespondUserId', 'QId', 'days']],])
                it = it[it['PostUserId']!=it['RespondUserId']]
                return it.dropna()
            else:
                
                print('ERROR')
                return 'None'
            
def filter_edges(df):
    """
    creates edge list from dataframe 
    Args:
    	df(Dataframe): First two columns are PostUserId and RespondUserId
    Returns:
    	edges(list of tuples): edge list
    """
    
    df = df.reset_index()
    edges = [ ((df.loc[i][1]), (df.loc[i][2])) for i in range(0, len(df))]
    return edges



def write_results( results, fname, window):

    """
    writes core-periphery results into hdf5 format
    Input: 
    	results: list of results for all subnetworks
    	fname(string): filename
    	window(int): lenght of sliding window
    	
    """
    with h5py.File(fname, 'a') as W:
        for r in range(len(results)):
            #print (r)
            ltlim =  r
            htlim = window + r
            if 'ns_%s-%sdays'%(ltlim, htlim) in W.keys():
                print(ltlim, htlim, 'calculated')
            else:
            	#print(ltlim, htlim)
            	W['labels_%s-%sdays'%(ltlim, htlim)] = np.array(list(results[r][0].items()))
            	W['ns_%s-%sdays'%(ltlim, htlim)] = np.array(results[r][1]) #number of nodes
            	W['ms_%s-%sdays'%(ltlim, htlim)] = np.array(results[r][2]) #number of edges between blocks
                W['ms_%s-%sdays'%(ltlim, htlim)] = np.array(results[r][3]) #Maximum number of edges between blocks
                W['mdl_%s-%sdays'%(ltlim, htlim)] = np.array(results[r][4]) #MDL
            	#W['Ms'] = np.array(results[i][3])               
    




