import csv

from userInfo import  username , password
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

class Twitter:
    def __init__(self,username,password):

        #self.browserProfile = webdriver.ChromeOptions()
        #self.browserProfile.add_argument('--headless')
        #self.browserProfile.add_experimental_option("prefs", {"intl.accept_language":"eng, eng-US"})
        #self.browserProfile= webdriver.Chrome("chromedriver.exe",chrome_options=self.browserProfile)
        self.browser = webdriver.Chrome()
        self.username = username
        self.password =password
    def signIn(self):
        self.browser.get("https://twitter.com/login")
        time.sleep(3)

        usernameInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input")
        passwordInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input")

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)

        btnSubmit=self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div")
        btnSubmit.click()
        time.sleep(2)
        self.browser.set_window_size(1920,1080)
        time.sleep(2)

    def search(self,hashtag):
        self.searchInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input")
        self.searchInput.send_keys(hashtag)
        time.sleep(2)
        self.searchInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def tweet(self):
        resultUser=[]
        resultText=[]
        resultComment=[]
        resultRetweet=[]
        resultLike=[]
        resultTime=[]
        listUser=self.browser.find_elements_by_xpath("//*[@id='react-root']/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[1]/div")
        listText = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[2]/div")
        listComment = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[3]/div[1]/div/div/div[2]")
        listReTweet = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[3]/div[2]/div/div/div[2]")
        listLike = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[3]/div[3]/div/div/div[2]")
        listTime=self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div/div/div/div/a")

        time.sleep(2)
        for element in listUser:
            resultUser.append(element.text)
        for element in listText:
            resultText.append(element.text)
        for element in listComment:
            resultComment.append(element.text)
        for element in listReTweet:
            resultRetweet.append(element.text)
        for element in listLike:
            resultLike.append(element.text)
        for element in listTime:
            resultTime.append(element.text)
        #Scrollbar yukseklıgı js ile
        loopCount=0

        self.lastHeight=self.browser.execute_script("return document.documentElement.scrollHeight/2")
        while True:
            if loopCount>10:
                break
            self.browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            time.sleep(3)
            self.newHeight=self.browser.execute_script("return document.documentElement.scrollHeight/2")
            if self.lastHeight == self.newHeight:
                break
            self.lastHeight=self.newHeight
            loopCount +=1
            listUser=self.browser.find_elements_by_xpath("//*[@id='react-root']/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[1]/div")
            #listUser = self.browser.find_elements_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[10]/div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[1]/div[1]")
            listText = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[2]/div")
            listComment = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[3]/div[1]/div/div/div[2]")
            listReTweet = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[3]/div[2]/div/div/div[2]")
            listLike = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div[2]/div[3]/div[3]/div/div/div[2]")
            listTime = self.browser.find_elements_by_xpath("//div[@data-testid='tweet']/div[2]/div/div/div/div/a")
            time.sleep(2)
            for element in listUser:
                resultUser.append(element.text)
            for element in listText:
                resultText.append(element.text)
            for element in listComment:
                resultComment.append(element.text)
            for element in listReTweet:
                resultRetweet.append(element.text)
            for element in listLike:
                resultLike.append(element.text)
            for element in listTime:
                resultTime.append(element.text)
            time.sleep(1)
        resultUser=pd.DataFrame({"User":resultUser})
        resultText=pd.DataFrame({"text":resultText})
        resultComment=pd.DataFrame({"comment":resultComment})
        resultRetweet=pd.DataFrame({"retweet":resultRetweet})
        resultLike=pd.DataFrame({"like":resultLike})
        resultTime=pd.DataFrame({"time":resultTime})


        r=pd.concat((resultText,resultComment),axis=1)
        r2=pd.concat((resultRetweet,resultLike),axis=1)
        r3=pd.concat((resultUser,resultTime),axis=1)
        res=pd.concat((r,r2),axis=1)
        res2=pd.concat((res,r3),axis=1)

        resultDataframe=pd.DataFrame(res2)
        return resultDataframe

    def saveToCvs(self,data):
        count = 1
        resultdataframe = data
        #resultdataframe= resultdataframe.rename(columns={"text": "Text","text":"Comment","text":"retweet","text":"like"},inplace=True)
        print(resultdataframe)

        resultdataframe.to_csv("tweet.csv",encoding="utf-8",index=True)
    def readtoCvs(self):
        dataFrame=pd.read_csv("tweet.csv")
        listText=dataFrame.iloc[:,1:2].values
        #print(listText)
        listComment=dataFrame.iloc[:,2:3].values
        #print(listComment)
        listReTweet=dataFrame.iloc[:,3:4].values
        #print(listReTweet)
        listLike=dataFrame.iloc[:,4:5]
        listTime=dataFrame.iloc[:,5:6]
        return listComment,listReTweet,listLike,listTime

    def browserClose(self):
        print("Browser closed")
        self.browser.close()



twitter=Twitter(username,password)
#login
twitter.signIn()
twitter.search("request for startup ")
data=twitter.tweet()
twitter.saveToCvs(data)
comment,retweet,like,time=twitter.readtoCvs()
twitter.browserClose()
