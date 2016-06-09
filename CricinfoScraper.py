# -*- coding: utf-8 -*-
"""
Created on Tue Jun 07 20:06:50 2016

@author: Utkarsh Rastogi
"""
from BalloonPopup import WindowsBalloonTip
import requests
from bs4 import BeautifulSoup
from time import sleep
import sys

pre_match = 'Match scheduled to begin'
inter_country = ['Australia','India','England','Pakistan','South Africa','New Zealand','Sri Lanka','West Indies','Zimbabwe','Bangladesh','Kenya','Ireland','Canada','Netherlands','Scotland','Afghanistan','USA']
international = []
international_url = []
domestic = []
domestic_url = []


def PopulateList(soup):
    description = soup.findAll('item')

    for data in description:
        des = data.find('description').text
        link = data.find('guid').text
        flag=0
        for country in inter_country:
            if country in des:
                flag=1
        
        if flag == 1:
            international.append(des)
            international_url.append(link)
        else:
            domestic.append(des)
            domestic_url.append(link)

def PrintForInput():
    
    cnt = 1
    if len(international) == 0:
        print 'No International Matches.'
    else:
        print 'International Matches:'
        for data in international:
            print str(cnt) + '. ' + data
            cnt = cnt + 1
    
    
    if domestic.count == 0:
        print '\nNo Domestic Matches.'
    else:
        print '\nDomestic Matches:'
        for data in domestic:
            print str(cnt) + '. ' + data
            cnt = cnt + 1
    
    return cnt
    
def GetUrl(inp):
    if inp <= len(international) :
        return international_url[inp-1]
    else:
        return domestic_url[inp - len(international) -1]
    
def PrintMessage(title, message):
    print title
    print message
    return
    
def GetStatus(soup):
    inreq = soup.body.find('div', attrs={'class': 'innings-requirement'})
    status = inreq.string.strip()
    return status

def GetTeam(soup, teamno):
    classname = 'team-'+teamno+'-name'
    team = soup.body.find('div', attrs={'class': classname})
    teamname = team.string.strip()
    return teamname

def GetMessage(score):
    idx=0
    for ch in score:
        idx = idx + 1
        if ch=="|":
            return score[0:idx-1]
    return score
        

def Main():
    
    print 'LIVE CRICKET MATCHES:\n'
    
    url = "http://static.cricinfo.com/rss/livescores.xml"
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'lxml')
    
    PopulateList(soup)
    
    count = PrintForInput()
    
    while True:       
        try:
            inp = int(input('\nEnter Match Number, 0 to exit\n'))
        except Exception:
            print 'Enter correct input',
            continue
        
        if inp < 0 or inp >= count:
            print 'Enter correct input',
            continue
        elif inp == 0:
            sys.exit()      
        else:
            break
    
    url = GetUrl(inp)
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'lxml')
    
    while True:
        try:
            req.raise_for_status()
            
            status = GetStatus(soup)
            team1 = GetTeam(soup, '1')
            team2 = GetTeam(soup, '2')
            title = team1 + ' v ' + team2        
                       
            if pre_match in status : 
                PrintMessage(title, status)
                WindowsBalloonTip(title, status)
                sleep(120)
            else:
                score = soup.findAll('title')
                message = GetMessage(score[0].text)
                PrintMessage(title, message + "\n" + "-"*len(message))
                WindowsBalloonTip(title, message)
                sleep (20)
            
            
        except Exception:
            PrintMessage('Connection Issue','Please check your network connection.')
            WindowsBalloonTip('Connection Issue', 'Please check your network connection.')
            break


if __name__=='__main__':
    Main()


