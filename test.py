from unittest import TestCase
import os
import requests

"""
TEST API 목록
 - JobCreateListView ( GET, POST )
 - JobRetriveUpdateDeleteView ( GET, PUT, DELETE )
 - JobTaskView ( GET )

TEST 방법
 - flask run server 상태에서
 - 각각의 API에 requests 요청을 성공/실패케이스로 나누어서 시도.
 - 검증은 status_code를 확인하거나
 - Return되는 json의 value가 예상과 맞는지 AssertEqual 이용
"""


class JobCreatListView(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:5000/api/v1/jobs'
        self.initial_data = {
                            "job_id" : 100,
                            "job_name" : "Job1",
                            "task_list" : {
                                "read" : ["drop"], 
                                "drop" : ["write"], 
                                "write" : []
                            },
                            "property" : {
                                "read": {
                                    "task_name": "read", 
                                    "filename" : "data/a.csv", 
                                    "sep" :","
                                }, 
                                "drop" : {
                                    "task_name": "drop", 
                                    "column_name": "date"
                                }, 
                                "write" : {
                                    "task_name": "write", 
                                    "filename" : "data/b.csv", 
                                    "sep": ","
                                }
                            }
                        }
        r = requests.post(self.url, json=self.initial_data)

    def test_success_create(self):
        data = self.initial_data
        data['job_id'] = 110
        r = requests.post(self.url, json=data)
        self.assertEqual(r.status_code, 201)

    def test_success_list(self):
        r = requests.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_fail_create(self):
        data = self.initial_data
        data['job_id'] = 100
        r = requests.post(self.url, json=data)
        self.assertEqual(r.status_code, 400)


class JobRetriveUpdateDeleteView(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:5000/api/v1/jobs/100'
        self.initial_url = 'http://127.0.0.1:5000/api/v1/jobs'
        self.initial_data = {
                            "job_id" : 100,
                            "job_name" : "Job1",
                            "task_list" : {
                                "read" : ["drop"], 
                                "drop" : ["write"], 
                                "write" : []
                            },
                            "property" : {
                                "read": {
                                    "task_name": "read", 
                                    "filename" : "data/a.csv", 
                                    "sep" :","
                                }, 
                                "drop" : {
                                    "task_name": "drop", 
                                    "column_name": "date"
                                }, 
                                "write" : {
                                    "task_name": "write", 
                                    "filename" : "data/b.csv", 
                                    "sep": ","
                                }
                            }
                        }
        r = requests.post(self.initial_url, json=self.initial_data)

    def test_success_retrieve(self):
        r = requests.get(self.url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()[0]["job_id"], 100)
        self.assertEqual(r.json()[0]["job_name"], "Job1")
        self.assertEqual(r.json()[0]["task_list"], self.initial_data["task_list"])
        self.assertEqual(r.json()[0]["property"], self.initial_data["property"])

    def test_success_update(self):
        data = self.initial_data
        data.pop('job_id')
        data['job_name'] = "new_job"
        r = requests.put(self.url, json=data)
        self.assertEqual(r.status_code, 200)
        r2 = requests.get(self.url).json()
        self.assertEqual(r2[0]['job_name'], "new_job")

    def test_success_delete(self):
        r = requests.delete(self.url)
        self.assertEqual(r.status_code, 200)

    def test_fail_update(self):
        data = self.initial_data
        data.pop('job_id')
        data['job_name'] = "new_job"
        none_url = 'http://127.0.0.1:5000/api/v1/jobs/5555'
        r = requests.put(none_url, json=data)
        self.assertEqual(r.status_code, 404)

    def test_fail_delete(self):
        none_url = 'http://127.0.0.1:5000/api/v1/jobs/6666'
        r = requests.delete(none_url)
        self.assertEqual(r.status_code, 404)
        

class JobTaskView(TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:5000/api/v1/jobs/100/run'
        self.initial_url = 'http://127.0.0.1:5000/api/v1/jobs'
        self.initial_data = {
                            "job_id" : 100,
                            "job_name" : "Job1",
                            "task_list" : {
                                "read" : ["drop"], 
                                "drop" : ["write"], 
                                "write" : []
                            },
                            "property" : {
                                "read": {
                                    "task_name": "read", 
                                    "filename" : "data/a.csv", 
                                    "sep" :","
                                }, 
                                "drop" : {
                                    "task_name": "drop", 
                                    "column_name": "date"
                                }, 
                                "write" : {
                                    "task_name": "write", 
                                    "filename" : "data/b.csv", 
                                    "sep": ","
                                }
                            }
                        }
        r = requests.post(self.initial_url, json=self.initial_data)

    def test_success_task(self):
        r = requests.get(self.url)
        path_dir = './data/'
        self.assertEqual(r.status_code, 200)
        self.assertEqual(os.listdir(path_dir),['a.csv', 'b.csv'])
