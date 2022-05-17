# 첫 번째 Flask Server
from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask import request, Response
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from mongoengine import *

from job import JobExecutor

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록
connect('moa')  # MongoDB Connector


class Job(Document):
    """
    몽고DB ORM
    """
    job_id = IntField(required=True, unique=True)
    job_name = StringField(required=True)
    task_list = DictField()
    property = DictField()

@api.route('/api/v1/jobs')
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


@api.route('/api/v1/jobs/<int:pk>')
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
        job.update(**data)
        return Response(f"job_id={pk} Updated OK", status=200)

    def delete(self, pk):
        job = Job.objects(job_id=pk).first()
        if job is None:
            return Response(f"Bad Request. job_id={pk} Not Found", status=404)
        job.delete()
        return Response(f"job_id={pk} deleted OK")

@api.route('/api/v1/jobs/<int:pk>/run')
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
        

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)