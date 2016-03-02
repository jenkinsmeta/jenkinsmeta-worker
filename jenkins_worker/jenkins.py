from caller import ComputersInfo, ViewInfo, QueueInfo, ViewsInfo
from serializers import serialize_views, serialize_queue, serialize_view, serialize_computers, ProtoResponse


def computers(host):
    return serialize_computers(ComputersInfo(host).build())

def view(host, name):
    return serialize_view(ViewInfo(host, name).build())

def queue(host):
    return serialize_queue(QueueInfo(host).build())

def views(host):
    return serialize_views(ViewsInfo(host).build())


