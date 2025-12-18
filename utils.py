from datetime import datetime
from typing import List

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
    try:
        for task in tasks:
            task_creation_time = datetime.fromisoformat(task['created_at'])
            if (task['status'] == status and 
                    start <= task_creation_time <= end        
                ):
                filtered_tasks.append(task)
    except Exception as e:
        print('\nTask creation time is not in ISO format.\n')
        return []
    
    return filtered_tasks
