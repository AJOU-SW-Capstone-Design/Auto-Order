import sys

from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import pyperclip
import account_info

def autoOrder(pl_road_address, pl_name, orderer_phone, order_url, order_list_string):
    '''
    필요 데이터: 나눔 위치 도로명 주소, 나눔 위치 이름, 주문자 정보(이름, 휴대폰번호), 식당 url, 주문 딕셔너리 리스트[{메뉴명, 가격, 요청사항}, ...]

    '''
    order_list = []
    temp_order_list = order_list_string.split(" AND ")
    temp_order_list.pop()
    for order in temp_order_list:
        temp_dict = dict()
        temp_dict["menu"] = order.split("menu=")[1].split("}")[0]
        temp_dict["price"] = int(order.split("price=")[1].split(",")[0])
        temp_dict["request"] = order.split("request=")[1].split(",")[0]
        order_list.append(temp_dict)
    
    driver = webdriver.Chrome('chromedriver.exe')
    url = "https://www.yogiyo.co.kr/"
    driver.get(url)
    driver.maximize_window()
    time.sleep(2)

    '''

    # 요기요 회원 로그인
    driver.find_element_by_xpath('//*[@id="cart"]/button[1]').click()
    time.sleep(2)
    # ID 입력
    driver.find_element_by_xpath('//*[@id="loginEmail"]').send_keys(account_info.yogiyo_id)
    time.sleep(2)
    # 비밀번호 입력
    driver.find_element_by_xpath('//*[@id="loginPwd"]').send_keys(account_info.yogiyo_pw)
    time.sleep(2)
    # 로그인 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div[1]/form/button').click()
    time.sleep(2)

    # 비밀번호 변경 확인 창 있으면 끄기
    try:
        driver.find_element_by_xpath('/html/body/div[10]/div/div/div[1]/button').click()
        time.sleep(2)
    except NoSuchElementException:
        pass
    '''

    print('Search')

    # 검색창 선택
    xpath = '''//*[@id="search"]/div/form/input'''
    element = driver.find_element_by_xpath(xpath)
    time.sleep(2)

    # 검색창에 나눔 위치 도로명 주소 입력
    element.clear()
    element.send_keys(pl_road_address)
    time.sleep(2)
    # 조회버튼 클릭
    search_xpath = '''//*[@id="button_search_address"]/button[2]'''
    driver.find_element_by_xpath(search_xpath).click()
    time.sleep(3)

    try:
        # 주소 검색 결과 없으면 해당 주소 pass
        no_result_xpath = '//*[@id="search"]/div/form/ul/li[1]'
        no_result = driver.find_element_by_xpath(no_result_xpath)
        time.sleep(2)
    except NoSuchElementException:
        time.sleep(2)

    print('restaurant url')

    # 식당 url 입력
    driver.get(order_url)
    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    menu_list = []
    lst = soup.select('table > tbody > tr > td.menu-text > div.menu-name.ng-binding')
    for s in lst:
        menu_list.append(s.get_text())

    basic_xpath1 = '//*[@id="menu"]/div/div['
    basic_xpath2 = ']/div[2]/div/ul/li['

    cut_index = 0
    index1 = 1
    index2 = 1
    xpath_list = []
    while True:
        xpath = basic_xpath1
        add_str = str(index1) + basic_xpath2 + str(index2) + ']'
        xpath += add_str
        while True:
            try:
                xpath = basic_xpath1
                add_str = str(index1) + basic_xpath2 + str(index2) + ']'
                xpath += add_str
                element = driver.find_element_by_xpath(xpath)
                xpath_list.append(xpath)
                if index1 == 1:
                    cut_index += 1
                index2 += 1
            except:
                index2 = 1
                break
        index1 += 1
        try:
            name = driver.find_element_by_xpath(basic_xpath1 + str(index1) + basic_xpath2 + '1]')
        except:
            break

    menu_name_list = menu_list[cut_index:]
    menu_xpath_list = xpath_list[cut_index:]

    tabs_xpath1 = '//*[@id="menu"]/div/div['
    tabs_xpath2 = ']/div[1]/h4/a'
    index = 3
    while True:
        tabs_xpath = tabs_xpath1 + str(index) + tabs_xpath2
        try:
            driver.find_element_by_xpath(tabs_xpath).click()
            time.sleep(2)
            index += 1
        except:
            break

    processed_menu_name_list = []
    for menu_name in menu_name_list:
        processed_menu_name_list.append(menu_name.lower().replace(' ', ''))

    for order in order_list:
        processed_menu_name = order['menu'].lower().replace(' ', '')
        if processed_menu_name in processed_menu_name_list:
            driver.find_element_by_xpath(menu_xpath_list[processed_menu_name_list.index(processed_menu_name)]).click()    # 메뉴 선택
            time.sleep(2)
            driver.find_element_by_xpath('/html/body/div[10]/div/div[3]/button[1]').click()                     # 메뉴 주문추가
            time.sleep(2)

    print('order')

    # 주문하기 버튼 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]/ng-include/div/div[2]/div[5]/a[2]').click()
    time.sleep(2)

    print('pay')

    # 결제 페이지 이동
    # 상세 주소(나눔위치 장소 이름) 입력
    driver.find_element_by_xpath('//*[@id="content"]/div/form[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/input').send_keys(pl_name)
    time.sleep(2)
    # 휴대폰 번호 입력
    driver.find_element_by_xpath('//*[@id="content"]/div/form[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[3]/div/div/input').send_keys(orderer_phone)
    time.sleep(2)
    # 요청사항 입력
    requests = ''
    for order in order_list:
        if order['request'] == "" or order['request'] == "없음":
            continue
        add_str = order['menu'] + ' - ' + order['request']
        requests += add_str + '\n'
    driver.find_element_by_xpath('//*[@id="content"]/div/form[1]/div[1]/div[2]/div[2]/div[2]/div/textarea').send_keys(requests)
    time.sleep(2)

    # 결제방법 > 네이버페이 선택
    driver.find_element_by_xpath('//*[@id="content"]/div/form[1]/div[1]/div[2]/div[3]/div[2]/div/div[1]/div[2]/label[3]').click()
    time.sleep(2)

    # 결제하기 클릭
    driver.find_element_by_xpath('//*[@id="content"]/div/form[1]/div[2]/div/button').click()
    time.sleep(2)

    '''
    # 인증번호 입력 ... 다른 사용자일 때?
    security_num = input("인증번호 입력: ")
    driver.find_element_by_xpath('/html/body/div[10]/div/div/div[2]/div/div[2]/div[1]/input').send_keys(security_num)
    time.sleep(2)
    driver.find_element_by_xpath('/html/body/div[10]/div/div/div[3]/button[2]').click()
    time.sleep(2)
    '''

    naver_id = account_info.naver_id
    naver_pw = account_info.naver_pw

    print('naver login')

    #네이버 로그인
    # id 복사 붙여넣기
    time.sleep(2)
    elem_id = driver.find_element_by_id('id')
    elem_id.click()
    time.sleep(2)
    pyperclip.copy(naver_id)
    time.sleep(2)
    elem_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(2)

    # pw 복사 붙여넣기
    elem_pw = driver.find_element_by_id('pw')
    elem_pw.click()
    time.sleep(2)
    pyperclip.copy(naver_pw)
    time.sleep(2)
    elem_pw.send_keys(Keys.CONTROL, 'v')
    time.sleep(1)

    # 로그인 버튼 클릭
    driver.find_element_by_id('log.login').click()
    time.sleep(1)

    print('done')

    time.sleep(30)

    driver.close() # 크롬드라이버 종료

def main(argv):
    autoOrder(argv[1], argv[2], argv[3], argv[4], argv[5])

if __name__ == "__main__":
    main(sys.argv)
