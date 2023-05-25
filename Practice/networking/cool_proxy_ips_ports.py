################################################################################
# File: cool_proxy_ips_ports.py
# Author(s): Jim Lee
# Updated: 5/25/23
# Description: This script will access a target URL "http://www.cool-proxy.net
#     /proxies/http_proxy_list/sort:score/direction:desc" then return a CSV
#	  file with two columns namely 'ip_address' and 'port_number' values from 
#     the HTTP Proxy list in descending order based of the 'score' column.
################################################################################

import csv
import json
import os
import requests

# Helper function to write HTTP Proxy table to a CSV file named 
# "http_proxy_ips_ports.csv" containing columns 'ip_address' and 'port'.
#
# Input: 'sortedPrx' i.e. sorted list of JSON objects
# Output: str() i.e. the name of the created CSV file
def writeCSV(sortedPrx):
    csvName = "http_proxy_ips_ports.csv"
    with open(csvName, 'w+', newline='') as csvFile:
        cols = ['ip_address', 'port_number']
        csvWriter = csv.DictWriter(csvFile, fieldnames=cols)
        csvWriter.writeheader()

        for i in range(len(sortedPrx)):
            ip, port = sortedPrx[i]['ip'], sortedPrx[i]['port']
            csvWriter.writerow({'ip_address': ip, 'port_number': port})

    return csvName

# Helper function to sort the JSON file which populates the specified URL
# i.e. HTTP Proxy table sorted by decreasing 'score'.
#
# Input: 'prx' i.e. unsorted list of JSON objects
# Output: list() i.e. sorted list of JSON objects
def sortProxyJSON(prx):
    return sorted(prx, key=lambda k: k['score'], reverse=True)

# Helper function to access and parse the JSON file which populates the 
# specified URL i.e. HTTP Proxy table.
#
# Input: 'headers' i.e. HTTP headers
# Output: list() i.e. list of JSON objects
def getProxyJSON(headers):
    proxies = []
    ip = "ip"
    port = "port"
    score = "score"
    jsonPath = "http://www.cool-proxy.net/proxies.json"
    respJSON = requests.get(jsonPath, headers=headers)
    dataJSON = json.loads(respJSON.text)

    for i in range(0, len(dataJSON)):
        proxies.append({ip: dataJSON[i][ip], port: dataJSON[i][port], 
        	            score: dataJSON[i][score]})
    return proxies

# Helper function to make HTTP GET request given target URL and HTTP headers.
# 
# Input: 'url' i.e. target URL, 'headers' i.e. HTTP headers
# Output: str() i.e. the HTML response from HTTP GET request
def getRequest(url, headers):
    resp = requests.get(url, headers=headers)
    return resp.text

# Helper function to return custom HTTP headers for GET request.
# 
# Input: None
# Output: dict() i.e. HTTP headers with 'User-Agent' and 'Content'
def createHeaders():
    ua0 = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 "
    ua1 = "(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    uaField = ua0 + ua1
    contentField = "text/html"

    return {'User-Agent': uaField, 'Content' : contentField}

# Helper function to return URL string specified.
# 
# Input: None
# Output: str() i.e. URL specified 
def createURL():
    tDom = "http://www.cool-proxy.net"
    return tDom + "/proxies/http_proxy_list/sort:score/direction:desc"

# Visit the specified URL , parse the HTTP Proxy table, and create a CSV
# file containing columns 'ip_address' and 'port' populated with
# the associated 'IP' and 'Port' columns from the parsed HTTP proxy table.
# main() will finish by printing a message specifying the current working
# directory where the CSV file mentioned above can be accessed.
#
# Input: None
# Output: None
def main():
    tPath = createURL()
    tHeaders = createHeaders()
    response = getRequest(tPath, tHeaders)

    if response.find('proxies.json') != -1:
        proxyUnsorted = getProxyJSON(tHeaders)
        proxySorted = sortProxyJSON(proxyUnsorted)
        csvFile = writeCSV(proxySorted)
        print("The CSV output file '{0}', can be found here: {1}".format(
        	  csvFile, os.getcwd()))

################################ MAIN CHUNK ###################################
main()
