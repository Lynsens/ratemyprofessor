from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import time
import datetime
from datetime import datetime

import atexit

from apscheduler.scheduler import Scheduler
from flask import Flask



cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()

    


# Shutdown your cron thread if the web process is stopped
atexit.register(lambda: cron.shutdown(wait=False))



app = Flask(__name__)

url = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2529012"

url2 = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2425127'

print("1233")
score = []

time1 = []

score2 = []

time2 = []

num = []

def getNum(url,score):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    divTags = soup.find_all('div', attrs ={'class': 'RatingValues__RatingValue-sc-6dc747-3'})
    for div in divTags:
        score.append(div.getText())

    return score
    
def getScore(num,score):
    for i in range(0,len(num),2):
        score.append(num[i])
    return score

def getDiff(num,diff):
    for i in range(1,len(num),2):
        diff.append(num[i])
    return diff


def getTime(url,time1):
    r= requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    divTags = soup.find_all('div', attrs ={'class': 'TimeStamp__StyledTimeStamp-sc-9q2r30-0 bXQmMr RatingHeader__RatingTimeStamp-sc-1dlkqw1-3 BlaCV'})

    for div in range(0,len(divTags),2):
        time1.append(toStamp(divTags[div].getText()))
    return time1

def calculateAve(score):
    ave = []
    total = 0
    for i in range(0, len(score)):
        total = total + float(score[i])
        a = total / (i+1)
        ave.append(a)
    return ave


def toStamp(input):
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    a = input.split(",")
    b = a[0].split(" ")
    month = str(months.index(b[0])+1).rstrip().lstrip()
    year = str(a[1]).rstrip().lstrip()
    day = str(b[1][:-2]).rstrip().lstrip()
    formatted = day+"/"+month+"/"+year
    return formatted

def getLoui():
	global louiNum
	global louiScore
	global louiDiff
	global louiTime
	global louiURL
	louiNum = []
	louiScore = []
	louiDiff = []
	louiTime = []
	louiURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2529012'
	louiTime = getTime(louiURL, louiTime)[::-1]
	louiScore = calculateAve(getScore(getNum(louiURL,louiNum), louiScore)[::-1])
	louiDiff = calculateAve(getDiff(getNum(louiURL,louiNum), louiDiff)[::-1])

def getXiao():
	global xiaoNum
	global xiaoScore
	global xiaoDiff
	global xiaoTime
	global xiaoURL
	xiaoNum = []
	xiaoScore = []
	xiaoDiff = []
	xiaoTime = []
	xiaoURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2355255'
	xiaoTime = getTime(xiaoURL, xiaoTime)[::-1]
	xiaoScore = calculateAve(getScore(getNum(xiaoURL,xiaoNum), xiaoScore)[::-1])
	xiaoDiff = calculateAve(getDiff(getNum(xiaoURL,xiaoNum), xiaoDiff)[::-1])

def getConn():
	global connNum
	global connScore
	global connDiff
	global connTime
	global connURL
	connNum = []
	connScore = []
	connDiff = []
	connTime = []
	connURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1658282'
	connTime = getTime(connURL, connTime)[::-1]
	connScore = calculateAve(getScore(getNum(connURL,connNum), connScore)[::-1])
	connDiff = calculateAve(getDiff(getNum(connURL,connNum), connDiff)[::-1])	

def getKoyu():
	global koyuNum
	global koyuScore
	global koyuDiff
	global koyuTime
	global koyuURL
	koyuNum = []
	koyuScore = []
	koyuDiff = []
	koyuTime = []
	koyuURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1104419'
	koyuTime = getTime(koyuURL, koyuTime)[::-1]
	koyuScore = calculateAve(getScore(getNum(koyuURL,koyuNum), koyuScore)[::-1])
	koyuDiff = calculateAve(getDiff(getNum(koyuURL,koyuNum), koyuDiff)[::-1])

def getWang():
	global wangNum
	global wangScore
	global wangDiff
	global wangTime
	global wangURL
	wangNum = []
	wangScore = []
	wangDiff = []
	wangTime = []
	wangURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2425127'
	wangTime = getTime(wangURL, wangTime)[::-1]
	wangScore = calculateAve(getScore(getNum(wangURL,wangNum), wangScore)[::-1])
	wangDiff = calculateAve(getDiff(getNum(wangURL,wangNum), wangDiff)[::-1])

