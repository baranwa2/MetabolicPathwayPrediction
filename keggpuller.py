#!/usr/bin/python
#
# Routines for scraping molecule from the KEGG pathway database.
#
from lxml import html;
import requests;
import json;
from rdkit import Chem;
from rdkit.Chem import MACCSkeys;
import csv;

#
# This is an example URL for the list of compounds associated with a given pathway (here given
# by map00010).
# https://www.genome.jp/dbget-bin/get_linkdb?-t+compound+path:map00010
#

#
#
#
class KEGGPathway:
    def __init__(self, id, name, className):
        self.id = id;
        self.name = name;
        self.className = className;
        self.compounds = []
        self.__compoundsFetched = False;
        #self.url = url;

    #
    #
    #
    def getCompoundsURL(self):
        return("https://www.genome.jp/dbget-bin/get_linkdb?-t+compound+path:map" + self.id);
 

    #
    # Fetch a list of KEGGCompound objects associated with this pathway.
    #
    def fetchCompounds(self):
        #TODO: Rewrite this!
        if (self.__compoundsFetched):
            return(self.compounds);
        retval = [];
        compoundsPage = requests.get(self.getCompoundsURL());
        compoundsPageTree = html.fromstring(compoundsPage.content);
        compoundIDList = compoundsPageTree.xpath('//pre/a/text()');
        # compoundIDList should contain a list of strings like "C00033".

#        modulePage = requests.get(self.getURL());
#        modulePageTree = html.fromstring(modulePage.content);
        #modulePageString = modulePage.text;
        #print("All compounds for this module: ");
        #print(modulePageString.split("www_bget?C"));
#        reactionCompoundLinkNodes = modulePageTree.xpath('//div[@id="definition"]/table/tr/td[text()="Reaction"]/../td[2]/a');
        #print(type(reactionCompoundLinkNodes))
        #print(reactionCompoundLinkNodes);
#        compoundNameList = [];
#        for reactionCompoundLinkNode in reactionCompoundLinkNodes:
#            reactionCompoundLink = reactionCompoundLinkNode.xpath('text()');
#            if (reactionCompoundLink[0][0] == 'C'):
                #print("Compound = " + reactionCompoundLink[0]);
                #compoundNameList.append(reactionCompoundLink[0]);
        for compoundID in compoundIDList:        
            retval.append(KEGGCompound(compoundID));
        self.compounds = retval;
        self.__compoundsFetched = True;
        return(retval);
#
#
#
class KEGGCompound:
    def __init__(self, id):
        self.id = id;
        self.__molFileText = None;
        self.__molFileFetched = False;
        #self.mol = None;
        self.pathways = [];
 
    #
    # Get the SMILES string associated with this compound.
    #
    def getSMILES(self):
        # Use RDKit to convert the mol file string to a SMILES. 
        mol = Chem.MolFromMolBlock(self.fetchMOLFileString());
        try:
            smilesString = Chem.rdmolfiles.MolToSmiles(mol);
        except:
            return("Unhandled");        # This was a polymer, which RDKit can't handle.
        return(smilesString);

    #
    # Get the MACCS fingerprint associated with this compound.
    #
    def getMACCS(self):
        mol = Chem.MolFromMolBlock(self.fetchMOLFileString());
        maccsFp = MACCSkeys.FingerprintMol(mol).ToBitString();
        return(maccsFp);

    #
    #
    #
    def fetchMOLFileString(self):
        if (self.__molFileFetched == True):
            return(self.__molFileText);
        urlStr = "https://www.genome.jp/dbget-bin/www_bget?-f+m+compound+" + self.id;
        molFile = requests.get(urlStr);
        self.__molFileText = str(molFile.text);
        self.__molFileFetched = True;
        #self.mol = Chem.MolFromMolBlock(self.__molFileText);
        return(self.__molFileText);

    #
    #
    #
    def addPathway(self, mod):
        self.pathways.append(mod);


#
# We have a file containing the list of modules, etc.  Each module name is M00... something.
# We can fetch the webpage for a given module by looking at https://www.genome.jp/kegg-bin/show_module?M00165.
# On this webpage, there are listed all the compounds involved in that module.  We can fetch the webpage
# for a given compound by looking at something like https://www.genome.jp/dbget-bin/www_bget?C00199 .
# On that webpage, there is a link like https://www.genome.jp/dbget-bin/www_bget?-f+m+compound+C00199
# to get the Mol file.  From the Mol file, we can convert to a compound object.
#



