import json
import pandas as pd
import collections
from utils.topology_sort import topology_sort

class JobExecutor:
    def run(self, job_info):

        task_list= job_info['task_list']
        
        task_queue = collections.deque(topology_sort(task_list))
        task_excutor = TaskExecutor()

        while task_queue:
            task = task_queue.popleft()
            task_func = getattr(task_excutor, task.lower())
            task_func(job_info)


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
