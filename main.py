#Notice tab Web crawling on Myongji University moblie website: m.mju.ac.kr
import requests
from bs4 import BeautifulSoup

for page in range(1,3):
    data = requests.get("http://m.mju.ac.kr/mbs/mjumob/jsp/board/list_mobile.jsp?boardId=11294&boardType=01&id=mjumob_010100000000&spage="+str(page))
    result = BeautifulSoup(data.text,"html.parser")
    title_list = result.select("ul.listType02 li")
    for title in title_list:
        what=title.select_one("a p.liTitle").text.strip()
        print(what)


#Credit check tab on Myongji University Student Portal Web crawling : myiweb.mju.ac.kr
import requests
import time
from bs4 import BeautifulSoup

LOGIN_INFOMATION = {
    'RSP':'myiweb.mju.ac.kr',
    'RelayState':'index_SSO.jsp',
    'INIpluginData':'',
    'userID': '60171918',
    'userPW':'password'
}

start = time.time()  # 시작 시간 저장
with requests.Session() as s:
    total_list="|강좌번호|교과목명|학점|성적|성적공개여부|강의평가여부|\n"
    #LOGIN---------------------------------
    login_req = s.post('http://sso.mju.ac.kr/swift/login/loginCheck.jsp', data=LOGIN_INFOMATION)
    #MYIWEB ACCESS(1)---------------------------------
    myiweb="https://myiweb.mju.ac.kr"
    raw = s.post(myiweb)
    html = BeautifulSoup(raw.text, 'html.parser')
    result=html.find_all('frame',{"src":True})
    result=result[1]
    #MYIWEB ACCESS(2)---------------------------------
    url = "https://myiweb.mju.ac.kr"+result['src']
    raw = s.post(url)
    html = BeautifulSoup(raw.text, 'html.parser')
    #MYIWEB ACCESS(3)---------------------------------
    start_index=html.select_one("script").text.find('https')
    end_index=-1
    url = html.select_one("script").text[start_index:end_index]
    raw = s.post(url)
    html = BeautifulSoup(raw.text, 'html.parser')
    #MYIWEB ACCESS(5)---------------------------------
    url = "https://myiweb.mju.ac.kr" + result['src']
    raw = s.post(url)
    html = BeautifulSoup(raw.text, 'html.parser')
    #MYIWEB_SCORE_ACCESS ---------------------------------
    url = "https://myiweb.mju.ac.kr/servlet/su/suh/suh09/Suh09Svl01showCurrentGrade"
    raw = s.post(url)
    html = BeautifulSoup(raw.text, 'html.parser')
    html_all = html.select("tr.lecture")
    for i in html_all:
        html_one = i.select("td")
        for j in html_one:
            html_last=j.text
            total_list=total_list+"|"+html_last.strip()
        total_list=total_list+"|\n"
    print(total_list)
    s.close();
print("time :", time.time() - start)


#library book search page Web crawling on Myongji University library website: lib.mju.ac.kr
import requests
from bs4 import BeautifulSoup

search="search text"

data = requests.get("https://lib.mju.ac.kr/search/Search.Result.ax?sid=16&q="+str(search))
result = BeautifulSoup(data.text,"html.parser")
book_list = result.select("div.body")

for book in book_list:

    title=book.select_one("a.title").text
    where=book.text.strip()
    for no_tag in result.find_all('strong'):
        print(no_tag.text, no_tag.next_sibling)
    borrow_seoul=book.select_one("p:nth-of-type(3)").text
    borrow_yongin=book.select_one("p:nth-of-type(4)").text
    for no_tag in book.find_all('a'):
        print(no_tag.next_sibling)