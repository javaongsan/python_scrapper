import cookielib, random, urllib, re, sys, sqlite3, datetime, os, urllib2, socket, multiprocessing, time, Queue, threading, mechanize
from BeautifulSoup import BeautifulSoup as Soup

table_name = 'proxies'
location= 'proxies.db'
queue = Queue.Queue()
output = []
useragents =[]
website="http://javaongsan.github.com/"
Referer="http://yahoo.com"
i=0

def init():    
    global conn
    global c
    conn = sqlite3.connect(location)
    c = conn.cursor()
    create_database()

def create_database():
    sql = 'create table if not exists ' + table_name + '  (proxy text, working text) '
    c.execute(sql)
    conn.commit()

def clear_database():
    sql = 'drop table ' + table_name
    c.execute(sql)
    conn.commit()

def get_records(sql):
    c.execute(sql)
    rows = c.fetchall()
    return rows

def get_record(sql):
    c.execute(sql)
    row = c.fetchone()
    return row

def insert_record(proxy, working):
    mylist = [proxy, working]
    sql = 'INSERT OR IGNORE INTO ' + table_name + ' (proxy, working) values (?, ?)' 
    c.execute(sql, mylist)
    conn.commit()

def bulk_insert_record(proxies):
    for proxy in proxies:
        mylist = [proxy, 'UNCHECK']
        sql = 'INSERT OR IGNORE INTO ' + table_name + ' (proxy, working) values (?, ?)' 
        c.execute(sql, mylist)
    conn.commit()

def update_record(proxy, working):
    sql = 'Update ' + table_name + " set `working` = '"+ working +"' where proxy = '" + proxy +"'"
    c.execute(sql)
    conn.commit()

def bulk_update_record(proxies):
    os.system('clear')
    print"Update Database"
    for proxy, working in proxies:
        sql = 'Update ' + table_name + " set `working` = '"+ working +"' where proxy = '" + proxy +"'"
        c.execute(sql)
    conn.commit()

def close_database():
    if conn:
        conn.close()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            #grabs host from queue
            proxy_info = self.queue.get().strip()

            try:
                ua=random.choice(useragents)
                cj = cookielib.LWPCookieJar()
                browser = mechanize.Browser()
                browser.set_cookiejar(cj)
                browser.set_handle_equiv(True)
                browser.set_handle_gzip(True)
                browser.set_handle_redirect(True)
                browser.set_handle_referer(True)
                browser.set_handle_robots(False)

                browser.addheaders = [('User-agent',ua), ('Referer', Referer)]
                browser.set_proxies({'http': proxy_info})

                site = browser.open(website,timeout=100)
                html = browser.read()
                output.append((proxy_info, 'GOOD'))
                print website + "-->"+proxy_info + ":" + "OK"
                i=i+1
            except:
                output.append((proxy_info, 'BAD'))
                print website + "-->"+proxy_info + ":" + "BAD"
            self.queue.task_done()

def hitprocess():
    try:
        os.system('clear')
        start = time.time()
        sql = "SELECT proxy from proxies where `working` = 'GOOD' "
        rows = get_records(sql)
        if rows:
            for i in range(50):
            		t = ThreadUrl(queue)
            		t.setDaemon(True)
            		t.start()
            for row in rows:
            	proxy = row[0]
            	queue.put(proxy)

            queue.join()
            time_taken = time.time() - start
            print "Elapsed Time: %s s" % time_taken
            print website + " hitted %d" % i
        else:
        	print 'Nothing'
    except Exception, detail:
    	print "ERROR:", detail

def parseLog():
    file = "useragentswitcher.xml"
    handler = open(file).read()
    soup = Soup(handler)
    for message in soup.findAll('useragent'):
        f_user_dict = dict(message.attrs)
        useragents.append(f_user_dict[u'useragent'])
	
def main():
    os.system('clear')
    init()
    parseLog()
    hitprocess()
    bulk_update_record(output)
if __name__ == "__main__":
    main()
	
