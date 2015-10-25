# SEIEE Assistant

**Simple and rapid** projects for realistic use.

## Seiee Rank Crawler

Obtain student id, name, score，rank from [z.seiee.com](http://z.seiee.com/)
Pair the name and id to supplement the missing file

**To do** : 
- make front-end web display
- use setting.conf start

## Seiee Reminder

Obatin news from [seiee xsb](http://xsb.seiee.sjtu.edu.cn/) on a regular bases,
filter the information by user's identity and send all the content(including files and images) to mailbox

**To do** :
- use lean cloud as backend
- use xxmail as mail service
- web control platform for modify user tags

### Usage

The script is run by reading the config file. **Make sure you create a config file before excution**

**Example:**
/setting.conf

[sender]

address: YOUR SENDING GMAIL

name: YOUR SENDING NAME

key: YOUR GMAIL PASSWORD

[receivers]

receivers: RECEIVER EMAIL ADDRESS,RECEIVER EMAIL ADDRESS 
> receivers' address are split by `,`

## Seiee Hacker

See this [article](http://blog.delvin.xyz/jekyll/update/2015/10/27/python-multithread-brute-force/).

Underworking
