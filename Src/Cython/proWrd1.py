import time


def Filter(item):
    lists = []
    item = str(item).split(" ")
    for r in item :
        q = ""
        for w in r:
            if w == "\n" and r == item[0]:
                continue
            elif w == "\n" and r == item[(len(item)-1)]:
                continue
            else:
                q = q + w
        lists.append(q)
    wrd = ""
    for i in range(len(lists)):
        if lists[i] == "" or lists[i] == " ":
            continue
        elif lists[i] == "\n" and lists[(i-1)] == "" :
            n= 0
            for e in range(0,i):
                if lists[e] != "":
                    n=n+1
                    if n > 0 and n <= 1 : 
                        wrd = wrd + lists[i]
                    else :
                        continue
                else :
                    continue
            continue
        elif lists[i] == "\n" and lists[(i+1)] == "" :
            n = 0
            for e in range(i,len(lists)):
                if lists[e] != "":
                    n= n + 1
                    if n > 0 and n <= 1 :
                        wrd = wrd + lists[i]
                    else :
                        continue
                else :
                    continue
            continue
        else :
            wrd = wrd + lists[i] +" "
    wrd = wrd[:(len(wrd)-1)]
    return wrd
def getTimetuple(stamp = None):
    if stamp == None :
        return time.localtime()
    return time.strptime(stamp)

def getTimeStamp(tuple = None):
    if tuple == None :
        return time.asctime()
    return time.asctime(tuple)

def InvoiceSplit(item):
    invoices = item.split(",")
    length = len(invoices)
    l = []
    for i in range(0, len(length)) :
        if invoices[i].isdigit() == True :
            l.append(invoices[i])
    return l

