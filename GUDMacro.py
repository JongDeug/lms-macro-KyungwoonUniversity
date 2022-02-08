from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import re

# print()
# print("*********** 필 독 ***********")
# print("1. 크롬 드라이버를 설치해주세요. <참고 https://chromedriver.chromium.org/downloads>")
# print("1.1 크롬 드라이버 버전을 확인하고 싶다면 크롬 주소창에 chrome://version를 입력해주신 뒤 제일 상단에 숫자를 확인하시면 됩니다.")
# print("2. 설치한 chromedriver.exe를 파일에 함께 넣어주신 뒤 실행해주세요.")
# print()
# print("=" * 60)



def hms(str, s):
    hours = s // 3600
    s = s - hours * 3600
    mu = s // 60
    ss = s - mu * 60
    print(str, hours, '시간', mu, '분', ss, '초')


def Run(number, lectureCountNumber):
    lectureTimeText = driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
        lectureCountNumber) + '"]/div/ul/li[1]/ol/li[5]/div/div[' + str(number) + ']/div[2]/div[3]').text

    lectureTimeTextSplit = lectureTimeText.split('/')
    search = "분"

    lectureTimeBack = re.findall(r'\d+', lectureTimeTextSplit[2])  # 수정 #정해진 강의 시간
    size = len(lectureTimeBack)

    if size == 3:
        lectureTimeBackInt = int(lectureTimeBack[0]) * 360 + int(lectureTimeBack[1]) * 60 + int(
            lectureTimeBack[2])
    elif size == 2:
        lectureTimeBackInt = int(lectureTimeBack[0]) * 60 + int(lectureTimeBack[1])
    elif size == 1:
        if search in lectureTimeTextSplit[1]:
            lectureTimeBackInt = int(lectureTimeBack[0]) * 60
        else:
            lectureTimeBackInt = int(lectureTimeBack[0])
    hms("강의 시간 : ", lectureTimeBackInt)

    lectureTimeFront = re.findall(r'\d+', lectureTimeTextSplit[0])  # 듣고 있는 강의 시간
    size = len(lectureTimeFront)
    if size == 3:
        lectureTimeFrontInt = int(lectureTimeFront[0]) * 360 + int(lectureTimeFront[1]) * 60 + int(
            lectureTimeFront[2])
    elif size == 2:
        lectureTimeFrontInt = int(lectureTimeFront[0]) * 60 + int(lectureTimeFront[1])
    elif size == 1:
        if search in lectureTimeTextSplit[0]:
            lectureTimeFrontInt = int(lectureTimeFront[0]) * 60
        else:
            lectureTimeFrontInt = int(lectureTimeFront[0])
    # hms("내가 들은 시간 : ", lectureTimeFrontInt)

    if lectureTimeBackInt > lectureTimeFrontInt:  # 이미 들었던 경우는 여기서 걸러짐
        runningTime = lectureTimeBackInt - lectureTimeFrontInt

        hms("남은 강의 시간 : ", runningTime)
        try:
            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                lectureCountNumber) + '"]/div/ul/li[1]/ol/li[5]/div/div[' + str(number) + ']/div[1]/div/span').click()
            sleep(6)


            try:
                driver.find_element(By.XPATH, '//*[@id="front-screen"]/div/div[2]/div[1]').click()
                driver.find_element(By.XPATH, '//*[@id="front-screen"]/div/div[2]/div[1]').send_keys(Keys.SPACE)
                print('front-screen')
            except:
                driver.find_element(By.XPATH, '//*[@id="test_player_html5_api"]').click()
                driver.find_element(By.XPATH, '//*[@id="test_player_html5_api"]').send_keys(Keys.SPACE)
                print('html_api')


            print()
            print("<강의 재생>")
            print()
            print("초 지나가는 건 아직 안넣었음. 야~~~~ 기분 좋다")
            sleep(runningTime + 5)
            driver.find_element(By.XPATH, '//*[@id="close_"]').click()
            print()
            print("<강의 종료>")
            print()
            sleep(5)
        except:
            print()
            print("<학습 기간이 아니거나 오류가 발생했습니다>")
            print()
            return False
    else:
        return lectureCountNumber


# driver = webdriver.Chrome() #같은 경로에 있으면 ()빈값 ㄱㅊ
# console에 표시되는 오류지우기
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.set_window_position(0, 0)
driver.set_window_size(700, 1000)

print("=" * 60)
print("경운대학교 LMS 강의 매크로(1.0.0) made by K.J.H")
print("=" * 60)

adminNumber = 2
"""
CLASS1 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[2]/em'
CLASS2 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[3]/em'
CLASS3 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[4]/em'
CLASS4 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[5]/em'
CLASS5 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[6]/em'
CLASS6 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[7]/em'
CLASS7 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[8]/em'
CLASS8 = '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[9]/em'
"""
LOGINURL = 'https://lms.ikw.ac.kr/ilos/main/member/login_form.acl'
LOGINBUTTON = '//*[@id="login_btn"]'
ONLINECLASS = '//*[@id="menu_lecture_weeks"]'
DOMAIN = 'https://lms.ikw.ac.kr/ilos/st/course/online_list_form.acl?WEEK_NO='
# https://eclass.seoultech.ac.kr/ilos/st/course/online_list_form.acl?WEEK_NO= (서울과기대)

