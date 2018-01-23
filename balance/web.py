import cherrypy
import configparser
import json
import pandas as pd
import numpy as np
from abc import ABCMeta, abstractmethod
from jinja2 import Environment, FileSystemLoader
SAMPLE_SIZE = 1000

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
        #score for candidates
        candidate_one_score = 0
        candidate_two_score = 0
        #only one dimension
        if len(striplist)==1:
            for name, group in gb:
                print(name,group)
                valid=True
                survey_percentage = len(group) / participant_len
                baseline_percentage = 1
                if name == 9:
                    valid=False
                if striplist[0]=="Race" and (name == 4 or name==5):
                    valid=False
                if striplist[0] == "Party" and name == 4:
                    valid = False
                if valid==True:
                    if striplist[0] == "Last Grade in School":
                        baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                    if striplist[0] == "Age":
                        baseline_percentage *= baseline_info["age"]["values"][name] / 100
                    if striplist[0] == "Region":
                        baseline_percentage *= baseline_info["region"]["values"][name] / 100
                    if striplist[0] == "Gender":
                        baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                    if striplist[0] == "Latino or Hispanic Origin":
                        baseline_percentage *= baseline_info["hispanic"]["values"][name ] / 100
                    if striplist[0] == "Race":
                        baseline_percentage *= baseline_info["race"]["values"][name] / 100
                    if striplist[0] == "Party":
                        baseline_percentage *= baseline_info["party"]["values"][name]/100
                candidate_one_filter = group.loc[group['vote'] == 1]
                candidate_one_count = candidate_one_filter['id'].count()
                candidate_two_filter = group.loc[group['vote'] == 2]
                candidate_two_count = candidate_two_filter['id'].count()
                newpercentage = (baseline_percentage - survey_percentage) * int(percentage) / 100+survey_percentage
                candidate_one_score += candidate_one_count * newpercentage/survey_percentage
                candidate_two_score += candidate_two_count * newpercentage/survey_percentage

        else:
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
                            baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                        if striplist[i]=="Age":
                            baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                        if striplist[i]=="Region":
                            baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                        if striplist[i]=="Gender":
                            baseline_percentage*=baseline_info["gender"]["values"][name[i]]/100
                        if striplist[i]=="Latino or Hispanic Origin":
                            baseline_percentage*=baseline_info["hispanic"]["values"][name[i]]/100
                        if striplist[i]=="Race":
                            baseline_percentage*=baseline_info["race"]["values"][name[i]]/100
                        if striplist[i]=="Party":
                            baseline_percentage*=baseline_info["party"]["values"][name[i]]/100
                #vote for the first candidate in this subgroup
                candidate_one_filter=group.loc[group['vote'] == 1]
                candidate_one_count=candidate_one_filter['id'].count()
                candidate_two_filter=group.loc[group['vote'] == 2]
                candidate_two_count=candidate_two_filter['id'].count()
                newpercentage = (baseline_percentage-survey_percentage) * int(percentage)/100 + survey_percentage
                candidate_one_score += candidate_one_count*newpercentage/survey_percentage
                candidate_two_score += candidate_two_count*newpercentage/survey_percentage
        sum=candidate_one_score+candidate_two_score
        candidate_one_score=round(candidate_one_score/sum * 100,4)
        candidate_two_score=round(candidate_two_score/sum * 100,4)

        # multiple dimensions
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return {"values":[candidate_one_score,candidate_two_score]}

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recaledu(self, percentage, balancebylist):
        #if already balance by edu, new distribution can be calculated by slider.js
        if balancebylist.find("Last Grade in School") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for edu. Number varies by dimensions
            ans=[0.0] * 5
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:

                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        edu_m_filter = group.loc[group["Last Grade in School"] == m]
                        edu_m_count = edu_m_filter['id'].count()
                        ans[m] += edu_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[i] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        edu_m_filter = group.loc[group["Last Grade in School"] == m]
                        edu_m_count = edu_m_filter['id'].count()
                        ans[m] += edu_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recalgender(self, percentage, balancebylist):
        #if already balance by gender, new distribution can be calculated by slider.js
        if balancebylist.find("Gender") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for gender. Number varies by dimensions
            ans=[0.0] * 2
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:
                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        gender_m_filter = group.loc[group["Gender"] == m]
                        gender_m_count = gender_m_filter['id'].count()
                        ans[m] += gender_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[i] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        gender_m_filter = group.loc[group["Gender"] == m]
                        gender_m_count = gender_m_filter['id'].count()
                        ans[m] += gender_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recalregion(self, percentage, balancebylist):
        #if already balance by region, new distribution can be calculated by slider.js
        if balancebylist.find("region") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for region. Number varies by dimensions
            ans=[0.0] * 5
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:
                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        region_m_filter = group.loc[group["Region"] == m]
                        region_m_count = region_m_filter['id'].count()
                        ans[m] += region_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        region_m_filter = group.loc[group["Region"] == m]
                        region_m_count = region_m_filter['id'].count()
                        ans[m] += region_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recalhispanic(self, percentage, balancebylist):
        #if already balance by hispanic, new distribution can be calculated by slider.js
        if balancebylist.find("Latino or Hispanic Origin") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for hispanic. Number varies by dimensions
            ans=[0.0] * 2
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:
                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        hispanic_m_filter = group.loc[group["Latino or Hispanic Origin"] == m]
                        hispanic_m_count = hispanic_m_filter['id'].count()
                        ans[m] += hispanic_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        hispanic_m_filter = group.loc[group["Latino or Hispanic Origin"] == m]
                        hispanic_m_count = hispanic_m_filter['id'].count()
                        ans[m] += hispanic_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recalage(self, percentage, balancebylist):
        #if already balance by age, new distribution can be calculated by slider.js
        if balancebylist.find("age") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for age. Number varies by dimensions
            ans=[0.0] * 6
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:
                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        age_m_filter = group.loc[group["Age"] == m]
                        age_m_count = age_m_filter['id'].count()
                        ans[m] += age_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[i] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        age_m_filter = group.loc[group["Age"] == m]
                        age_m_count = age_m_filter['id'].count()
                        ans[m] += age_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recalrace(self, percentage, balancebylist):
        #if already balance by race, new distribution can be calculated by slider.js
        if balancebylist.find("race") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for race. Number varies by dimensions
            ans=[0.0] * 3
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:
                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        race_m_filter = group.loc[group["Race"] == m]
                        race_m_count = race_m_filter['id'].count()
                        ans[m] += race_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[0] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        race_m_filter = group.loc[group["Race"] == m]
                        race_m_count = race_m_filter['id'].count()
                        ans[m] += race_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def recalparty(self, percentage, balancebylist):
        #if already balance by party, new distribution can be calculated by slider.js
        if balancebylist.find("party") != -1:
            pass
        else:
            # get polling data
            participant_info = pd.read_csv('./static/data/' + survey_data + '.csv')
            participant_len = len(participant_info)
            # get baseline data
            with open('./static/data/' + baseline_data + '_After_Adjust.json') as data_file:
                baseline_info = json.load(data_file)
            # get sample adata
            sample_info = pd.read_csv(open('./static/data/sample.csv'))
            # last item in the balancelist is empty
            balancebylist = balancebylist.strip()
            balancebylist = balancebylist[:-1]
            balancelist = balancebylist.split(",")
            striplist = [item.strip() for item in balancelist]
            # polling data group be list
            gb = participant_info.groupby(striplist)
            #there will be five values for party. Number varies by dimensions
            ans=[0.0] * 4
            #only one item in balance list
            if len(striplist) ==1:
                for name, group in gb:
                    valid=True
                    survey_percentage=len(group)/SAMPLE_SIZE
                    baseline_percentage = 1
                    if name == 9:
                        valid = False
                    if striplist[0] == "Race" and (name == 4 or name == 5):
                        valid = False
                    if striplist[0] == "Party" and name == 4:
                        valid = False
                    if valid == True:
                        if striplist[0] == "Last Grade in School":
                            baseline_percentage *= baseline_info["edu"]["values"][name] / 100
                        if striplist[0] == "Age":
                            baseline_percentage *= baseline_info["age"]["values"][name] / 100
                        if striplist[0] == "Region":
                            baseline_percentage *= baseline_info["region"]["values"][name] / 100
                        if striplist[0] == "Gender":
                            baseline_percentage *= baseline_info["gender"]["values"][name] / 100
                        if striplist[0] == "Latino or Hispanic Origin":
                            baseline_percentage *= baseline_info["hispanic"]["values"][name] /100
                        if striplist[0] == "Race":
                            baseline_percentage *= baseline_info["race"]["values"][name] / 100
                        if striplist[0] == "Party":
                            baseline_percentage *= baseline_info["party"]["values"][name] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        party_m_filter = group.loc[group["Party"] == m]
                        party_m_count = party_m_filter['id'].count()
                        ans[m] += party_m_count * newpercentage/survey_percentage
            else:
                for name, group in gb:
                    # contains 9 or not
                    valid = True
                    survey_percentage = len(group) / SAMPLE_SIZE
                    baseline_percentage = 1
                    for i in range(len(striplist)):
                        if name[i] == 9:
                            valid = False
                            break
                        if striplist[i] == "Race" and (name[i] == 4 or name[i] == 5):
                            valid = False
                            break
                        if striplist[i] == "Party" and name[i] == 4:
                            valid = False
                            break
                    if valid == True:
                        for i in range(len(striplist)):
                            if striplist[i] == "Last Grade in School":
                                baseline_percentage *= baseline_info["edu"]["values"][name[i]] / 100
                            if striplist[i] == "Age":
                                baseline_percentage *= baseline_info["age"]["values"][name[i]] / 100
                            if striplist[i] == "Region":
                                baseline_percentage *= baseline_info["region"]["values"][name[i]] / 100
                            if striplist[0] == "Gender":
                                baseline_percentage *= baseline_info["gender"]["values"][name[i]] / 100
                            if striplist[i] == "Latino or Hispanic Origin":
                                baseline_percentage *= baseline_info["hispanic"]["values"][name[i]] / 100
                            if striplist[i] == "Race":
                                baseline_percentage *= baseline_info["race"]["values"][name[i]] / 100
                            if striplist[i] == "Party":
                                baseline_percentage *= baseline_info["party"]["values"][name[i]] / 100
                    newpercentage = (baseline_percentage - survey_percentage) * int(
                        percentage) / 100 + survey_percentage
                    for m in range(len(ans)):
                        party_m_filter = group.loc[group["Party"] == m]
                        party_m_count = party_m_filter['id'].count()
                        ans[m] += party_m_count * newpercentage / survey_percentage
            s = sum(ans)
            for i in range(len(ans)):
                 ans[i] = round(ans[i] / s * 100,4)

            cherrypy.response.headers['Content-Type'] = 'application/json'
            return {"values": ans}

