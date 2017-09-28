import cherrypy
import configparser
import json
import pandas as pd
import numpy as np
from abc import ABCMeta, abstractmethod
from jinja2 import Environment, FileSystemLoader


class BalanceJSONSerializable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_json(self):
        pass


class BalanceJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BalanceJSONSerializable):
            return obj.to_json()
        else:
            return super().default(obj)

    def iterencode(self, value):
        for chunk in super().iterencode(value):
            yield chunk.encode('utf-8')


# Custom json_handler which should be extended as needed to allow custom serialization of objects.
def json_handler(*args, **kwargs):
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return WebApplication.json_encoder.iterencode(value)


class WebApplication(object):
    json_encoder = BalanceJSONEncoder()
    survey_data = ""
    balance_data = ""
    def __init__(self):
        # Read the tempo config file to initialize the web application.
        self.config = configparser.ConfigParser()
        self.config.read("cfg/balance.cfg")

        # Configure cherrypy to use our custom JSON handler.
        cherrypy.config['tools.json_out.handler'] = json_handler

        # Set the environment
        self.env = Environment(loader=FileSystemLoader('templates'))
        # Start the web server using the cherrypy config file.
        cherrypy.config.update({'tools.sessions.on': True})
        cherrypy.quickstart(self, "", "cfg/cherrypy.cfg")

    @cherrypy.expose
    def index(self, dataisset=None):
        # Render the user interface and return it to the browser.

        template = self.env.get_template('index.html')
        return template.render(title='<b>Polling</b><i>Balance</i>', plaintitle="Polling Balance")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def requestdata(self, name):
        if name == "MUP48":
            global survey_data
            survey_data = "MUP48"
            with open('./static/data/MUP48.json') as data_file:
                data = json.load(data_file)
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return data
        if name == "MUP126":

            survey_data = "MUP126"
            with open('./static/data/MUP126.json') as data_file:
                data = json.load(data_file)
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return data
        if name == "All_Adults":
            global baseline_data
            baseline_data = "All_Adults"
            with open('./static/data/All_Adults.json') as data_file:
                data = json.load(data_file)
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return data
        if name == "All_Voters":
            baseline_data = "All_Voters"
            with open('./static/data/All_Voters.json') as data_file:
                data = json.load(data_file)
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return data


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def dobalance(self, percentage, balancebylist):
        ne={"NY", "NJ", "PA", "CT", "MA", "VT", "NH", "ME", "RI"}
        s= {"OK"  ,  "TX"  ,  "LA"  ,  "AR"  ,  "KY" ,"TN","MS","AL","FL","GA","SC", "NC"  ,  "VA"  ,  "WV"  ,  "MD",  "DE"  ,  "DC"}
        mw={"ND","SD","NE","KS","MN","IA","MO","WI","IL","IN","MI","OH"}
        w={"WA","OR","ID","MT","WY","CA","NV","UT","CO","AZ","NM"}
        o={"HI","AK"}
        #get polling data
        participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
        participant_len=len(participant_info)
        #get baseline data
        with open('./static/data/' + baseline_data + '.json') as data_file:
            baseline_info = json.load(data_file)
         #last item in the balancelist is empty
        balancebylist=balancebylist.strip()
        balancebylist=balancebylist[:-1]
        balancelist = balancebylist.split(",")
        striplist=[item.strip() for item in balancelist]
        gb=participant_info.groupby(striplist)
        #
        # #score for candidates
        candidate_one_score = 0
        candidate_two_score = 0
        for name, group in gb:
            #contains 9 or not
            valid=True
            survey_percentage=len(group)/participant_len
            baseline_percentage=1
            for i in range(len(striplist)):
                if name[i] == 9:
                    valid=False
                    break
                if striplist[i]=="Race" and (name[i] == 4 or name[i] == 5):
                    valid=False
                    break
                if striplist[i]== "Party" and name[i] ==4:
                    valid=False
                    break
            if valid==True:
                for i in range(len(striplist)):
                    if striplist[i]=="Last Grade in School":
                        if name[i] == 1 or name[i] == 2:
                            baseline_percentage *= baseline_info["edu"]["values"][0]
                        if name[i] == 3 or name[i] == 4:
                            baseline_percentage *= baseline_info["edu"]["values"][1]
                        if name[i] == 5 or name[i] == 6:
                            baseline_percentage *= baseline_info["edu"]["values"][2]
                        if name[i] == 7 or name[i] == 8:
                            baseline_percentage *= baseline_info["edu"]["values"][name[i]-4]
                    if striplist[i]=="Age":
                        if 18 <= name[i] <= 24:
                            baseline_percentage *= baseline_info["age"]["values"][0]
                        if 25 <= name[i] <= 29:
                            baseline_percentage *= baseline_info["age"]["values"][1]
                        if 30 <= name[i] <= 39:
                            baseline_percentage *= baseline_info["age"]["values"][2]
                        if 40 <= name[i] <= 49:
                            baseline_percentage *= baseline_info["age"]["values"][3]
                        if 50 <= name[i] <= 65:
                            baseline_percentage *= baseline_info["age"]["values"][4]
                        else:
                            baseline_percentage *= baseline_info["age"]["values"][5]
                    if striplist[i]=="Region":
                        if name[i] in ne:
                            baseline_percentage *= baseline_info["region"]["values"][0]
                        if name[i] in s:
                            baseline_percentage *= baseline_info["region"]["values"][1]
                        if name[i] in mw:
                            baseline_percentage *= baseline_info["region"]["values"][2]
                        if name[i] in w:
                            baseline_percentage *= baseline_info["region"]["values"][3]
                        if name[i] in o:
                            baseline_percentage *= baseline_info["region"]["values"][4]

                    if striplist[i]=="Gender":
                        baseline_percentage*=baseline_info["gender"]["values"][name[i]-1]/100
                    if striplist[i]=="Latino or Hispanic Origin":
                        baseline_percentage*=baseline_info["hispanic"]["values"][name[i]-1]
                    if striplist[i]=="Race":
                        baseline_percentage*=baseline_info["race"]["values"][name[i]-1]/100
                    if striplist[i]=="Party":
                        baseline_percentage*=baseline_info["party"]["values"][name[i]-1]
            #vote for the first candidate in this subgroup
            candidate_one_filter=group.loc[group['vote'] == 1]
            candidate_one_count=candidate_one_filter['id'].count()
            candidate_two_filter=group.loc[group['vote'] == 2]
            candidate_two_count=candidate_two_filter['id'].count()
            newpercentage = (baseline_percentage-survey_percentage) * int(percentage)/100
            candidate_one_score += candidate_one_count*(survey_percentage+newpercentage)

            candidate_two_score += candidate_two_count*(survey_percentage+newpercentage)
        sum=candidate_one_score+candidate_two_score
        candidate_one_score=round(candidate_one_score/sum * 100,2)
        candidate_two_score=round(candidate_two_score/sum * 100,2)
        print(percentage)
        print(candidate_one_score)
        print(candidate_two_score)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return {"values":[candidate_one_score,candidate_two_score]}
