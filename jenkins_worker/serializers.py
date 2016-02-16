from jenkinsmeta_pb2 import computers_pb2, queue_pb2, views_pb2, view_pb2
from flask_utils import ProtoResponse

def serialize_computers(computers):
    proto_computers = computers_pb2.Computers()
    for computer in computers:
        proto_computer = proto_computers.computer.add()
        proto_computer.name = computer
        proto_computer.executors = computers[computer]['executors']
        for job in computers[computer]['jobs_active']:
            proto_job = proto_computer.job.add()
            proto_job.state = job['state']
            proto_job.name = job['name']
            proto_job.build_number = int(job['number'])
            proto_job.url = job['url']
            if 'duration' in job:
                proto_job.duration = job['duration']
            if 'estimated_duration' in job:
                proto_job.estimated_duration = job['estimated_duration']
    return ProtoResponse(proto_computers)

def serialize_queue(queue):
    proto_queue = queue_pb2.Queue()
    for job in queue:
        proto_job = proto_queue.job.add()
        proto_job.name = job
        proto_job.url = queue[job]['url']
        proto_job.in_queue_since = queue[job]['in_queue_since']
        proto_job.id = queue[job]['id']
        if 'why' in queue[job]:
            proto_job.why = queue[job]['why']
        if 'blocked' in queue[job]:
            proto_job.blocked = bool(queue[job]['blocked'])
    return ProtoResponse(proto_queue)

def serialize_views(views):
    proto_views = views_pb2.Views()
    for view in views:
        proto_view = proto_views.view.add()
        proto_view.name = view
        proto_view.url = views[view]['url']
    return ProtoResponse(proto_views)

def serialize_view(view):
    proto_view = view_pb2.View()
    if 'description' in view:
        proto_view.description = view['description']
    proto_jobs = proto_view.jobs.add()
    for job in view['jobs']:
        proto_job = proto_jobs.job.add()
        proto_job.name = job
        proto_job.url = view['jobs'][job]['url']
        proto_job.state = view['jobs'][job]['state']
    return ProtoResponse(proto_view)



