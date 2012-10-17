#!/usr/bin/python

import sys
import os
import json
import urllib2
import re
import commands
import getpass
import threading
from stratuslab.Exceptions import InputException, ExecutionException
from stratuslab.ManifestInfo import ManifestInfo
import stratuslab.Util as Util
import time

###
### Define this variables to get your certificates
#path for usercert.pem and userkey.pem files
certpath="~/.globus"
#path for CA's files
capath="/etc/grid-security/certificates/"
###
###

### TIMEOUT is used for debug purposes to limit curl opetation max time
TIMEOUT = 999
###

etree = Util.importETree()

NS_DCTERMS = 'http://purl.org/dc/terms/'

def _parseXml(xmlAsString):
    return etree.fromstring(xmlAsString)


def _extractMetadataInfos(manifestRootElement):
    manifestElements = manifestRootElement.findall('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF')
    manifests = []
    infos = []
    for e in manifestElements:
	manifest = ManifestInfo()
	manifest.parseManifestFromXmlTree(e)
	print manifest
	if len(manifest.locations)>0:
	    info = {'md5': manifest.md5, 'os': manifest.os, 'os-version':manifest.osversion,'os-arch':manifest.arch, 'location':manifest.locations[0], 'creator':manifest.creator, 'valid':manifest.valid.replace("T"," "), 'description':manifest.comment, 'publisher':manifest.publisher, 'identifier':manifest.identifier}
	    #parse extra attributes
	    requires = getattr(e.find('.//{%s}requires' % NS_DCTERMS), 'text','')
	    if requires:
		info['requires'] = requires
		# now is assumed that if network and storage info is the same, so system
		# is openstack else is opennebula, this is done only for demo in Technical Forum
		# for future this info should be taked from LDAP info
		if manifest.locations[0] == requires:
		    # if is a OpenStack machine identifier is not more used, because it doesn't publish it
		    # so we use to identify it from another possible machines running in site
		    # i use the template name https://site:port/template
		    pat = re.compile(r'http[s]{0,1}://[a-z].[a-z][a-z\.\-0-9]*:[0-9]+[a-z.0-9/\-]')
		    domain = re.findall(pat,manifest.locations[0])
		    info['identifier'] = manifest.locations[0].replace(domain[0],"").replace("/","")
		    info['cloud'] = "openstack"
		else:
		    info['cloud'] = "opennebula"
		infos.append(info)
    return infos


def _getMetadataInfo(endpoint):
    url = '%s/metadata' % endpoint 
    metadataEntries = ''
    try:
	metadataEntries = Util.wstring(url)
    except urllib2.HTTPError:
	raise InputException('Failed to find metadata entries: %s' % url)
    return _extractMetadataInfos(_parseXml(metadataEntries))


def menuMain():
    os.system('clear')
    print ("\n\n\n")
    print "\t[1] List Running Machines"
    print "\t[2] Launch Machine"
    print "\t[3] Delete Machine"
    print "\t[4] Exit"
	
	
def menuLaunch(dataList):
    os.system('clear')
    print ("\n\n")
    i=0
    for machine in dataList:
	print "\n\t[",i,"] ",machine["publisher"]," |-| ",machine["description"]
	print "\t\tMachine created by",machine["creator"]," with",machine["os"],machine["os-version"],machine["os-arch"]," is valid until",machine["valid"]
	print "\t\tMachine location: ",machine["location"]
	i+=1
    print "\n\t[",i,"] Back."
    return i


def menuMachines(machines):
    os.system('clear')
    print "\n\n\n"
    i=0
    for machine in machines:
	if 'title' in machine:
	    print "\t[",i,"] ",machine['title']," running in ",machine['endpoint']," with ",machine['framework']," framework"
	if 'summary' in machine:
	    print "\t\t",machine['summary']
        ips = ""
        if 'floating_ip' in machine:
            ips += "\t\tFloating IP:" + machine['floating_ip']
	if 'ip' in machine:
            ips += "\t\tIP:" + machine['ip']
        if ips != "":
            print ips
	dates = ""
	if 'cores' in machine:
	    dates += "\t\tNumber of cores:"+machine['cores']
	if 'memory' in machine:
	    dates += " Memory:"+machine['memory']
	if 'architecture' in machine:
	    dates += " Architecture:"+machine['architecture']
	print dates
	if 'status' in machine:
	    print "\t\tStatus: ",machine['status']," with OCCI id: ",machine['occi_id']
	if 'vncweb' in machine:
	    print "\t\tVNC web link: ",machine['vncweb']
	print ""
	i+=1
    if len(machines)==0:
	print "\n\t\tThere is not any machine running yet."
    return i
    

