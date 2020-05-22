
import numpy as np 
import pandas as pd


import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))


file_division = pd.read_csv('/kaggle/input/taxonomy1/division.dmp.txt', sep= '\t\\|\t', engine = 'python')
file_nodes = pd.read_csv('/kaggle/input/taxonomy2/nodes.dmp.txt', sep= '\t\\|\t', engine = 'python' )
file_delnodes = pd.read_csv('/kaggle/input/taxonomy1/delnodes.dmp.txt', sep= '\t\\|\t', engine = 'python' )
file_gencode = pd.read_csv('/kaggle/input/taxonomy1/gencode.dmp.txt', sep= '\t\\|\t', engine = 'python' )
file_citations = pd.read_csv('/kaggle/input/taxonomy1/citations.dmp.txt', sep= '\t\\|\t', engine = 'python' )
files_merged = pd.read_csv('/kaggle/input/taxonomy1/merged.dmp.txt', sep= '\t\\|\t', engine = 'python' )
file_names = pd.read_csv('/kaggle/input/taxonomy3/names.dmp.txt', sep= '\t\\|\t', engine = 'python' )


file_division.columns = ['division_id','division_cde', 'division_name', 'comments'  ]
file_nodes.columns = ['tax_id', 'parent_tax_id', 'rank', 'embl_code', 'division_id', 'inherited_div_flag', 'genetic_code_id', 'inherited_GC_flag', 'mitochondrial_genetic_code_id'
             ,'inherited_MGC_flag', 'GenBank_hidden_flag', 'hidden_subtree_root_flag', 'comments']
file_delnodes = ['tax_id']
file_gencode.columns = ['genetic_code_id', 'abbreviation', 'name', 'cde', 'starts']
file_citations = ['cit_id','cit_key', 'medline_id', 'pubmed_id', 'url', 'text']
files_merged.columns = ['old_tax_id', 'new_tax_id']
file_names.columns = ['tax_id', 'name_txt', 'unique_name', 'name_class']


file_division.head(20)


file_names.head(20)


file_nodes.head(20)


file_gencode.head(20)


test = pd.merge(file_division, file_nodes, how="outer", on='division_id')
test2 = pd.merge(test, file_gencode, how="outer", on='genetic_code_id')
main_data = pd.merge(test2, file_names, how="outer", on='tax_id')
main_data.head(80)


# No need for the citation dump files as it does not correspond to what objective is. Will not be including merged_files as not exactly sure what these files will be including except for deleted id nodes and new nodes from merged file



main_data.head(10)


dict = {}
def initiation_funct():
    rank_names = main_data['rank']
    for i in rank_names:
        if i in dict:
            dict[i] += 1
        else:
            dict[i] = 1
    return dict
initiation_funct()
display(dict)

#Gives the names of rank and amount in each rank to visualize the data


main_data['counter'] = 1
main_grouped = main_data.groupby(['rank', 'division_name'])['counter'].count()
display(main_grouped)


# The following graphs will be displaying the information from the table above. These graphas are grouped together by the rank and division name and includes the percentage of organisms in that classification according to this grouping.


import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

try:
    for i in dict:
            plt.figure()
            class_data = main_grouped.loc[str(i)]
            class_graph = class_data.plot.pie(autopct='%1.1f%%', figsize = (7,7), fontsize = 9, title = str(i))
except KeyError:
    pass


