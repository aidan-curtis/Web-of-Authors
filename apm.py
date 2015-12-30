import re
import json
import math
from webofsciencescraper import bcolors
import argparse
def name_finder(name):
    if name and " and" in  name:
        name = name.replace(" and", "")
    elif name and "and "in name:
        name = name.replace("and ", "")
    if(name):
        if ',' in name:
            string_to_fix=name[name.find(',')+1:]
            regular_expression=re.compile("([A-Z]+)[-\s\.a-z]*([A-Z]*)[-\s\.a-z]*([A-Z]*)")
            final=re.search(regular_expression, string_to_fix)
            return name[:name.find(',')]+", "+final.group(1)+final.group(2)+final.group(3)
        else:
            return name
    else:
        return None

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description='Process some strings')
    parser.add_argument('source', metavar='N', nargs='+',help='a source file')
    parser.add_argument('target', metavar='N', nargs='+',help='a target file')
    source= parser.parse_args().source[0]
    target=parser.parse_args().target[0]

    
    file = open(source, 'rb')
    data = json.load(file)
    file.close()
    jsondata=[]

    for b in data:
        print "#",
        if b['author'] != None:
            for a in filter(None, re.split("[;\n]+", b['author'])):
                name = name_finder(a)
                if name not in [ x['Author'] for x in jsondata]:
                    jsonfile = open("authorProfiles", "wb")
                    jsondata.append({"Author": name, "Number_Of_Papers_Written": 1})
                else:
                    jsonfile = open("authorProfiles", "wb")
                    jsondata[[x['Author'] for x in jsondata].index(name)]['Number_Of_Papers_Written'] += 1


    for datum in jsondata:
        print ()
        jsondata[jsondata.index(datum)]['Number_Of_Papers_Written_Second_Author']=0
        jsondata[jsondata.index(datum)]['Number_Of_Papers_Written_First_Author']=0

    for b in data:
        print "#",
        if b['author'] != None:
            try:
                a=filter(None, re.split("[;\n]+", b['author']))[1]
                name=name_finder(a)
                jsonfile = open("authorProfiles", "wb")
                jsondata[[x['Author'] for x in jsondata].index(name)]['Number_Of_Papers_Written_Second_Author'] += 1
            except:
                #only one author
                print()

            a=filter(None, re.split("[;\n]+", b['author']))[0]
            name=name_finder(a)
            jsonfile = open("authorProfiles", "wb")
            jsondata[[x['Author'] for x in jsondata].index(name)]['Number_Of_Papers_Written_First_Author'] += 1
           
    for datum in jsondata:
        print ()
        jsondata[jsondata.index(datum)]['average_year_published']=0
        jsondata[jsondata.index(datum)]['Total_Number_Of_Citations']=0
        jsondata[jsondata.index(datum)]['Co-Authors']=[]
        
        
        current=0
    for a in data:
        print "#",
        if a['author'] != None:
            for author in filter(None, re.split("[;\n]+", a['author'])):
                name=name_finder(author)
                if name in [x['Author'] for x in jsondata]:
                    jsondata[[x['Author'] for x in jsondata].index(name)]["average_year_published"]+=int(a['year'])

                    

    for datum in jsondata:
        datum['average_year_published']=int(datum['average_year_published']/datum['Number_Of_Papers_Written'])



    for a in data:
        print "##",
        if a['author'] != None:
            for author in filter(None, re.split("[;\n]+", a['author'])):
                name=name_finder(author)
                if name in [x['Author'] for x in jsondata]:
                    jsondata[[x['Author'] for x in jsondata].index(name)]["Total_Number_Of_Citations"]+=int(a['timesCited'])


    for datum in data:
        print "###",
        if(datum['author']):
            for a in filter(None, re.split("[;\n]+", datum['author'])):
                name = name_finder(a)
                for b in filter(None, re.split("[;\n]+", datum['author'])):
                    name2=name_finder(b)
                    if(name2!=name):
                        jsondata[[x['Author'] for x in jsondata].index(name)]['Co-Authors'].append(name2)


                    
                    
jsonfile=open(target, "a")
json.dump(jsondata, jsonfile)
print bcolors.OKGREEN
jsonfile.close()
