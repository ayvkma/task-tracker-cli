import json
import uuid
from datetime import datetime 
from pathlib import Path
from typing import List

from utils import (
            filter_tasks, 
            clean_tasks, 
            is_valid_task, 
            is_valid_iso_string, 
            convert_to_iso_datetime, 
            is_valid_status
        )


class TaskService:
    """
    TaskService class provides methods to interact with tasks data:
        - creating new tasks
        - persist changes safely
        - updating status of a task
        - list tasks on basis of status, and specific time duration.
    """
    
    def __init__(self, file):
        self.file = file
        # loading tasks in-memory for faster access
        self.tasks = self.load_tasks()
        
    def load_tasks(self) -> List:
        """
        This method loads the json task data into a python list of task dicts.
        """
        if not self.file.exists():
            raise FileNotFoundError(f"\nFile path: {self.file.name} doesn't exist.\n")

        with open(self.file) as tasks_json:
            raw_tasks = json.load(tasks_json)
            if not isinstance(raw_tasks, list):
                raise TypeError('\nInvalid JSON File, not a list.\n')
            cleaned_tasks = clean_tasks(raw_tasks)
            self.tasks = cleaned_tasks
            return self.tasks
     
    def save_tasks(self) -> None: 
        """
        This method dumps the updated tasks and overwrites exising data in the json file.
        """   
        if not self.file.exists():
            raise FileNotFoundError(f"File path: {self.file.name} doesn't exist.")
        
        # create new json file
        old_file = self.file
        new_file = Path(f'{str(uuid.uuid4())}.json')
        with open(new_file, 'w') as tasks_json:
            json.dump(self.tasks, tasks_json, indent=4)
        new_file.replace(old_file)
        
            
    def create_task(self, task_name) -> None:
        """
        This method creates a task, adds it to exising tasks and the calls save_tasks() to overwrite the json file.
        
        :param task_name: The name of new task.
        """
        # check if task already exists
        for task in self.tasks:
            if task['name'].lower().strip() == task_name.lower().strip():
                raise ValueError('Task already exists.')
        
        task_id = str(uuid.uuid4())
        task_status = "running"
        task_creation_time = datetime.now().isoformat()
        task_updation_time = task_creation_time
        task = {
            'id': task_id,
            'name': task_name,
            'status': task_status,
            'created_at': task_creation_time,
            'updated_at': task_updation_time
        }
        
        # Task validation
        if not is_valid_task(task):
            raise ValueError('Invalid Task data.\n')
        
        self.tasks.append(task)
        self.save_tasks()
                    

    def list_tasks(self, start_time, end_time, status) -> List:
        """
        This method lists the tasks filtered on the basis of status and a timeline.
        
        :param start_time: start of the time window
        :param end_time: end of the time window
        :param status: status of the task
        :return: filtered_tasks
        :rtype: List
        """
            
        is_start_valid_iso = is_valid_iso_string(start_time)
        is_end_valid_iso = is_valid_iso_string(end_time)
        is_status_valid = is_valid_status(status)
        
        if not is_start_valid_iso:
            raise ValueError('Start time is not valid ISO String.\n')
        if not is_end_valid_iso:
            raise ValueError('End time is not valid ISO String.\n')
        if not is_status_valid:
            raise ValueError('Status must be from one of the given categories.\n')
        
        start = convert_to_iso_datetime(start_time) 
        end = convert_to_iso_datetime(end_time)
        
        filtered_tasks = filter_tasks(start, end, status, self.tasks)
        return filtered_tasks
        
    
    def update_task_status(self, task_id, new_status) -> None:        
        if is_valid_status(new_status):
            for task in self.tasks:
                if task['id'] == task_id:
                    if task['status'] == new_status:
                        raise ValueError(f'Status is already set to: {new_status}.')
                    task['status'] = new_status
                    task['updated_at'] = datetime.now().isoformat()
                    self.save_tasks()
                    return
        else:
            raise ValueError(f'Status: {new_status} is not valid.')
        raise ValueError(f'Task Not Found with Id: {task_id}')
                