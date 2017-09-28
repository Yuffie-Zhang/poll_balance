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
                if name[i] == 4 or name[i] == 5 or name[i] == 9:
                    valid=False
                    break
            if valid==True:
                for i in range(len(striplist)):
                    if striplist[i]=="Last Grade in School":
                        baseline_percentage*=baseline_info["edu"]["values"][name[i]-1]
                    if striplist[i]=="Age":
                        baseline_percentage*=baseline_info["age"]["values"][name[i]-1]
                    if striplist[i]=="Region":
                        baseline_percentage*=baseline_info["region"]["values"][name[i]-1]
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
            candidate_one_score+=candidate_one_count*baseline_percentage/survey_percentage
            candidate_two_score+=candidate_two_count*baseline_percentage/survey_percentage
            sum=candidate_one_score+candidate_two_score
            candidate_one_score=round(candidate_one_score/sum * 100)
            candidate_two_score=round(candidate_two_score/sum * 100)
            print(candidate_one_score)
            print(candidate_two_score)
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return {"values":[candidate_one_score,candidate_two_score]}
