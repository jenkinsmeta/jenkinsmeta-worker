import requests


##Direct calls
class JenkinsCalls(object):
    def __init__(self, hostname):
        self.host = hostname

    def queue(self):
        return requests.get('http://'+self.host+'/queue/api/json').json()['items']

    def views(self):
        return requests.get('http://'+self.host+'/api/json?tree=views[name,url]').json()['views']

    def view(self, view):
        return requests.get('http://'+self.host+'/view/'+view+'/api/json').json()

    def active_jobs_on_computers(self):
        return requests.get('http://'+self.host+'/computer/api/json?tree=computer[executors[currentExecutable[url]],displayName,numExecutors,offline]').json()['computer']


### Computers
def build_info(url):
    return requests.get(url+'api/json?tree=actions[causes[shortDescription]],duration,estimatedDuration,url,number,fullDisplayName,building').json()

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
        #TODO: state should be building or not? or maybe it is not needed?
        build = build_info(job_url)
        self.jobs_active.append({
            'number':build['number'],
            'estimated_duration': build['estimatedDuration'],
            'duration': build['duration'],
            'url': build['url'],
            'name': build['fullDisplayName'].split('#')[0].strip(),
            'state': int(build['building'])
            })

class ComputersInfo(object):
    #TODO: jobs_active key is confusing, should be builds_active
    def __init__(self, host):
        self.jc = JenkinsCalls(host)
        self.result = {}
    def build(self):
        for computer in self.jc.active_jobs_on_computers():
            self.result[computer['displayName']] = {
                'jobs_active': BuildsActiveOnComputer(computer).builds_active(),
                'executors': computer['numExecutors'],
                'offline': computer['offline']
                }
        return self.result



#### View
def get_job_state(color):
    if 'anime' in color:
        return 1
    elif color == 'aborted':
        return 2
    elif color == 'red':
        return 3
    elif color == 'blue':
        return 4
    else:
        return 5

class JobsInView(object):
    def __init__(self, view):
        self.result = {}
        self.view = view
    def build(self):
        for job in self.view['jobs']:
            self.result[job['name']] = {
            'state': get_job_state(job['color']),
            'url': job['url']}
        return self.result

class ViewInfo(object):
    def __init__(self, host, name):
        self.jc = JenkinsCalls(host)
        self.name = name
        self.result = {}

    def set_description(self, view):
        if 'description' in view and view['description']:
            self.result['description'] = view['description']

    def build(self):
        view = self.jc.view(self.name)
        self.set_description(view)
        self.result['jobs'] = JobsInView(view).build()
        print self.result
        return self.result



#### Queue

class QueueInfo(object):
    def __init__(self, host):
        self.jc = JenkinsCalls(host)
        self.result = {}
    def build(self):
        for item in self.jc.queue():
            self.result[item['task']['name']] = {
                'in_queue_since': item['inQueueSince'],
                'why': item['why'],
                'blocked': item['blocked'],
                'id': item['id'],
                'url': item['task']['url']
                }
        return self.result



#### Views

class ViewsInfo(object):
    def __init__(self, host):
        self.jc = JenkinsCalls(host)
        self.result = {}
    def build(self):
        for view in self.jc.views():
            self.result[view['name']] = {'url':view['url']}
        return self.result



