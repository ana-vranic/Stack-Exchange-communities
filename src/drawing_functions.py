# libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# single panel plot
def single_panel_plot(data, community_name, y_column_name, color_dict, y_label, x_label = 'Time [days]', x_column_name=None, lines_s=None, marker_s=None, marker_fill = None, markers_on=None, xticks_size=None):
    '''
    '''
    comms = [key for key in data.keys() if community_name in key]
    
    for comm in comms:
        if comm[0].isdigit():
            if lines_s==None:
                ls = '--'
                status = 'closed'
            else:
                ls=lines_s[comm]
        else:
            if lines_s==None:
                ls = '-'
            else:
                ls=lines_s[comm]
            if comm == 'physics':
                status = 'active'
            else:
                status = 'active'
        
        if marker_s == None:
            ms=" "
            markers_on = np.arange(0, 150, 30)
        else:
            ms=marker_s
            markers_on = markers_on
            
        if marker_fill==None:
            mf=None
        else:
            mf=marker_fill[comm]
        
            
        if x_column_name==None:
            plt.plot(data[comm][y_column_name], ls=ls, lw = 2, label = status, color = color_dict[community_name])
        else:
            plt.plot(data[comm][x_column_name], data[comm][y_column_name], ls=ls, lw = 2, label = status, marker=ms, markevery=markers_on, markersize=10, fillstyle=mf, color = color_dict[community_name])
    plt.legend(fontsize=12)
    if xticks_size==None:
        plt.xticks(fontsize=12)
    else:
        plt.xticks(fontsize=xticks_size)
    plt.yticks(fontsize=12)
    plt.ylabel(y_label,fontsize=14)
    plt.xlabel(x_label,fontsize=14)

    
    
# single variable plot
# 2 x 2

def single_variable_plot_square(data, column_name, color_dict, y_label, x_label = 'Time [days]',):
    plt.figure(figsize = (10,8))
    
    plt.subplot(2,2,1)
    single_panel_plot(data,'physics',column_name,color_dict, y_label, x_label='')
    #plt.legend(['Beta','Area 51'],fontsize=12)
    plt.title('Physics',fontsize=18)
    plt.ylabel(y_label,fontsize=16)

    #plt.ylim(0)
    
    plt.subplot(2,2,2)
    single_panel_plot(data,'economics',column_name,color_dict, '', '')
    plt.legend().set_visible(False)
    plt.title('Economics',fontsize=18)
    #plt.ylim(0)
    
    plt.subplot(2,2,3)
    single_panel_plot(data,'astronomy',column_name,color_dict, y_label, x_label)
    plt.legend().set_visible(False)
    plt.title('Astronomy',fontsize=18)
    plt.ylabel(y_label,fontsize=16)
    plt.xlabel(x_label,fontsize=16)
    #plt.ylim(0)
    
    plt.subplot(2,2,4)
    single_panel_plot(data,'literature',column_name,color_dict, '', x_label)
    plt.legend().set_visible(False)
    plt.title('Literature',fontsize=18)
    plt.xlabel(x_label,fontsize=16)
    #plt.ylim(0)
    
    
# single variable plot
# 4 x 1

def single_variable_plot_column(data, column_name, color_dict,y_label,x_label='Time [days]'):
    plt.figure(figsize = (5,10))
    #plt.figure(figsize=(4,7))
    
    plt.subplot(4,1,1)
    single_panel_plot(data,'physics',column_name,color_dict, 'Physics', '')
    plt.title(y_label,fontsize=14)
    plt.ylim(0)
    #plt.legend(['Beta','Area 51'],fontsize=12,loc='lower left')
    
    plt.subplot(4,1,2)
    single_panel_plot(data,'economics',column_name,color_dict, 'Economics', '')
    plt.legend().set_visible(False)
    plt.ylim(0)
    
    plt.subplot(4,1,3)
    single_panel_plot(data,'astronomy',column_name,color_dict, 'Astronomy', '')
    plt.legend().set_visible(False)
    plt.ylim(0)
        
    plt.subplot(4,1,4)
    single_panel_plot(data,'literature',column_name,color_dict, 'Literature', x_label)
    plt.ylim(0)
    plt.legend().set_visible(False)
    
    
# single variable plot
# 1 x 4

