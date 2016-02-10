import requests
from config import host
from pprint import pprint

##Direct calls
class JenkinsCalls(object):
    def __init__(self, host):
        self.host=host
    def executors(self):
        return requests.get('http://'+self.host+'/computer/api/json').json()['computer']

    def queue(self):
        return requests.get('http://'+self.host+'/queue/api/json').json()['items']

    def views(self):
        return requests.get('http://'+self.host+'/api/json').json()['views']

    def jobs(self):
        return requests.get('http://'+self.host+'/api/json').json()['jobs']

    def job(self, job):
        return requests.get('http://'+self.host+'/job/'+job+'/api/json').json()

    def get_executor_for_job(self, job, number):
        return requests.get('http://'+self.host+'/job/'+job+'/'+number+'/api/json').json()['builtOn']

    def build_is_building(self, job, number):
        return requests.get('http://'+self.host+'/job/'+job+'/'+str(number)+'/api/json').json()['building']

    def build(self, job, number):
        return requests.get('http://'+self.host+'/job/'+job+'/'+str(number)+'/api/json').json()




def get_active_builds(job_name, jc):
    ##TODO, Jenkins api does not provide information about all active execution of specific build, this needs to be reimplemented
    active_builds= []
    response = jc.job(job_name)
    last_build = response['lastBuild']['number']
    scenarios = []
    for scenario in ["lastBuild", "lastCompletedBuild", "lastStableBuild", "lastSuccessfulBuild", "lastUnstableBuild", "lastUnsuccessfulBuild"]:
        try:
            scenarios.append(response[scenario]['number'])
        except TypeError:
            #debug
            print('Job '+job_name+' does not contain: '+scenario)
    if not scenarios:
        print('We are fallbacking')
        scenarios.append('1')
    lower_limit = min(scenarios)
    for number in range(last_build, lower_limit,-1):
        #TODO: in range, when last build is the same as lower limit, it does not work
        if jc.build_is_building(job_name, number):
            active_builds.append(str(number))
    return active_builds



#TODO:  "builtOn" : "", from $job/$number/api/json could be used to determinate slave
def build_executors_info(jc):
    jobs_on_executors={}
    result = {}
    for job in jc.jobs():
        for active_build in get_active_builds(job['name'], jc):
            exec_name = jc.get_executor_for_job(job['name'], active_build)
            #TODO: this might be optimized by using one call and taking each node to the dictionary
            build_info = {'number':active_build, 
                    'estimated_duration': jc.build(job['name'], active_build)['estimatedDuration'],
                    'duration': jc.build(job['name'], active_build)['duration']
                    }
            if exec_name in jobs_on_executors:
                jobs_on_executors[exec_name].append(dict(build_info, **job))
            else:
                jobs_on_executors[exec_name] = [dict(build_info, **job)]
        for computer in jc.executors():
            ###if master then empty
            jobs_on_executor = []
            if computer['displayName'] in jobs_on_executors:
                jobs_on_executor = jobs_on_executors[computer['displayName']]
            elif 'master' == computer['displayName']:
                if '' in jobs_on_executors:
                    jobs_on_executor = jobs_on_executors['']
            result[computer['displayName']]= {'executors':computer['numExecutors'],'offline': computer['offline'], 'jobs_active':jobs_on_executor}
    return result


def build_queue_info():
    for item in jc.queue():
        #'id' needed to cancel item -> http://localhost:8080/queue/cancelItem?id=5
        #'why' as popup
        pprint(item['task']['name'])







def executors():
    jc = JenkinsCalls(host)

    return build_executors_info(jc)
#pprint(executors(host))
#build_queue_info()

if __name__ == '__main__':
    executors()