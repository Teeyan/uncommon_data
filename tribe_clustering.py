import pandas as pd
import sklearn
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
import math
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='Teeyan', api_key='9gnWe4vFPKT5iGTc05ob')


def tribe_cluster(file):
    # Get the data file name and the number of tribes
    tribe_names = ["Ugandan", "Sanic", "Classical", "NANI?!?"]
    tribe_colors = ["rgb(255, 0, 0)", "rgb(30,144,255)", "rgb(0,0,0)", "rgb(148,0,211)"]
    img_link = ["https://imgur.com/VZAOqE0.png", "https://imgur.com/2LkeG4V.png", "https://imgur.com/WSZwQ4O.png",
                "https://imgur.com/Bd8Iafa.png"]
    
    # Read in the data set to a clean frame
    data = pd.read_csv(file, sep=",")
    
    # Clean the dataset with respect to categorical vs continuous variables
    drop_columns = []
    for i in range(0, len(data.columns)):
        if not np.issubdtype(data.iloc[:,i], np.number):
            drop_columns.append(i)
    
    data.drop(data.columns[drop_columns], axis=1, inplace=True)
    
    # Standardize the data
    unit_data = data.copy()
    for i in range(0, len(unit_data.columns)):
        unit_data.iloc[:,i] = unit_data.iloc[:,i] - unit_data.iloc[:,i].mean()
        unit_data.iloc[:,i] = unit_data.iloc[:,i] / unit_data.iloc[:,i].std()
    
    # Perform PCA on the data to get 3 principle components
    data_pca = PCA(n_components=3)
    proj_data = data_pca.fit_transform(unit_data)
    
    # Calculate appropriate amount of tribes (clusters) using the avg silhouette method
    clust_vals = np.arange(2, 11)
    avg_sil_score = []
    for cv in clust_vals:
        cv_cluster = KMeans(n_clusters = cv)
        cluster_labels = cv_cluster.fit_predict(proj_data)
        avg_sil_score.append(silhouette_score(proj_data, cluster_labels))
    
    n_clusters = avg_sil_score.index(max(avg_sil_score))
    
    # Perform actual tribe partitioning -> list of tribes by index of data point
    cluster_data_fit = KMeans(n_clusters=n_clusters+2)
    cluster_labels = cluster_data_fit.fit_predict(proj_data)
    
    tribes = []
    for i in range(n_clusters+2):
        tribes.append([])
        
    for i in range(len(cluster_labels)):
        tribes[cluster_labels[i]].append(i)
    
    # Get metadata about the tribes
    meta_tribe = []
    tribe_num = 0
    for indices in tribes:
        tribe_data = data.iloc[indices,]
        tribe_mean = []
        tribe_var = []
        for i in range(0, len(tribe_data.columns)):
            tribe_mean.append(round(tribe_data.iloc[:, i].mean(), 2))
            tribe_var.append(round(math.pow(tribe_data.iloc[:, i].std(), 2), 2))
        meta_tribe.append({"img": img_link[tribe_num], "tribe": tribe_names[tribe_num], "members": len(tribes[tribe_num]),
                           "mean": tribe_mean, "var": tribe_var})
        tribe_num = tribe_num + 1
        
    # Plot tribe data 3D
    plot_data_3d = []
    tribe_num = 0
    for indices in tribes:
        trace_3d = go.Scatter3d(
            x=proj_data[indices,0], y=proj_data[indices,1], z=proj_data[indices,2],
            mode="markers",
            name=tribe_names[tribe_num],
            marker=dict(
                color=tribe_colors[tribe_num],
                size=12,
                symbol="circle",
                opacity=0.8
            ),
            line=dict(
                color="rgba(217,217,217,0.14)",
                width=0.5
            )
        )
        plot_data_3d.append(trace_3d)
        tribe_num = tribe_num + 1
    
    layout = go.Layout(
            margin=dict(
                l=0,r=0,b=0,t=0
            )
        )
    fig = go.Figure(data=plot_data_3d, layout=layout)
    py.iplot(fig, filename='tribe-3d')

    return meta_tribe, tribe_colors
