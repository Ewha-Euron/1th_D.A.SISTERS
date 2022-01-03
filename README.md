# 1th_D.A.SISTERS

## django 구축
### vscode 가상환경 생성
`python -m venv venv`

(ctrl+shift+p)
select interpreter    
생성한 가상환경 선택 후 터미널 확인

### django 설치
`python -m pip install django`

### django 프로젝트 생성
`django-admin startproject DAsisters .`

### django 서버 실행
`python manage.py runserver`

### app 생성
`python manage.py startapp WNrecomm`    
생성 후 settings.py에 등록

## github와 연결할 때
### 가상환경 키기

### 레포지토리 가져오기
`git clone [레포 경로]`

### 일단 무조건 풀하고 시작
`git pull`

### 브랜치 생성 (절대 master에서 작업시작XX)
`git branch [브랜치 이름]` : 브랜치 생성    
`git checkout [브랜치 이름]` : 브랜치 이동

### 수정한 뒤 커밋하고 푸시
`git add *`    
`git commit -m "메시지"`    
`git push`

### 깃허브에 접속해서 풀리퀘 보내기
풀리퀘 보내고 카톡보내기!

### 작업완료 후
내 branch 수정 사항을 master 브랜치에 반영

참고 : https://vanillacreamdonut.tistory.com/67
