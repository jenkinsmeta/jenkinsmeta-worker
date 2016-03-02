[![Build Status](https://travis-ci.org/jenkinsmeta/jenkinsmeta-worker.svg?branch=master)](https://travis-ci.org/jenkinsmeta/jenkinsmeta-worker)
# jenkinsmeta-worker

This component provides common API for jenkinsmeta-server by parsing and crunching CI API.


Example call for testing:
curl -H "X-JenkinsMeta-URL: localhost:8080" -H "X-JenkinsMeta-API: Jenkins" http://127.0.0.1:5000/computers -X GET
Normally, the calls are produced by jenkinsmeta-server.
