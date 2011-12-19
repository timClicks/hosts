#!/usr/bin/env python

import sys
import socket
import http.client
import urllib.parse

if __name__ == '__main__':
    urls = sys.argv[1:]
    if urls:
        source = urls
    else:
        source = sys.stdin

    for line in source:
        url = line.split('\t')[0].split(' ')[0]
        ip_address = None
        if not url:
            continue
        if not ip_address:
            parsed_url = urllib.parse.urlparse('http://%s/' % url)
            host = parsed_url.hostname
            if host == None:
                continue
            ip_address = socket.gethostbyname_ex(host)[2][0]
        connection = http.client.HTTPConnection(ip_address)
        connection.request("GET", "/")
        response = connection.getresponse()
        headers = response.getheaders()
        if 'Location' in headers:
            url = urllib.parse.urlparse(headers['Location'])
            if host == url.hostname:
                print("%s (%s) redirects back to the original \
                        site you'll need a to do some header tricking to make \
                        the site work without DNS" % (host, ip_address))
            elif host != ip_address:
                print("%s (%s) redirects" % (host, ip_address))
#        elif int(response.status / 100) == 3:
#            print("%s (%s) has a redirect" % (host, ip_address))
        elif int(response.status / 100) == 4:
            print("%s (%s) could not be found" % (host, ip_address))

