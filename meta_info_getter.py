import os
import shutil
import time
import requests
import re  #regular expression ''
import random
import sys



workdir = sys.argv[1]  #命令行传入参数

desktop = 'C:\\Users\\XUSHENG\\Desktop\\'
os.chdir(workdir)

#这个函数有误删文件的风险, 先不要用
def move(sourcefile,targetdir):    #移动sourcefile至targetdir,如果已存在同名文件则覆盖
    pwd = os.getcwd()
    os.chdir(targetdir)
    filelist = os.listdir(targetdir)
    if sourcefile in filelist:
        os.remove(sourcefile)
    os.chdir(pwd)
    shutil.move(sourcefile,targetdir)

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

def urlgen(filename):
    m = re.search(r'(^[a-zA-Z]{1,6})\D{1,2}([0-9]{2,5}).*',filename)
    if m:
        url = 'https://www.javbus.com/'+m.group(1)+'-'+m.group(2)  
        return url
    else:
        return str(code)+' failed to get url'

def img_download(url,imgname,local_location,proxy='on'): #网址/文件命名/本地存储路径/是否走代理?('on'/'off')
    if proxy == 'on':
        proxies = {
                "http": "http://127.0.0.1:1080",
                "https": "http://127.0.0.1:1080", 
                }
    if proxy == 'off':
        proxies = {
        }
    req = requests.get(url,proxies=proxies)
    f = open(imgname,'wb')  
    f.write((req.content))
    f.close()
    move(imgname,local_location)




fulllist = os.listdir()
if 'failed to recognize' in fulllist:
    pass
else:
    os.mkdir('failed to recognize')

for eachfile in FilelistGetter(workdir):
    htmlurl = urlgen(eachfile)  #获取当前文件的网站url
    if 'failed' in htmlurl:
        move(eachfile,workdir+'failed to recognize\\')
        print(eachfile,'被跳过, 未能成功识别番号')
        continue  #跳过未能识别番号的文件
    else:
        htmltxt = html_getter(htmlurl)
        htmltxt = htmltxt  #完整的未分割的文本
        htmlsp = htmltxt.split('\n')  #分割好的文本
        if '404 Page Not Found' in htmltxt:
            move(eachfile,workdir+'failed to recognize\\')
            print('番号识别错误, 网页404! 将跳过该文件')
            continue

        avcode = re.search(r'([A-Z]{1,6}-[0-9]+)',htmltxt).group(1)
        # 获取番号, 后面经常使用来替换
        print(avcode)
        
        try:
            os.mkdir(avcode)  #创建新文件夹用于存储封面\元数据\影片本体
            move(eachfile,workdir+avcode+'\\')  #本体移动
        except FileExistsError as ee:
            print('dir exits already because of duplicate files')
            move(eachfile,workdir+avcode+'\\')

        m_title = re.search(r'(title)(.*)(title)',htmltxt).group(2)
        title = re.sub(r'(.*[A-Z]*-[0-9]+\s)|(\s-\sJ.*)','',m_title)
        #获取文件名
        print('title is ',title)

        tag = htmlsp[8].split(',')
        tag = tag[1:]
        tag[-1] = re.sub(r'\".*','',tag[-1])
        #获取tag列表
        print('tags are: ',tag)

        #这B用的是中文逗号 ,草...
        m_length = re.search(r'.長度.(.*)，',htmlsp[9])
        length = m_length.group(1)
        #获取影片长度
        print('长度: ',length)

        cover_url = re.search(r'(https://pics.javbus.com/cover/.*\.jpg)',htmltxt).group(1)
        img_download(cover_url,str(avcode)+'_cover.jpg',workdir+avcode+'\\')
        #获取封面
        
        meta_name = avcode+'.txt'
        with open(meta_name,'w',encoding='utf-8') as f:
            f.write('番号: '+str(avcode)+'\n')
            f.write('    \n')
            f.write('片名: '+str(title)+'\n')
            f.write('    \n')
            f.write('时长: '+str(length)+'\n')
            f.write('    \n')
            f.write('tags: '+'\n')
            for item in tag:
                f.write(str(item))
                f.write('\n')
        f.close()
        move(meta_name,workdir+avcode+'\\')
        #元数据移动

        print('等待半分钟左右, 防止封IP')
        print('    ')
        time.sleep(0+((random.randint(80,120)-60)/8))
        #暂停防封










''' 提取功能测试区
b = 'ssni-413'
a = 'nhdta-666'
c = 'ipx 177-C'
print(urlgen(b))
print(urlgen(a))
print(urlgen(c))
'''

'''
d = 'ajldjadjlajd'
m = re.match(r'([a-zA-Z]{1,6}).([0-9]{2,5}).*',d)
n = re.search(r'[0-9]',d)
if n:
    print('d')
print(m.group(0),m.group(1),m.group(2))
'''