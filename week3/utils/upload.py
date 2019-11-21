import os
import shutil
from datetime import datetime
def task_document_path(instance, filename):
    project_id = instance.task.block.project.id
    task_id= instance.task.id
    return f'projects/{project_id}/{task_id}/{filename}'



def task_delete_path(document):
    print(document)
    task_path = os.path.abspath(os.path.join(document.path, '..'))
    shutil.rmtree(task_path)