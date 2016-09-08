'''
Raspberry pi get rules (Join table) 
from DB by RestfulAPI
'''
import sys
import urllib2, base64

if len (sys.argv) < 2 :
  print("No argv! exit. Please use following argv..." + "\n-username -password -eid -url_con -method")
  exit(1)

def getrules(username, password, eid, url_con, method):
  # url_con = "http://localhost:5000/v1.0/demand/getjoin"
  url_con = url_con + "/" + eid
  opener = urllib2.build_opener(urllib2.HTTPHandler)
  req = urllib2.Request(url_con)

　req.add_header('Content-Type', 'application/json')
  
  req.get_method = lambda: method
  url = opener.open(req)
  JSONResult = url.read()
  JSONResult_decode = JSONResult.decode('utf-8')
  return (JSONResult_decode)

def main(username, password, eid,url_con, method):
  try:
    #"testuser"
    #"testpassword"
    #Rasp01
    #http://140.138.77.98:5000/v1.0/demand/getjoin
    #GET
    data = getrules(username, password, eid, url_con , method)
  except:
    print("Error! Please use following argv..."  + "\n-username -password -eid -url_con -method")
    exit(1)
  return data
