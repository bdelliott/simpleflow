import swf.models

from simpleflow.swf.executor import Executor
from . import (
    Decider,
    DeciderPoller,
)


def load_workflow(domain, workflow_name, task_list=None, **kwargs):
    module_name, object_name = workflow_name.rsplit('.', 1)
    module = __import__(module_name, fromlist=['*'])

    workflow = getattr(module, object_name)
    return Executor(swf.models.Domain(domain), workflow, task_list, **kwargs)


def make_decider_poller(workflows, domain, task_list, repair_with=None, **kwargs):
    """
    Factory to build a decider.

    """
    if repair_with and len(workflows) != 1:
        # too complicated ; I even wonder why passing multiple workflows here is
        # useful, a domain+task_list is typically handled in a single workflow
        # definition, seems like good practice (?)
        raise ValueError("Sorry you can't repair more than 1 workflow at once!")

    executors = [
        load_workflow(domain, workflow, task_list, repair_with=repair_with, **kwargs)
        for workflow in workflows
    ]
    domain = swf.models.Domain(domain)
    return DeciderPoller(executors, domain, task_list)


def make_decider(workflows, domain, task_list, nb_children=None, **kwargs):
    poller = make_decider_poller(workflows, domain, task_list, **kwargs)
    return Decider(poller, nb_children=nb_children)
