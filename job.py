import json
import pandas as pd

class JobExecutor:
    def run(self, job_info):

        task_list = job_info['task_list']
        
        task_excutor = TaskExecutor()

        for task in task_list.keys():
            # WRAN
            print("Run Task:", task)
            task_fucntion = getattr(task_excutor, task.lower())
            task_fucntion(job_info)


class TaskExecutor:
    df = None

    def read(self, job):
        task = job['property']['read']
        self.df = pd.read_csv(task['filename'], delimiter=task['sep'])
        return self.df

    def drop(self, job):
        task = job['property']['drop']
        self.df = self.df.drop(task['column_name'], axis=1)
        return self.df

    def write(self, job):
        task = job['property']['write']
        self.df.to_csv(task['filename'], sep=task['sep'], index=False)
