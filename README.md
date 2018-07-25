# UNCOMMON HACKS 2018 Most Innovative Hack WINNER
This project won most innovative hack for UChicago's 2018 Hackathon! Thanks to all the judges for their hard work and the opportunity to bring this meme dream to fruition. 

# uncommon_data
Visualize csv datasets with Ugandan Knuckles Tribes using Principle Component Analysis and pandas/scikit-learn.

The primary script with data processing logic is contained in **tribe_clustering.py**.

The script is wrapped up inside a flask application which ties it to a simple UI that accepts a user uploaded .txt or .csv file and displays the resultant figures.

# Caveats
Obviously the nuances of doing data visualization in this manner is such that results are not always going to be pristine.

It should be noted that blindly throwing any dataset at this visualization tool is not a good approach.

Ideal use case would be for a very high dimensional continuous dataset as is the usual targets for PCA and K-Means.

In the future we would like to expand the platform to include different approaches and aid in visualization of many more different dataset tasks.
