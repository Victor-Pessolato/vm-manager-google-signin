from googleapiclient.discovery import build

compute = build('compute', 'v1')
project = 'test-project-pessolato-251712'


def list_instances(zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def list_zones():
    result = compute.zones().list(project=project).execute()
    return result['items'] if 'items' in result else None


"""
def list_instances(project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None
"""
