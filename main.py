ownurl = "http://94.79.54.21:3000"
token = "dIlUIIpKrjCcrmmM"
emails = ['sscherepanov@edu.hse.ru','sscherepanov@miem.hse.ru']
from datetime import datetime
import requests
import json
from jinja2 import Template
import plotly.graph_objects as go

def GetDataFromGit():
    responseGit = requests.post("http://94.79.54.21:3000/api/git/getDataPerWeek", json= {
        "studEmail": "sscherepanov@miem.hse.ru",
        "beginDate": "2021-01-01",
        "endDate": "2022-03-30",
        "timeRange": 1,
        "hideMerge": True,
            "token": token }).json()
    GIT_commits_and_dates_forBar = {}
    GIT_commits_and_dates_forLinear = {}
    for project in responseGit['projects']:
        if (project['name'] == "ivt21-miniproject / Сергей Черепанов"):
            for Dates in project["commits_stats"]:
                GIT_commits_and_dates_forBar[Dates["beginDate"][4:15]] = Dates["commitCount"]
                GIT_commits_and_dates_forLinear[Dates["beginDate"][4:15]]=Dates["commitCount"]
    Git_summ = sum(GIT_commits_and_dates_forBar.values())
    Commits=0
    for key in GIT_commits_and_dates_forBar.keys():
        Commits+=GIT_commits_and_dates_forBar[key]
        GIT_commits_and_dates_forLinear[key]=Commits
    return GIT_commits_and_dates_forBar,Git_summ,GIT_commits_and_dates_forLinear
def GetDataFromZulip():
        responseZulip = requests.post('http://94.79.54.21:3000/api/zulip/getData', json=
        {
            "studEmail": "sscherepanov@miem.hse.ru",
  	        "beginDate": "2022-01-10",
           	"endDate": "2022-03-30",
             "timeRange": 1,
             "token": token
        }).json()
        Zulip_msg_and_datesForBar = {}
        Zulip_msg_and_datesForLinear = {}
        channels = []
        for Dates in responseZulip['stats']:
                    Zulip_msg_and_datesForBar[Dates["beginDate"][4:15]] = Dates['messageCount']
                    Zulip_msg_and_datesForLinear[Dates["beginDate"][4:15]] = Dates['messageCount']
        for channel in responseZulip['messages']:
            channels.append(channel['name'])
        Count_of_messages = sum(Zulip_msg_and_datesForBar.values())
        channels = list(set(channels))
        All_messages=0
        for key in Zulip_msg_and_datesForBar.keys():
            All_messages += Zulip_msg_and_datesForBar[key]
            Zulip_msg_and_datesForLinear[key] = All_messages
        return Zulip_msg_and_datesForBar,Count_of_messages,channels,Zulip_msg_and_datesForLinear
def GetDataFromJitsi():
    Jitsi_rooms = []
    Visited_classes_dates = {}
    Visited_classes_dates = set(Visited_classes_dates)
    Visited_classes_for_linear_count = []
    class_i_visited_per_day_count = []
    for num_of_mail in range(0,2):
            responseJitsi = requests.post('http://94.79.54.21:3000/api/jitsi/sessions', json=
            {
                    "studEmail":emails[num_of_mail],
                    'beginDate':'2021-09-01',
                    "endDate":'2022-03-30',
                    'token':token
            }).json()
            for index in responseJitsi:
                Jitsi_rooms.append(index['room'])
                Visited_classes_dates.add(index['date'])
    Visited_classes_dates=list(Visited_classes_dates)
    Visited_classes_dates.sort()
    count_of_classes = 0
    classes_visited_per_day = 1
    for classes in Visited_classes_dates:
        count_of_classes+=1
        Visited_classes_for_linear_count.append(count_of_classes)
        class_i_visited_per_day_count.append(classes_visited_per_day)
    Amount_of_visited_classes = max(Visited_classes_for_linear_count)
    Jitsi_rooms = list(set(Jitsi_rooms))
    return Amount_of_visited_classes,Jitsi_rooms,Visited_classes_for_linear_count,Visited_classes_dates,class_i_visited_per_day_count


