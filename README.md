# Auto-Order
요기요 자동 주문 접수  

## 기술 스택
### Python
Python 기반 자동화 코드 작성  

### 사용 모듈
* BeautifulSoup  
* Selenium  
* xerox  
* pyvirtualdisplay  


## 자동 주문 접수 구조
### 필요 Arguments
    plRoadAddress: 나눔 위치 도로명 주소  
    plName: 나눔 위치 장소명  
    ordererPhone: 주문자 전화번호  
    orderUrl: 요기요 웹사이트 내 식당 주문 URL  
    orderList: 주문 정보 리스트  

### 자동 주문 과정
1) 요기요 웹사이트 접속
2) 주소 입력창에 나눔 위치 도로명 주소(plRoadAddress) 입력
3) 식당 주문 URL(orderUrl)로 이동
4) 모든 메뉴 탭 클릭해 전체 메뉴명 및 xpath 정보 저장
5) 주문 정보 리스트(orderList)의 메뉴명이 전체 메뉴명 리스트 내에 존재하는지 확인
6) 존재하면 해당 메뉴명의 xpath를 이용해 클릭한 후, 메뉴 장바구니에 담기
7) 주문 정보 리스트 내의 메뉴를 모두 장바구니에 담은 뒤, '주문하기' 버튼 클릭
8) 배달 받을 장소의 상세주소에 나눔 위치 장소명(plName) 입력
9) 주문자 전화번호(ordererPhone) 입력
10) 주문시 요청사항 칸에 주문 정보 리스트(orderList)의 요청사항 입력
11) 결제수단 '네이버페이' 선택
12) '결제하기' 클릭
13) 네이버 로그인 화면으로 이동 후, 네이버 로그인
14) 네이버 결제창에서 결제하기 클릭 
