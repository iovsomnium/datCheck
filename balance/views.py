from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen

# Create your views here.
def getData(symbol):
    url = "https://finance.naver.com/item/sise.nhn?code={}".format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, 'lxml', from_encoding="euc-kr")
        curPrice = soup.find('strong', id='_nowVal') # 주식사이트에서 _nowVal인 strong tag 찾기
        curRate = soup.find('strong', id='_rate')# _rate라는 strong tag 찾음
        stock = soup.find('title') # title tag 찾음
        stockName = stock.text.split(':')[0].strip() # 콜론 문자를 기준으로 문자열을 분리해 종목명을 구한 뒤 문자열 좌우의 공백문자를 제거
        return curPrice.text, curRate.text.strip(), stockName

def mainView(request):
    querydict = request.GET.copy()
    mylist = querydict.lists() # GET방식으로 넘어온 QueryDict 형태의 URL을 리스트 형태로 반환
    rows = []
    total = 0

    for x in mylist:
        curPrice, curRate, stockName = getData(x[0]) #getData함수를 호출해 현자가, 등락률, 종목명을 구한다.
        price = curPrice.replace(',','')
        stockCount = format(int(x[1][0]), ',') # myList의 종목수를 int형으로 변환후 천 자리마다 쉼표 ','를 포함하는 문자열로 변환
        sum = int(price)*int(x[1][0],',')
        stockSum = format(sum, ',')
        rows.append([stockName, x[0], curPrice, stockCount, curRate,stockSum]) # 종목명, 종목코드, 현재가, 주식수, 등락률, 평가금액을 리스트로 생성 rows 리스트에 추가
        total = total + int(price) * int(x[1][0]) # 평가금액을 주식수로 곱해서 total에 더한다

    totalAmount = format(total, ',')
    values = {'rows':rows, 'total' : totalAmount} # balance.html 파일에 전달할 값들을 values 딕셔너리에 저장한다.
    return render(request, 'balance.html', values) # balace.html 파일을 표시하도록 render() 함수를 호출하면서 인숫값에 해당하는 values 딕셔너리를 넘겨준다.
