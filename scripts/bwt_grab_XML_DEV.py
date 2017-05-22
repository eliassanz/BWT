# PASSWORD HAS BEEN REMOVED
# ---------------------------------------------------------------------------
# bwt_grab_XML.py
# Arpil 2010 - Steve
# Revised October 2011 - Steve
# Revised October 2013 to run on GISB8 and write to PILA - Pat Landrum
# 
#  A rapid prototype script designed to extract border wait times for the 
#  border crossings in San Diego county.
#  it grabs the entire XML at
#  http://apps.cbp.gov/bwt/bwt.xml
#  Just run at command prompt (i.e. C:\>python bwt_grab_XML.py) without args
# ---------------------------------------------------------------------------

import urllib2,sys
import pyodbc
from xml.etree import ElementTree as ET

if __name__ == "__main__":
    address = "http://apps.cbp.gov/bwt/bwt.xml"
    xmlText = urllib2.urlopen(address).read()
    #xmlText = "<border_wait_time><last_updated_date>2012-8-22</last_updated_date><last_updated_time>6:31:1</last_updated_time><number_of_ports>72</number_of_ports></border_wait_time>"
    element = ET.XML(xmlText)
    
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=pila\SdgIntDb;DATABASE=borderwaittimes_DEV;UID=bwt_app_rw;PWD=**********')
    cursor = conn.cursor()
    
    strSQL = "insert into dbo.border_wait_time_XML2 (xstamp, xml_doc) values ("
    strSQL += "GETDATE(), CAST('" + ET.tostring(element) + "' as XML))"
    #print strSQL
    cursor.execute(strSQL)
    conn.commit()
    conn.close()
    