def machineLaunch(metadataList):
    numberMachines=menuLaunch(metadataList)
    key=-1
    numList=[]
    numbs=raw_input("\n\t - Enter a list of number machine separated by commas (,) : ").split(",")
    for i in numbs:
	try:
	    numbs2=int(i)
	    numList.append(numbs2)
	except ValueError:
	    print "\n\t - Value ",i," is incorrect. Ignoring ..."  
	    raw_input('\n\n\n\tPress enter to continue...')

    for key in numList:
	if key>=0 and key<numberMachines:
	    os.system('clear')
	    print "\n\n ****** Launching machine ",metadataList[key]["location"],"\n"
	    print " ****** Network ",metadataList[key]["requires"],"\n"
	    #compute value is not present in xml info, so it must be calculate from location or requires
	    pat = re.compile(r'http[s]{0,1}://[a-z].[a-z][a-z\.\-0-9]*:[0-9]+')
	    endpoint = re.findall(pat,metadataList[key]["location"])
	    print " ****** Compute: ",endpoint[0]
	    
	    if metadataList[key]["cloud"] == "opennebula":
		#create necessary values for curl command
		comCategory = 'compute;scheme="http://schemas.ogf.org/occi/infrastructure#";class="kind";'	    
		comAttribute = "occi.core.title="+"\"FedCloud Testing:"+metadataList[key]["identifier"]+"\","
		comAttribute += "occi.core.summary=\""+metadataList[key]["description"]+"\","
		comAttribute += "occi.compute.architecture=\"x64\","
		comAttribute += "occi.compute.cores=1,"
		comAttribute += "occi.compute.memory=2"

		#comLink = "<"+metadataList[key]["requires"].replace(endpoint[0],'')+">"+";rel=\"http://schemas.ogf.org/occi/infrastructure#network\";category=\"http://schemas.ogf.org/occi/core#link\";,"
		comLink = "<"+metadataList[key]["requires"].replace(endpoint[0],'')+">"+";rel=\"http://schemas.ogf.org/occi/infrastructure#network\";category=\"http://schemas.ogf.org/occi/infrastructure#networkinterface\";,"
		#comLink += "<"+metadataList[key]["location"].replace(endpoint[0],'')+">"+";rel=\"http://schemas.ogf.org/occi/infrastructure#storage\";category=\"http://schemas.ogf.org/occi/core#link\";"
		comLink +="<"+metadataList[key]["location"].replace(endpoint[0],'')+">"+";rel=\"http://schemas.ogf.org/occi/infrastructure#storage\";category=\"http://schemas.ogf.org/occi/infrastructure#storagelink\";"
            
		found=0
		if len(insecures) > 0:
		    for site in insecures:
			if endpoint[0].find(site) != -1:
			    instantiate="curl -s --sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -X POST -v "+endpoint[0]+"/compute/ --header \'Link: "+comLink+"\' --header \'X-OCCI-Attribute: "+comAttribute+"\' --header \'Category: "+comCategory+"\'"
			    found = 1
			    break
		if found == 0:
		    instantiate="curl -s --sslv3 --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -X POST -v "+endpoint[0]+"/compute/ --capath "+capath+" --header \'Link: "+comLink+"\' --header \'X-OCCI-Attribute: "+comAttribute+"\' --header \'Category: "+comCategory+"\'"
		
		if debug == 1: print "Launched:",instantiate.replace(passwd,"xxxxxx")
		status, result = commands.getstatusoutput(instantiate)
		
		if result.find('Status: 20') != -1:
		    if debug == 1: print result
		    print "\n\n ****** Machine ",metadataList[key]["identifier"]," launched in ",endpoint[0]," correctly."
		    pat = re.compile(r'http[s]{0,1}://[a-z].[a-z][a-z\.\-0-9]*:[0-9]+[a-z.0-9/\-]*')
		    link = re.findall(pat,result)
		    print "\t  Link to machine: ",link[0]
		else: 
		    if debug == 1: print result
		    print "\n\t\tError launching selected machine."
		raw_input('\n\n\n\tPress enter to continue...')
	    else: #if not opennebula create openstack values
		#create necessary values for curl command
		headers = " -H 'Category: compute; scheme=\"http://schemas.ogf.org/occi/infrastructure#\"; class=\"kind\"' -H 'Category: m1.tiny; scheme=\"http://schemas.openstack.org/template/resource#\"; class=\"mixin\"' -H 'Category: "
		headers += metadataList[key]["identifier"]
		headers += "; scheme=\"http://schemas.openstack.org/template/os#\"; class=\"mixin\"'"
		found=0
		if len(insecures) > 0:
		    for site in insecures:
			if endpoint[0].find(site) != -1:
			    instantiate="curl -v -s --sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X POST "+endpoint[0]+headers
			    found = 1
			    break
		if found == 0:
		    instantiate="curl -s --sslv3 --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X POST -v "+endpoint[0]+headers
		
		if debug == 1: print "Launched:",instantiate.replace(passwd,"xxxxxx")
		status, result = commands.getstatusoutput(instantiate)
		
		if result.find('Created') != -1:
		    if debug == 1: print result
		    print "\n\n ****** Machine ",metadataList[key]["identifier"]," launched in ",endpoint[0]," correctly."
		    pat = re.compile(r'http[s]{0,1}://[a-z].[a-z][a-z\.\-0-9]*:[0-9]+[a-z.0-9/\-]*')
		    link = re.findall(pat,result)
		    print "\t  Link to machine: ",link[0]

                    # Wait a tiny bit to allow for a fixed_ip to be
                    # associated.  Without a fixed_ip, the allocation
                    # and association of the floating IP will fail
                    time.sleep(2)

                    ## Allocate a floating IP
                    alloc_ip_headers = " -H 'Category: alloc_float_ip; scheme=\"http://schemas.openstack.org/instance/action#\"; class=\"action\"; title=\"Allocate a floating IP to the compute resource.\"'"
                    alloc_ip_headers += " -H 'X-OCCI-Attribute: org.openstack.network.floating.pool=\"public_ips\"'"

                    if len(insecures) > 0:
                        for site in insecures:
                            if endpoint[0].find(site) != -1:
                                alloc_ip="curl -v -s --sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X POST " +link[0]+"?action=alloc_float_ip"+alloc_ip_headers
                                found = 1
                                break
                    if found == 0:
                        alloc_ip = "curl -s --sslv3 --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X POST -v "+link[0]+"?action=alloc_float_ip"+alloc_ip_headers

                    if debug == 1: print alloc_ip.replace(passwd,"xxxxxx")
                    alloc_ip_status, alloc_ip_result = commands.getstatusoutput(alloc_ip)
                    if debug == 1: print alloc_ip_result
		else: 
		    if debug == 1: print result
		    print "\n\t\tError launching selected machine."
		raw_input('\n\n\n\tPress enter to continue...')
		
	if key==numberMachines: 
	    break
	