def getTotal():
	global totalScore
	global totalTime
	global totalDiff
	
	totalScore = xiaoScore + wangScore + connScore + koyuScore + louiScore
	totalTime = xiaoTime + wangTime + connTime + koyuTime +louiTime
	totalDiff = xiaoDiff + wangDiff + connDiff + koyuDiff + louiDiff

	total = {totalTime[i]: totalScore[i] for i in range(len(totalTime))}
	total2 = {totalTime[i]: totalDiff[i] for i in range(len(totalTime))}

	ordered_data = sorted(total.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y'))
	ordered_data2 = sorted(total2.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y'))

	totalTime= map(lambda x: x[0], ordered_data) 
	totalTime2= map(lambda x: x[0], ordered_data2)   

	totalScore = map(lambda x: x[1], ordered_data) 
	totalDiff = map(lambda x: x[1], ordered_data2) 

	totalTime = list(totalTime) 
	totalScore = list(totalScore)
	totalScore = calculateAve(totalScore)


	totalTime2 = list(totalTime2) 
	totalDiff = list(totalDiff)
	totalDiff = calculateAve(totalDiff)

louiNum = []
louiScore = []
louiDiff = []
louiTime = []
louiURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2529012'
louiTime = getTime(louiURL, louiTime)[::-1]
louiScore = calculateAve(getScore(getNum(louiURL,louiNum), louiScore)[::-1])
louiDiff = calculateAve(getDiff(getNum(louiURL,louiNum), louiDiff)[::-1])

xiaoNum = []
xiaoScore = []
xiaoDiff = []
xiaoTime = []
xiaoURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2355255'
xiaoTime = getTime(xiaoURL, xiaoTime)[::-1]
xiaoScore = calculateAve(getScore(getNum(xiaoURL,xiaoNum), xiaoScore)[::-1])
xiaoDiff = calculateAve(getDiff(getNum(xiaoURL,xiaoNum), xiaoDiff)[::-1])

connNum = []
connScore = []
connDiff = []
connTime = []
connURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1658282'
connTime = getTime(connURL, connTime)[::-1]
connScore = calculateAve(getScore(getNum(connURL,connNum), connScore)[::-1])
connDiff = calculateAve(getDiff(getNum(connURL,connNum), connDiff)[::-1])

koyuNum = []
koyuScore = []
koyuDiff = []
koyuTime = []
koyuURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1104419'
koyuTime = getTime(koyuURL, koyuTime)[::-1]
koyuScore = calculateAve(getScore(getNum(koyuURL,koyuNum), koyuScore)[::-1])
koyuDiff = calculateAve(getDiff(getNum(koyuURL,koyuNum), koyuDiff)[::-1])

wangNum = []
wangScore = []
wangDiff = []
wangTime = []
wangURL = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2425127'
wangTime = getTime(wangURL, wangTime)[::-1]
wangScore = calculateAve(getScore(getNum(wangURL,wangNum), wangScore)[::-1])
wangDiff = calculateAve(getDiff(getNum(wangURL,wangNum), wangDiff)[::-1])

totalScore = xiaoScore + wangScore + connScore + koyuScore + louiScore
totalTime = xiaoTime + wangTime + connTime + koyuTime +louiTime
totalDiff = xiaoDiff + wangDiff + connDiff + koyuDiff + louiDiff

total = {totalTime[i]: totalScore[i] for i in range(len(totalTime))}
total2 = {totalTime[i]: totalDiff[i] for i in range(len(totalTime))}

ordered_data = sorted(total.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y'))
ordered_data2 = sorted(total2.items(), key = lambda x:datetime.strptime(x[0], '%d/%m/%Y'))

totalTime= map(lambda x: x[0], ordered_data) 
totalTime2= map(lambda x: x[0], ordered_data2)   

totalScore = map(lambda x: x[1], ordered_data) 
totalDiff = map(lambda x: x[1], ordered_data2) 

totalTime = list(totalTime) 
totalScore = list(totalScore)
totalScore = calculateAve(totalScore)


totalTime2 = list(totalTime2) 
totalDiff = list(totalDiff)
totalDiff = calculateAve(totalDiff)

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]



# @app.route('/')
# def home():
# 	return render_template('home.html')

def te():
	print("test")

@app.route('/')
def line():
    return render_template('home.html', title='Home Page', max=5, 
    	xiaoScore = xiaoScore, xiaoDiff = xiaoDiff, xiaoTime = xiaoTime,
    	louiScore = louiScore, louiDiff = louiDiff, louiTime = louiTime,
    	wangScore = wangScore, wangDiff = wangDiff, wangTime = wangTime,
    	koyuScore = koyuScore, koyuDiff = koyuDiff, koyuTime = koyuTime, 
    	connScore = connScore, connDiff = connDiff, connTime = connTime,
    	totalTime = totalTime, totalScore = totalScore, totalDiff = totalDiff )
 

@cron.interval_schedule(minutes=1)
def job_function():
	getLoui()
	getWang()
	getConn()
	getXiao()
	getKoyu()
	getTotal()
	print(123)


if __name__ == "__main__":
    app.run(debug=True)
    te()
 
 
if __name__ == "__main__":
    app.run(debug=True)


if __name__ == '__main__':
	app.run(debug=True)
