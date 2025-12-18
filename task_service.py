import json
import uuid
from datetime import datetime 
from pathlib import Path

from utils import filter_tasks


class TaskService:
    """
    TaskService class provides methods to interact with tasks data:
        - creating new tasks
        - updating status of a task
        - list tasks on basis of status, and specific time duration.
    """
    
    def __init__(self, file):
        self.file = file
        
    def load_tasks(self):
        """
        This method loads the json task data into a python list of task dicts.
        """
        if not self.file.exists():
            print("\nFile path doesn't exist.\n")
            return
        try:
            with open(self.file.name) as tasks_json:
                tasks = json.load(tasks_json)
                return tasks
        except Exception as e:
            print('\nError reading json file\n', e)
        
    def save_tasks(self, updated_tasks): 
        """
        This method dumps the updated tasks and overwrites exising data in the json file.
        
        :param updated_tasks: It is the updated version of list of task dicts.
        """   
        if not self.file.exists():
            print(f"File path: {self.file.name} doesn't exist.")
            return
        try:
            # create new json file
            new_file = Path('_tasks.json')
            with open(new_file.name, 'w') as tasks_json:
                json.dump(updated_tasks, tasks_json, indent=4)
            # delete old json file
            self.file.unlink()
            # rename the newly created json file
            new_file.rename('tasks.json')
        except Exception as e:
            print('\nError updating json file.\n')
            
    def create_task(self, task_name):
        """
        This method creates a task, adds it to exising tasks and the calls save_tasks() to overwrite the json file.
        
        :param task_name: The name of new task.
        """
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
        
        curr_tasks = self.load_tasks()
        curr_tasks.append(task)
        self.save_tasks(curr_tasks)
                    

    def list_tasks(self, start_time, end_time, status):
        """
        This method lists the tasks filtered on the basis of status and a timeline.
        
        :param start_time: start of the time window
        :param end_time: end of the time window
        :param status: status of the task
        """
        try:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
        except Exception as e:
            print('\nStart or End times are not in datetime format\n', e)
            return
        tasks = self.load_tasks()
        filtered_tasks = filter_tasks(start, end, status, tasks)
        print('\n----------------------------------------\n')
        for task in filtered_tasks:
            print(f"---> {task['name']}\n")
        print('----------------------------------------')