def checkMachine(machine,validMachines):
    pat = re.compile(r'http[s]{0,1}://[a-z0-9].[a-z][a-z\.\-0-9]*:[0-9]+')
    endpoint = re.findall(pat,machine["location"])
    #check that endpoint/compute has at least one "X-OCCI-Location:" running, else don't do nothing
    #usefull also to check that user running script has appropiate cerficate
    if machine["cloud"] == "opennebula":
	found=0
	if len(insecures) > 0:
	    for site in insecures:
		if endpoint[0].find(site) != -1:
		    checkRunning = "curl -s -sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0]+"/compute/ | awk \'{ print $1 }\'"
		    found = 1
		    break
	if found == 0:
	    checkRunning = "curl -s --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0]+"/compute/ --capath "+capath+" | awk \'{ print $1 }\'"
	if debug == 1: print "Launched:",checkRunning.replace(passwd,"xxxxxx")
	status, checkResult = commands.getstatusoutput(checkRunning)
        if debug == 1: print "Returned:\n", checkResult
	if checkResult.find("X-OCCI-Location:") != -1:
	    found=0
	    if len(insecures) > 0:
		for site in insecures:
		    if endpoint[0].find(site) != -1:
			runningMachines = "curl -s --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0]+"/compute/ | awk \'{ print $2 }\'"
			found = 1
			break
	    if found == 0:
		runningMachines = "curl -s --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0]+"/compute/ --capath "+capath+" | awk \'{ print $2 }\'"
	    if debug == 1: print "Launched:",runningMachines.replace(passwd,"xxxxxx")
	    status, machines = commands.getstatusoutput(runningMachines)
            if debug == 1: print "Returned:\n", machines
	    listMachines = machines.splitlines()
	    
	    for m in listMachines:
		found=0
		if len(insecures) > 0:
		    for site in insecures:
			if endpoint[0].find(site) != -1:
			    comm = "curl -s --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+m
			    found = 1
			    break
		if found == 0:
		    comm = "curl -s --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem --capath "+capath+" "+m
		if debug == 1: print "Launched:",comm.replace(passwd,"xxxxxx")
		status, occiValues = commands.getstatusoutput(comm)
                if debug == 1: print "Returned:\n", occiValues
		##only must be saved/showed valid machines for fedcloud or by user, attending occi values
		machineValues = occiValues.splitlines()
		info = {}
		for m in machineValues:
		    if m.find("X-OCCI-Attribute") != -1:
			if m.find("occi.core.title=") != -1:
			    info['title']=m.replace("X-OCCI-Attribute: occi.core.title=","").replace("\"","")
			if m.find("occi.core.summary=") != -1:
			    info['summary']=m.replace("X-OCCI-Attribute: occi.core.summary=","").replace("\"","")
			if m.find("opennebula.vm.ip=") != -1:
			    info['ip']=m.replace("X-OCCI-Attribute: opennebula.vm.ip=","").replace("\"","")
			if m.find("opennebula.vm.web_vnc=") != -1:
			    info['vncweb']=m.replace("X-OCCI-Attribute: opennebula.vm.web_vnc=","").replace("\"","")
			if m.find("occi.compute.cores=") != -1:
			    info['cores']=m.replace("X-OCCI-Attribute: occi.compute.cores=","").replace("\"","")
			if m.find("occi.compute.memory=") != -1:
			    info['memory']=m.replace("X-OCCI-Attribute: occi.compute.memory=","").replace("\"","")
			if m.find("occi.compute.architecture=") != -1:
			    info['architecture']=m.replace("X-OCCI-Attribute: occi.compute.architecture=","").replace("\"","")
			if m.find("occi.core.id=") != -1:
			    info['occi_id']=m.replace("X-OCCI-Attribute: occi.core.id=","").replace("\"","")
			if m.find("X-OCCI-Attribute: occi.compute.state=") != -1:
			    info['status']=m.replace("X-OCCI-Attribute: occi.compute.state=","").replace("\"","")
                if debug == 1: print "Looking for:\n", machine["identifier"]
                if debug == 1: print "Looking in:\n", info['title']
	        if 'title' in info and info['title'].find(machine["identifier"]) != -1:
                    if debug == 1: print "Found!"
		    info['endpoint']=endpoint[0]
		    info['framework']="OpenNebula"
		    validMachines.append(info)
    else:#if not opennebula
	found=0
	if len(insecures) > 0:
	    for site in insecures:
		if endpoint[0].find(site) != -1:
		    checkRunning = "curl -s -sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0]+"/compute/ -H 'Content-Type: text/occi'| awk \'{ print $1 }\'"
		    found = 1
		    break
	if found == 0:
	    checkRunning = "curl -s --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0]+"/compute/ -H 'Content-Type: text/occi' --capath "+capath+" | awk \'{ print $1 }\'"
	if debug == 1: print "Launched:",checkRunning.replace(passwd,"xxxxxx")
	
	status, checkResult = commands.getstatusoutput(checkRunning)
	if checkResult.find("X-OCCI-Location:") != -1:
	    found=0
	    if len(insecures) > 0:
		for site in insecures:
		    if endpoint[0].find(site) != -1:
			runningMachines = "curl -s -m "+str(TIMEOUT)+" --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0].replace("8787","8788")+"/compute/ -H 'Content-Type: text/occi' | grep -v \"^$\" | awk \'{ print $2 }\'"
			found = 1
			break
	    if found == 0:
		runningMachines = "curl -s -m "+str(TIMEOUT)+" --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+endpoint[0].replace("8787","8788")+"/compute/ --capath "+capath+" -H 'Content-Type: text/occi' | grep -v \"^$\" | awk \'{ print $2 }\'"
	    if debug == 1: print "Launched:",runningMachines.replace(passwd,"xxxxxx")
	    status, machines = commands.getstatusoutput(runningMachines)
	    listMachines = machines.splitlines()
	    
	    for m in listMachines:
		found=0
		if len(insecures) > 0:
		    for site in insecures:
			if endpoint[0].find(site) != -1:
			    comm = "curl -s -m "+str(TIMEOUT)+" --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem "+m.replace("http:","https:").replace("8787","8788")+" -H 'Content-Type: text/occi'"
			    found = 1
			    break
		if found == 0:
		    comm = "curl -s -m "+str(TIMEOUT)+" --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem --capath "+capath+" "+m.replace("http:","https:").replace("8787","8788")+" -H 'Content-Type: text/occi'"
		if debug == 1: print "Launched:",comm.replace(passwd,"xxxxxx")
		status, occiValues = commands.getstatusoutput(comm)
		##only must be saved/showed valid machines for fedcloud or by user, attending occi values
		machineValues = occiValues.splitlines()
		info = {}
		error = 0
		if len(machineValues) == 0:
		    error = 1
		for m in machineValues:
		    if m.find("VM not found!") != -1:
			error = 1
		    if m.find("template/os") != -1:
			pat = re.compile(r'Category:.[^;]*')
			tit = re.findall(pat,m)
			info['title'] = tit[0].replace("Category:","").replace("\"","")
			pat = re.compile(r'title=\".[^\"]*\"')
			summ = re.findall(pat,m)
			info['summary'] = summ[0].replace("title=","").replace("\"","")
		    if m.find("/network/") != -1:
			pat = re.compile(r'occi.networkinterface.address=\"[0-9.^;]*\"')
			ip = re.findall(pat,m)
			info['ip'] = ip[0].replace("occi.networkinterface.address=","").replace("\"","")
                    if m.find("X-OCCI-Attribute: org.openstack.network.floating.ip=") != -1:
                        info['floating_ip']=m.replace("X-OCCI-Attribute: org.openstack.network.floating.ip=", "").replace("\"", "")
		    if m.find("/console/vnc/") != -1:
			pat = re.compile(r'occi.core.target=\".[^\"]*\"')
			vnc = re.findall(pat,m)
			info['vncweb'] = endpoint[0]+vnc[0].replace("occi.core.target=","").replace("\"","")
		    if m.find("occi.compute.cores=") != -1:
			info['cores'] = m.replace("X-OCCI-Attribute: occi.compute.cores=","").replace("\"","")
		    if m.find("occi.compute.memory=") != -1:
			info['memory'] = m.replace("X-OCCI-Attribute: occi.compute.memory=","").replace("\"","")
		    if m.find("occi.compute.architecture=") != -1:
			info['architecture'] = m.replace("X-OCCI-Attribute: occi.compute.architecture=","").replace("\"","")
		    if m.find("occi.core.id=") != -1:
			info['occi_id'] = m.replace("X-OCCI-Attribute: occi.core.id=","").replace("\"","")
		    if m.find("occi.compute.state=") != -1:
			info['status'] = m.replace("X-OCCI-Attribute: occi.compute.state=","").replace("\"","")
		if error == 0:
		    if 'title' in info and info['title'].find(machine["identifier"]) != -1:
			info['endpoint']=endpoint[0]
			info['framework']="OpenStack"
			validMachines.append(info)    


