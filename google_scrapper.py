import sqlite3, os, time, random, urlparse, urllib2, shutil, datetime, sys

from xgoogle.search import GoogleSearch, SearchError

table_name = 'scrapper'

def init(location):    
    global conn
    global c
    conn = sqlite3.connect(location)
    c = conn.cursor()
    create_database()

def create_database():
    sql = 'create table if not exists ' + table_name + '  (date text, url text, content text) '
    c.execute(sql)
    conn.commit()

def clear_database():
    sql = 'drop table ' + table_name
    c.execute(sql)
    conn.commit()

def insert_record(date, url, content):
    mylist = [date, url, buffer(content)]
    sql = 'INSERT OR IGNORE INTO ' + table_name + ' (date, url, content) values (?, ?, ?, )' 
    c.execute(sql, mylist)
    conn.commit()

def close_database():
    if conn:
        conn.close()

def getFileName(metainfo, site):
    try:
        FORMAT = '%Y%m%d%H%M%S'
        if 'Content-Disposition' in metainfo:
            cd = dict(map(lambda x: x.strip().split('=') if '=' in x else (x.strip(),''),metainfo.getheaders("Content-Disposition")[0].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename: 
                    return str(datetime.datetime.now().strftime(FORMAT))+"-"+filename
        return str(datetime.datetime.now().strftime(FORMAT))+"-"+os.path.basename(urlparse.urlsplit(site.url)[2])
    except Exception, e:
        print "Get File Name failed: %s" % e

def get_url_info(url, mb=1):
    try:
        FORMAT = '%Y%m%d%H%M%S'
        print datetime.datetime.now().strftime(FORMAT) + ": Checking %s" % url
        site = urllib2.urlopen(url)
        meta = site.info()  
        if 'Content-Length' in meta:            
            size = meta.getheaders("Content-Length")[0]            
            if (int(size)/1024/1024) > mb:              
                print datetime.datetime.now().strftime(FORMAT) + ": Downloading " + url + " " + size + "mb" 
                r = urllib2.urlopen(urllib2.Request(url))
                insert_record(datetime.datetime.now().strftime(FORMAT), url, r.read())
                r.close()
                print datetime.datetime.now().strftime(FORMAT) + ": Downloaded %s" % url
    except Exception, e:
        print "Download failed: %s" % e

def scrapsomesqlfiles(keyword, pages=20):
    try:
        for i in range(0,pages+1):
            wt = random.uniform(2, 5)   
            gs = GoogleSearch(keyword)
            gs.results_per_page = 50
            gs.page = i 
            results = gs.get_results()
            time.sleep(wt)
            print 'This is the %dth iteration and waited %f seconds' % (i, wt)
            for res in results:
                get_url_info(res.url.encode('utf8'))    
    except SearchError, e:
      print "Search failed: %s" % e

def main():
    db=sys.argv[1].replace(' ','_') + ".db"
    init(db)
    scrapsomesqlfiles(sys.argv[1] + ' + filetype:txt')
    shutil.move(sb, "collected/"+db)

if __name__ == "__main__":
    main()


