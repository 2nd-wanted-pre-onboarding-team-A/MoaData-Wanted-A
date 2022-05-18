# 원티드 프리온보딩 백엔드 프로젝트 4

<br>

<img width=831 src="https://user-images.githubusercontent.com/74187642/168935905-335b7bcc-6a81-44ae-b82e-4810ad675362.jpg">



<br>

## 목차

- [팀 구성](#팀구성)
- [기술스택](#기술스택)
- [프로젝트 진행과정](#프로젝트-진행과정)
- [DFD](#-DFD)
- [API 명세서](#-API-명세서)
- [프로그램 설치 및 테스트방법](#프로그램-설치-및-테스트방법)

<br>

<br>

## 팀구성

- **[양수영](https://github.com/tasddc1226)**
- **[권은경](https://github.com/fore0919)** - 조기취업으로 이번 과제 미참여
- **[윤상민](https://github.com/redtea89)**

<br>

## 기술스택

<img src="https://img.shields.io/badge/python-3.8.10-green">  <img src="https://img.shields.io/badge/flask-2.1.2-red">   <img src="https://img.shields.io/badge/mongodb-5.0.7-black">

<img src="https://img.shields.io/badge/pandas-1.4.2-blue">  <img src="https://img.shields.io/badge/mongoengine-0.24.1-blue">



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

### Job Save
- `Tag: 1.0.0` : Client는 Job 정보를 Server에게 전송
- `Tag: 1.1.0` : Server는 받은 정보를 job.json(mongodb)에 저장

<br>

### Job Delete
- `Tag: 2.0.0` : Client는 특정 Job정보를 삭제하기 위해 job id를 서버로 전송
- `Tag: 2.1.0` : Server는 받아온 job id에 해당하는 job 정보를 삭제

<br>

### Job Modify
- `Tag: 3.0.0` : Client는 특정 Job정보를 수정하기 위해 job id를 서버로 전송
- `Tag: 3.1.0` : Server는 받아온 job id에 해당하는 job 정보를 수정

<br>

### Job Run
- `Tag: 4.0.0` : Client는 특정 Job을 실행하기 위해 job id를 서버로 전송
- `Tag: 4.1.0` : Server는 받아온 job id에 해당하는 job list를 얻음
  - `Tag: 4.1.1` : read task를 수행을 위해 특정 file에 접근
  - `Tag: 4.1.2` : file의 값을 얻어 pandas의 DataFrame으로 전달
- `Tag: 4.2.0` : 특정 column_name을 제외하여 DataFrame으로 전달
- `Tag: 4.3.0` : 전달받은 데이터를 새로운 file로 저장 및 Client에게 전달

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

    ```json
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



<br>

<br>

## 프로그램 설치 및 테스트방법

> MAC OS 기준으로 설명되었습니다.
>
> Python=3.8 이상, 그리고 MongoDB가 로컬에 설치되어 있다고 가정하고 작성하였습니다.
>
> [파이썬 설치 링크](https://www.python.org/downloads/),  [MongoDB 설치 링크](https://www.mongodb.com/try/download/community)

<br>

#### 1. 깃을 내려받는다.

```bash
% git clone https://github.com/2nd-wanted-pre-onboarding-team-A/MoaData-Wanted-A.git
```

#### <br>2. 디렉터리 변경

```bash
% cd MoaData-Wanted-A
```

#### <br>3. 가상환경생성 및 진입

```bash
% python -m venv venv
```

```bash
% source venv/bin/activate
```

#### <br>4. 모듈 설치

```bash
% pip install --upgrade pip
```

```bash
% pip install -r requirements.txt
```

#### <br>5. flask 서버 실행 

```bash
% flask run
```

###### 서버실행 후 같은 위치에 터미널을 하나 더 생성하고 파이썬 가상환경에 진입한다. 

<br>

#### 6. 테스트케이스 실행

```bash
% python -m unittest test.py
```

<img width="654" alt="image" src="https://user-images.githubusercontent.com/74187642/168972491-4c1dee8b-8cee-4b86-a136-2567fd8525f6.png">



#### <br>7. API GET으로 자료 요청 확인

```bash
% curl http://127.0.0.1:5000/api/v1/jobs
```

<img width="654" alt="image" src="https://user-images.githubusercontent.com/74187642/168972261-691903b2-b195-4763-ab08-8e3f052b78a7.png">