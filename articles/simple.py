import mechanize, sys, urllib2, urllib, sqlite3, webbrowser, re, cookielib, os, random, time
from BeautifulSoup import BeautifulSoup 
from urllib2 import HTTPError

baseURL="http://www.goarticles.com"   
conn = sqlite3.connect("goarticles.db")
conn.row_factory = sqlite3.Row
USER_AGENT = ""

c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS goarticles (`url`, `title`, `content`, `signature`)')
conn.commit()

def getUserAgent():
  useragents = ['Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.307.11 Safari/532.9',
      'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6', 
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)', 
      'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)', 
      'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)',
      'Mozilla/5.0 (X11; Arch Linux i686; rv:2.0) Gecko/20110321 Firefox/4.0','Mozilla/5.0 (Windows; U; Windows NT 6.1; ru; rv:1.9.2.3) Gecko/20100401 Firefox/4.0 (.NET CLR 3.5.30729)', 
      'Mozilla/5.0 (Windows NT 6.1; rv:2.0) Gecko/20110319 Firefox/4.0','Mozilla/5.0 (Windows NT 6.1; rv:1.9) Gecko/20100101 Firefox/4.0',
      'Opera/9.20 (Windows NT 6.0; U; en)','Opera/9.00 (Windows NT 5.1; U; en)', 
      'Opera/9.64(Windows NT 5.1; U; en) Presto/2.1.1',
      'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1']
  return random.choice(useragents)

def getproxy():
  fileContents = open('myproxies.txt').read().splitlines()      
  return random.choice(fileContents)

def search(url):    
    try:
          # Browser
          br = mechanize.Browser()
          # Cookie Jar
          cj = cookielib.LWPCookieJar()
          br.set_cookiejar(cj)
          # Browser options
          br.set_handle_equiv(False)
          br.set_handle_gzip(True)
          br.set_handle_redirect(True)
          br.set_handle_referer(True)
          br.set_handle_robots(False)
          br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=60)
          
          r=''
          while True:
            try:
              USER_AGENT = getUserAgent()
              PROXY = getproxy()
              br.addheaders = [('User-agent', USER_AGENT)]
              br.set_proxies({"http": PROXY})
              r = br.open(url)
            except HTTPError, e:
              err = e.code
              if err == 403:
                  print '403 take 5' + '\n' + USER_AGENT + '\n' + PROXY
                  time.sleep(5)
              elif err == 404:
                  print '404 take 5' + '\n' + USER_AGENT + '\n' + PROXY
                  time.sleep(5)
              else:
                print err
    except Exception, detail:
      print "ERROR:", detail
      return ''

def getCategories(page):
    categories=[]
    soup = BeautifulSoup(page)
    excerpts = soup.findAll(attrs={'class':'indicator'}) 
    for excerpt in excerpts:
        links = excerpt.findAll('li')
        for link in links:
            category = link.find('a').get('href')
            categories.append(category)
    return categories

def parseCategoriesPages(categories):
    for category in categories:
        loop_pages(category)

def loop_pages(category):
    for i in range(1, 20):
        url = baseURL + category + str(i) 
        if url:       
          page = search(url)
          parse_search_results(page)

def parse_search_results(page):
    soup = BeautifulSoup(page)
    urls = soup.findAll(attrs={'class':'s_article_info'})  
    for url in urls:
        link = url.find('a').get('href') 
        if link:
            store_links(baseURL+link)

def get_article_content():
    rows = getlinksfromDB()
    if rows:
      for row in rows:
          url = row['url'] 
          HTML = search(str(url))
          if HTML:
            soup = BeautifulSoup(HTML)
            search_results= {'text':soup.find(id='body'), 'sig':soup.find(id='sig')}
            store_results(search_results)
    
def store_results(search_results):
    try:
        c = conn.cursor()
        for row in search_results:
            title = row[0]            
            link = title.find('a').get('href')
            content = get_article_content(baseURL + link.replace('//', '/'))
            c.execute('INSERT OR IGNORE INTO goarticles (`title`, `url`, `content`, `signature`) VALUES (?,?,?,?)', ( title.find('a').find(text=True), link, str(content['text']), str(content['sig'])) )
        conn.commit()
    except:
        pass

def getlinksfromDB():
    try:
        c = conn.cursor()
        c.execute("SELECT url from goarticles where content = ''")        
        rows = c.fetchall()
        return rows
    except:
        pass

def store_links(link):
    try:
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO goarticles (`title`, `url`, `content`, `signature`) VALUES (?,?,?,?)', ("", buffer(link), "", "" ))
        conn.commit()
    except:
        pass


if __name__=='__main__':  
    print 'Select:'
    print '1. Scrape Links'
    print '2. Scrape Articles'  
    choice = raw_input()
    if choice == "1":
      page = search(baseURL)
      if page:
          categories = getCategories(page)
          parseCategoriesPages(categories)
          store_results()
      else:
          print 'I got no shit'  
    else:
      get_article_content()
   