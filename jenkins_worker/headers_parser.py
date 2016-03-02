
def parse_headers(headers):
    return { 'url': headers.get('X-JenkinsMeta-URL')
            'api': headers.get('X-JenkinsMeta-API') }

