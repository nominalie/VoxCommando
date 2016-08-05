## Script for VoxCommando users.
## For context, see forum thread:
## http://voxcommando.com/forum/index.php?topic=1679.0
#############################################################

import urllib2, re, time, thread, traceback
from System.Collections.Generic import *
ATOM_URL='https://mail.google.com/mail/feed/atom'
gusr="ENTER YOUR GMAIL USERNAME IN QUOTES"
gpwd="ENTER YOUR GMAIL PASSWORD IN QUOTES"#Disclaimer: Anyone who reads this python file can see this.

class mailChecker:

    def __init__(self, uName,pwd):
        self.username = uName
        self.password = pwd
        self.fullCount = "0"#I don't use message count as a condition in this script, but one could
        self.msgID = "dummy"
        self.timestamp = round(time.clock())
        vc.log("gmail_notifier.py - mailChecker initialized")     
            
    def get_feed(self,user, passwd):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='mail.google.com',uri='https://mail.google.com',user='{user}@gmail.com'.format(user=user),passwd=passwd)
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)
        feed = urllib2.urlopen(ATOM_URL)
        message_text=feed.read()
        
        try:
            message_text=message_text.decode('utf-8')#try to deal with most non-Latin characters
            
        except:
            pass
        
        return message_text
               
    def readMail(self):
        timeNow = round(time.clock())
        feedData=self.get_feed(self.username, self.password)
        matchObj = re.search( r"fullcount>(\d*)<.*?title>(.*?)<.*?<summary>(.*?)</summary>.*?message_id=(.*?)&amp.*?email>(.*?)<", feedData, re.I)
        
        if matchObj:#if the match object was successfully created, then store matches as variables
        
            if self.msgID == "dummy" and timeNow-self.timestamp<10:
                self.msgID = matchObj.group(4)
                vc.log("gmail_notifier.py - setting msgID to existing unread msg on 1st launch")
        
            elif matchObj.group(4)==self.msgID:
                pass
                #vc.log("gmail_notifier.py - no new messages")
        
                
            else:    
                self.fullCount = matchObj.group(1)
                subject = matchObj.group(2)
                summary = matchObj.group(3)
                self.msgID = matchObj.group(4)
                sender = matchObj.group(5)
                
                if subject.lower()=="motion detected".lower():
                    vc.triggerEvent("newMsg", List[str]([subject,summary]))
                    vc.log("gmail_notifier.py - condition matched, triggering newMsg event")  
                    
                #else: -->not needed except if you're debugging/problem-hunting 
                    #vc.log("No match. Message was: "+subject+"from "+sender)
                                    
        #else: -->not needed except if you're debugging/problem-hunting 
            #vc.log("gmail_notifier.py - no unread messages")
        
def checkMsg(delay):    

    while 1:
        time.sleep(delay)
        try:
            myMailChecker.readMail()            
        
        except:
            error = traceback.format_exc().splitlines()
            vc.log("%s"%error[-1])
            
            

myMailChecker = mailChecker(gusr,gpwd)
thread.start_new_thread(checkMsg, (300,))# checks mail every 300 seconds (5 mins). Change to your preference.


