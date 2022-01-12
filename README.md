# 1th_D.A.SISTERS

## github와 연동하기
### git clone하기
`git clone [주소]`

### 가상환경 생성
`python -m venv venv`

(ctrl+shift+p)
select interpreter    
생성한 가상환경 선택 후 터미널 확인

### django 설치
`python -m pip install django`

### django 서버 실행
- 잘 받아왔는지 확인    
`python manage.py runserver`

### 일단 무조건 풀하고 시작
- vscode 상에서 소스제어->점 3개->풀    
`git pull`

### 브랜치 생성 (절대 master에서 작업시작XX)
- vscode 상에서 왼쪽 아래 현재 브랜치 클릭 -> 새 분기 만들기    
`git branch [브랜치 이름]` : 브랜치 생성    
`git checkout [브랜치 이름]` : 브랜치 이동

### 수정한 뒤 커밋하고 푸시
- vscode 상에서 소스제어->새로고침->커밋(+스테이징)->푸쉬    
`git add *`    
`git commit -m "메시지"`    
`git push`

### 깃허브에 접속해서 풀리퀘 보내기
- 인터넷으로 깃허브 접속해서 pull request 생성
- 풀리퀘 보내고 카톡보내기!

### merge 후(작업완료 후)
- 내 branch 수정 사항을 master 브랜치에 반영
- 그냥 작업하던 브랜치 삭제하고 master 브랜치로 이동해서 pull 받기

참고 : https://vanillacreamdonut.tistory.com/67
