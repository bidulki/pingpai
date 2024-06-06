## 1. Aibackend.ipynb를 colab으로 열기
## 2. ngrok에 가입해서 authtoken 받아서 아래 ********에 넣기
<img width="238" alt="image" src="https://github.com/bidulki/pingpai/assets/55395688/c899b1de-9791-432c-9943-4975b0741953">

## 3. 해당 코드 실행 마다 colab의 ip가 바뀜, client에 적용하기
<img width="665" alt="image" src="https://github.com/bidulki/pingpai/assets/55395688/28d60e88-6295-4d78-a235-123b20b0f5ee">

NgrokTunnel: url -> "http://localhost:8000"의 url을 복사해서 client.py의 url에 붙여넣기
ex) url = "https://4eca-34-145-30-155.ngrok-free.app"

## 4. client.py 다운해서 로컬에서 실행(git clone으로)
<img width="263" alt="image" src="https://github.com/bidulki/pingpai/assets/55395688/0ffe117e-8ee9-4c61-ab5d-d4576524650b">

1. faq 리스트 출력
2. faq 추가
3. faq 제거
4. faq 검색
5. 실시간 검색기능( 구현 안됨 )
6. 종료

## 5. 데이터 확인
faq.tsv에 client.py로 추가, 제거가 반영된 데이터가 기록됩니다.  
각자 쌓은 데이터 공유해주시면 감사하겠습니다.  
<img width="758" alt="image" src="https://github.com/bidulki/pingpai/assets/55395688/074c159a-d995-4471-8b85-dd70aee7d529">