# 서울 과기대는 들은시간 / 총 강의시간
# 경운대는 들은시간 / 기간 외 학습 시간 /총강의 시간

while True:
    id = input("아이디를 입력해주십시오 : ")
    pw = input("비밀번호를 입력해주십시오 : ")

    while True:
        try:
            subNumber = input("LMS로 듣고 있는 전체 수강 과목 수를 모두 입력해주십시오(숫자만 입력) : ")
            intSubNumber = int(subNumber) + 1
            break
        except:
            print("숫자만 입력해주십시오.")

    driver.get(LOGINURL)
    driver.find_element(By.NAME, 'usr_id').send_keys(id)
    driver.find_element(By.NAME, 'usr_pwd').send_keys(pw)
    driver.find_element(By.XPATH, LOGINBUTTON).click()

    try:
        driver.get(LOGINURL)
        break
    except:
        print("아이디 혹은 비밀번호가 틀렸습니다.")

while True:

    sleep(2)
    driver.get(LOGINURL)

    subjectName = driver.find_element(By.XPATH,
                                      '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[' + str(adminNumber) + ']/em').text
    driver.find_element(By.XPATH, '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[' + str(adminNumber) + ']/em').click()
    driver.find_element(By.XPATH, ONLINECLASS).click()

    print()
    print(subjectName + "과목에 진입하였습니다. *numbers(for admin) : " + str(adminNumber))
    print()
    adminNumber += 1


    allWeekElement = driver.find_elements(By.CSS_SELECTOR, '#chart > div > div')  # ~주 박스 나누기


    for weekOfNumber in allWeekElement:  # ~주 박스 카운터식으로 반복문 돔

        weekOfNumberText = weekOfNumber.find_element(By.CLASS_NAME, "wb-week").text
        progressNumberText = weekOfNumber.find_element(By.CLASS_NAME, "wb-status").text
        #print(weekOfNumberText)
        #print(progressNumberText)

        completeLectureNumber = 0  # 주차 바뀔때마다 초기화
        if weekOfNumberText != '':  # ~주 박스 확인
            progressNumberTextSplit = progressNumberText.split('/')

            if (int(progressNumberTextSplit[1]) - int(progressNumberTextSplit[0])) != 0:

                # 여기 안에서 다돌게끔 만들어야함 ---------------------------------------------------------------------------
                while True:
                    try:
                        weekOfNumber.find_element(By.TAG_NAME, "span").click()  # 완료되지 않은 주 클릭
                    except:
                        pass

                    # lecture 번호만 찾기
                    lectureCountNumber = 1
                    while True:
                        try:
                            if lectureCountNumber == completeLectureNumber: #이미 들은 lecture는 제외
                                lectureCountNumber += 1

                            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                                lectureCountNumber) + '"]/div/ul/li[1]/ol/li[5]/div/div/div[2]/div[3]')
                            break
                        except:
                            lectureCountNumber += 1
                            # sleep(0.5)
                            print("...")

                    print()
                    # 해당 lecture-?에 몇 차시 까지 있는지 확인하고 돌리기
                    chasi = 0
                    while True:
                        try:
                            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                                lectureCountNumber) + '"]/div/ul/li[1]/ol/li[5]/div/div[2]/div[2]/div[3]')
                        except:
                            print("1차시")
                            chasi = 1
                            break
                        try:
                            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                                lectureCountNumber) + '"]/div/ul/li[1]/ol/li[5]/div/div[3]/div[2]/div[3]')
                        except:
                            print("2차시")
                            chasi = 2
                            break
                        try:
                            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                                lectureCountNumber) + '"]/div/ul/li[1]/ol/li[5]/div/div[4]/div[2]/div[3]')
                            print("4차시")
                            chasi = 4
                        except:
                            print("3차시")
                            chasi = 3
                            break

                    bucket = 0
                    if chasi == 1:
                        bucket = Run(1, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                    elif chasi == 2:
                        bucket = Run(1, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                        bucket = Run(2, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                    elif chasi == 3:
                        bucket = Run(1, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                        bucket = Run(2, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                        bucket = Run(3, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                    elif chasi == 4:
                        bucket = Run(1, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                        bucket = Run(2, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                        bucket = Run(3, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket
                        bucket = Run(4, lectureCountNumber)
                        if bucket == False:
                            break
                        else:
                            completeLectureNumber = bucket

                    if (int(progressNumberTextSplit[1]) - int(progressNumberTextSplit[0])) == 0:  # 강의를 다들은거지
                        break

    if adminNumber > intSubNumber:  # 8대신에 subject넣으면 됨!!!!!! #과목 넘기면 종료
        print("프로그램을 종료합니다.")
        driver.close()
        break
