def task_document_path(instance, filename):
    project_id = instance.task.block.project.id
    task_id= instance.task.id
    return f'projects/{project_id}/{task_id}/{filename}'