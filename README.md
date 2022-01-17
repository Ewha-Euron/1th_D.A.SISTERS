# 1th_D.A.SISTERS

## 리디북스 로멘스 웹소설 추천 시스템 구현 프로젝트 📚 (2021.09 ~ 2022.01) 

<img src="https://user-images.githubusercontent.com/77307201/149685598-3e0f59b3-861f-492e-98ed-a2800e46d139.png" width="60%" height="50%"/>

추천시스템 이론을 학습하고, 리디북스 데이터를 활용하여 가중치 하이브리드 추천시스템을 구현하였습니다. 
<details>
<summary> 스터디 </summary>
<div markdown="1">   
  
 학습자료

 * [SKPlanet Tacademy 추천시스템 분석 입문하기](https://www.youtube.com/watch?v=43gb7WK56Sk) 
 * 파이썬 머신러닝 완벽가이드 추천시스템
 * [맥주 추천시스템 구현](https://western-sky.tistory.com/category/%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%82%AC%EC%9D%B4%EC%96%B8%EC%8A%A4/%EC%B6%94%EC%B2%9C%EC%8B%9C%EC%8A%A4%ED%85%9C)
 * 그외, 깃헙 프로젝트 다수 
 
 매주 정기 스터디 및 회의 진행   
  
</div>
</details>

### 💁 팀원 소개
〰️ 권지수(CF 모델링, 프론트엔드, GUI) redo@ewhain.net

〰️ 문소연(전처리,통계분석, 백엔드) moonsy0221@ewhain.net

〰️ 이지원(팀 작업 총괄 멘토, 프론트엔드, 모델링 로직 설계) jiddoly@gmail.com

〰️ 이다현(팀장, CB 모델링, 백엔드) dahyun3422@gmail.com

〰️ 최하경(전처리, 통계분석, 백엔드) hakyung0007@gmail.com

---

### 1️⃣ 기획 배경 및 의도 

#### 서비스 기획 

  > **필요성**

    - 추천 시스템을 통해 보증된 콘텐츠를 발굴하여 IP 확장 
    - 리디북스 내, 로맨스 장르 키워드 검색 적극 활용 
    - 리디북스 내, 기존 유저의 개인 맞춤형 추천 시스템의 부재
    - 인기작 위주의 작품 추천 
    - 키워드를 적극적으로 활용하여 다수의 범용 사용자를 대상으로 마케팅 진행 
  
  > **목적**  
  
    개인 맞춤형 로맨스 웹소설 추천 시스템 구현 

  > **타겟** 
    
    기존 리디북스 웹소설 콘텐츠를 이용해 본 사용자 

  > **내용** 
   
    CB 와 CF 를 조합한 가중치 Hybrid 추천 시스템 구현 

  > **기대효과** 
  
    웹소설 콘텐츠 사용자들의 취향, 상황에 맞는 추천을 통한 개인 맞춤형 콘텐츠 향유 지원 

---

### 2️⃣ 데이터 수집 및 전처리 

#### 🔹 데이터 수집

<img src="https://user-images.githubusercontent.com/77307201/149686497-4912f518-c0f2-4190-894c-e4ad2dfad796.png" width="60%" height="50%"/>

#### 🔹 전처리

> 기본 전처리, 누락할 데이터 파악 및 제거, user rating table 생성을 위한 ID 가공 

#### 🔹 EDA
> 변수 간 관계 분석을 위한 통계 분석 및 변수 중요도 탐색 : 회귀분석, ID 기준 5진 분류분석 

> 변수 중요도 결과를 바탕으로, 사용자가 작품을 고를 때 중요하게 고려하는 요소를 선정하여 가중치 부여 기준 변수로 활용

---

### 3️⃣ 모델링 
<img src="https://user-images.githubusercontent.com/77307201/149686863-262293f4-7d5c-4cfe-b6f2-0bb1fc18a7b3.png" width="60%" height="50%"/>

#### 🔹 CB 

 > 형태소 분석기 : mecab (웹소설 용어 사용자 사전 추가) , 주인공 이름 불용어 제거 

 >  텍스트 벡터화 : countervectorizer, tf-idf, word2vec

 > 평균 코사인 유사도 행렬 도출  

 > 기다무/무료공개 회차수 , 키워드에 대한 가중치 부여 

#### 🔹 CF

 > ID 식별자 그룹화 처리 

 >  Item based CF

 >  Surprise module  

 >  좋아요수,평균별점,전체리뷰수,구매자수 에 대한 가중치 부여 

---

### 4️⃣ 최종 결과

[✨ 프로젝트 시연영상입니다. 클릭해주세요! ✨](https://youtu.be/JvLYGp920C8) 

>  구현 형태 : 웹 애플리 케이션 

>  Framework : Django, python 

>  메인, 작품 필터링, 가중치 Input, 작품평가(장바구니 기능), 추천 결과 

>  GUI 
<img src="https://user-images.githubusercontent.com/77307201/149688235-fc284a4d-7b5e-4215-b8c1-e939dcbbaace.png" width="60%" height="50%"/>


<img src="https://user-images.githubusercontent.com/77307201/149688290-41b14c9b-9503-480b-8f94-9d9251fff926.png" width="60%" height="50%"/>

---

### 5️⃣ 의의 및 한계 

> **한계** 
    
  👉 유저 ID 식별화로 인한 CF 성능 개선 불가, 사용자 데이터 정보를 확보하기 어려워 모델 성능을 평가할 객관적인 지표 수립이 제대로 이루어지지 않음 

> **확장가능성** 

  👉 유저로부터 추천 결과의 만족도를 받거나 리디북스 링크로 연결되어 유저 로그 기록 데이터를 수집해, 추천 결과의 성능개선 지표로 활용하여 고도화된 모델링 진행 가능 

> **의의 및 기대효과** 

  👉 사용자 개인의 웹소설 소비 성향을 세부적으로 파악해 리디북스에서 운영하는 웹소설 플레이리스트, 키워드 이벤트, 큐레이션 채널 운영 등의 차별화된 마케팅을 개별 사용자에게 맞춤화하여 제공 가능 
  
  👉 작품별 함께 구매 및 둘러본 작품 추천을 넘어서, 특정 유저가 소비한 작품을 기반으로 한 사용자 개인 맞춤형 추천 시스템 구현 가능 


---

<details>
<summary> ✳️ vscode 깃허브 연동 방법</summary>
<div markdown="1">   

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
  
</div>
</details>
