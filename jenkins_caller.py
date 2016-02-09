import requests
from config import host

##Direct calls
def executors(host):
    return requests.get('http://'+host+'/computer/api/json').json()['computer']

def queue(host):
    return requests.get('http://'+host+'/queue/api/json').json()['items']

def views(host):
    return requests.get('http://'+host+'/api/json').json()['views']

def jobs(host):
    return requests.get('http://'+host+'/api/json').json()['jobs']

def get_executor_for_job(host, job, number):
    return requests.get('http://'+host+'/job/'+job+'/'+number+'/api/json').json()['builtOn']




def get_active_builds(host, job):
    ##TODO, Jenkins api does not provide information about all active execution of specific build, this needs to be reimplemented
    active_builds= []

    response = requests.get('http://'+host+'/job/'+job+'/api/json').json()
    last_build = response['lastBuild']['number']
    scenarios = []
    for scenario in ["lastBuild", "lastCompletedBuild", "lastStableBuild", "lastSuccessfulBuild", "lastUnstableBuild", "lastUnsuccessfulBuild"]:
        try:
            scenarios.append(response[scenario]['number'])
        except TypeError:
            pass

    lower_limit = min(scenarios)
    for number in range(last_build, lower_limit,-1):
        if 'True' in str(requests.get('http://'+host+'/job/'+job+'/'+str(number)+'/api/json').json()['building']):
            active_builds.append(str(number))
    return active_builds




def build_executors_info():
    jobs_on_executors={}
    result = {}
    for job in jobs(host):
        active_builds = get_active_builds(host, job['name'])
        for active_build in active_builds:
            exec_name = get_executor_for_job(host, job['name'], active_build)
            if exec_name in jobs_on_executors:
                jobs_on_executors[exec_name].append({'name':job, 'number':active_build})
            else:
                jobs_on_executors[exec_name] = [{'name':job, 'number':active_build}]
        for computer in executors(host):
            ###if master then empty
            jobs_on_executor = []
            if computer['displayName'] in jobs_on_executors:
                jobs_on_executor = jobs_on_executors[computer['displayName']]
            elif 'master' == computer['displayName']:
                jobs_on_executor = jobs_on_executors['']
            result[computer['displayName']]= {'executors':computer['numExecutors'],'offline': computer['offline'], 'jobs_active':jobs_on_executor}
    return result


def build_queue_info():
    for item in queue(host):
        #'id' needed to cancel item -> http://localhost:8080/queue/cancelItem?id=5
        #'why' as popup
        #pprint(item['task']['name'])









pprint(build_executors_info())
#pprint(executors(host))
#build_queue_info()
