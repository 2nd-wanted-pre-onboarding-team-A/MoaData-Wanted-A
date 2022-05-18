from mongoengine import *

class Job(Document):
    """
    몽고DB ORM
    """
    job_id = IntField(required=True, unique=True)
    job_name = StringField(required=True)
    task_list = DictField()
    property = DictField()