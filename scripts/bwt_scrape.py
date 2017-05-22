# PASSWORD HAS BEEN REMOVED
# ---------------------------------------------------------------------------
# bwt_scrape.py
# Arpil 2010 - Steve
# 
#  A rapid prototype script designed to extract border wait times for the 
#  border crossings in San Diego county.
#  it scrapes: http://apps.cbp.gov/bwt/
#  Just run at command prompt (i.e. C:\>python bwt_scrape.py) without args
# ---------------------------------------------------------------------------

from BeautifulSoup import BeautifulSoup,NavigableString
import urllib2,sys
import re
from time import *
import _mssql

GlobalSubName = ''


    

def removeExcessiveSpaces(t):
    tList = t.split(' ')
    newList = []
    newString = ''
    
    for x in tList:
        if len(x) > 0:
            newList.append(x)
            
    for x in newList:
        newString = newString + ' ' + x
        
    newString = newString.strip()
    return newString

def makeColVal(t):
    newString = ''
    for x in t:
        if x.__class__ == NavigableString:
            #print str(x).strip()
            colVal = str(x).strip()
            colVal = colVal.replace('\n', '')
            colVal = colVal.replace('\r', '')
            colVal = removeExcessiveSpaces(colVal)
            newString = newString + ' ' + colVal
    newString = newString.strip()
    return newString                

def returnText(tags):
    global GlobalSubName
    for tag in tags:
	if tag.__class__ == NavigableString:
	    GlobalSubName = GlobalSubName + tag
	else:
	    returnText(tag)
    

def printText(tags):
	for tag in tags:
		if tag.__class__ == NavigableString:
			print tag
		else:
			printText(tag)
		
class BWTRec: pass
if __name__ == "__main__":
	address = "http://apps.cbp.gov/bwt/"
	#address = "D:\bwt\html\bwt2.html"
	#html = open('D:\\bwt\\html\\bwt2.html', 'r')
	html = urllib2.urlopen(address).read()
	badString = ""
	bcList = ["Otay", "Ysidro", "Tecate", "Calexico", "Andrade"] #["Ysidro", "Tecate"]
	colList = ["pc_id hrs", "cv maxcv", "cv stdcv",
	         "cv xcv", "pv maxpv", "pv stdpv",
		 "pv xpv", "ped maxped", "ped stdped"]
		
	
	#html = open('D:\\bwt\\html\\bwt2.html', 'r')
	
	
	soup = BeautifulSoup(html)
	
	bwtRecList = []
			
	for bc in bcList:

		
		searchResults = soup.findAll(text=re.compile(bc))
		for searchResult in searchResults:
		    bwtrec = BWTRec()
		    bwtrec.BWTId = bc
		    bwtrec.timestamp =  strftime("%m/%d/%Y - %H:%M:%S %p %Z", localtime())
		    bwtrec.HoursOfOperation = ''
		    bwtrec.CommVehMaxLanes = ''
		    bwtrec.CommVehStdWait = ''
		    bwtrec.CommVehFastWait = ''
		    bwtrec.PassVehMaxLanes = ''
		    bwtrec.PassVehStdWait = ''
		    bwtrec.PassVehSENTRIWait = ''
		    bwtrec.PedMaxLanes = ''
		    bwtrec.PedStdWait = ''		    
		    subName = ''
		    GlobalSubName = ''
		    if len(searchResults) > 1:
			subNameResults = searchResult.findNext('span')
			returnText(subNameResults)
			subName = GlobalSubName

		    recSet = searchResult.findPrevious('tr')
		    #print "=====================================" + bc + "====" + subName
		    if len(subName) > 0:
			bwtrec.BWTId = bc + "-" + subName
		    else:
			bwtrec.BWTId = bc

		    # Get HOURS - pc_id hrs
		    rec = recSet.find('td', attrs={'headers' : 'pc_id hrs'})
		    #print "--HOURS-- " + makeColVal(rec)
		    bwtrec.HoursOfOperation = makeColVal(rec)
                  
		    # Get CV Max Lns - cv maxcv
		    rec = recSet.find('td', attrs={'headers' : 'cv maxcv'})
		    #print "--CV Max Lns-- " + makeColVal(rec)
		    bwtrec.CommVehMaxLanes = makeColVal(rec)
                
		    # Get CV Std Wait - cv stdcv
		    rec = recSet.find('td', attrs={'headers' : 'cv stdcv'})
		    #print "--CV Std Wait-- " + makeColVal(rec)
		    bwtrec.CommVehStdWait = makeColVal(rec)
                 
		    # Get CV Fast Wait - cv xcv
		    rec = recSet.find('td', attrs={'headers' : 'cv xcv'})
		    #print "--CV Fast Wait-- " + makeColVal(rec)
		    bwtrec.CommVehFastWait = makeColVal(rec)
                
		    # Get Pass Max Lns - pv maxpv
		    rec = recSet.find('td', attrs={'headers' : 'pv maxpv'})
		    #print "--Pass Max Lns-- " + makeColVal(rec)
		    bwtrec.PassVehMaxLanes = makeColVal(rec)
		    
		    # Get Pass Std Wait - pv stdpv
		    rec = recSet.find('td', attrs={'headers' : 'pv stdpv'})
		    #print "--Pass Std Wait-- " + makeColVal(rec)
		    bwtrec.PassVehStdWait = makeColVal(rec)
		    
		    # Get Pass SENTRI Wait - pv xpv
		    rec = recSet.find('td', attrs={'headers' : 'pv xpv'})
		    #print "--Pass SENTRI Wait-- " + makeColVal(rec)
		    bwtrec.PassVehSENTRIWait = makeColVal(rec) 
                
		    # Get Ped Max Lns - ped maxped
		    rec = recSet.find('td', attrs={'headers' : 'ped maxped'})
		    #print "--Ped Max Lns-- " + makeColVal(rec)
		    bwtrec.PedMaxLanes = makeColVal(rec) 
		    
		    # Get Ped Std Wait - ped stdped
		    rec = recSet.find('td', attrs={'headers' : 'ped stdped'})
		    #print "--Ped Std Wait-- " + makeColVal(rec)
		    bwtrec.PedStdWait = makeColVal(rec)
		    bwtRecList.append(bwtrec)
	
	conn = _mssql.connect(server='shos\shos', user='bwt_app_rw', password='********', database='borderwaittimes')
	for x in bwtRecList:
	    strSQL = "insert into dbo.border_wait_time_log (tstamp, time_collected, port_name, hours_open, "
	    strSQL += "cv_max_lanes, cv_std_wait, cv_fast_wait, pv_max_lanes, pv_std_wait, pv_sentri_wait,"
	    strSQL += "ped_max_lanes, ped_std_wait) values ("
	    strSQL += "GETDATE(), '" + x.timestamp + "','" +  x.BWTId + "','" + x.HoursOfOperation + "','"
	    strSQL += x.CommVehMaxLanes + "','" + x.CommVehStdWait + "','" + x.CommVehFastWait + "','"
	    strSQL += x.PassVehMaxLanes + "','" + x.PassVehStdWait + "','" + x.PassVehSENTRIWait + "','"
	    strSQL += x.PedMaxLanes + "','" + x.PedStdWait + "')"
	    conn.execute_non_query(strSQL)
	    #print strSQL
	    
	conn.close()    