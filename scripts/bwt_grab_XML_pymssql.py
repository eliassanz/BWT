# PASSWORD HAS BEEN REMOVED
# ---------------------------------------------------------------------------
# bwt_grab_XML.py
# Arpil 2010 - Steve
# Revised October 2011 - Steve
# 
#  A rapid prototype script designed to extract border wait times for the 
#  border crossings in San Diego county.
#  it grabs the entire XML at
#  http://apps.cbp.gov/bwt/bwt.xml
#  Just run at command prompt (i.e. C:\>python bwt_grab_XML.py) without args
# ---------------------------------------------------------------------------

import urllib2,sys
import _mssql
from xml.etree import ElementTree as ET

if __name__ == "__main__":
    address = "http://apps.cbp.gov/bwt/bwt.xml"
    xmlText = urllib2.urlopen(address).read()
    element = ET.XML(xmlText)
    

    conn = _mssql.connect(server='shos\shos', user='bwt_app_rw', password='********', database='borderwaittimes')
    
    strSQL = "insert into dbo.border_wait_time_XML (tstamp, xml_doc) values ("
    strSQL += "GETDATE(), CAST('" + ET.tostring(element) + "' as XML))"
    #print strSQL
    conn.execute_non_query(strSQL)
    conn.close()
    
    #for x in bwtRecList:
    #    strSQL = "insert into dbo.border_wait_time_log (tstamp, time_collected, port_name, hours_open, "
    #    strSQL += "cv_max_lanes, cv_std_wait, cv_fast_wait, pv_max_lanes, pv_std_wait, pv_sentri_wait,"
    #    strSQL += "ped_max_lanes, ped_std_wait) values ("
    #    strSQL += "GETDATE(), '" + x.timestamp + "','" +  x.BWTId + "','" + x.HoursOfOperation + "','"
    #    strSQL += x.CommVehMaxLanes + "','" + x.CommVehStdWait + "','" + x.CommVehFastWait + "','"
    #    strSQL += x.PassVehMaxLanes + "','" + x.PassVehStdWait + "','" + x.PassVehSENTRIWait + "','"
    #    strSQL += x.PedMaxLanes + "','" + x.PedStdWait + "')"
    #    conn.execute_non_query(strSQL)
    #    #print strSQL
    #    
    #conn.close()