from task_service import TaskService
from pathlib import Path
from datetime import datetime

def main():
    print('\n-------------------------------------------------------------------- TASK TRACKER CLI -----------------------------------------------------------------\n')
    file = Path(input('Enter the path for the tasks-file: '))
    file_path = file.name
    
    # Check for non existent or files other than JSON
    while not file.exists() or not file_path.endswith('.json'):
        print('\n----> Only existing JSON files are supported in this application.')
        file = Path(input('\nEnter the path for the tasks-file: '))
        file_path = file.name
  
    # Instance of Task Service
    Tasks = TaskService(file)
    
    while True:
        print("""\n
    1. Create a Task.
    2. Update status of a Task.
    3. List tasks, filter by status, start-time and end-time.
    4. Exit the application.
        \n""")
        
        option = input('Select one of the options above: ')

        # Validate the selected option
        while not option.isdigit() or option not in ['1', '2', '3', '4']:
            print('\nOption must be a number between 1 and 4 both inclusive.\n')
            option = input('Select one of the options above: ')
        
        option = int(option)
        
        # -------------- CREATE TASK ---------------
        if option == 1:
            task_name = input("\nEnter task name: ")
            try:
                Tasks.create_task(task_name)
                print('\n>-------------------- Task created successfully --------------------<\n')
            except Exception as e:
                print('\nError: ', e)

        # ------------- UPDATE STATUS --------------
        elif option == 2:
            task_id = input('\nEnter the task_id: ')
            new_status = input('\nEnter new status: \nPick from these options:\n1.running\n2.pending\n3.done\n4.failed\n\n ---- ')
            while new_status not in ['running', 'pending', 'done', 'failed']:
                print('\nStatus must be one of the given options.\n')
                new_status = input('\nEnter new status: \nPick from these options:\n1.running\n2.pending\n3.done\n4.failed\n\n ---- ')
        
            try:
                # update status and the tasks
                Tasks.update_task_status(task_id, new_status)
                print('\n>------------- Status Updated Successfully. ------------<')
            except Exception as e:
                print('\nError: ', e)
               
        # -------------- LIST TASKS ----------------
        elif option == 3:
            start_time = input('\nEnter start time: ')
            end_time = input('\nEnter end time: ')
            status = input('\nEnter status: ')
            
            try:
                filtered_tasks = Tasks.list_tasks(start_time, end_time, status)
                if len(filtered_tasks) > 0:
                    print('\n----------------------------------------------\n')
                    for task in filtered_tasks:
                        print(f"---> {task['name']}")
                    print('\n----------------------------------------------\n')
            except Exception as e:
                print('\nError: ', e)
        else:
            print('\n-------------------------------------------------------------------- TASK TRACKER CLI -----------------------------------------------------------------\n')
            break
        
if __name__ == "__main__":
    main()