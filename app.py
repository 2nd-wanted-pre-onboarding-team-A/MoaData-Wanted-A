# 첫 번째 Flask Server
from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask import request, Response
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from mongoengine import *

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
class JobCreatUpdateDeleteView(Resource):
    """
    작성자: 윤상민

    [POST] Create Job
    [PUT] Update Job
    [DELETE] Delete Job
    url의 pk를 사용하지 않고 입력값의 unique한 job_id로 자료를 컨트롤하기 때문에 CUD url을 한 곳에 두었습니다.
    """
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
        return Response(f"job_id={job_id}의 데이터가 생성되었습니다.", status=201)

    def put(self, pk):
        data = request.get_json()
        job_id = data['job_id']
        job = Job.objects(job_id=job_id).first()
        if job is None:
            return Response(f"Bad Request. job_id={job_id} Not Found", status=404)
        job.update(**data)
        return Response(f"job_id={job_id} Updated", status=200)

    def delete(self, pk):
        data = request.get_json()
        job_id = data['job_id']
        job = Job.objects(job_id=job_id).first()
        if job is None:
            return Response(f"Bad Request. job_id={job_id} Not Found", status=404)
        job.delete()
        return Response(f"job_id={job_id} Deleted", status=200)
        

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)