# 단비교육 백엔드 사전 과제
## 지원자 : 성 현

## 기능
1. 유저 로그인/로그아웃
로그인 : [POST] /users/login/
로그아웃 : [POST] /users/logout/
2. 매 주별 해야할 일의 등록 / 수정 / 삭제 / 조회 기능
등록 : [POST] /routines/create/
수정 : [PUT] /routines/update/
삭제 : [DELETE] /routines/delete/
전체조회 : [GET] /routines/get/list/
단일조회 : [GET] /routines/get/
3. 일정이 지난 후 진행한 할 일들에 대한 해결여부 기록
해결여부 : [PUT] /routines/solve/