#
# Get list of pathways.  A pathway is an object with a string name, 
# a string class, a string subclass, and a string URL.
# Associated with a pathway object, we should write a routine
# that fetches all compound names.
#
def getPathways():
    retval = [];        # This will be a list of KEGGModule objects.
    # Get the KEGG modules page as a string.
    #page = requests.get("https://www.genome.jp/kegg-bin/download_htext?htext=ko00002.keg&format=json&filedir=");
    #jsonFile = open("../../data/kegg-data/ko00002.json");
    #jsonStr = jsonFile.read();
    #jsonFile.close();
    #print(page.text);
    #jsonData = json.loads(jsonStr);
    #print(jsonData.keys());
    #print(type(jsonData));
    #tree = html.fromstring(page.content);

    page = requests.get("https://www.genome.jp/kegg/pathway.html");
    tree = html.fromstring(page.content);
    #.xpath('//div[@id="definition"]/table/tr/td[text()="Reaction"]/../td[2]/a');
    for bNode in tree.xpath('//b'):
        pathwayClassNum = bNode.xpath('text()')[0].split(' ')[0];
        pathwayClassName = bNode.xpath('text()')[0].split(' ')[1];

        if (pathwayClassNum != '1.0' and pathwayClassNum != '1.' and pathwayClassNum != '1.12' and pathwayClassNum[0] == '1'):
            print("b node = " + bNode.xpath('text()')[0]);
            print("Pathway class number and name: " + pathwayClassNum + ", " + pathwayClassName);

            # We are interested in this pathway.
            pathwayIDNodes = bNode.xpath('following-sibling::div')[0].xpath('dl/dt');
            for pathwayIDNode in pathwayIDNodes:
                # Get the id.
                pathwayID = pathwayIDNode.xpath('text()')[0];
                pathwayName = pathwayIDNode.xpath('following-sibling::dd/a/text()')[0];
                print("Pathway id and name: " + str(pathwayID) + ", " + str(pathwayName));
                newPathway = KEGGPathway(pathwayID, pathwayName, pathwayClassName);
                retval.append(newPathway);
        #print(tree.xpath('//b/text()'));
    return(retval);    


#
#
#
def getPathwayIDFromName(pathwayName):
    return(pathwayName.split(" ")[0]);


##################################################################
# MAIN
##################################################################
#compoundDict = {};
#moduleDict = {};


#
# Assemble database of compounds in compoundDict.
#
pathways = getPathways();
print("Number of pathways: " + str(len(pathways)));
#for pw in pathways:
    
#
# Convert the list of modules to a CSV.
#
with open('keggdb2.csv', 'w') as csvfile:
    headers = ['ID', 'SMILES', 'MACCS', 'Pathway ID', 'Pathway name', 'Pathway class'];
    writer = csv.DictWriter(csvfile, fieldnames=headers);
    writer.writeheader();
    for mod in pathways:
        print(mod.className + ", " + mod.name + "," + mod.id);
        compounds = mod.fetchCompounds();
        for comp in compounds:
            #print(comp.fetchMOLFileString());
            #print(comp.getSMILES());
    #        print(comp.getMACCS());
    #        smiles = comp.getSMILES();
    #        if (smiles not in compoundDict):
    #            compoundDict[smiles] = comp;
            comp.addPathway(mod);
        #for comp in mod.compounds:
            if ("Unhandled" in comp.getSMILES()):
                # Skip this compound, as rdkit can't handle it.
                print("Skipping a compound because RDKit can't handle it.");
                continue;
            #if (comp.id in compoundWrittenSet):
            #    continue;
            # Indicate that this compound has already been written.
            #compoundWrittenSet.add(comp.id);
            
            #TODO: Write the row for this compound.
            writer.writerow({'ID':comp.id, 'SMILES':comp.getSMILES(), 'MACCS':comp.getMACCS(), 'Pathway ID':mod.id, 'Pathway name':mod.name, 'Pathway class':mod.className });
    
    
            #for modComp in comp.modules:
                #TODO: Append to the modules string some representation of
                # these modules..
            #print(comp.getSMILES() + "," + 
            #print(comp.getMACCS());