# The following code will be to set up a hierarchy based off of the class that the organism is in. The main ranking of organisms goes as follows.
# 1. Domain
# 2. Kingdom
# 3. Phylum
# 4. Class
# 5. Order
# 6. Family
# 7. Genus
# 8. Species
# 
# The first colored name will be the classification of the organism. The following will only display part of the data.


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# If there is a TypeError such as a NaN rank name or other type then it will be skipped 
class root:
    
    def __init__(self): 
        self.rank = main_data['rank'].head(200)
        self.names = main_data['name_txt'].head(200)
        
    def hierarchy(self):
        self.lst = ['kingdom', 'class', 'family', 'genus', 'order', 'phylum', 'cohort', 'tribe', 'species group']
        try:
            for i, j in zip(self.rank, self.names):
                rank = i 
                names = j
                if 'super' in rank:
                    print(bcolors.OKBLUE + rank + bcolors.ENDC ,'--->', rank.replace('super', ''),'--->', 'sub' + rank.replace('super', ''),'--->',
                         'infra' + rank.replace('super', ''),'--->' ,'parv' + rank.replace('super', ''),
                          bcolors.OKGREEN + 'Name:' + bcolors.ENDC, bcolors.FAIL + names  + bcolors.ENDC)
                elif 'sub' in rank:
                    print('super' + rank.replace('sub', ''), '--->' ,rank.replace('sub', ''),'--->',bcolors.OKBLUE + rank + bcolors.ENDC ,
                         '--->' ,'infra'+ rank.replace('sub', ''), '--->' ,'parv' + rank.replace('sub', ''),
                          bcolors.OKGREEN + 'Name:' + bcolors.ENDC, bcolors.FAIL + names  + bcolors.ENDC)
                elif 'infra' in rank:
                    print('super' + rank.replace('infra', ''), '--->' ,rank.replace('infra', ''),
                          '--->', 'sub' + rank.replace('infra', ''),bcolors.OKBLUE + rank + bcolors.ENDC , '--->' ,'parv'+ rank.replace('infra', ''),
                          bcolors.OKGREEN + 'Name:' + bcolors.ENDC, bcolors.FAIL + names  + bcolors.ENDC)
                else:
                    if 'parv' in self.rank:
                        print('super' + rank.replace('parv', ''), '--->' ,rank.replace('parv', ''),
                              '--->', 'sub' + rank.replace('parv', ''),'--->', 'infra' + rank.replace('parv', ''),'--->',bcolors.OKBLUE + rank + bcolors.ENDC ,
                              bcolors.OKGREEN + 'Name:' + bcolors.ENDC, bcolors.FAIL + names  + bcolors.ENDC)
                for i in self.lst:
                    lst_name = i
                    if lst_name == rank:
                        print('super'+ rank,'--->', bcolors.OKBLUE + rank + bcolors.ENDC ,'--->', 'sub' + rank,'--->', 'infra' + rank ,
                             '--->', 'parv' + rank, bcolors.OKGREEN + 'Name:' + bcolors.ENDC, bcolors.FAIL + names  + bcolors.ENDC)
        except TypeError:
            pass
        
root_init = root()
root_init.hierarchy()


pip install taxopy


# The following will showcase 10,000 lines of data and will traceback that organisms ancestor all the way to the root.


import taxopy

taxonomydata = taxopy.TaxDb(nodes_dmp ='/kaggle/input/taxonomy4/nodes.dmp', names_dmp = '/kaggle/input/taxonomy4/names.dmp', keep_files=True)

# If there is a ValueError such as a NaN or other type then it will be skipped

class ancestor_tracking:
    
    def __init__(self):
        self.num_str_lst = []
        self.counter = 0
        self.limit = 200

    def lst_initiation(self):
        while self.counter < self.limit:
            try:
                for i in main_data['parent_tax_id'].head(200):
                    float_to_int = int(i)
                    self.num_str_lst.append(str(float_to_int))
                    self.counter += 1
            except ValueError:
                continue


    def lowest_common_anc(self):
        for i, name in zip(self.num_str_lst, main_data['name_txt'].head(200)):
            new_str = i.replace(',','')
            ancestor_track = taxopy.Taxon(new_str, taxonomydata)
            print(ancestor_track,',', bcolors.OKGREEN + 'Name:' + bcolors.OKGREEN, bcolors.FAIL + name + bcolors.ENDC )
            print('-------------------------------------------------')

test = ancestor_tracking()
test.lst_initiation()
test.lowest_common_anc()


