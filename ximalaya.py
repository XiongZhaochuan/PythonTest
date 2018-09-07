# -*- utf-8 -*-
'''
    name = 下载器
    aothor = 熊
    time = 20180716
'''

import urllib.request
import requests
import os
import re
import time
import random

#文件下载函数
def Download(url,filename,dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    fileType = url.split(".")[-1]
    #下载文件
    urllib.request.urlretrieve(url,dirname+os.sep+filename+"."+fileType)



# 输入关键词
def inputkw():
    kw = input("*****请输入搜索关键词：*****\n")
    return kw

# https://www.ximalaya.com/revision/search?core=album&kw=关键词&page=1&spellchecker=false&rows=50
# 抓取关键词相关前五十的专辑,并用正则表达式抓取信息：专辑名，专辑编号，作者，节目数
def album():
    kw = inputkw()
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    kwUrl = "https://www.ximalaya.com/revision/search?core=album&kw={}&page=1&spellchecker=false&rows=100".format(kw)
    response = requests.get(kwUrl,headers = head )
    data = response.text
    p = re.compile(r'.*?"title":(.*?),.*?"id":(.*?),.*?"nickname":(.*?),.*?"tracks":(.*?),.*?')
    res = p.findall(data)
    return res

# 遍历专辑信息
def showAlbum():
    List = album()
    for i in range(len(List)):
        if List[i][0].strip('"').endswith("》") and List[i][0].strip('"').startswith("》"):
            albumName= List[i][0][2:-2]
        else:
            albumName = List[i][0][1:-1]
        albumNum = List[i][1]
        albumAuthor = List[i][2].strip('"')
        albumTracks = List[i][3]
        print("{}.专辑名：{}***专辑编号：{}***作者：{}***节目数{}".format(i,albumName,albumNum,albumAuthor,albumTracks))
    choice = int(input("*****请输入序号：*****\n"))
    Num = List[choice][1]
    Tracks = List[choice][3]
    # https://www.ximalaya.com/revision/play/album?albumId=Num&pageNum=1&sort=-1&pageSize=Tracks
    URL = "https://www.ximalaya.com/revision/play/album?albumId={}&pageNum=1&sort=-1&pageSize={}".format(Num,Tracks)
    return URL

# 分析信息抓取名字和地址
def programMess():
    Url = showAlbum()
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    response = requests.get(Url,headers = head)
    data = response.text
    p = re.compile(r'.*?"trackName":(.*?),.*?"src":(.*?),.*?')
    res = p.findall(data)
    return res

# 遍历program的名字地址生成序号选择
def showProgram():
    List = programMess()
    os.system("cls")
    for i in range(len(List)):
        programName = List[i][0].strip('"')
        print("{}.*****{}*****".format(i,programName))
    print("若要全部下载，请输入A")
    choice = input("*****请输入序号或者A：*****\n")
    if choice == "A" or choice == "a":
        for j in range(len(List)):
            programUrl = List[j][1].strip('"')
            filename = str(j) +"_"+ List[j][0].strip('"')
            Download(programUrl, filename, "XiMaLaYa")
            print("*****第【{}】下载成功*****".format(j+1))
            time.sleep(random.randint(1,2))
        pass
    elif int(choice) >= 0 :
        programUrl = List[int(choice)][1].strip('"')
        filename = choice + List[int(choice)][0].strip('"')
        Download(programUrl,filename,"XiMaLaYa")
        print("*****下载成功*****")

# 下载界面
def main():
    print("*"*15+"喜马拉雅下载器"+"*"*15+"\n")
    print("*"*15+"仅用于参考学习"+"*"*15)
    time.sleep(2)
    while True:
        os.system("cls")
        showProgram()
        choice = input("*****是否返回首页Y/N？*****")
        if choice == "Y" or choice == "y":
            continue
        elif choice == "N" or choice =="n":
            print("*****系统将自动关闭，谢谢使用*****")
            break
        else:
            print("*****输入错误，系统自动关闭*****")
            break


if __name__ == '__main__':
    main()
