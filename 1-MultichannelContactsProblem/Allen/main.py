import pandas as pd
import numpy as np

# disjoint set implementation
class DisjointSet(object):
    def __init__(self,size=1):
        self.parent = [n for n in range(size)]    
    
    def find(self, x):
        if (self.parent[x] != x):
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        xset = self.find(x)
        yset = self.find(y)

        if xset == yset: 
            return
        
        self.parent[yset] = xset
    def list_groups(self):
        parent_set = set(self.parent)
        grouped_sets = {x: set([x]) for x in parent_set}
        for count, x in enumerate(self.parent):
            grouped_sets[x].add(count)
        return [sorted(x) for x in grouped_sets.values()]

# for debugging
pd.set_option('display.max_rows', 50)

# read data from input
df = pd.read_json(r'..\\Resources\\contact.json')
N = len(df.index)

# isolate into the 3 contact columns and drop empty values
df_email_clean = df[['Id', 'Email']].replace('', np.nan).dropna()
df_phone_clean = df[['Id', 'Phone']].replace('', np.nan).dropna()
df_orderid_clean = df[['Id', 'OrderId']].replace('', np.nan).dropna()

# group into adjacent sets per column
email_sets = df_email_clean.groupby(by=['Email'])['Id'].apply(list).values
phone_sets = df_phone_clean.groupby(by=['Phone'])['Id'].apply(list).values
orderid_sets = df_orderid_clean.groupby(by=['OrderId'])['Id'].apply(list).values

# join all the sets together
all_sets = np.concatenate((email_sets, phone_sets, orderid_sets), axis=0)
all_sets = np.array([s for s in all_sets if len(s) > 1])

# reduce/simplify the sets using a disjoint set data structure
reduced_sets = DisjointSet(N)
for cur_set in all_sets:
    for c in cur_set:
        reduced_sets.union(cur_set[0], c)

# process sets into trace ticket id's and total contacts
contacts_count_list = df['Contacts']
adjacency_column = ['' for x in range(N)]
for set_item in reduced_sets.list_groups():
    trace_ticket_id = '-'.join([str(x) for x in set_item])
    total_contacts = sum(set_item)
    output_val = trace_ticket_id + ', ' + str(total_contacts)
    for i in set_item:
        adjacency_column[i] = output_val

# parse into a dataframe and export to csv
df_final = pd.DataFrame(enumerate(adjacency_column), columns=['ticket_id', 'ticket_trace/contact'])
print(df_final)
df_final.to_csv('outputs\\output' + datetime.today().strftime("%d-%m-%YT%H-%M-%S") + '.csv', index=False)