def machineList(metadataList):
    os.system('clear')
    print "\n\n\n"
    print "\t\tLooking for valid fedcloud machines running....\n"
    validMachines = []
    info = []
    threads = [] 
    for machine in metadataList:
        checkMachine(machine,validMachines)
	#t = threading.Thread(target=checkMachine, args=(machine,validMachines))
	#threads += [t]
	#t.start()
    #for x in threads: 
	#x.join()
    return validMachines


def machineDelete(machines):
    #TODO: check user dn and try to show only machines matching dn
    numberMachines=menuMachines(machines)
    print "\n\t[",numberMachines,"] Back."
    key=-1
    numList=[]
    numbs=raw_input("\n\t - Enter a list of number machine separated by commas (,) : ").split(",")
    for i in numbs:
	try:
	    numbs2=int(i)
	    numList.append(numbs2)
	except ValueError:
	    print "\n\t - Value ",i," is incorrect. Ignoring ..."  
	    raw_input('\n\n\n\tPress enter to continue...')  

    for key in numList:
	if key>=0 and key<numberMachines:
	    os.system('clear')
	    print "\n\nDeleting machine: ", machines[key]['endpoint']+machines[key]['occi_id']
	    if machines[key]['framework'] == "OpenNebula":
		found=0
		if len(insecures) > 0:
		    for site in insecures:
			if machines[key]['endpoint'].find(site) != -1:
			    instantiate="curl -s --sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -X DELETE -v "+machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']
			    found = 1
			    break
		if found == 0:
		    instantiate="curl -s --sslv3 --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -X DELETE -v "+machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']+" --capath "+capath
		if debug == 1: print "Launched:",instantiate.replace(passwd,"xxxxxx")
		status, result = commands.getstatusoutput(instantiate)
		
		if result.find('Status: 20') != -1:
		    if debug == 1: print result
		    print "\n\n ****** Machine ",machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']," deleted correctly."
		else: 
		    if debug == 1: print result
		    print "\n\t\tError deleting selected machine."
		raw_input('\n\tPress enter to continue')
	    else: # We're talking to an OS instance
		found=0
		if len(insecures) > 0:
		    for site in insecures:
			if machines[key]['endpoint'].find(site) != -1:
                            dealloc_floating_ip="curl -v -s --sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X POST -H 'Category: dealloc_float_ip; scheme=\"http://schemas.openstack.org/instance/action#\"; class=\"action\"' "+machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']+"?action=dealloc_float_ip"
			    instantiate="curl -v -s --sslv3 --insecure --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X DELETE "+machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']
			    found = 1
			    break
		if found == 0:
                    dealloc_floating_ip="curl -s --sslv3 --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X POST -H 'Category: dealloc_float_ip; scheme=\"http://schemas.openstack.org/instance/action#\"; class=\"action\"' "+machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']+"?action=dealloc_float_ip --capath "+capath
                    instantiate="curl -s --sslv3 --cert "+certpath+"/usercert.pem:"+passwd+" --key "+certpath+"/userkey.pem -H 'Content-Type: text/occi' -X DELETE "+machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']+" --capath "+capath
                if debug == 1: print "Launched:",dealloc_floating_ip.replace(passwd,"xxxxxx")
                dealloc_floating_ip_status, dealloc_floating_ip_result = commands.getstatusoutput(dealloc_floating_ip)
		if debug == 1: print "Launched:",instantiate.replace(passwd,"xxxxxx")
		status, result = commands.getstatusoutput(instantiate)
		
		if result.find('OK') != -1:
		    if debug == 1: print result
		    print "\n\n ****** Machine ",machines[key]['endpoint']+"/compute/"+machines[key]['occi_id']," deleted correctly."
		else: 
		    if debug == 1: print result
		    print "\n\t\tError deleting selected machine."
		raw_input('\n\tPress enter to continue')
		
	if key==numberMachines: 
	    break
	    

