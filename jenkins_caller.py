import requests
from config import host
from pprint import pprint

##Direct calls
class JenkinsCalls(object):
    def __init__(self, host):
        self.host=host
    def computers(self):
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


def get_job_state(color):
    if 'anime' in color:
        return '1'
    elif 'blue' == color:
        return '4'
    elif 'red' == color:
        return '3'
    elif 'aborted' == color:
        return '2'
    else:
        return '5'

#"builtOn" : "", from $job/$number/api/json could be used to determinate slave, -> if "" -> name=master
def build_computers_info(jc):
    jobs_on_computers={}
    result = {}
    for job in jc.jobs():
        for active_build in get_active_builds(job['name'], jc):
            computer_name = jc.get_executor_for_job(job['name'], active_build)
            build = jc.build(job['name'], active_build)
            build_info = {'number':active_build,
                    'estimated_duration': build['estimatedDuration'],
                    'duration': build['duration'],
                    'url': job['url'],
                    'name': job['name'],
                    'state': get_job_state(job['color'])
                    }
            if computer_name in jobs_on_computers:
                jobs_on_computers[computer_name].append(dict(build_info, **job))
            else:
                jobs_on_computers[computer_name] = [dict(build_info, **job)]
        for computer in jc.computers():
            ###if master then empty
            jobs_on_computer = []
            if computer['displayName'] in jobs_on_computers:
                jobs_on_computer = jobs_on_computers[computer['displayName']]
            elif 'master' == computer['displayName']:
                if '' in jobs_on_computers:
                    jobs_on_computer = jobs_on_computers['']
            result[computer['displayName']]= {'executors':computer['numExecutors'],'offline': computer['offline'], 'jobs_active':jobs_on_computer}
    return result


def build_queue_info():
    for item in jc.queue():
        #'id' needed to cancel item -> http://localhost:8080/queue/cancelItem?id=5
        #'why' as popup
        pprint(item['task']['name'])





def queue():
    jc = JenkinsCalls(host)
    print(jc.queue())
    return jc.queue()

def computers():
    jc = JenkinsCalls(host)
    return build_computers_info(jc)
#pprint(computers(host))
#build_queue_info()

if __name__ == '__main__':
    computers()
