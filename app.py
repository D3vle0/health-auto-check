from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import WebDriverException

from json.decoder import JSONDecodeError

import json,time,sys

def init():
    print("[*] 건강상태 자가진단 자동화 프로그램")
    print("[*] 건강상태에 이상이 없을 때에만 사용하시기 바랍니다.")

    f = open("./data.json", "r", encoding="utf8")
    try:
        data = json.load(f)
    except JSONDecodeError:
        print("[-] data.json 파일이 올바르지 않습니다.")
        sys.exit(0)
    cnt=0
    if data["region"] == "":
        print("[-] 지역이 비어있습니다.")
    else:
        cnt+=1
    if data["school"] == "":
        print("[-] 학교 이름이 비어있습니다.")
    else:
        cnt+=1
    if data["name"] == "":
        print("[-] 이름이 비어있습니다.")
    else:
        cnt+=1
    if data["birth"] == "":
        print("[-] 생년월일이 비어있습니다.")
    else:
        cnt+=1
    if data["pw"] == "":
        print("[-] 비밀번호가 비어있습니다.")
    else:
        cnt+=1
    if cnt==5:
        login()

def driverVersion():
    with open("./data.json", "r", encoding="utf8") as f:
        return json.load(f)["driver-version"]

def login():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')

    try:
        browser = webdriver.Chrome("./chromedriver/windows/" + driverVersion() + ".exe", options=options)
    except WebDriverException:
        print("[-] 크롬 브라우저 버전이 올바르지 않습니다.")
        sys.exit(0)
    browser.get("https://hcs.eduro.go.kr/#/loginHome")

    browser.find_elements_by_xpath("//*[@id=\"btnConfirm2\"]")[0].click()
    print("[+] 자가진단 사이트 접속 완료!")
    
    schoolSelect(browser)

def getData(data):
    with open("./data.json", "r", encoding="utf8") as f:
        return json.load(f)[data]

def regionSelect():
    with open("./data.json", "r", encoding="utf8") as f:
        data = json.load(f)["region"]
    if "서울" in data:
        return 2
    elif "부산" in data:
        return 3
    elif "대구" in data:
        return 4
    elif "인천" in data:
        return 5
    elif "광주" in data:
        return 6
    elif "대전" in data:
        return 7
    elif "울산" in data:
        return 8
    elif "세종" in data:
        return 9
    elif "경기" in data:
        return 10
    elif "강원" in data:
        return 11
    elif "충북" in data or "충청북도" == data:
        return 12
    elif "충남" in data or "충청남도" == data:
        return 13
    elif "전북" in data or "전라북도" == data:
        return 14
    elif "전남" in data or "전라남도" == data:
        return 15
    elif "경북" in data or "경상북도" == data:
        return 16
    elif "경남" in data or "경상남도" == data:
        return 17
    elif "제주" in data:
        return 18

def schoolLevel():
    with open("./data.json", "r", encoding="utf8") as f:
        data = json.load(f)["school"]
    if "유치원" in data:
        return 2
    elif "초등학교" in data:
        return 3
    elif "중학교" in data:
        return 4
    elif "고등학교" in data:
        return 5
    else:
        return 6
    


def schoolSelect(browser):
    print("[+] 학교 정보 입력 ... ", end="")
    browser.find_elements_by_xpath("//*[@id=\"WriteInfoForm\"]/table/tbody/tr[1]/td/input")[0].click()

    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/table/tbody/tr[1]/td/select")[0].click()
    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/table/tbody/tr[1]/td/select/option[" + str(regionSelect()) +"]")[0].click()
    
    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/table/tbody/tr[2]/td/select")[0].click()
    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/table/tbody/tr[2]/td/select/option["+ str(schoolLevel()) +"]")[0].click()

    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/table/tbody/tr[3]/td[1]/input")[0].send_keys(getData("school"))
    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/table/tbody/tr[3]/td[2]/button")[0].click()

    time.sleep(0.5)
    try:
        browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[1]/ul/li/p/a")[0].click()
    except UnexpectedAlertPresentException:
        print("\n[-] 학교를 검색할 수 없습니다. 지역과 학교명을 다시 확인해주세요.")
        sys.exit(0)
    browser.find_elements_by_xpath("//*[@id=\"softBoardListLayer\"]/div[2]/div[2]/input")[0].click()
    print("완료! ✔")
    
    inputName(browser)

def inputName(browser):
    print("[+] 인적사항 입력 ... ", end="")
    time.sleep(0.5)
    browser.find_elements_by_xpath("//*[@id=\"WriteInfoForm\"]/table/tbody/tr[2]/td/input")[0].send_keys(getData("name"))
    browser.find_elements_by_xpath("//*[@id=\"WriteInfoForm\"]/table/tbody/tr[3]/td/input")[0].send_keys(getData("birth"))
    browser.find_elements_by_xpath("//*[@id=\"btnConfirm\"]")[0].click()
    print("완료! ✔")

    inputPassword(browser)

def inputPassword(browser):
    print("[+] 비밀번호 입력 ... ", end="")
    time.sleep(0.5)
    try:
        browser.find_elements_by_xpath("//*[@id=\"WriteInfoForm\"]/table/tbody/tr/td/input")[0].send_keys(getData("pw"))
    except UnexpectedAlertPresentException:
        print("\n[-] 참여자를 확인할 수 없습니다. 이름과 생년월일을 확인해주세요.")
        sys.exit(0)
    browser.find_elements_by_xpath("//*[@id=\"btnConfirm\"]")[0].click()
    time.sleep(1)
    try:
        browser.find_elements_by_xpath("//*[@id=\"container\"]/div[2]/section[2]/div[2]/ul/li/a/span[1]")[0].click()
    except UnexpectedAlertPresentException:
        print("\n[-] 비밀번호가 맞지 않습니다.")
        sys.exit(0)
    print("완료! ✔")

    takeSurvey(browser)

def takeSurvey(browser):
    time.sleep(1)
    for i in range(1,6):
        browser.find_elements_by_xpath("//*[@id=\"container\"]/div[2]/div/div[2]/div[2]/dl[" + str(i) + "]/dd/ul/li[1]/label")[0].click()
    browser.find_elements_by_xpath("//*[@id=\"btnConfirm\"]")[0].click()

    print("\n[+] 설문 제출 완료! ✔")

if __name__ == "__main__":
    init()