def GetDataFromTaiga():
    #id 891
    Taiga_Tasks = list()
    responseTaigaStories = requests.get("https://track.miem.hse.ru/api/v1/userstories",
                         headers={"x-disable-pagination": "True"}).json()
    responseTaigaTasks = requests.get("https://track.miem.hse.ru/api/v1/tasks",
                         headers={"x-disable-pagination": "True"}).json()
    AmountTaigaStories=0
    AmountTaigaTasks=0
    Taiga_Dates_and_Tasks = {'2022-01-14':0,
             '2022-01-21':0, '2022-01-28':0, '2022-02-04':0,
             '2022-02-11':0, '2022-02-18':0, '2022-02-19':0,
             '2022-02-25':0, '2022-02-26':0, '2022-03-03':0, '2022-03-04':0,
             '2022-03-11':0, '2022-03-18':0, '2022-03-25':0, '2022-03-26':0, '2022-03-27':0, '2022-03-28':0, '2022-03-29':0, '2022-03-30':0, '2022-03-31':0}
    Taiga_Dates_and_Tasks2 = Taiga_Dates_and_Tasks
    for index in responseTaigaStories:
        if type(index["assigned_to_extra_info"])!=type(None):
           if index["assigned_to_extra_info"]["full_name_display"] == "Черепанов Сергей Степанович":
                AmountTaigaStories+=1
    for index1 in responseTaigaTasks:
        if type(index1["assigned_to_extra_info"])!=type(None):
           if index1["assigned_to_extra_info"]["full_name_display"] == "Черепанов Сергей Степанович":
                AmountTaigaTasks+=1
                Taiga_Tasks.append(index1)
    for index2 in Taiga_Dates_and_Tasks.keys():
        for num_of_task in Taiga_Tasks:
            if (str(num_of_task['created_date'][:10])) == index2:
                Taiga_Dates_and_Tasks[index2] += 1

    count_for_generate=0
    for key in Taiga_Dates_and_Tasks.keys():
        count_for_generate += Taiga_Dates_and_Tasks[key]
        Taiga_Dates_and_Tasks2[key] = count_for_generate
    return AmountTaigaStories,AmountTaigaTasks,Taiga_Dates_and_Tasks2

#Вызов всех функций

Zulip_msg_and_datesForBar, Count_of_messages, Channels,Zulip_msg_and_datesForLinear = GetDataFromZulip()
GIT_commits_and_dates_forBar, Git_summ,GIT_commits_and_dates_forLinear = GetDataFromGit()
Amount_of_visited_classes, Jitsi_rooms, Visited_classes_for_linear_count,Visited_classes_dates,class_i_visited_per_day_count = GetDataFromJitsi()
AmountTaigaStories, AmountTaigaTasks, Taiga_Dates_and_Tasks = GetDataFromTaiga()


def HTML_PAGE():
    FirstFile = open('shablon.html', encoding='utf8').read()
    shablon = Template(FirstFile)
    New_page = open('sscherepanov.html', 'w' ,encoding='utf8')
    New_page.write(shablon.render(#Time
                                  data=datetime.now().isoformat(),
                                  #GIT
                                  LinearGraphGit = go.Figure([go.Scatter(x=list(GIT_commits_and_dates_forLinear.keys()),y=list(GIT_commits_and_dates_forLinear.values()))]).to_html(),
                                  Git_summ = Git_summ,
                                  BarGraphGit = go.Figure([go.Bar(x=list(GIT_commits_and_dates_forBar.keys()),y=list(GIT_commits_and_dates_forBar.values()))]).to_html(),
                                  #Jitsi
                                  Amount_of_visited_classes = Amount_of_visited_classes,
                                  Jitsi_rooms = Jitsi_rooms,
                                  LinearGraphJitsi = go.Figure([go.Scatter(x=list(Visited_classes_dates),y=list(Visited_classes_for_linear_count))]).to_html(),
                                  BarGraphJitsi = go.Figure([go.Bar(x=list(Visited_classes_dates),y=list(class_i_visited_per_day_count))]).to_html(),
                                  #ZULIP
                                  LinearGraphZulip=go.Figure([go.Scatter(x=list(Zulip_msg_and_datesForLinear.keys()),y=list(Zulip_msg_and_datesForLinear.values()))]).to_html(),
                                  Count_of_messages_Zulip=Count_of_messages,
                                  Channels = Channels,
                                  BarGraphZulip=go.Figure([go.Bar(x=list(Zulip_msg_and_datesForBar.keys()),y=list(Zulip_msg_and_datesForBar.values()))]).to_html(),
                                  #Taiga
                                  LinearGraphTaiga=go.Figure([go.Scatter(x=list(Taiga_Dates_and_Tasks.keys()),y=list(Taiga_Dates_and_Tasks.values()))]).to_html(),
                                  Amount_of_tasks = AmountTaigaTasks,
                                  Amount_of_stories = AmountTaigaStories
                                  ))

HTML_PAGE()





