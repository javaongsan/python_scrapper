#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# (C) 2009 HalOtis Marketing
# written by Matt Warren
# http://halotis.com/
import os.path
import sys, urllib2, urllib, sqlite3, webbrowser, re

from BeautifulSoup import BeautifulSoup # available at: http://www.crummy.com/software/BeautifulSoup/

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; AskTB5.6)'

conn = sqlite3.connect("ezines.db")
conn.row_factory = sqlite3.Row

c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Ezines (`url`, `title`, `summary`, `tail`, `content`, `signature`)')
conn.commit()

def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)
   
def search(query, parameters=''):
    url='http://www.ezinearticles.com/search/?q=' + query 
    try:        
        if parameters:
          req = urllib2.Request(url, parameters)
        else:
          req = urllib2.Request(url)

        req.add_header('User-agent', USER_AGENT)
        response = urllib2.urlopen(req)
        body = response.read()  
        response.close()          
        return body        
    except urllib2.HTTPError, e:
        res = e.fp.read()
        print res
        output_decaptcha(res, query)
        return ''

def check_for_captcha(source):
     #check for recaptcha in the page source, and return true or false.
     has_recaptcha = re.search('recaptcha_challenge_field', source)

     if has_recaptcha is None:
          return False
     elif has_recaptcha is not None:
          return True

def output_decaptcha(obj, query):
    try:
        print 'initiating recaptcha passthrough'
        soup=BeautifulSoup(obj)
        token= soup.find('iframe')['src'].replace("http://www.google.com/recaptcha/api/noscript?k=", "")
        print "token %s" % token
        surl = 'http://www.google.com/recaptcha/api/challenge?k=' + token
        req = urllib2.Request(surl)
        #req.add_header('User-agent', USER_AGENT)
        tokenlink = urllib2.urlopen(req).read()     
        print 'tokenlink %s' % tokenlink
        matchy=re.compile("challenge : '(.+?)'").findall(tokenlink)
        for challenge in matchy:
            imageurl='http://www.google.com/recaptcha/api/image?c='+challenge
            print "Opening Captcha Link..."
            webbrowser.open(imageurl, new=2, autoraise=True)
            userInput = raw_input()
            if userInput != '':
               print 'challenge token:'+token + ' recaptcha_response_field:' + userInput
               parameters = urllib.urlencode({'recaptcha_challenge_field': token, 'recaptcha_response_field': userInput})
               search(os.path.realpath('.'), parameters)
    except Exception, e:
        print e        

def parse_search_results(HTML):
    """Givin the result of the search function this parses out the results into a list
    """
    soup = BeautifulSoup(HTML)
    match_titles = soup.findAll(attrs={'class':'srch_title'})
    match_sum = soup.findAll(attrs={'class':'srch_sum'})
    match_tail = soup.findAll(attrs={'class':'srch_tail'})
    
    return transposed([match_titles, match_sum, match_tail])
    
def get_article_content(url):  
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(url)).read())
    return {'text':soup.find(id='article-content'), 'title':soup.find(id='article-title')}
    
def store_results(search_results):
    """put the results into an sqlite database if they haven't already been downloaded.
    """
    c = conn.cursor()
    for row in search_results:
        title = row[0]
        summary = row[1]
        tail = row[2]
        
        link = title.find('a').get('href')
        have_url = c.execute('SELECT url from Ezines WHERE url=?', (link, )).fetchall()
        if not have_url:
            content = get_article_content('http://www.ezinearticles.com' + link)
            c.execute('INSERT INTO Ezines (`title`, `url`, `summary`, `tail`, `content`, `signature`) VALUES (?,?,?,?,?,?)', 
                      (title.find('a').find(text=True), 
                       link, 
                       summary.find(text=True), 
                       tail.find(text=True), 
                       str(content['text']), 
                       str(content['sig'])) )
    conn.commit()

def grab_article(url):
    content = get_article_content(url)
    print str(content['text'])
    


if __name__=='__main__':
    #example usage
    #page = search('seo')
    #search_results = parse_search_results(page)
    #store_results(search_results)
    grab_article('http://ezinearticles.com/?Weight-Loss-Tips-and-Secrets-That-Work&id=5291653')