def single_variable_plot_row(data, column_name, color_dict,y_label,x_label='Time [days]', x_column_name=None, xticks_size=None):
    plt.figure(figsize = (18,4))
    
    plt.subplot(1,4,1)
    single_panel_plot(data,'physics',column_name,color_dict, y_label, x_label=x_label, x_column_name=x_column_name, xticks_size=xticks_size)
    #plt.legend().set_visible(False)
    plt.title('Physics',fontsize=16)
    
    plt.subplot(1,4,2)
    single_panel_plot(data,'economics',column_name,color_dict,'',x_label, x_column_name=x_column_name, xticks_size=xticks_size)
    plt.legend().set_visible(False)
    plt.title('Economics',fontsize=16)
    
    plt.subplot(1,4,3)
    single_panel_plot(data,'astronomy',column_name,color_dict,'',x_label, x_column_name=x_column_name, xticks_size=xticks_size)
    plt.legend().set_visible(False)
    plt.title('Astronomy',fontsize=16)
    
    plt.subplot(1,4,4)
    single_panel_plot(data,'literature',column_name,color_dict,'',x_label, x_column_name=x_column_name, xticks_size=xticks_size)
    plt.legend().set_visible(False)
    plt.title('Literature',fontsize=16)
    
    
# two variable plot
# 2 x 4

def two_vars_plot_rows(data, column_name1, column_name2, color_dict, y1_label, y2_label,x_label='Time [days]'):
    plt.figure(figsize = (15,6))
    
    plt.subplot(2,4,1)
    single_panel_plot(data,'physics',column_name1,color_dict,y1_label,'')
    plt.title('Physics',fontsize=14)
    #plt.legend(['Beta','Area 51'],fontsize=12,loc='upper left')

    
    plt.subplot(2,4,2)
    single_panel_plot(data,'economics',column_name1,color_dict,'','')
    plt.title('Economics',fontsize=14)
    plt.legend().set_visible(False)
    
    plt.subplot(2,4,3)
    single_panel_plot(data,'astronomy',column_name1,color_dict,'','')
    plt.title('Astronomy',fontsize=14)
    plt.legend().set_visible(False)
    
    plt.subplot(2,4,4)
    single_panel_plot(data,'literature',column_name1,color_dict,'','')
    plt.title('Literature',fontsize=14)
    plt.legend().set_visible(False)
    
    plt.subplot(2,4,5)
    single_panel_plot(data,'physics',column_name2,color_dict,y2_label)
    plt.legend().set_visible(False)
    
    plt.subplot(2,4,6)
    single_panel_plot(data,'economics',column_name2,color_dict,'',x_label)
    plt.legend().set_visible(False)
    
    plt.subplot(2,4,7)
    single_panel_plot(data,'astronomy',column_name2,color_dict,'',x_label)
    plt.legend().set_visible(False)
    
    plt.subplot(2,4,8)
    single_panel_plot(data,'literature',column_name2,color_dict,'',x_label)
    plt.legend().set_visible(False)
    
# two variable plot
# 4 x 2

def two_vars_plot_cols(data, column_name1, column_name2, color_dict, y1_label, y2_label,x_label='Time [days]'):
    plt.figure(figsize = (10,10))
    
    plt.subplot(4,2,1)
    single_panel_plot(data,'physics',column_name1,color_dict,'Physics','')
    plt.title(y1_label,fontsize=14)
    plt.legend().set_visible(False)
    
    plt.subplot(4,2,2)
    single_panel_plot(data,'physics',column_name2,color_dict,'','')
    plt.title(y2_label,fontsize=14)
    plt.legend().set_visible(False)
    
    plt.subplot(4,2,3)
    single_panel_plot(data,'economics',column_name1,color_dict,'Economics','')
    plt.legend().set_visible(False)
    
    plt.subplot(4,2,4)
    single_panel_plot(data,'economics',column_name2,color_dict,'','')
    plt.legend().set_visible(False)

    plt.subplot(4,2,5)    
    single_panel_plot(data,'astronomy',column_name1,color_dict,'Astronomy','')
    plt.legend().set_visible(False)
    

    plt.subplot(4,2,6)
    single_panel_plot(data,'astronomy',column_name2,color_dict,'','')
    plt.legend().set_visible(False)

    plt.subplot(4,2,7) 
    single_panel_plot(data,'literature',column_name1,color_dict,'Literature',x_label)
    plt.legend().set_visible(False)

    
    plt.subplot(4,2,8)
    single_panel_plot(data,'literature',column_name2,color_dict,'',x_label)
    plt.legend().set_visible(False)
    
    
    
