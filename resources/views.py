from flask import request, Response  # 서버 구현을 위한 Flask 객체 import
from database.model import Job
from flask_restx import Resource
from job import JobExecutor

class JobCreatView(Resource):
    """
    작성자: 윤상민
    
    [GET] List Jobs
    [POST] Create Job
    """
    def get(self):
        jobs_json = Job.objects.to_json()
        return Response(f"{jobs_json}", status=200)

    def post(self):
        data = request.get_json()
        job_id = data['job_id']
        job = Job.objects(job_id=job_id).first()
        job_last = Job.objects.order_by('-job_id').first()
        if job is not None:
            return Response(f"job_id={job_id} is exist. {job_last['job_id']+1} or higher is recommended", status=400)
        try:
            Job(**data).save()
        except:
            return Response("Bad Request", status=400)
        return Response(f"job_id={job_id} created OK", status=201)


class JobRetrieveUpdateDeleteView(Resource):
    """
    작성자: 윤상민

    [GET] Retrieve Job
    [PUT] Update Job
    [DELETE] Delete Job
    """
    def get(self, pk):
        job_json = Job.objects(job_id=pk).to_json()
        return Response(f"{job_json}", status=200)

    def put(self, pk):
        data = request.get_json()
        job = Job.objects(job_id=pk).first()
        if job is None:
            return Response(f"Bad Request. job_id={pk} Not Found", status=404)
        try:
            job.update(**data)
        except:
            return Response("Bad Request.", status=400)
        return Response(f"job_id={pk} Updated OK", status=200)

    def delete(self, pk):
        job = Job.objects(job_id=pk).first()
        if job is None:
            return Response(f"Bad Request. job_id={pk} Not Found", status=404)
        job.delete()
        return Response(f"job_id={pk} deleted OK")


class JobTaskView(Resource):
    """
    작성자: 양수영
    
    [GET] Run Job
    """
    def get(self, pk):
        job = Job.objects(job_id=pk).first()
        if job is None:
            return Response(f"Bad Request. job_id={pk} Not Found", status=404)
        executor = JobExecutor()
        executor.run(job)
        return Response(f"job_id={pk} run task Success", status=200)