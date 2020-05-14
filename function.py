# -*- coding: utf-8 -*-
# make by szymou
# time at 2020-05-14 22:29:46
# my csdn blog : https://blog.csdn.net/weixin_43548748
# this project's github : https://github.com/Szymou/pluginOfKodi.git

# this plugin's movie site is not mine. it come from Internet, if it infringes on your rights and your money ,you can email me 1047697114@qq.com
# this plugin have no bussisness purpose. just me use it to study for myself

# Thanks!-----Here i thanks Roman V. M. , because i was inspired Roman V. M.'s code of plugin,such as 66ys.

from xbmcswift2 import Plugin
import requests
from bs4 import BeautifulSoup
import xbmcgui
import urllib
import logging
import json

plugin = Plugin()

headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4'}

def get_categories():
    return [{'name':'首页','link':'http://zuidazy4.com/'},
            {'name':'动作片','link':'http://zuidazy4.com/?m=vod-type-id-5'},
            {'name':'喜剧片','link':'http://zuidazy4.com/?m=vod-type-id-6'},
            {'name':'爱情片','link':'http://zuidazy4.com/?m=vod-type-id-7'},
            {'name':'科幻片','link':'http://zuidazy4.com/?m=vod-type-id-8'},
            {'name':'恐怖片','link':'http://zuidazy4.com/?m=vod-type-id-9'},
            {'name':'剧情片','link':'http://zuidazy4.com/?m=vod-type-id-10'},
            {'name':'战争片','link':'http://zuidazy4.com/?m=vod-type-id-11'},
            {'name':'纪录片','link':'http://zuidazy4.com/?m=vod-type-id-22'},
            {'name':'动漫片','link':'http://zuidazy4.com/?m=vod-type-id-4'},
            {'name':'电视剧','link':'http://zuidazy4.com/?m=vod-type-id-12'},
            {'name':'福利','link':'http://zuidazy4.com/?m=vod-type-id-16'},
            {'name':'伦理','link':'http://zuidazy4.com/?m=vod-type-id-17'},
            {'name':'音乐','link':'http://zuidazy4.com/?m=vod-type-id-18'},
            {'name':'综艺','link':'http://zuidazy4.com/?m=vod-type-id-3'}]

def get_videos(category,page):
    if int(page) == 1:
        pageurl = category
    else:
        pageurl = category + '-pg-' + page

    r = requests.get(pageurl, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text)
    videos = []
    videoelement1=soup.select("span.xing_vb4")


    if videoelement1 is None:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('提醒', '这个视频没有播放地址')
    else:
        for videoelement in videoelement1:
            videoitem1 = {}
            videoitem1['name'] = videoelement.find('a').get_text()
            videoitem1['href'] = "http://zuidazy4.com"+videoelement.find('a')['href']
            videos.append(videoitem1)
        return videos


def get_sources(videolink):
    r = requests.get(videolink, headers=headers)
    r.encoding = 'UTF-8'
    soup = BeautifulSoup(r.text)
    sources = []
    categoryname = soup.find('dd').find('a').next_sibling.next_sibling.get_text()
    sourcetitle = soup.find('div', id='down_1')
    thumbimg = soup.find('div', class_='vodImg').find('img')['src']
    if sourcetitle is not None:
        i = 1
        sourceitems = sourcetitle.find_all('input')
        for sourceitem in sourceitems[:-4]:
            videosource = {}
            videosource['name'] = i
            videosource['thumb'] = thumbimg
            videosource['category'] = categoryname
            videosource['href'] = sourceitem['value']
            sources.append(videosource)
            i = i+1
        return sources
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok('提醒', '这个视频没有播放地址')


@plugin.route('/sources/<url>/')
def sources(url):
    sources = get_sources(url)
    # sources = json.dumps(sources,ensure_ascii=False)
    readysource = []
    for s in sources:
        s['category'] = s['category'].encode('utf-8')
        s['href'] = s['href'].encode('utf-8')
        readysource.append(s)
    items = [{
        'label': str(source['name']),
        'path': source['href'],
        'is_playable': True
        # 'path': plugin.url_for('play', url=source['href'])
    } for source in readysource]
    return items



@plugin.route('/category/<url>/<page>/')
def category(url,page):
    videos = get_videos(url, page)
    items = [{
        'label': video['name'],
        'path': plugin.url_for('sources', url=video['href'])
        # 'thumbnail': video['thumb']
        # 'icon': video['thumb']
    } for video in videos]
    sorted_items = items
    pageno = int(page) + 1
    nextpage = {'label': ' 下一页','path': plugin.url_for('category', url=url,page=pageno)}
    sorted_items.append(nextpage)
    return sorted_items



@plugin.route('/')
def index():
    categories = get_categories()
    items = [{
        'label': category['name'],
        'path': plugin.url_for('category', url=category['link'],page=1),
    } for category in categories]
    #sorted_items = sorted(items, key=lambda item: item['label'])
    return items


if __name__ == '__main__':
    plugin.run()
    plugin.set_view_mode(500)