def plot_jaccard(data, colors):
    
    def one_plot(df, colors_dict, x_label, y_label):
        g = sns.lineplot(data=df,  x="time-delta", y="jaccard", style="name", hue="name", ci='sd', palette=[colors_dict[comm1], colors_dict[comm1]] )
        
        g.legend(fontsize = 12,
               title="",)

        plt.xscale("log"); plt.yscale("log")
        #plt.legend(labels=["active", "closed"], fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylabel(y_label,fontsize=14)
        plt.xlabel(x_label,fontsize=14)


    plt.figure(figsize = (18,4))

    plt.subplot(1,4,1)
    comm1 = "physics"; comm2 = "052012-theoretical-physics"
    df1 = data[comm1]; df1["name"]="active"
    df2=data[comm2]; df2["name"]="closed"
    df = pd.concat([df1, df2]).reset_index()
    one_plot(df, colors, r'$|t_i - t_j|$', r'$J(core(t_i), core (t_j))$')
    plt.title("Physics", fontsize=16)

    
    
    plt.subplot(1,4,2)
    comm1 = "economics"; comm2 = "052012economics"
    df1 = data[comm1]; df2=data[comm2]; df = pd.concat([df1, df2]).reset_index()
    one_plot(df, colors, r'$|t_i - t_j|$', '')
    plt.title("Economics", fontsize=16)
    plt.legend().set_visible(False)



    plt.subplot(1,4,3)
    comm1 = "astronomy"; comm2 = "052012astronomy"
    df1 = data[comm1]; df2=data[comm2]; df = pd.concat([df1, df2]).reset_index()
    one_plot(df, colors, r'$|t_i - t_j|$', '')
    plt.title("Astronomy", fontsize=16)
    plt.legend().set_visible(False)



    plt.subplot(1,4,4)
    comm1 = "literature"; comm2 = "052012-literature"
    df1 = data[comm1]; df2=data[comm2]; df = pd.concat([df1, df2]).reset_index()
    one_plot(df, colors, r'$|t_i - t_j|$', '')
    plt.title("Literature", fontsize=16)
    plt.legend().set_visible(False)



def plot_jaccard_heatmap(data, palette):

    i = 1
    plt.figure(figsize = (15,6))
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.5)
    lab = {'052012astronomy':"closed Astronomy",  '052012economics':"closed Economics",  '052012-literature':"closed Literature",  '052012-theoretical-physics':"closed Physics",
                 'astronomy':"Astronomy", 'economics':"Economics", 'literature':"Literature",   'physics':"Physics",  }

    for community in [   'physics', 'economics', 'astronomy', 'literature', 
                      '052012-theoretical-physics',  '052012economics', 
                      '052012astronomy',  '052012-literature', 
                ]:
        
        plt.subplot(2, 4, i)
        
        df = data[community]
        df_p = df.pivot("t1", "t2", "J")

        cmap = sns.color_palette(palette, as_cmap=True)
        sns.heatmap(df_p, cmap=cmap)

        plt.title(lab[community], fontsize=16)
        if i==1 or i==5: 
            plt.ylabel("t1", fontsize=14)
        else:
            plt.ylabel(" ")
        if i>4: 
            plt.xlabel("t2", fontsize=14)
        else:
            plt.xlabel(" ")

        i +=1
            
def plot_ensemble_statistics(all_data, colors_dict):
    
    def plot_csv_data(all_data, prop, xlabel):

        data = all_data[prop]

        mean = np.array(data.mean())
        std = np.array(data.std())

        plt.plot(mean, color=colors_dict["052012astronomy"])
        x = np.arange(0, len(mean))
        plt.fill_between(x, mean - std, mean + std, color='gray', alpha=0.5)
        plt.tick_params(axis='both', which='major', labelsize=12)
        plt.xlabel(xlabel,fontsize=14)
    
    
    properties = ["mdl", "nodes_in_core", "nmi", "ari", "f1", "jacc"]
    lab = {"mdl":"MDL", "nodes_in_core": "Nodes in core", "nmi": "NMI", "ari": "ARI", "f1":"F1", "jacc":"Jaccard"}

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1, hspace=1)

    plt.figure(figsize = (12,8))
    i = 1
    for prop in properties:
        if i>3:
            xlabel="Time [days]"
        else:
            xlabel=" "
        plt.subplot(2, 3, i)
        plot_csv_data(all_data, prop, xlabel,)
        plt.title("closed Astronomy:"+" "+lab[prop], fontsize=14)

        i+=1
            
            
