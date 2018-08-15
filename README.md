# Description
A voting bot written in python 3.x for strawpoll.com. It uses a proxy list to vote multiple times in a survey.
It works on Mac, Windows and Linux.

### Features
- Easy to use command line driven program
- 15000+ proxies are given from the get-go. More can be easily added
- The program saves already used proxies in an txt file to enhance the voting speed dramatically

# Usage
```
Usage: Main.py [options]

Options:
  -h, --help            show this help message and exit
  -v VOTES, --votes=VOTES
                        number of votes to give
  -s SURVEY, --survey=SURVEY
                        id of the survey
  -t TARGET, --target=TARGET
                        checkbox to vote for
  -p PROXY, --proxy=PROXY
                        proxylist file in txt format
  -f, --flush           Deletes skipping proxy list
```

### Example
```
python main.py -v 10 -s abbcw17 -t check3537987 -p proxylist.txt
```

# How to install it ?
Download the zip or clone it with git then install the required library with:
```
pip install requests
```

## What is pip? I don't understand!
If you don't understand how to install a library also called a "module" in Python please go checkout YouTube: 
[How to download and install Python Packages and Modules with Pip](https://www.youtube.com/watch?v=jnpC_Ib_lbc)

## Proxy timeout?
If a proxy times out it means the server is not reachable anymore. The predefined list given with this repository most likely only has
proxies that are not online anymore thus you get many proxy timeouts. To get a new list of proxies just search for proxy lists on the web. 

# How to add proxies to the list
Open the proxylist file in a text editor. 
Paste on each new line the proxy IP and a port divided by a colon.
Example:
```
149.56.160.23:80
193.108.38.23:80
94.56.130.89:3128
```
Save the file and use the file path as the `-p` argument.

# How do I get the survey id and the target ?
The survey id is always in the url pointing to your survey for example: https://strawpoll.com/abbcw17 then abbcw17 would be the id.
To find the target you have to right click the checkbox you want to vote for, then go to inspect element and search for a
value with 'check' at the beginning like check3537987. This is the checkbox id.



