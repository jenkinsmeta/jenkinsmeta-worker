import requests
from config import host


##Direct calls
class JenkinsCalls(object):
    def __init__(self, host):
        self.host=host

    def queue(self):
        return requests.get('http://'+self.host+'/queue/api/json').json()['items']

    def views(self):
        return requests.get('http://'+self.host+'/api/json?tree=views[name,url]').json()['views']

    def view(self, view):
        return requests.get('http://'+self.host+'/view/'+view+'/api/json').json()

    def active_jobs_on_computes(self):
        return requests.get('http://'+self.host+'/computer/api/json?tree=computer[executors[currentExecutable[url]],displayName,numExecutors,offline]').json()['computer']

def build_info(url):
    return requests.get(url+'api/json?tree=actions[causes[shortDescription]],duration,estimatedDuration,url,number,fullDisplayName,building').json()

def get_job_state(color):
    if 'anime' in color:
        return 1
    elif 'aborted' == color:
        return 2
    elif 'red' == color:
        return 3
    elif 'blue' == color:
        return 4
    else:
        return 5


def extract_build_info(jobs_active, job_url):
    build = build_info(job_url)
    jobs_active.append({
        'number':build['number'],
        'estimated_duration': build['estimatedDuration'],
        'duration': build['duration'],
        'url': build['url'],
        'name': build['fullDisplayName'].split('#')[0].strip(),
        'state': int(build['building'])
        })

class BuildsActiveOnComputer(object):
    def __init__(self, computer):
        self.computer = computer
        self.jobs_active = []

    def builds_active(self):
        for job in self.computer['executors']:
           if job['currentExecutable']:
               self.extract_builds_active(job['currentExecutable']['url'])
        return self.jobs_active

    def extract_builds_active(self, job_url):
        build = build_info(job_url)
        self.jobs_active.append({
            'number':build['number'],
            'estimated_duration': build['estimatedDuration'],
            'duration': build['duration'],
            'url': build['url'],
            'name': build['fullDisplayName'].split('#')[0].strip(),
            'state': int(build['building'])
            })

def build_computers_info(jc):
    result = {}
    for computer in jc.active_jobs_on_computes():
        jobs_active = []
        for job in computer['executors']:
            if job['currentExecutable']:
                extract_build_info(jobs_active, job['currentExecutable']['url'])
        result[computer['displayName']] = {
                'executors': computer['numExecutors'],
                'offline': computer['offline'],
                'jobs_active': jobs_active}
    return result





class Computers(object):
    def __init__(self, host):
        self.host = host
        self.jc = JenkinsCalls(host)
        self.result = {}
    def build_computers_info(self):
        #jobs_active is confusing, should be builds_active
        for computer in self.jc.active_jobs_on_computes():
            self.result[computer['displayName']] = {
                'jobs_active': BuildsActiveOnComputer(computer).builds_active(),
                'executors': computer['numExecutors'],
                'offline': computer['offline']
                }
        return self.result

def computers():
    return Computers(host).build_computers_info()

####

def build_queue_info(jc):
    result = {}
    for item in jc.queue():
        result[item['task']['name']] = {
                'in_queue_since': item['inQueueSince'],
                'why': item['why'],
                'blocked': item['blocked'],
                'id': item['id'],
                'url': item['task']['url']
            }
    return result

def views_info(jc):
    result = {}
    for view in jc.views():
        result[view['name']] = {'url':view['url']}
    return result



####
def view_info(jc, name):
    result = {}
    view = jc.view(name)
    result['description']= str(view['description'])
    result['jobs'] = {}
    for job in view['jobs']:
        result_job = {}
        result_job['url'] = job['url']
        result_job['state'] = get_job_state(job['color'])
        result['jobs'][job['name']] = result_job
    return result


####

def queue():
    jc = JenkinsCalls(host)
    return build_queue_info(jc)



def _computers():
    jc = JenkinsCalls(host)
    return build_computers_info(jc)

def views():
    jc = JenkinsCalls(host)
    return views_info(jc)

def view(name):
    jc = JenkinsCalls(host)
    return view_info(jc, name)
