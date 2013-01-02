#coding: utf8 

import random, urllib, re, sys, sqlite3, datetime, os, urllib2, socket, multiprocessing, time, Queue, threading
from BeautifulSoup import BeautifulSoup as Soup

table_name = 'proxies'
location= 'proxies.db'
queue = Queue.Queue()
output = []
useragents =[]
website="http://javaongsan.github.com/"
Referer="http://yahoo.com"
i=0
resolutions=["1024×768","1280×800","1280×1024","1440×900","1680×1050"];
flash=["10.0%20r2","10.0%20r1","9.0%20r12"];
languages=["en-us","de","ja","ko","pt-br"];
ga_ua = 'UA-35588905-1'

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

    def mt_rand (low = 0, high = sys.maxint):
        return random.randint (low, high)

    def run(self):
        while True:
            #grabs host from queue
            proxy_info = self.queue.get().strip()

            try:
                proxy_handler = urllib2.ProxyHandler({'http':proxy_info})
                opener = urllib2.build_opener(proxy_handler)
                ua=random.choice(useragents)
                res=random.choice(resolutions)
                lang=random.choice(languages)
                fas=random.choice(flash)
                gmt=round(getmicrotime(),0);
                uid=mt_rand(70710490,92710490);
                #id=mt_rand(21234567,91234567).mt_rand(1018864,9999999).mt_rand(1021,9999); 

                opener.addheaders = [('User-agent',ua), ('Referer', Referer)]
                urllib2.install_opener(opener)
                x="http://www.google-analytics.com/__utm.gif?utmwv=4.3&utmn="+_mt_rand(64045995,94045995)+"&utmhn="+website.replace("http://","")+"&utmcs=ISO-8859-1&utmsr="+res+"&utmsc=32-bit&utmul="+lang+"&utmje=1&utmfl="+fas+"&utmhid="+mt_rand(1650046796,1890046796)+"&utmr=-&utmp="+website+"&utmac="+ga_ua+"&utmcc=__utma%3D"+uid+"."+bid+"."+gmt+"."+gmt+"."+gmt+".1%3B%2B__utmz%3D"+uid+"."+gmt+".1.1.utmcsr%3D(direct)%7Cutmccn%3D(direct)%7Cutmcmd%3D(none)%3B";
                req=urllib2.Request(x) 
                sock=urllib2.urlopen(req, timeout= 10)
                output.append((proxy_info, 'GOOD'))
                print website + "-->"+proxy_info + ":" + "OK"
                i=i+1
            except:
                output.append((proxy_info, 'BAD'))
                print website + "-->"+proxy_info + ":" + "BAD"
            #signals to queue job is done
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

if __name__ == "__main__":
    main()
	
