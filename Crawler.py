#!bin/bash/python3
# -*- coding: utf-8 -*-
import re

import requests
import bs4
from random import choice

def randomAgent():
    with open("Externos/UserAgents.txt") as users:
        return choice(users.read().splitlines())


class Crawlers:

    def __init__(self,text):
        self.text = text.get('text')
    
    def filtro(self,html):
        soup = bs4.BeautifulSoup(html,'html.parser')
        result = []

        [s.extract() for s in soup('span')]
        unwantedTags = ['a', 'strong', 'cite']
        for tag in unwantedTags:
            for match in soup.findAll(tag):
                match.replaceWithChildren()

        rt = soup.findAll('li', {"class": "b_algo"})
        for t in rt:
            result.append('<i>{}</i>'.format(t.find('h2').text))

        return result

    def bing(self, count=1):
        dork = self.text.replace("/bing ","")
        count = count
        while count < 10:
            try:
                headers = {
                    'User-Agent': randomAgent(),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection': 'Keep-alive',
                }
                link = ('http://www.bing.com/search?q=' + dork + '&first='+str(count))
                req = requests.get(link,headers=headers)
                
                titles = self.filtro(req.text)
            except Exception as erro:
                return "<b>Scrutin - Crawlers : Bing</b>\n\n<b>[-] Error : </b></i>"+str(erro)+"</i>"

            links_Data = re.findall('<h2><a href="(.+?)"', req.text)
            links = [link for link in links_Data if not ".r.bat.bing.com" in link]
            
            tot_links = 0
            send = ''
            for i, name in enumerate(titles):  
                send += '\n\n{} :\n$ {}'.format(name, links[i])
                tot_links +=1

            count +=1
        return "<b>Scrutin - Crawler : Bing </b>\n\n<b>[+] Information [+]</b>\n\n  - Dork : <i>{0}</i>\n  - Total : <i>{1}</i>\n\n <b>[+] Results : </b>{2}".format(dork,str(tot_links),send)