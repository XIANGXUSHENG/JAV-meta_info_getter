import os
import shutil
import time
import requests
import re  #regular expression ''
import random

workdir = '\\\DESKTOP-EMUQ54U\\drivers\\JAV\\'
#workdir = 'Z:\\(๑•́ ₃ •̀๑)\\AV2020'
desktop = 'C:\\Users\\XUSHENG\\Desktop\\'
os.chdir(workdir)

#这个函数有误删文件的风险, 先不要用
def move(sourcefile,targetdir):    #移动sourcefile至targetdir,如果已存在同名文件则覆盖
    pwd = os.getcwd()
    os.chdir(targetdir)
    filelist = os.listdir(targetdir)
    if sourcefile in filelist:
        os.remove(sourcefile)
        print('file with same name has been deleted')
    os.chdir(pwd)
    shutil.move(sourcefile,targetdir)
    print(str(sourcefile),'has been moved to',str(targetdir),' successfully')

def html_getter(url):
    try:
        proxies = {
        "http": "http://127.0.0.1:1080",
        "https": "http://127.0.0.1:1080",  #使用SSR代理访问
        }
        req = requests.get(url,proxies=proxies)
        text = req.text
        return text
    except Exception as e:
        print(e)
    except IOError as o:
        print(o)

def FilelistGetter(dirname):
    temp = os.listdir()
    filelist = []
    for item in temp:
        if os.path.isdir(item):  #判断是否是dir
            pass
        if os.path.isfile(item):  #判断是否是file
            filelist.append(item)
    filelist = filelist  #文件名字列表, 不包含文件夹
    return filelist

def urlgen(code):
    m = re.search(r'([a-zA-Z]{1,6}).([0-9]{2,5}).*',code)  
    if m:
        av_code = m.group(1) + '-' + m.group(2) 
        code = av_code
        av_code = str.upper(av_code) #顺手把番号存下来
        code = str.lower(code)  #将大写字母改成小写字母
        extrastrings = ['.mp4','.mkv','.rmvb','.avi','.wmv','-c','-C']
        for eachstring in extrastrings:  #去除格式后缀和中文字幕标注
            code = code.replace(eachstring,'')
        #注意re.split和一般的split方法不同, 必须写成re.split(pattern,anastr)格式
        [engpart,numberpart] = re.split(r'\s+|-',code)
        url = 'https://www.javbus.com/'+engpart+'-'+numberpart  #javbus网址更容易生成
        return url
    else:
        return str(code)+' failed to get url'

fulllist = os.listdir()
if 'failed to recognize' in fulllist:
    pass
else:
    os.mkdir('failed to recognize')

for eachfile in FilelistGetter(workdir):
    htmlurl = urlgen(eachfile)  #获取当前文件的网站url
    if 'failed' in htmlurl:
        print(eachfile,'被跳过, 未能成功识别番号')
        move(eachfile,workdir+'failed to recognize\\')
        continue  #跳过未能识别番号的文件
    else:
        htmltxt = html_getter(htmlurl)
        htmltxt = htmltxt  #完整的未分割的文本
        htmlsp = htmltxt.split('\n')  #分割好的文本

        avcode = re.search(r'([A-Z]{1,6}-[0-9]+)',htmltxt).group(1)
        # 获取番号, 后面经常使用来替换
        print(avcode)

        m_title = re.search(r'(title)(.*)(title)',htmltxt).group(2)
        title = re.sub(r'(.*[A-Z]*-[0-9]+\s)|(\s-\sJ.*)','',m_title)
        #获取文件名
        print('title is ',title)

        avformat = re.search(r'.*(\.[a-zA-Z0-9]+$)',eachfile).group(1)
        newname = avcode+'_'+title+'_'+avformat
        try:
            os.rename(eachfile,newname)
        except OSError as oe:
            print('OSError')  #有时候含有奇怪的不能作为文件名的字符,就会报OSError
        print('等待半分钟左右, 防止封IP')
        time.sleep(30+((random.randint(1,120)-60)/8))
        #暂停防封

