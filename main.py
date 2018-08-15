#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################################################
#                                                  #
#  Created By Luis Hebendanz                       #
#  Modified By Nithin S Varrier                    #
#  This bot only works with https://strawpoll.com. #
#                                                  #
####################################################
# Usage: main.py [options]
#
# Options:
#   -h, --help            show this help message and exit
#   -v VOTES, --votes=VOTES
#                         number of votes to give
#   -s SURVEY, --survey=SURVEY
#                         id of the survey
#   -t TARGET, --target=TARGET
#                         checkbox to vote for
#   -p PROXY, --proxy=PROXY
#                         proxylist file in txt format 
#   -f, --flush           Deletes skipping proxy list
#
#   EXAMPLE
#
# python main.py -v 10 -s abbcw17 -t check3537987
#
#
import os,sys,requests
from optparse import OptionParser

class Main:

    # SETTINGS
    maxVotes = 1
    voteFor = ""
    surveyId = ""

    # GLOBAL VARIABLES
    proxyListFile = ""
    saveStateFile = "saveState.txt"
    proxyTimeout = 1 # Seconds
    currentProxyPointer = 0
    successfulVotes = 0

    def __init__(self):
        try:

            ###
            # Command line argument parser
            ###
            parser = OptionParser()
            parser.add_option("-v", "--votes", action="store", type="string", dest="votes",help="number of votes to give")
            parser.add_option("-s", "--survey", action="store", type="string", dest="survey",help="id of the survey")
            parser.add_option("-t", "--target", action="store", type="string", dest="target", help="checkbox to vote for")
            parser.add_option("-p", "--proxy", action="store", type="string", dest="proxy",help="proxylist file in txt format")
            parser.add_option("-f", "--flush", action="store_true", dest="flush",help="Deletes skipping proxy list")
            (options, args) = parser.parse_args()

            if len(sys.argv) > 2:
                if options.votes is None:
                    print("[-] Number of votes not defined with: -v ")
                    exit(1)
                if options.survey is None:
                    print("[-] Survey id not defined with: -s")
                    exit(1)
                if options.target is None:
                    print("[-] Target to vote for is not defined with: -t")
                    exit(1)
                if options.proxy is None:
                    print("[-] Proxy List File is not defined with: -p")
                    exit(1)
                try:
                    self.maxVotes = int(options.votes)
                except ValueError:
                    print("[-] Please define an integer for -v")

                # Save arguments into global variable
                self.voteFor = options.target
                self.surveyId = options.survey
                self.proxyListFile = options.proxy

                # Flush saveState.xml
                if options.flush == True:
                    print("[*] Flushing saveState.txt file...")
                    os.remove(self.saveStateFile)

            # Print help
            else:
                print("[-] Not enough arguments given")
                print()
                parser.print_help()
                exit()

            # Read proxy list file
            alreadyUsedProxy = False
            taglist = [line.rstrip('\n') for line in open(self.proxyListFile)]
            tagList2 = None

            # Check if saveState.txt exists and read file
            if os.path.isfile(self.saveStateFile):
                tagList2 = [line.rstrip('\n') for line in open(self.saveStateFile)]

            # Print remaining proxies
            if tagList2 is not None:
                print("[*] Number of remaining proxies in list: " + str(len(taglist) - len(tagList2)))
                print()
            else:
                print("[*] Number of proxies in new list: " + str(len(taglist)))
                print()

            # Go through proxy list
            for tag in taglist:

                # Check if max votes has been reached
                if self.successfulVotes >= self.maxVotes:
                    break

                # Increase number of used proxy integer
                self.currentProxyPointer += 1

                # Read value out of proxy list
                tagValue = tag

                # Read in saveState.txt if this proxy has already been used
                if tagList2 is not None:
                    for tag2 in tagList2:
                        if tagValue == tag2:
                            alreadyUsedProxy = True
                            break

                # If it has been used print message and continue to next proxy
                if alreadyUsedProxy == True:
                    print("["+ str(self.currentProxyPointer) +"] Skipping proxy: " + tagValue)
                    alreadyUsedProxy = False
                    continue

                # Print current proxy information
                print("["+ str(self.currentProxyPointer) +"] New proxy: " + tagValue)
                print("[*] Connecting... ")

                # Connect to strawpoll and send vote
                self.sendToWebApi('https://' + tagValue)

                # Write used proxy into saveState.txt
                self.writeUsedProxy(tagValue)
                print()

            # Check if max votes has been reached
            if self.successfulVotes >= self.maxVotes:
                print("[+] Finished voting: " + str(self.successfulVotes))
            else:
                print("[+] Finished every proxy!")

            exit()
        except IOError as ex:
            print("[-] " + ex.strerror + ": " + ex.filename)

        except KeyboardInterrupt as ex:
            print("[*] Saving last proxy...")
            print("[*] Programm aborted")
            exit()

    # def getClientIp(self, httpProxy):
        # proxyDictionary = {"https": httpProxy}
        # rsp = requests.get("https://api.ipify.org/", proxies=proxyDictionary)
        # return str(rsp.text)


    def writeUsedProxy(self, proxyIp):
        if os.path.isfile(self.saveStateFile):
            # Write to file
            with open(self.saveStateFile, 'a') as f:
                f.write(proxyIp + '\n')
        else:
            open(self.saveStateFile, "w")

            # Now write defined entry into file
            self.writeUsedProxy(proxyIp)



    def sendToWebApi(self, httpsProxy):
        try:
            headers = \
                {
                    'Host': 'strawpoll.com',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Referer': 'https://strawpoll.com/' + self.surveyId,
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Length': '31',
                    'Cache-Control'	: 'no-cache',
                    'Pragma' : 'no-cache',
                    'Connection': 'close'
                }
            payload = {'pid': self.surveyId, 'oids': self.voteFor}
            proxyDictionary = {"https": httpsProxy}

            # Connect to server
            s = requests.Session()
            s.get("https://www.strawpoll.com/" + self.surveyId)
            r = s.post('https://strawpoll.com/vote', data=payload, headers=headers, proxies=proxyDictionary, timeout=self.proxyTimeout)
            json = r.json()
            s.close()

            # Check if succeeded
            if(bool(json['success'])):
                print("[+] Successfully voted.")
                self.successfulVotes += 1
                return True
            else:
                print("[-] Voting failed. This Ip already voted.")
                return False

        except requests.exceptions.Timeout as ex:
            print("[-] Timeout")
            return False

        except requests.exceptions.ConnectionError as ex:
            print("[-] Couldn't connect to proxy")
            return False

        except Exception as ex:
            print(str(ex))
            return False

# Execute main
Main()
