import urllib2,time

# Created for Gon and Lucy
# Getting name data from Korean website for his testing

def little_search(text,start,end):
    if text.find(start)!=-1:
        id1=text.find(start)+len(start)
        id2=text.find(end,id1)
        return text[id1:id2].strip()
    else:
        return "N/A"



fOpen = open("name_ko.txt","r")
fSave = open("testtext.txt","w")

count = 0
line = fOpen.readline()

while line:
    line = line.strip()
    count+=1
    data1 = urllib2.urlopen("http://s.lab.naver.com/translation/?query="+line+"&x=0&y=0&where=name").read()
    eng_name = little_search(data1,'<td class="cell_order">1</td>\n\t\t\t<td class="cell_engname" title="','">')
    print count,
    fSave.write(str(count)+","+eng_name+"\n")
    print " - done ("+eng_name+")"
    line = fOpen.readline()
    """
    if count%100==0:
        print "\n\nSleep for 10 seconds\n\n"
        time.sleep(10)
    else:
        time.sleep(1)
    """
fSave.close()
fOpen.close()



