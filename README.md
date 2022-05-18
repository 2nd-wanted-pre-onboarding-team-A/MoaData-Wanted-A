# 원티드 프리온보딩 백엔드 프로젝트 4

<br>

<img width=831 src="https://user-images.githubusercontent.com/74187642/168935905-335b7bcc-6a81-44ae-b82e-4810ad675362.jpg">



<br>

## 목차

- [팀 구성](#-팀구성)
- [기술스택](#-기술스택)
- [프로젝트 진행과정](#-프로젝트-진행과정)
- [DFD](#-DFD)
- [API 명세서](#-API-명세서)

<br>

<br>

## 팀구성

- **[양수영](https://github.com/tasddc1226)**
- **[권은경](https://github.com/fore0919)** - 조기취업으로 이번 과제 미참여
- **[윤상민](https://github.com/redtea89)**

<br>

## 기술스택

<img src="https://img.shields.io/badge/python-3.8.10-green"><img src="https://img.shields.io/badge/flask-2.1.2-red"><img src="https://img.shields.io/badge/mongodb-5.0.7-black">

<img src="https://img.shields.io/badge/pandas-1.4.2-blue"><img src="https://img.shields.io/badge/mongoengine-0.24.1-blue">



<br>

<br>

## 프로젝트 진행과정

- Notion과 Git branch를 연동하여 작업 진행 ([Notion 링크](https://www.notion.so/dd9e9b0d64e24eddb78515620075f933))

<img width="1157" alt="image" src="https://user-images.githubusercontent.com/74187642/168936506-b1b399b8-b624-47c0-9f8d-f9f999963a00.png">

<img width="1130" alt="image" src="https://user-images.githubusercontent.com/74187642/168937357-b39bf6aa-cb6e-43e1-9046-abb2c122687e.png">



<br>

## ✎ DFD

<img width="853" alt="Screen Shot 2022-05-17 at 14 30 07" src="https://user-images.githubusercontent.com/55699007/168735949-770e1b8e-c6a9-4c80-a569-aa05873d13b2.png">



<br>

<br>

## 📝 API 명세서

#### Job 실행 : `api/v1/jobs/<int:pk>/run`

- `GET` `/api/v1/jobs/1/run` 

  - 요청 Body

    ```
    None
    ```

  - server 응답

    ```json
    "job_id=1 run task Success"
    ```

  - 결과
    - task_list의 작업(예를들면 read -> drop -> write)이 진행된다. 
    - a.csv파일 수정의 결과값인 b.csv파일이 생성된다. 

<br>

#### Job 저장 및 리스트 : `api/v1/jobs`

- `POST` `/api/v1/jobs` 

  - 요청 Body

    ```json
    {
    	"job_id" : 1,
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
    ```

  - server 응답

    ```json
    "job_id=1 created OK"
    ```

<br>

- `GET  ` `/api/v1/jobs` 

  - 요청 Body

    ```
    None
    ```

  - Server 응답

    ```
    [
    	{
    		"_id": {
    			"$oid": "6283915c6e955720caac4535"
    		},
    		"job_id": 1,
    		"job_name": "Job1",
    		"task_list": {
    			"read": [
    				"drop"
    			],
    			"drop": [
    				"write"
    			],
    			"write": []
    		},
    		"property": {
    			"read": {
    				"task_name": "read",
    				"filename": "data/a.csv",
    				"sep": ","
    			},
    			"drop": {
    				"task_name": "drop",
    				"column_name": "date"
    			},
    			"write": {
    				"task_name": "write",
    				"filename": "data/b.csv",
    				"sep": ","
    			}
    		}
    	},
      
      ,
      (중간생략)
    	,
    ]
    ```



<br>

#### Job 수정, 삭제 및 상세보기 `api/v1/jobs/<int:pk>`

- `DELETE `  `/api/v1/jobs/1` 

  - 요청 Body

    ```
    None
    ```

  - Server 응답

    ```json
    "job_id=1 deleted OK"
    ```



<br>

- `PUT ` `/api/v1/jobs/1` 

  - 요청 Body

    ```
    {
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
    ```

  - Server 응답

    ```json
    "job_id=1 Updated OK"
    ```



<br>

- `GET` `/api/v1/jobs/1` 

  - 요청 Body

    ```
    None
    ```

  - Server 응답

    ```json
    [
    	{
    		"_id": {
    			"$oid": "62844f8bbade6a84942682b9"
    		},
    		"job_id": 1,
    		"job_name": "Job1",
    		"task_list": {
    			"read": [
    				"drop"
    			],
    			"drop": [
    				"write"
    			],
    			"write": []
    		},
    		"property": {
    			"read": {
    				"task_name": "read",
    				"filename": "data/a.csv",
    				"sep": ","
    			},
    			"drop": {
    				"task_name": "drop",
    				"column_name": "date"
    			},
    			"write": {
    				"task_name": "write",
    				"filename": "data/b.csv",
    				"sep": ","
    			}
    		}
    	}
    ]
    ```



