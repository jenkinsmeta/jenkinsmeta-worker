import jenkins_worker

def get_api(request):
     api = request.headers.get('X-JenkinsMeta-API')
     if 'Jenkins' in api:
         return jenkins_worker




