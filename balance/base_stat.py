import json
from random import randint

def base_stat(baseline_data):
    with open('../static/data/'+baseline_data+'.json') as data_file:
        baseline_info = json.load(data_file)
    res=[]
    for i in range (0,500):
        person={}
        person['id']=i
        person['edu']=getRandom(baseline_info['edu']['values'])
        person['region']=getRandom(baseline_info['region']['values'])
        person['gender'] = getRandom(baseline_info['gender']['values'])
        person['hispanic'] = getRandom(baseline_info['hispanic']['values'])
        person['race'] = getRandom(baseline_info['race']['values'])
        person['age'] = getRandom(baseline_info['age']['values'])
        person['party'] = getRandom(baseline_info['party']['values'])
        person['income'] = getRandom(baseline_info['income']['values'])
        person['political_view'] = getRandom(baseline_info['political_view']['values'])
        res.append(person)
    for i in res:
        print(i)


def getRandom(stat_data):
    new_values=[]
    new_values.append(stat_data[0])
    for i in range(1,len(stat_data)):
        new_values.append(stat_data[i]+new_values[i-1])
    r=randint(0,100)
    for i in range(len(stat_data)):
        if r<= new_values[i]:
            return i+1



base_stat('All_Adults')
