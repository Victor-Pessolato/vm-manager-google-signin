from googleapiclient.discovery import build

compute = build('compute', 'v1')
project = 'test-project-pessolato-251712'


def list_instances(zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def list_zones():
    result = compute.zones().list(project=project).execute()
    return result['items'] if 'items' in result else None


def start_vm(zone, vm):
    result = compute.instances().start(
        project=project, zone=zone, instance=vm).execute()
    return result


def stop_vm(zone, vm):
    result = compute.instances().stop(
        project=project, zone=zone, instance=vm).execute()
    return result


def get_op(zone, operation):
    result = compute.zoneOperations().get(
        project=project, zone=zone, operation=operation).execute()
    return result
