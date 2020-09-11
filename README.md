# 건강상태 자가진단 자동화 프로그램

<b>❗ 반드시 건강 상태에 이상이 없을 때에만 사용하세요.</b>  
9월 9일 기준으로 하나로 통합된 자가진단 사이트에 맞는 자동화 프로그램입니다.  
http://hcs.eduro.go.kr/

<img src="./img/main.png">

## 사용법

```sh
git clone https://github.com/D3vle0/health-auto-check.git
cd health-auto-check
```

https://chromedriver.chromium.org/downloads 에서 자신의 크롬 브라우저 버전에 맞는 드라이버를 다운받고, 압축을 풀어 `chromedriver` 폴더에 넣어줍니다.  

python3 selenium 모듈을 설치합니다. 
```py
pip install selenium
```

`data.json` 파일에 데이터를 넣어줍니다.

```json
{
    "region":"경기도",
    "school":"한국디지털미디어고등학교",
    "name":"배상혁",
    "birth":"040324",
    "pw":"비밀번호 4자리"
}
```
 

```py
python3 app.py
```
또는  
```py
py app.py
```
로 실행하면 검사가 자동으로 완료됩니다.
