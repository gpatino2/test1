import requests, json
import urllib3
import sys
import random
import time

from pprint import pprint

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

gHeaders = None
vraServer = 'vra72.gp.local'
userName = 'gpatino@gp.local'
userPwd = 'P@ssw0rd!'
tenant = 'gplab'

##############################################
# Authenticate & return vRA bearer token     #
##############################################
def getvRAToken():

  global gHeaders

  headers = {'Content-Type':'application/json','Accept':'application/json'}

  url = 'https://{}/identity/api/tokens'.format(vraServer)
  
  #print (url)

  #jsonPayload = {"username":"gpatino@gp.local","password":"P@ssw0rd!","tenant":"gplab"}
  jsonPayload = {"username":userName,"password":userPwd,"tenant":tenant}

  data = json.dumps(jsonPayload)
  
  retPayload = requests.post(url, data=data, verify=False, auth="", headers=headers)

  retData = json.loads(retPayload.text)
 
  bToken = "Bearer " + retData['id']
  
  gHeaders = {'Content-Type':'application/json','Accept':'application/json','Authorization':bToken}
  
########################
# Get Catalog Item     #
########################
def getCatalogItem(bpName):

  url = "https://{}/catalog-service/api/consumer/entitledCatalogItemViews?%24filter=name+eq+'{}'".format(vraServer, bpName)
  
  response = requests.get(url, auth="", verify=False, headers=gHeaders)
  
  data = response.json()
  
  #print(data['content'][0]['catalogItemId'])
  
  catItem = data['content'][0]['catalogItemId']
  
  return catItem
  
########################
# Get Template Item    #
########################
def getRequestTemplate(catalogID):

  url = 'https://{}/catalog-service/api/consumer/entitledCatalogItems/{}/requests/template'.format(vraServer, catalogID)
  
  #template = requests.get(url, auth="", verify=False, headers=gHeaders)
  
  template = requests.get(url, headers = gHeaders, verify=False)
  
  template = template.json()
  
  # Get BP component ID
  catData = template['data']
  for dataKey in catData:
     componentID = dataKey
     break

  return (template)

##########################
# Provision Template     #
##########################
def provisionBluePrint(reqTemplate, catalogID):

  url = 'https://{}/catalog-service/api/consumer/entitledCatalogItems/{}/requests'.format(vraServer, catalogID)
 
  #print (url)

  data = json.dumps(reqTemplate)
 
  retPayload = requests.post(url, headers=gHeaders, data=data, verify=False)

  retData = json.loads(retPayload.text) 

  return(retData['id'])  

########################
# Get Request Status   #
########################
def getResquestStatus(requestID):

  url = 'https://{}/catalog-service/api/consumer/requests/{}'.format(vraServer, requestID)
  
  status = requests.get(url, headers = gHeaders, verify=False)
  
  status = status.json()
 
  return (status['state'])

########
# main #
########  
def main():   

    # check command line syntax   
  if (len(sys.argv) < 2):
      print ("Usage:")
      print ("  vraprov2g.py <blueprintname>")
      sys.exit(1) 
  
  # Get command line args
  bluePrint = sys.argv[1]

  getvRAToken()
  #print (vraToken)

  ci = getCatalogItem(bluePrint)
  #print(ci)

  rt = getRequestTemplate(ci)
  #print(json.dumps(rt))
  
  reqID = provisionBluePrint(rt, ci)
  
  reqStatus = getResquestStatus(reqID)
 
  while (True):
    if (reqStatus == "FAILED" or reqStatus == "SUCCESSFUL" or reqStatus == "PROVIDER_FAILED"):
	     break
    reqStatus = getResquestStatus(reqID)		 
    print(reqStatus)
    time.sleep(30)
	
  if (reqStatus == "SUCCESSFUL"):
      print('Deployment {} completed successfully'.format(bluePrint))
  else:
      print('Deployment {} : {}'.format(bluePrint, reqStatus))
      sys.exit(1)	  
	
# Call main()
main()
