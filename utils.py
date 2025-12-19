from datetime import datetime
from typing import List
import uuid

def convert_to_iso_datetime(time_string):
    """
    This method converts ISO string to datetime object.
    
    :param time_string: string time
    :rtype: datetime
    """
    return datetime.fromisoformat(time_string)

def is_valid_iso_string(time_string) -> bool:
    """
    This method checks if a string is a valid ISO formatted time string.
    
    :param time_string: string time
    :rtype: bool
    """
    try:
        dt = convert_to_iso_datetime(time_string)
        return True
    except:
        return False

def is_valid_status(status) -> bool:
    """
    This method checks if the status is valid.
    
    :param status: Status of the task.
    :rtype: bool
    """
    if status in ['done', 'running', 'failed', 'pending']:
        return True
    return False

def filter_tasks(start, end, status, tasks) -> List:
    """
    This method contains the logic to filter tasks based on status and the timeline of their creation.
    
    :param start: start of time window
    :param end: end of the time window
    :param status: status of the task
    :param tasks: current tasks-list containing tasks as dicts.
    :returns filtered_tasks: list of filtered tasks.
    :rtype: List
    """
    
    filtered_tasks = []
    for task in tasks:
        task_creation_time = convert_to_iso_datetime(task['created_at'])
        if (task['status'] == status and 
                start <= task_creation_time <= end        
            ):
            filtered_tasks.append(task)

    return filtered_tasks

def is_valid_uuid_v4(uuid_to_test):
    """
    This method checks if the id of the task is a valid UUID.
    
    :param uuid_to_test: task_id
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=4)
    except:
        return False
    return str(uuid_obj) == uuid_to_test

def clean_tasks(tasks: List) -> List:
    """
    This method cleans up the list of tasks by filtering out corrupt tasks or tasks with disallowed values.
    
    :param tasks: list of tasks
    :return: cleaned_tasks
    :rtype: List
    """
    cleaned_tasks = []
    name_set = set()
    id_set = set()
    
    for task in tasks:
        # cleaning corrupt, duplicate tasks
        if (is_valid_task(task) and 
                task['name'].strip().lower() not in name_set and 
                task['id'] not in id_set
            ):
            cleaned_tasks.append(task)
            name_set.add(task['name'].strip().lower())
            id_set.add(task['id'])
            
    return cleaned_tasks
        
def is_valid_task(task) -> bool:
    """
    This method validates a task by checking its contents.
    
    :param task: 
    :rtype: bool
    """
    # id check
    has_valid_uuid = is_valid_uuid_v4(task['id'])
    has_valid_name = True
    if task['name'].strip() == "":
        has_valid_name = False
    has_valid_status = is_valid_status(task['status'])
    has_valid_iso_timestamps = False
    if is_valid_iso_string(task['created_at']) and is_valid_iso_string(task['updated_at']):
        has_valid_iso_timestamps = True
        
    if (
        has_valid_uuid and
        has_valid_name and
        has_valid_status and
        has_valid_iso_timestamps
    ):
        return True
    
    return False
    

