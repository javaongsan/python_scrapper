import urllib, re, sys, sqlite3, datetime, os, urllib2, socket, multiprocessing, time, Queue, threading

table_name = 'proxies'
location= 'proxies.db'

queue = Queue.Queue()
output = []

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
                proxy_handler = urllib2.ProxyHandler({'http':proxy_info})
                opener = urllib2.build_opener(proxy_handler)
                opener.addheaders = [('User-agent','Mozilla/5.0')]
                urllib2.install_opener(opener)
                req=urllib2.Request('http://www.example.com') 
                sock=urllib2.urlopen(req, timeout= 7)
                output.append((proxy_info, 'GOOD'))
                print proxy_info + ":" + "OK"
            except:
                output.append((proxy_info, 'BAD'))
                print proxy_info + ":" + "BAD"
            #signals to queue job is done
            self.queue.task_done()

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

def scrapeproxies():
	os.system('clear')
	print "Scraping Sites this may take a minute"
	sites = ['http://elite-proxies.blogspot.com/', 
	'http://www.proxies.cz.cc/',
	'http://www.proxylists.net/http.txt', 
	'http://www.proxylists.net/http_highanon.txt',
	'http://multiproxy.org/txt_all/proxy.txt',
	'http://www.digitalcybersoft.com/ProxyList/fresh-proxy-list.shtml',
	'http://tools.rosinstrument.com/proxy/?rule1', 
	'http://www.scrapeboxproxies.cz.cc/',
	'http://proxylist.j1f.net/', 
	'http://proxies.my-proxy.com/',
	'http://www.proxy-server.info/proxy-server-list.shtml',
	'http://www.proxyserverprivacy.com/free-proxy-list.shtml']

	for site in sites:
		print "Scraping " + site
		content = urllib.urlopen(site).read()
		e = re.findall("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+", content)
		bulk_insert_record(e)
		print site + " completed"
	print "Your proxies are in"

def checkproxiesmulitpprocess():
	try:
		os.system('clear')
		start = time.time()
		print 'Checking Proxies'
		sql = "SELECT proxy from proxies where `working` = 'UNCHECK'"
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
			bulk_update_record(output)
			time_taken = time.time() - start
			print "Elapsed Time: %s s" % time_taken
		else:
			print 'Nothing'
	except Exception, detail:
		print "ERROR:", detail

def noofworkingproxies():
	try:
		sql = "SELECT count(*) from proxies where `working` = 'GOOD'"
		count = get_record(sql)
		print 'No. of working proxies : ', count[0]
	except Exception, detail:
		print "ERROR:", detail

def noofuncheckproxies():
	try:
		sql = "SELECT count(*) from proxies where `working` = 'UNCHECK'"
		count = get_record(sql)
		print 'No. of unchecked proxies : ', count[0]
	except Exception, detail:
		print "ERROR:", detail

def noofbadproxies():
	try:
		sql = "SELECT count(*) from proxies where `working` = 'BAD'"
		count = get_record(sql)
		print 'No. of bad proxies : ', count[0]
	except Exception, detail:
		print "ERROR:", detail

def WriteGoodProxiesToFile():
	try:
		filename = raw_input("Enter Name Of Save File:")
		proxies = open(filename, "w")
		os.system('clear')
		print 'Checking Proxies'
		sql = "SELECT proxy from proxies where `working` = 'GOOD' Limit 1000"
		rows = get_records(sql)
		if rows:
			for row in rows:
				proxy = row[0]
				proxies.writelines(proxy + '\n')
		else:
			print 'Nothing'
		
	except Exception, detail:
		print "ERROR:", detail
	
def main():
	os.system('clear')
	init()
	print "Welcome to Proxy Scrape 1.0"
	print "Select:"
	print "1.Scrape Proxies"
	print "2.Validate Proxies"
	print "3.Count Good Proxies"
	print "4.Count Unchecked Proxies"
	print "5.Count Bad Proxies"
	print "6.Write to File Good Proxies"
	print "7.Clear all"
	choice = raw_input()
	if choice == '1':
		scrapeproxies()
	elif choice == '2':	
		checkproxiesmulitpprocess()
	elif choice == '3':
		noofworkingproxies()
	elif choice == '4':
		noofuncheckproxies()
	elif choice == '5':
		noofbadproxies()
	elif choice == '6':
		WriteGoodProxiesToFile()
	elif choice == '7':
		clear_database()

if __name__ == "__main__":
    main()
	
