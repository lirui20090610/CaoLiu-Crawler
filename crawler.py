import os
import urllib
import requests
from bs4 import BeautifulSoup
#soup = bs4.BeautifulSoup(open('C:/Users/Ray/Desktop/calculate.html'),'lxml')
# print(soup.head)
# print(soup.prettify())


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
        # print(link)def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
            return i + 1
        filename = link.split('/')[-1]
        name = filename.split('.')[0]
        filetype = '.'+filename.split('.')[-1]
        # print(name+filetype)
        r = requests.get(link)
        with open(directory+'\\'+name+filetype, 'wb') as f:
            f.write(r.content)
    print('done')


def output_video(url, keyinf, start, end):
    source = get_content(url, keyinf, start, end)  # list of link dict
    txt = '1024video    '+keyinf

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
        with open(txt+'.txt', 'a+', encoding='utf-8') as f:
            f.write(title+'\n')
            f.write(video_link+'\n')


if __name__ == "__main__":
    function = input('enter function video/image:')
    start = input('enter start page:')
    end = input('enter end page:')
    keyinf = input('enter key information:')
    if function == 'image':
        download_image(
            'http://www.t66y.com/thread0806.php?fid=16&search=&page=', keyinf, int(start), int(end))
    elif function == 'video':
        output_video('http://www.t66y.com/thread0806.php?fid=22&search=&page=',
                     keyinf, int(start), int(end))
    else:
        print('wrong function')
