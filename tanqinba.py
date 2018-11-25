import requests
from bs4 import BeautifulSoup
from urllib import request
import urllib

def get_person(url):
    req = requests.get(url)
    html = req.text
    bf = BeautifulSoup(html, 'html.parser')
    text = bf.find_all('div', class_='author_text')
    person = text[0].find('p').text
    return person
def get_url_by_key(key_word):
    req = requests.get('http://www.tan8.com/codeindex.php?d=web&c=weixin&m=search_list&type=1&keyword={}'.format(key_word))
    html = req.text
    bf = BeautifulSoup(html, 'html.parser')
    text = bf.find_all('a')
    yp_name_url = {}
    for each in text:
        u = each.get('href')
        yp_name_url[each.text] = u
    return yp_name_url


def get_title(url):
    req = requests.get(url=url)                                          # 爬取网站源码
    req_text = req.text                                                  # 转为文本
    bf = BeautifulSoup(req_text, 'html.parser')                          # 转为BS对象
    text = bf.find_all('h3', class_='content_title_1113')
    return text[0].get_text()


def get_replace(string, pos, c):                                         # 替换指定位置的字符串
    '''string: 被处理的字符串  pos: 索引  c: 索引处被替换的'''
    list = []
    for s in string:
        list.append(s)
    list[pos] = str(c)
    return ''.join(list)


def download(yp_url=''):
    if yp_url == '':
        id = input('\n输入乐谱ID: ')
        url = 'http://www.tan8.com/codeindex.php?d=web&c=weixin&m=piano&id={}&isalbum=0&sharepage=1&uid=2632107'.format(id)
    else:
        url = yp_url

    try:
        req = requests.get(url=url)                                   # 爬取网站源码
        req_text = req.text                                              # 转为文本
        bf = BeautifulSoup(req_text, 'html.parser')                      # 转为BS对象
        png_urls = bf.find_all('img', width='100%')                      # 找到所有图片链接源代码
        root_url = png_urls[0].get('src')                                # 找到第一个链接
        title = get_title(url)
    except:
        print('乐谱ID错误！\n')
        return 'url wrong'
    path = input('存储位置 (如 C:/Windows, 不填写自动存入C盘根目录): ')
    if path == '':
        path = 'C:/'

    n = 0
    print('乐谱名：{}'.format(title))
    person = get_person(url)
    print('上传者: ' + person)
    w = input('是否继续下载？(y/n): ')
    if w == 'y':
        while True:
            try:
                url = get_replace(root_url, -5, n)
                request.urlretrieve(url, '{}/{}.png'.format(path, str(n+1))) # 下载图片
                print('正在下载第{}张乐谱......'.format(str(n + 1)))           # 发出提示
                n = n + 1
            except FileNotFoundError:
                print('路径错误！\n')
                return 'path wrong'
            except urllib.error.HTTPError:
                print('下载完成！\n乐谱名：{}\n共下载{}张图片！\n存储位置：{}\n\n'.format(title, str(n), path))
                break
        return 'end'
    if w == 'n':
        return

if __name__ == '__main__':
    print('1. 本工具仅供学习交流，请勿使用于商业用途！！\n2. 只能下载钢琴谱。\n'
          '3. 乐谱ID是指链接中的数字，如链接 http://www.tan8.com/yuepu-677.html 中，ID是677。\n'
          '4. 文件名为1.png, 2.png ... 会替换目录下所有同名文件，请给它们一个新的文件夹。')

    while True:
        i = input('\n请选择钢琴谱获取方式: \n'
                  '\t输入 1: 通过乐谱id获取 \n'
                  '\t输入 2: 通过关键字搜索获取 \n'
                  '\t输入 0: 退出 \n'
                  '请输入: ')
        if i == '1':
            w = download()
            if w == 'end':
                pass
            elif w == 'url wrong':
                continue
            elif w == 'path wrong':
                continue
        elif i == '2':
            key_word = input('请输入搜索关键词: ')
            dis = get_url_by_key(key_word=key_word)
            url_list = []
            n = 0
            for name, url in dis.items():
                n = n + 1
                url_list.append(url)

                print(str(n) + '. ' + name)
            if url_list:
                num = input('请输入你需要的乐谱的序号: ')
                url = url_list[int(num)-1]
                w = download(yp_url=url)
                if w == 'end':
                    pass
                elif w == 'url wrong':
                    continue
                elif w == 'path wrong':
                    continue
            else:
                print('没有搜索结果！请重试！')
                continue
        elif i == '0':
            exit()
        else:
            print('输入错误！请重新输入！')
            continue
