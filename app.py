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
class JobCreatView(Resource):
    """
    [POST] Create Job
    """
    def post(self):
        data = request.get_json()
        job_id = data['job_id']
        try:
            Job(**data).save()
        except:
            # 몽고 ORM에서 뿜뿜하는 Validation조건을 아래에서 Raise할 수 있으면 좋겠음. 
            return Response("입력조건 에러", status=400)
        return Response(f"job_id={job_id}의 데이터가 생성되었습니다.", status=201)


@api.route('/api/v1/jobs/<int:pk>')
class JobUpdateDeleteView(Resource):
    """
    [PUT] Update Job
    [DELETE] Delete Job
    """
    def put(self, pk):
        data = request.get_json()
        job = Job.objects(job_id=pk).first()
        if job is None:
            return Response(f"job_id={pk}에 해당하는 job이 없습니다.", status=400)
        job.update(**data)
        return Response(f"job_id={pk}가 업데이트되었습니다.", status=200)

    def delete(self, pk):
        job = Job.objects(job_id=pk).first()
        if job is None:
            return Response(f"job_id={pk}에 해당하는 job이 없습니다.", status=400)
        job.delete()
        return Response(f"job_id={pk}데이터 삭제 완료.")
        

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)