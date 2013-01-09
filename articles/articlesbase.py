#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# (C) 2009 HalOtis Marketing
# written by Matt Warren
# http://halotis.com/

import sys, urllib2, urllib, sqlite3, webbrowser, re

from BeautifulSoup import BeautifulSoup # available at: http://www.crummy.com/software/BeautifulSoup/

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; AskTB5.6)'

conn = sqlite3.connect("articlesbase.db")
conn.row_factory = sqlite3.Row

c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Ezines (`url`, `title`, `content`, `signature`)')
conn.commit()

def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)
  
def search2(query):
    url="http://www.articlesbase.com/find-articles.php?q=" + query
    HTML=set()
    try:          
        req = urllib2.Request(url)
        req.add_header('User-agent', USER_AGENT)
        HTML = urllib2.urlopen(req).read()     
    except urllib2.HTTPError, e:
       print e.message  
    finally:
        return HTML

def search(query):
    url='http://ezinearticles.com/search/?q=' + '+'.join(query.split())
    try:        
        req = urllib2.Request(url)
        req.add_header('User-agent', USER_AGENT)
        HTML = urllib2.urlopen(req).read()        
        return HTML        
    except urllib2.HTTPError, e:
        #print e.fp.read()
        output_decaptcha(e.fp.read(), url)
        return ''

def check_for_captcha(source):
     #check for recaptcha in the page source, and return true or false.
     has_recaptcha = re.search('recaptcha_challenge_field', source)

     if has_recaptcha is None:
          return False
     elif has_recaptcha is not None:
          return True

def output_decaptcha(obj, self):
    try:
        print 'initiating recaptcha passthrough'
        soup=BeautifulSoup(obj)
        token= soup.find('iframe')['src'].replace("http://www.google.com/recaptcha/api/noscript?k=", "")
        print "token %s" % token
        surl = 'http://www.google.com/recaptcha/api/challenge?k=' + token
        req = urllib2.Request(surl)
        req.add_header('User-agent', USER_AGENT)
        tokenlink = urllib2.urlopen(req).read()     
        print 'tokenlink %s' % tokenlink
        matchy=re.compile("challenge : '(.+?)'").findall(tokenlink)
        for challenge in matchy:
            imageurl='http://www.google.com/recaptcha/api/image?c='+challenge
            print "Opening Captcha Link..."
            webbrowser.open(imageurl, new=2, autoraise=True)
            userInput = raw_input()
            self.br.select_form(nr=0)
            self.br["captcha"] = userInput
            try:
                self.br.submit()
            except Exception, e:
                print 'Error %s' % e.message
                return
    except Exception, e:
        print 'Error %s' %  e.message       

def parse_search_results(HTML):
    """Givin the result of the search function this parses out the results into a list
    """
    soup = BeautifulSoup(HTML)
    match_titles = soup.findAll(attrs={'class':'article_row'})       
    print match_titles
    return transposed([match_titles])
    
def get_article_content(url):
    """Parse the body and signature from the content of an article
    """
    req = urllib2.Request(url,headers=USER_AGENT)  
    HTML = urllib2.urlopen(req).read()
    soup = BeautifulSoup(HTML)
    return {'text':soup.find(id='KonaBody'), 'sig':soup.find(id='sig')}
    
def store_results(search_results):
    """put the results into an sqlite database if they haven't already been downloaded.
    """
    c = conn.cursor()
    for row in search_results:
        title = row[0]    
        print title
        link = title.find('a').get('href')
        have_url = c.execute('SELECT url from Ezines WHERE url=?', (link, )).fetchall()
        if not have_url:
          content = get_article_content(link)
          c.execute('INSERT INTO Ezines (`title`, `url`, `content`, `signature`) VALUES (?,?,?,?)', (title.find('a').find(text=True), link, str(content['text']), str(content['sig'])) )
    conn.commit()
    
if __name__=='__main__':
    #example usage
    page = search('seo')
    if len(page) > 0:
        search_results = parse_search_results(page)
        store_results(search_results)
    else:
        print "Empty"    