import os
import urllib
import requests
from bs4 import BeautifulSoup
import itchat
import importlib
import sys
importlib.reload(sys)


def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("ERROR")


def get_content(url, keyinf, start, end):
    comments = []
    for page in range(start, end+1):
        # print(page)
        temp = url+str(page)
        html = get_html(temp)
        soup = BeautifulSoup(html, 'lxml')
        PostTag = soup.find_all('tr', attrs={'class': 'tr3 t_one tac'})
        for i in PostTag:
            comment = {}
            try:
                comment['title'] = i.find(
                    'td', attrs={'class': 'tal'}).text.strip()
                comment['link'] = 'http://www.t66y.com/' + \
                    i.find('a', attrs={'target': '_blank'})['href']

                if keyinf in comment['title']:
                    comments.append(comment)
                    # print(comment['title'])
                    # print(comment['link'])
            except:
                print("shit happens")
    return comments


def download_image(url, keyinf, start, end):
    src = []  # vlist to store the link of each image
    all_image=[]
    source = get_content(url, keyinf, start, end)  # list of link dict
    for i in range(len(source)):
        temp = source[i]['link']
        html = get_html(temp)
        soup = BeautifulSoup(html, 'lxml')
        image_link = soup.find_all('input', attrs={'type': 'image'})
        for image in image_link:
            src.append(image['data-src'])

    directory = '1024image'+keyinf
    if directory not in os.listdir(os.getcwd()):
        os.makedirs(directory)
    for link in src:
        #print(link)
        filename = link.split('/')[-1]
        name = filename.split('.')[0]
        filetype = '.'+filename.split('.')[-1]
        all_image.append(directory+'\\'+name+filetype)
        r = requests.get(link)
        with open(directory+'\\'+name+filetype, 'wb') as f:
            f.write(r.content)
    print('done')
    return all_image


def output_video(url, keyinf, start, end):
    source = get_content(url, keyinf, start, end)  # list of link dict
    txt = '1024video    '+keyinf
    all_video=[]
    for i in range(len(source)):
        title = source[i]['title']
        temp = source[i]['link']
        html = get_html(temp)
        soup = BeautifulSoup(html, 'lxml')
        #video_link=soup.find('div',attrs={'class':'tpc_content do_not_catch'})
        # video_link=soup.find('a',attrs={'target':'_blank'})['href']

        # video_link=video_link.split('?')[-1]
        # video_link=video_link.replace('______','.')
        # video_link=video_link.replace('&z','')
        video_link = soup.find('a', attrs={'style': 'cursor:pointer'})[
            'onclick']
        video_link = video_link.split('src=')[-1]
        video_link = video_link.replace("'", '')
        video_link = video_link.replace('#iframeload', '')
        print(video_link)
        all_video.append(video_link)
        with open(txt+'.txt', 'a+', encoding='utf-8') as f:
            f.write(title+'\n')
            f.write(video_link+'\n')
    print('done')
    return all_video

def handle_msg(text):
    lst = []
    if text[0:4] == '1024':
        if text[4:9] == 'image':
            plus = text.find('+')
            minus = text.find('-')
            time = text.find('*')
            start = text[plus+1:minus]
            end = text[minus+1:time]
            inf = text[time+1:]
            lst.append('image')
            lst.append(start)
            lst.append(end)
            lst.append(inf)
        elif text[4:9] == 'video':
            plus = text.find('+')
            minus = text.find('-')
            time = text.find('*')
            start = text[plus+1:minus]
            end = text[minus+1:time]
            inf = text[time+1:]
            lst.append('video')
            lst.append(start)
            lst.append(end)
            lst.append(inf)
        else:
            lst.append('error')
    elif text == '搞快点':
        lst.append("输入【1024】+【video或者image】+【+起始页数】+【-结束页数】+【*关键词】例如‘1024image+1-2*捆绑’")
    elif text == 'robot':
        lst.append('啊哦，因为我没有实名制绑定，暂不能使用图灵机器人')
    else:
        lst.append("俺在睡觉(●'◡'●)，自动回复中,输入【robot】切换图灵机器人回复,输入【搞快点】进行成人活动")
    return lst


@itchat.msg_register(itchat.content.TEXT)
def _(msg):
    # equals to print(msg['FromUserName'])
    user_name = msg.fromUserName  # 第一步先记录用户id
    #itchat.send('Hello, filehelper', toUserName=user_name)
    reaction = []
    reaction = handle_msg(msg["Text"])  # 对用户发出的消息进行处理,handle_msg return list
    if reaction[0] == 'image':
        start=reaction[1]
        end=reaction[2]
        key=reaction[3]
        if (int(end)-int(start)) >5:
            return '对系统占用资源过高，请尝试较少页数（5页内）'
        try:
            all_image=download_image('http://www.t66y.com/thread0806.php?fid=16&search=&page=', key,int(start),int(end))
        except:
            return '请严格按照格式输入(例：1024image+1-2*捆绑)'
        if all_image==[]:
            return '未找到当前关键字资源，请尝试更多页数或者其他关键字'
        for image in all_image:
            itchat.send_image(image,toUserName=user_name)
        
            
    elif reaction[0] == 'video':
        start=reaction[1]
        end=reaction[2]
        key=reaction[3]
        if (int(end)-int(start)) >5:
            return '对系统占用资源过高，请尝试较少页数（5页内）'
        try:
            all_video=output_video('http://www.t66y.com/thread0806.php?fid=22&search=&page=',key,int(start),int(end))
        except:
            return '请严格按照格式输入(例：1024video+1-2*捆绑)'
        if all_video==[]:
            return '未找到当前关键字资源，请尝试更多页数或者其他关键字'
        try:
            for video in all_video:
                itchat.send(video,toUserName=user_name)
        except:
            return '未找到当前关键字资源，请尝试更多页数或者其他关键字'
    elif reaction[0]=='啊哦，因为我没有实名制绑定，暂不能使用图灵机器人':
        return reaction[0]
    elif reaction[0] == "输入【1024】+【video或者image】+【+起始页数】+【-结束页数】+【*关键词】例如‘1024image+1-2*捆绑’":
        return reaction[0]
    else:
        return "俺在睡觉(●'◡'●)，自动回复中,输入【robot】切换图灵机器人回复,输入【搞快点】进行成人活动"
if __name__ == '__main__':
    itchat.auto_login()                  # hotReload = True, 保持在线，下次运行代码可自动登录  hotReload=True
    itchat.run()
    #handle_msg('1024video+500-71*打算')
    '''function=input('enter function video/image:')
    start=input('enter start page:')
    end=input('enter end page:')
    keyinf=input('enter key information:')
    if function=='image':
        download_image('http://www.t66y.com/thread0806.php?fid=16&search=&page=', keyinf,int(start),int(end))
    elif function=='video':
        output_video('http://www.t66y.com/thread0806.php?fid=22&search=&page=',keyinf,int(start),int(end))
    else:
        print('wrong function')'''