def loadCertPasswd():
    os.system('clear')
    print ("\n\n\n Your passwd will be stored only in memory for this script running, to avoid ask many times. It will not be stored in any file.\n\n\n")
    valid = 0
    i = 0
    while valid == 0 and i < 5:
	p = getpass.getpass("\t - Insert userkey.pem password:")
	#status, result = commands.getstatusoutput("curl -s -S --insecure --cert usercert.pem:"+p+" --key userkey.pem https://meghacloud.cesga.es:3202")
	status, result = commands.getstatusoutput("openssl rsa -in "+certpath+"/userkey.pem -passin pass:"+p+" -check")
	if status == 0:
	    valid = 1
	    break
	i +=1
	print "\t\t\tWrong password, try number ",i,"\n"
    if i == 5:
	print "\n\n\n - Too many tries with wrong password.\n\n\tExiting ... \n\n"
	sys.exit()
    return p    

    
    
def usage():
    print "\n\tUsage: fedcloud.py <marketplace-endpoint> [--insecure=<site1,site2,site3> [--debug]"
    print "\t\tExample: python fedcloud.py http://marketplace.egi.eu --insecure=site1.com,site2.com --debug"
    exit(1)    


#main program
if (len(sys.argv) < 2):
    usage()
else:
    #checking args passed
    debug=0
    insecures=[]
    if len(sys.argv) > 2:
	if sys.argv[2].find("--insecure=") != -1:
	    insecures=sys.argv[2].replace("--insecure=","").split(",")
	    if len(sys.argv) > 3:
		if sys.argv[3] == "--debug":
		    debug=1
		else:
		    usage()
	else:
	    if sys.argv[2] == "--debug":
		debug=1
	    else:
		usage()
    ## 
    metadataList = _getMetadataInfo(sys.argv[1])
    passwd=loadCertPasswd()
    op = 1
    key=-1    
    while op>0 and op<5:
	menuMain()
	try:
	    key=int(raw_input('\n\t - Input one option above: '))
	except ValueError:
	    print "*-*-* You must enter a number *-*-*"
	    continue
	if key == 1:
	    menuMachines(machineList(metadataList))
	    raw_input('\n\tPress enter to continue')
	if key == 2:
	    machineLaunch(metadataList)
	if key == 3:
	    machineDelete(machineList(metadataList))
	if key == 4:
	    break
