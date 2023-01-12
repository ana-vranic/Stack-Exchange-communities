from src import drawing_functions as df
import matplotlib.pyplot as plt


def plot_8_variables_2row(data_questions, data_nets, data_coreper, data_rep_agg, community, colors, legendtxt=["active", "closed"]):

    plt.figure(figsize = (16,6))
    plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
    i=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_questions, community, 'Number_of_active_questions',colors, 'Weekly active \n questions' )
    plt.legend(legendtxt)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_nets, community, 'Clustering_coef',colors, 'Mean clustering \n coefficient')
    plt.legend(legendtxt)
    plt.legend().set_visible(False)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, community, 'LN_core',colors, 'L/N within core')
    plt.legend(legendtxt)
    plt.legend().set_visible(False)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, community, 'LN_core_periphery',colors, 'L/N core to periphery')
    plt.legend(legendtxt)
    plt.legend().set_visible(False)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_rep_agg, community, "Number of active users", colors, "N active users")
    plt.legend(legendtxt)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_rep_agg, community, "Mean user reputation", colors, "Mean reputation")
    plt.legend(legendtxt)
    plt.legend().set_visible(False)
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, community, 'N_core',colors, 'N users in core')
    plt.legend(legendtxt)
    plt.legend().set_visible(False)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, community, 'Mean_dr_core',colors, 'Mean reputation \n within core')
    plt.legend(legendtxt)
    plt.legend().set_visible(False)
    i+=1
    
    
def comparestartups_2rows(data_rep_agg, data_coreper, comm1, commr1, commr2, colors, legendtext1=["active", "closed", "st1"], legendtext2=["active", "closed", "st2"], ylim=None):
    plt.figure(figsize = (18,6))
    plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
    i=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_rep_agg, comm1, "Number of active users", colors, "N active users")
    plt.plot(data_rep_agg[commr1]["Number of active users"], ".-", color=colors[commr1], label="startups")
    plt.legend(legendtext1)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_rep_agg, comm1, "Mean user reputation", colors, "Mean reputation")
    plt.plot(data_rep_agg[commr1]["Mean user reputation"], ".-", color=colors[commr1], label="startups")
    plt.legend().set_visible(False)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, comm1, 'N_core',colors, 'N users in core')
    plt.plot(data_coreper[commr1]["N_core"], ".-", color=colors[commr1], label="startups")
    plt.legend().set_visible(False)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1


    plt.subplot(2, 4, i)
    df.single_panel_plot(data_coreper, comm1, 'Mean_dr_core',colors, 'Mean reputation \n within core')
    plt.plot(data_coreper[commr1]["Mean_dr_core"], ".-", color=colors[commr1], label="startups")
    plt.legend().set_visible(False)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_rep_agg, comm1, "Number of active users", colors, "N active users")
    plt.plot(data_rep_agg[commr2]["Number of active users"], ".-", color=colors[commr2], label="startups")
    plt.legend(legendtext2)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_rep_agg, comm1, "Mean user reputation", colors, "Mean reputation")
    plt.plot(data_rep_agg[commr2]["Mean user reputation"], ".-", color=colors[commr2], label="startups")
    plt.legend().set_visible(False)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, "physics", 'N_core',colors, 'N users in core')
    plt.plot(data_coreper[commr2]["N_core"], ".-", color=colors[commr2], label="startups")
    plt.legend().set_visible(False)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1


    plt.subplot(2, 4, i)
    df.single_panel_plot(data_coreper, "physics", 'Mean_dr_core',colors, 'Mean reputation \n within core')
    plt.plot(data_coreper[commr2]["Mean_dr_core"], ".-", color=colors[commr2], label="startups")
    plt.legend().set_visible(False)
    if ylim==None:
        plt.ylim(ymin=0)
    else:
        plt.ylim(ymin=0, ymax=ylim[i-1])
    i+=1

    
def comparestartups_net_2rows(data_questions, data_nets, data_coreper, comm1, commr1, commr2, colors, legendtext1=["active", "closed", "st1"], legendtext2=["active", "closed", "st2"] ):
    plt.figure(figsize = (18,6))
    plt.subplots_adjust(left=0.1,bottom=0.1,right=0.9,top=0.9,wspace=0.4,hspace=0.4)
    i=1
    
    
    plt.subplot(2,4,i)
    df.single_panel_plot(data_questions, comm1, 'Number_of_active_questions',colors, 'Weekly active \n questions' )
    plt.plot(data_questions[commr1]["Number_of_active_questions"], ".-", color=colors["startups"], label="startups")
    plt.legend(legendtext1)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_nets, comm1, 'Clustering_coef',colors, 'Mean clustering \n coefficient')
    plt.plot(data_nets[commr1]["Clustering_coef"], ".-", color=colors["startups"], label="startups")
    plt.legend().set_visible(False)
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, comm1, 'LN_core',colors, 'L/N within core')
    plt.plot(data_coreper[commr1]["LN_core"], ".-", color=colors["startups"], label="startups")
    plt.legend().set_visible(False)
    i+=1


    plt.subplot(2, 4, i)
    df.single_panel_plot(data_coreper, comm1, 'LN_core_periphery',colors, 'L/N core to periphery')
    plt.plot(data_coreper[commr1]["LN_core_periphery"], ".-", color=colors["startups"], label="startups")
    plt.legend().set_visible(False)
    i+=1
    
    plt.subplot(2,4,i)
    df.single_panel_plot(data_questions, comm1, 'Number_of_active_questions',colors, 'Weekly active \n questions' )
    plt.plot(data_questions[commr2]["Number_of_active_questions"], ".-", color=colors["startups"], label="startups")
    plt.legend(legendtext2)
    i+=1

    plt.subplot(2,4,i)
    df.single_panel_plot(data_nets, comm1, 'Clustering_coef',colors, 'Mean clustering \n coefficient')
    plt.plot(data_nets[commr2]["Clustering_coef"], ".-", color=colors["startups"], label="startups")
    plt.legend().set_visible(False)
    i+=1


    plt.subplot(2,4,i)
    df.single_panel_plot(data_coreper, comm1, 'LN_core',colors, 'L/N within core')
    plt.plot(data_coreper[commr2]["LN_core"], ".-", color=colors["startups"], label="startups")
    plt.legend().set_visible(False)
    i+=1


    plt.subplot(2, 4, i)
    df.single_panel_plot(data_coreper, comm1, 'LN_core_periphery',colors, 'L/N core to periphery')
    plt.plot(data_coreper[commr2]["LN_core_periphery"], ".-", color=colors["startups"], label="startups")
    plt.legend().set_visible(False)
    i+=1
