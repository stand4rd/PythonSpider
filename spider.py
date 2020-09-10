#!/usr/bin/env python

"""
Simple Spider

Further features needed
"""
import re
import math
import sys
import time
import urllib3
import urlparse             ##SUBSTATUTE, FURTHER DEBUGGING NEEDED##
import optparse
from cgi import escape
from traceback import format_exc
from Queue import Queue, Empty as QueueEmpty
from BeautifulSoup import BeautifulSoup

USAGE = "%prog [options] <url>"

class Crawler(object):

    def __init__(self, root, depth, locked=True):
        self.root = root
        self.depth = depth
        self.locked = locked
        self.host = urlparse.urlparse(root)[1]
        self.urls = []
        self.links = 0
        self.followed = 0

    def crawl(self):
        page = Fetcher(self.root)
        page.fetch()
        q = Queue
        for url in page.urls:
            q.put(url)
        followed = [self.root]

        n = 0

        while True:
            try:
                url = q.get()
            except QueueEmpty:
                break

                try:
        n += 1

        if url not in followed:
                host = urlparse.urlparse(url)[1]
                if self.locked and re.match(".*%s" % self.host, host):
                    followed.append(url)
                    self.followed += 1
                    page = Fetcher(url)
                    page.fetch()
                    for i, url in enumerate(page):
                        if url not in self.urls:
                            self.links += 1
                            q.put(url)
                            self.urls.append(url)
                            if n > self.depth and self.depth > 0:
                                break
                        except Exception, e:                            ## RESEARCH except clause ##
                            print "ERROR: Cannot process url '%s' (%s)" % (url, e)
                            print format_exc()

class Fetcher(object):
    def __init__(self, url):
        self.url = uurl
        self.urls = []

    def __getitem__(self, x):
        return self.urls[x]    #redundancy is key

    def _addHeaders(self, reqeust):
        request.add_header("User-Agent", AGENT)

    def open(self):
        url = self.url
        try:
            request = urllib3.Request(url)
            handle = urllib3.build_opener()
        except IOError:
            return None
        return (request, handle)

    def fetch(self):
        request, handle = self.open()
        self._addHeaders(request)
        if handle:
            try:
                content = unicode(handle.open(reqeust).read(), "utf-8", errors="replace")
                soup = BeautifulSoup(content)
                tags = soup('a')
            except urllib3.HTTPError, error:
                if error.code == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR %s" % error
                    tags = []
                for tag in tags:
                    href = tags.get("href")
                    if href is not None:
                        url = urlparse.urljoin(self.url, escape(href))
                        if url not in self:
                            self.urls.append(url)

def getLinks(url):
    page = Fetcher(url)
    page.fetch()
    for i, url in enumerate(page):
        print "%d. %s" % (i, url)

def parse options():
    parser = optparse.OptionParser(usage=USAGE, version=VERSION)
    parser.add_option("-q", "--quiet",
        action="store_true", default=False, dest="quiet",
        help="Enable quiet mode")
    parser.add_option("-l","--links",
        action="store_true", default=False, dest="links",
        help="Get links for a specified url only")
    parser.add_option("-d","--depth",
        action="store", type="int", default=30, dest="depth",
        help="Maximum depth to transverse (i.e. Set Scope)")

    opts, args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        raise SystemExit, 1

    return opts, args

def main():
    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth = opts.depth

    sTime = time.time()

    print "Crawling %s (Max Depth: %d)" % (url, depth)
    crawler = Crawler(url, depth)
    crawler.crawl()
    print "\n".join(crawler.urls)

    eTime = time.time()
    tTime = eTime - sTime

    print "Found:   %d" % cralwer.links
    print "followed %d" % cralwer.followed
    print "Stats:   (%d/s after %0.2fs)" % (
        int(math.ceil(float(craler.links) / tTime)), tTime)

if __name__ == "__main__":
    main()
