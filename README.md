# A Deep Learning Architecture for Metabolic Pathway Prediction

This code is an implementation of our graph-convolutional network (GCN) and random forest (RF) classifiers for predicting one or many metabolic pathway classes for a query compound (paper currently under review). 

![Proposed GCN architecture](model.png)

We use SMILES representation of query molecules to generate relevant fingerprints, which are then fed to the GCN/RF architecture for producing binary labels corresponding to each of the 11 metabolic pathway classes. The details of the GCN and RF architectures are described in our paper (currently under review).

A dataset of 6669 compounds belonging to one or more of these 11 constituent pathway classes was downloaded (February 2019) from the KEGG database: https://www.genome.jp/kegg/pathway.html.

### Requirements
* PyTorch
* scikit-learn
* RDKit
* Jupyter Notebook

### Usage
We provide two notebook files, one each for the multi-class GCN classifier and the multi-class RF classifier. The notebooks are self-sufficient and various relevant details have been marked in the files themselves.

### Acknowledgements
Part of the code was adopted from [1], and suitably modified for the pathway prediction task.

### References
1. Tsubaki, Masashi, Kentaro Tomii, and Jun Sese. "Compound–protein interaction prediction with end-to-end learning of neural networks for graphs and sequences." Bioinformatics 35.2 (2018): 309-318.