def plot_compare_tw(data, column_order, row_order, colors_dict, ylab_order):

    def plot_line(data,col, prop, x_label, y_label, colors_dict):
        communities = list(data[col].keys())
        for comm in communities:
            
            if comm[0].isdigit():
                ls = '--'
                status = 'closed'
            else:
                ls = '-'
                status = "active"
                
            color = colors_dict[comm]
    
            df = data[col][comm][prop]
            plt.plot(data[col][comm][prop], ls=ls, label=status, color=color, lw=2)
        plt.legend(fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylabel(y_label,fontsize=14)
        plt.xlabel(x_label,fontsize=14)
        
    plt.figure(figsize = (14,24))
    i=1
    
    for num  in range(len(row_order)):
        
        row = row_order[num]
        lab = ylab_order[num]
        
        
        k=0
        
        for col in column_order:
            
            plt.subplot(8, 3, i )
            if (i == 24) or (i==23) or (i==22):
                xlabel="Time [days]"
            else:
                xlabel = " " 
            if k==0:
                ylabel = lab
            else: ylabel=" " 
                
            plot_line(data, col, row,  xlabel, ylabel, colors_dict )
            if i!=1: plt.legend().set_visible(False)
            if (i == 1) or (i==2) or (i==3):
                plt.title("Astronomy: %s days window"%col, fontsize=16)
            
            
            i+=1
            k+=1
            
            
def plot_active_users_beta(data, colors_dict):
    
    lab = {'052012astronomy':"closed Astronomy",  '052012economics':"closed Economics",  '052012-literature':"closed Literature",  '052012-theoretical-physics':"closed Physics",
                     'astronomy':"Astronomy", 'economics':"Economics", 'literature':"Literature",   'physics':"Physics",  }

    plt.figure(figsize=(16, 8))
    i=1
    for community in [   'physics', 'economics', 'astronomy', 'literature', 
                          '052012-theoretical-physics',  '052012economics', 
                          '052012astronomy',  '052012-literature', 
                    ]:

        plt.subplot(2,4,i)

        color = colors_dict[community]

        bettas = list(data[community].keys())
        for b in bettas:
            if type(b) == str:
                ls = '-'
                plt.plot(data[community][b][0], data[community][b][1], ls = ls, lw=2, color="gray", label="30 days w")

            else:
                if b==0.96:
                    ls= '-'
                else:
                    ls= '--'
                plt.plot(data[community][b], ls=ls, lw=2, color=color, label=r"$\beta=%s$"%b)

        plt.title(lab[community], fontsize=16)
        plt.legend(fontsize=12)
        plt.xticks(range(0,180,50), fontsize=12)
        plt.yticks(fontsize=12)
        if i>4: plt.xlabel("Time [days]", fontsize=14)
        if i==1 or i==5: plt.ylabel("Active users", fontsize=14)

        i+=1
        
        
def two_variable_plot_one_row(data, column_name, column_name2, color_dict, y_label, x_label='Time [days]', x_column_name=None):
    plt.figure(figsize = (18,4))
    
    lines_s = {'052012astronomy':":",  '052012economics':":",  '052012-literature':":",  '052012-theoretical-physics':":",
                 'astronomy':"-", 'economics':"-", 'literature':"-",   'physics':"-",  }
    
    markerfills = {'052012astronomy':"none",  '052012economics':"none",  '052012-literature':"none",  '052012-theoretical-physics':"none",
                 'astronomy':"full", 'economics':"full", 'literature':"full",   'physics':"full",  }
    ms1 = "o"
    ms2 = "v"
    markers_on1 = np.arange(0, 150, 30)
    markers_on2 = np.arange(15, 150, 30)
    
    plt.subplot(1,4,1)
    single_panel_plot(data,'physics',column_name, color_dict, y_label, x_label=x_label, x_column_name=x_column_name, marker_s = ms1,
                      markers_on=markers_on1, marker_fill=markerfills, lines_s=lines_s)
    single_panel_plot(data,'physics',column_name2, color_dict, y_label, x_label=x_label, x_column_name=x_column_name, marker_s= ms2,
                      markers_on=markers_on2, marker_fill=markerfills, lines_s=lines_s)
    plt.legend([ "active - reputation users", "closed - reputation users", "active - permanent users", "closed - permanent users",])
    #plt.legend().set_visible(False)
    #plt.legend().set_visible(False)
    plt.title('Physics',fontsize=16)
    
    plt.subplot(1,4,2)
    single_panel_plot(data,'economics',column_name, color_dict,'',x_label, x_column_name=x_column_name, marker_s = ms1,
                      markers_on=markers_on1, marker_fill=markerfills, lines_s=lines_s)
    single_panel_plot(data,'economics',column_name2, color_dict,'',x_label, x_column_name=x_column_name, marker_s = ms2,
                      markers_on=markers_on2, marker_fill=markerfills, lines_s=lines_s)
    plt.legend().set_visible(False)
    plt.title('Economics',fontsize=16)
    
    plt.subplot(1,4,3)
    single_panel_plot(data,'astronomy',column_name,color_dict,'',x_label, x_column_name=x_column_name, marker_s = ms1,
                      markers_on=markers_on1,marker_fill=markerfills, lines_s=lines_s)
    single_panel_plot(data,'astronomy',column_name2,color_dict,'',x_label, x_column_name=x_column_name, marker_s = ms2,
                      markers_on=markers_on2,marker_fill=markerfills, lines_s=lines_s)
    plt.legend().set_visible(False)
    plt.title('Astronomy',fontsize=16)
    
    plt.subplot(1,4,4)
    single_panel_plot(data,'literature',column_name,color_dict,'',x_label, x_column_name=x_column_name, marker_s = ms1,
                      markers_on=markers_on1, marker_fill=markerfills, lines_s=lines_s)
    single_panel_plot(data,'literature',column_name2,color_dict,'',x_label, x_column_name=x_column_name, marker_s = ms2,
                      markers_on=markers_on2, marker_fill=markerfills, lines_s=lines_s)
    plt.legend().set_visible(False)
    plt.title('Literature',fontsize=16)


def plot_reputation_decay():

    colors_list =  ['#c73b0b', '#d35f21','#de7d3a', '#e99a55', '#f4b573', '#ffd094']
    lines_list = ['-', '--', ':', '-.', '-', '--']
    fs = 14

    beta = lambda x: (In0/In)**(1/x)
    i=0
    for In in [5, 10, 50, 100, 500, 1000]:
        In0 = 1
        delta = np.linspace(10, 500,50)
        b = beta(delta)
        plt.plot(delta, b, lw=2, ls=lines_list[i], color = colors_list[i], label = 'In = %d'%In)
        
        i+=1

    plt.legend(fontsize=fs)
    plt.xlabel('Time [days]', fontsize=fs)
    plt.ylabel(r'$\beta$', fontsize=fs)
    plt.ylim(0.9,1)
    plt.xlim(0, 400)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(visible=True, which='both', color='lightgrey', linestyle='--')

def plot_interactions(t):
    for i in t:
        plt.axvline(x=i, color='gainsboro')
    
    plt.axhline(y=1, color='black')
    
def plot_single_user_reputation(data_dict, xlabel="Time [days]", ylabel="User reputation"):

    lines_list = ['--', ':', '-', '-.',   ]
    colors_list =  ['#c73b0b', '#e99a55', '#d35f21','#de7d3a','#f4b573', '#ffd094', '#c73b0b','#d35f21','#de7d3a','#e99a55','#f4b573', '#ffd094']
    fs = 14

    keys = data_dict.keys()
    plot_interactions(data_dict["ts"])
    i=0
    for key in keys:
        if key!="ts":
            urep = data_dict[key]
            b = key[0]; a = key[1]
            x, y = zip(*urep)
            plt.plot(x, y, label = r"$\beta$=%s""\n"r"$\alpha$=%s"%(b,a), ls=lines_list[i], color=colors_list[i], lw=2)
            i+=1

    plt.legend(fontsize=fs)
    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlim(xmax=180)

    plt.legend(ncol=4, bbox_to_anchor=(1.1, 1.2))
