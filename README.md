# A Deep Learning Architecture for Metabolic Pathway Prediction

This code is an implementation of our graph-convolutional network (GCN) and random forest (RF) classifiers for predicting one or many metabolic pathway classes for a query compound (paper accepted at Bioinformatics, Oxford University Press). 

![Proposed GCN architecture](model.png)

We use SMILES representation of query molecules to generate relevant fingerprints, which are then fed to the GCN/RF architecture for producing binary labels corresponding to each of the 11 metabolic pathway classes. The details of the GCN and RF architectures are described in our paper (currently under review).

A dataset of 6669 compounds (4935 unique compounds) belonging to one or more of these 11 constituent pathway classes was downloaded (February 2019) from the KEGG database: https://www.genome.jp/kegg/pathway.html. We used keggpuller.py to download the dataset. All scripts pertaining to multi-label classification are available in the *multi-class* directory.

We also obtained a dataset with a single classification category that includes 4,539 unique compounds. Subsequently, we created a distinct model specifically for the single-class classification task. You can find the scripts for this model in the *single-class* directory.

### Requirements
* PyTorch
* scikit-learn
* RDKit
* Jupyter Notebook

### Usage
* For multi-label classification, we provide two notebook files, one each for the multi-class GCN classifier and the multi-class ML classifiers. The notebooks are self-sufficient and various relevant details have been marked in the files themselves.
* For single-class classification, we provide two notebook files: *data_handling.ipynb* to prepare the dataset, and *train_models.ipynb* to create and train GCN and Random Forest classifiers.
### Acknowledgements
Part of the code was adopted from [2], and suitably modified for the pathway prediction task.

### References
1. Baranwal, Mayank, Abram Magner, Paolo Elvati, Jacob Saldinger, Angela Violi, and Alfred Hero. "A deep learning architecture for metabolic pathway prediction." Bioinformatics (2019)
2. Tsubaki, Masashi, Kentaro Tomii, and Jun Sese. "Compound–protein interaction prediction with end-to-end learning of neural networks for graphs and sequences." Bioinformatics 35.2 (2018): 309-318.
