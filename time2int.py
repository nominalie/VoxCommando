## Very specific, simple script for VoxCommando users.
## See forum thread http://voxcommando.com/forum/index.php?topic=1948 for context.
## This time2int function is specifically scripted to allow you to dictate "QuickAdd" events to  
## your Google Calendar feeds from VoxCommando. ***It's an amateur, hacky script.*** 
## So far it's meeting my needs. There are two problems we're trying to address: 
## 1) MS SAPI's dictation feature interprets dictated numbers as words, not digits; 
## 2) Google Calendar requires event times to be provided as *digits*.
## This script translates event times into digits that Google can understand.
## NOTE: The script  is designed for a 12-hour clock ("7:30 pm" not "19:30").
####################################################################################################

def time2int(text_with_num):

    everything=''
    units = {
        "zero":"0", "oh":"0","one":"1", "two":"2", "three":"3", "four":"4", "five":"5", "six":"6", "seven":"7", "eight":"8",
        "nine":"9", "ten":"10", "eleven":"11","twelve":"12","fifteen":"15","twenty":"20","thirty":"30","forty five":"45",
        "forty":"40","fifty":"50"}
    
    lastWordWasNum = False
    
    for word in text_with_num.split():

        if word not in units:
            everything = everything+" "+word
            lastWordWasNum = False

        elif not lastWordWasNum:
            everything = everything + " "

            everything = everything + units[word]
            lastWordWasNum = True
            lastWord = int(units[word])
           
        else:
            if word in units:
                if (lastWordWasNum & 0 < lastWord <=12):
                    everything = everything+":"+units[word]
                    lastWordWasNum = True 
                    lastWord = int(units[word])                
                    
                elif 0 <= lastWord < 13:
                    everything = everything+units[word]
                    lastWordWasNum = True 
                    lastWord = int(units[word])
                    
                elif lastWord >12 and int(units[word]) >19:
                    everything = everything+units[word]
                    lastWordWasNum = True
                                    
                else:
                    everything = everything[:-1]
                    everything = everything + units[word]
                    lastWordWasNum = True 
               

    return everything.lstrip()