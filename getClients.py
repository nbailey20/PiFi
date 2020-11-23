#!/usr/bin/env python3

import csv, json

## Retrieve currently connected client MAC addresses via airodump-ng output
def getAllClients(dumpFile, debug):
  ## use csv library on the airodump-ng output file
  with open(dumpFile) as scanFile:
    rows = csv.reader(scanFile)

    if debug:
      print("DEBUG: successfully parsed airodump output file " + dumpFile + " as CSV")

    ## look at rows containing client MAC info - skip first lines
    clientLine = False
    allClients = {}
    for row in rows:
      if len(row) == 0:
        continue 
      if row[0] == "Station MAC":
        clientLine = True
        continue   

      ## gather client MAC address and last seen time to help determine if they are currently connected
      if clientLine:
        ## {MAC: LastSeen, ...}
        allClients[row[0].strip()] = row[2].strip()

    if debug:
      print("DEBUG: read the following information from dump file: " + str(allClients))

    return allClients



## Load previous run client data and save as a list of dict objects of the form {"MAC": , "LastSeen": }
##  If no previous state file, return None
def getPreviousData(stateFile, debug):
  try:
    with open(stateFile) as prevRun:

      ## grab second line, first line is key,value names
      prevRun.readline()
      previousRunString = prevRun.readline().replace("'", '"')
      previousRunData = json.loads(previousRunString)

      if debug:
        print("DEBUG: retrieved previous data: " + str(previousRunData)) + " from statefile " + stateFile

    return previousRunData

  except:
    if debug:
      print("DEBUG: did not find or could not read data from " + stateFile + ", this is normal if running first time")
    return None


## Update old client data with newly gathered information
def updateStateFile(stateFile, data, debug):
  with open(stateFile, "w") as dataFile:
    dataFile.writelines(["Client MAC: LastSeen", "\n"+str(data)])

    if debug:
      print("DEBUG: wrote " + str(data) + " to statefile " + stateFile)
  return


## Calculate current clients by seeing if the last seen time has changed since previous run
##  Return list of currently connected client MAC addresses
def calculateCurrentClients(prevData, newData, debug):
  currClients = []
  for clientMac in newData.keys():
    if debug:
      print("DEBUG: new Client MAC: " + clientMac)

    if clientMac in prevData.keys():
      newLastSeen = newData[clientMac]
      oldLastSeen = prevData[clientMac]
  
      if debug:
        print("DEBUG: client previously seen: prevLastSeen = " + oldLastSeen + ", newLastSeen = " + newLastSeen)

      if newLastSeen != oldLastSeen:
        currClients.append(clientMac) 

  if debug:
    print("DEBUG: calculated current clients: " + str(currClients))
  return currClients


## Retrieve currently connected client MAC addresses via airodump-ng output
##  Connected status is determined by checking if the last seen time has changed since previous run
##  Data saved in client state file to be used next run
def main(debug=False):
  ## load necessary variables from config file
  stateFile = "state"
  dumpFile = "out-01.csv"

  previousRunData = getPreviousData(stateFile, debug) 
  clients = getAllClients(dumpFile, debug)
  updateStateFile(stateFile, clients, debug)

  currentClients = []

  if not previousRunData:
    currentClients = clients
  else:
    currentClients = calculateCurrentClients(previousRunData, clients, debug)

  if debug:
    print("DEBUG: returning current clients: " + str(currentClients))

  return currentClients


    
if __name__ == "__main__":
  main()
