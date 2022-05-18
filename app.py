# 첫 번째 Flask Server
from flask import Flask # 서버 구현을 위한 Flask 객체 import
from flask_restful import Api  # Api 구현을 위한 Api 객체 import
from database.db import initialize_db
from resources.routes import initialize_routes
from resources.errors import errors

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app, errors=errors)  # Flask 객체에 Api 객체 등록

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)