import jenkins_worker

def get_api(api):
     if 'Jenkins' in api:
         return jenkins_worker

def parse_headers(headers):
    return headers.get('X-JenkinsMeta-API'), headers.get('X-JenkinsMeta-URL')

class APIFactory(object):
    def __init__(self, headers):
        api_type, self.url = parse_headers(headers)
        self.api = get_api(api_type)

    def computers(self):
        return self.api.computers(self.url)

    def queue(self):
        return self.api.queue(self.url)

    def views(self):
        return self.api.views(self.url)

    def view(self, name):
        return self.api.view(self.url, name)



