import csv

import os
import datetime

mydate = datetime.datetime.now()

DIRECTORY = '.'
SHEET_FILE_NAME = 'Packet_Drop_'+mydate.strftime("%d-%B")+'.csv'




files = [f for f in os.listdir(DIRECTORY) if os.path.isfile(f) & f.endswith('.txt')]


files.sort(key=lambda x: x.split('_')[0])

#Create CSV file with header
with open(SHEET_FILE_NAME, 'w') as outcsv:
    writer = csv.DictWriter(outcsv, lineterminator='\n', fieldnames=["IP_ADDRESS", "FREE_MEMORY", "INTERFACES",
                                                                     "TABLE_ALLOCATION_SIZE", "PERF_DROPS",
                                                                     "TABLE_DROPS", "TIMESTAMP"])
    # add empty row after header
    #writer.writeheader()
    writer.writerow(dict(zip(writer.fieldnames, writer.fieldnames)))




# collect data from output file

for file in files:
    interfaces = []
    inf_drops = []
    free_memory = ''
    ip_address = ''
    f = open(file, 'r+')
    lines = f.readlines()
    parsing_allocation = False
    parsing_drops = False
    inf_index = 0
    inf_number=[]
    parsing = False
    for i in range(0, len(lines)):
        line = lines[i]

        # get the ip address
        if line.__contains__('Probe IP V4 address '):
            ip_address = line.split()[4]
        # get the free memory
        if line.__contains__('Free memory available ='):
            free_memory = filter(str.isdigit, line)


        if line.startswith(' ** Interface '):
            inf_index = filter(str.isdigit, line)
            parsing=True
            interface = {}
            interface['inf'] = inf_index
            interface['table allocation size'] = ''
            interface['Perf drops']=''
            interface['Timestamp'] = ''
            interface['Table Drops'] = ''
            interfaces.append(interface)

            if inf_index not in inf_number:
                inf_number.append(inf_index)

        if parsing:


            if line.__contains__('Processing drops'):

                for i in interfaces:
                    if (inf_index==i['inf'] ):
                        if i['Perf drops']=='':

                             i['Perf drops'] = filter(str.isdigit, line)







            if line.__contains__("%  Table size allocation"):
                    inf = line.split()
                    # get interfaces & table size allocation


                    parsing_allocation = True



            elif line.startswith('% ifn  custom_dpi'):
                        parsing_allocation = False
            if parsing_allocation:
                        # get interfaces details
                        info=line.split()

                        if (len(info) > 0 and info[0].isdigit()):

                            for inf in interfaces:

                                    if inf['inf']==info[0]:
                                        inf['table allocation size']=info[1]








            #get perf drops


        #get timestamp and table drops
        if line.startswith("Ifn  TableName           Configured MaxUse    InUse     LastDropTime"):

            parsing_drops = True

        elif line.startswith ("%"):
            parsing_drops = False
        if parsing_drops:

            if (len(line.split()) == 6):

                if (line.split()[0].isdigit())&(line.split()[5].__contains__(':')):


                    for index in interfaces:

                        if index['inf'] == line.split()[0]:
                            if index['Timestamp'] == '':
                                index['Timestamp'] = line.split()[5]
                                index['Table Drops'] = line.split()[1]

                            else:
                            #
                                new_item = {}
                                new_item['inf'] = index['inf']
                                new_item['table allocation size'] = index['table allocation size']
                                new_item['Perf drops'] = index['Perf drops']
                                new_item['Timestamp'] = line.split()[5]
                                new_item['Table Drops'] = line.split()[1]

                                inf_drops.append(new_item)

    interfaces.extend(inf_drops)
    interfaces.sort(key=lambda x:x['inf'])

    #fill empty fields
    for f in interfaces:
        for j in interfaces:
            if j['inf']==f['inf']:
                j['table allocation size']=f['table allocation size']
    #print items
    #for x in interfaces : print x
    with open(SHEET_FILE_NAME, 'a') as outcsv:
        writer = csv.DictWriter(outcsv,  lineterminator='\n', fieldnames = ["IP_ADDRESS", "FREE_MEMORY", "INTERFACES" ,
                                                                            "TABLE_ALLOCATION_SIZE", "PERF_DROPS", "TABLE_DROPS","TIMESTAMP"])
        #add empty row after header
        #writer.writeheader()

        writer.writerow({})
        writer.writerow({'IP_ADDRESS': ip_address,'FREE_MEMORY': free_memory} )

        writer.writerows({'INTERFACES': inf['inf'], 'TABLE_ALLOCATION_SIZE': inf['table allocation size'],'PERF_DROPS':inf['Perf drops'],
                          'TABLE_DROPS':inf['Table Drops'],'TIMESTAMP':inf['Timestamp']
                          } for inf in interfaces)
        #add empty row
        writer.writerow({})

