from flask import request, Response  # 서버 구현을 위한 Flask 객체 import
from database.model import Job
from flask_restx import Resource
from utils.executors import JobExecutor
from mongoengine.errors import (
    NotUniqueError,
    DoesNotExist, 
)
from resources.errors import (
    JobAlreadyExistsError,
    InternalServerError,
    UpdatingJobError,
    DeletingJobError,
    JobNotExistsError
)


class JobCreatView(Resource):
    """
    writer: 윤상민
    refactor: 양수영

    [GET] List Jobs
    [POST] Create Job
    """
    def get(self):
        jobs_json = Job.objects.to_json()
        return Response(f"{jobs_json}", status=200)

    def post(self):
        try:
            data = request.get_json()
            job_id = data['job_id']
            job = Job.objects(job_id=job_id).first()
            job_last = Job.objects.order_by('-job_id').first()

            if job is not None:
                return Response(f"job_id={job_id} is exist. {job_last['job_id']+1} or higher is recommended", status=400)
            Job(**data).save()
            return Response(f"job_id={job_id} created OK", status=200)
            
        except NotUniqueError:
            raise JobAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class JobRetrieveUpdateDeleteView(Resource):
    """
    writer: 윤상민
    refactor: 양수영

    [GET] Retrieve Job
    [PUT] Update Job
    [DELETE] Delete Job
    """
    def get(self, pk):
        try:
            job_json = Job.objects(job_id=pk).to_json()
            return Response(f"{job_json}", status=200)
        except DoesNotExist:
            raise JobNotExistsError
        except Exception as e:
            raise InternalServerError

    def put(self, pk):
        try:
            data = request.get_json()
            job = Job.objects.get(job_id=pk)
            job.update(**data)
            return Response(f"job_id={pk} Updated OK", status=200)
        except DoesNotExist:
            raise UpdatingJobError
        except Exception as e:
            raise InternalServerError

    def delete(self, pk):
        try:
            job = Job.objects.get(job_id=pk)
            job.delete()
            return Response(f"job_id={pk} deleted OK", status=200)
        except DoesNotExist:
            raise DeletingJobError
        except Exception as e:
            raise InternalServerError


class JobTaskView(Resource):
    """
    writer: 양수영
    
    [GET] Run Job
    """
    def get(self, pk):
        try:
            job = Job.objects.get(job_id=pk)
            executor = JobExecutor()
            executor.run(job)
            return Response(f"job_id={pk} run task Success", status=200)
        except DoesNotExist:
            raise JobNotExistsError
        except Exception as e:
            raise InternalServerError