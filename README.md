# 단비교육 백엔드 사전 과제
- 지원자 : 성 현
<br>
<br>

## 1. 기능

### 1-1. 유저 로그인/로그아웃
- 로그인 : [POST] /users/login/<br>
- 로그아웃 : [POST] /users/logout/<br>
<br>

### 1-2. 매 주별 해야할 일의 등록 / 수정 / 삭제 / 조회 기능
- 등록 : [POST] /routines/create/<br>
- 수정 : [PUT] /routines/update/<br>
- 삭제 : [DELETE] /routines/delete/<br>
- 전체조회 : [GET] /routines/get/list/<br>
- 단일조회 : [GET] /routines/get/<br>
<br>

### 1-3. 일정이 지난 후 진행한 할 일들에 대한 해결여부 기록
- 해결여부 : [PUT] /routines/solve/<br>

<br>
<br>

## 2. 서버 실행방법
### 2-1. 가상환경 설치 및 실행
```python
python -m venv myvenv
source myvenv/Scripts/activate
```
<br>

### 2-2. 패키지 설치
```python
pip install -r requirements.txt
```
<br>

### 2-3. 로컬 서버 실행
```python
cd danbiedu_assignment/assignment
python manage.py runserver
```

<br>
<br>

## 3. 테스트 코드 실행 방법
### 3-1. 테스트 코드 실행
```python
cd danbiedu_assignment/assignment
python manage.py test
```
<br>



