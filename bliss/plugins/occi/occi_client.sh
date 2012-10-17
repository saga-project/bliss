#!/bin/bash
# FedCloud VM script v0.3


# Define this variable
CERTPATH="/home/matteo/.certs"
CAPATH="/etc/grid-security/certificates"


# Global values
# All VMs are instantiated with the same values
COM_CATEGORY='compute;scheme="http://schemas.ogf.org/occi/infrastructure#";class="kind";'
COM_ATTRIBUTE='occi.core.title="FedCloud Test VM",'
COM_ATTRIBUTE+='occi.core.summary="This a testing VM for FedCloud demo",'
COM_ATTRIBUTE+='occi.compute.architecture="x64",'
COM_ATTRIBUTE+='occi.compute.cores=1,'
COM_ATTRIBUTE+='occi.compute.memory=2'


ask_resources ()
{
	clear
	echo "# FedCloud VM script#"
	echo "Please select a Resource Provider:"
	echo "1) CESGA"
	echo "2) CESNET"
	echo "3) GWDG"
	echo "4) KTH"
	echo "5) CYFRONET"
	echo "6) Exit"
	echo
	echo -n "Enter your selection: "
	read RESOURCE
	echo You typed: "$RESOURCE"
}

ask_management ()
{
	clear
	echo 
	echo "Please select an option:"
	echo "1) List running VMs"
	echo "2) Create a new VM"
	echo "3) Remove a VM"
	echo "4) View specific VM"
	echo "5) Come Back"
	echo
	echo -n "Enter your selection: "
	read MANAGEMENT
	echo You typed: "$MANAGEMENT"
}

RESOURCE=8
while [ $RESOURCE != "6" ]
do
	until [ $RESOURCE -gt 0 -a $RESOURCE -lt 7 ]
	do 
		ask_resources 
	done

	if [[ "$RESOURCE" = "1" || "$RESOURCE" == "CESGA" ]]
	then
		echo "CESGA Resource Provider"
		ENDPOINT="https://meghacloud.cesga.es:3202"
		COM_LINK="</network/6f2e5a0a-8fa2-5578-9fac-539215119801>"';rel="http://schemas.ogf.org/occi/infrastructure#network";category="http://schemas.ogf.org/occi/core#link";,'
		COM_LINK+="</storage/fec277b8-c1a3-5dcb-a764-93bc268cc7a2>"';rel="http://schemas.ogf.org/occi/infrastructure#storage";category="http://schemas.ogf.org/occi/core#link";'

	elif [[ "$RESOURCE" = "2" || "$RESOURCE" == "CESNET" ]]
	then
		echo "CESNET Resource Provider"
		ENDPOINT="https://carach5.ics.muni.cz:10443"
		COM_LINK="</network/d71df087-9a55-5228-822b-1f1a57107851>"';rel="http://schemas.ogf.org/occi/infrastructure#network";category="http://schemas.ogf.org/occi/core#link";,'
		#COM_LINK+="</storage/de48d92c-6288-5a81-bc12-d3f9fedc1ec8>"';rel="http://schemas.ogf.org/occi/infrastructure#storage";category="http://schemas.ogf.org/occi/core#link";'
		COM_LINK+="</storage/a39a1d08-bff8-5a62-ba68-a1cd76bb4511>"';rel="http://schemas.ogf.org/occi/infrastructure#storage";category="http://schemas.ogf.org/occi/core#link";'

	elif [[ "$RESOURCE" = "3" || "$RESOURCE" == "GWDG" ]]
	then
		echo "GWDG Resource Provider"
		ENDPOINT="https://occi.cloud.gwdg.de:3100"
		COM_LINK="</network/d71df087-9a55-5228-822b-1f1a57107851>"';rel="http://schemas.ogf.org/occi/infrastructure#network";category="http://schemas.ogf.org/occi/core#link";,'
		COM_LINK+="</storage/72666675-9e33-55c7-8205-b157e3c8e580>"';rel="http://schemas.ogf.org/occi/infrastructure#storage";category="http://schemas.ogf.org/occi/core#link";'

	elif [[ "$RESOURCE" = "4" || "$RESOURCE" == "KTH" ]]
	then
		echo "KTH Resource Provider"
		ENDPOINT="https://front.redcloud.pdc.kth.se:3043"
		COM_LINK="</network/d71df087-9a55-5228-822b-1f1a57107851>"';rel="http://schemas.ogf.org/occi/infrastructure#network";category="http://schemas.ogf.org/occi/core#link";,'
		COM_LINK+="</storage/68b778b9-1945-51ec-928d-707e3a388675>"';rel="http://schemas.ogf.org/occi/infrastructure#storage";category="http://schemas.ogf.org/occi/core#link";'
		INSECURE="yes"
	elif [[ "$RESOURCE" = "5" || "$RESOURCE" == "CYFRONET" ]]
	then
		echo "CYFRONET Resource Provider"
		ENDPOINT="https://cloud-lab.grid.cyf-kr.edu.pl:3443/"
		COM_LINK="</network/bde75d53-637b-5eba-941c-50bf3305cf48>"';rel="http://schemas.ogf.org/occi/infrastructure#network";category="http://schemas.ogf.org/occi/core#link";,'
		COM_LINK+="</storage/32fc6c92-88aa-54dc-b814-be0df741278e>"';rel="http://schemas.ogf.org/occi/infrastructure#storage";category="http://schemas.ogf.org/occi/core#link";'
	    
	elif [[ "$RESOURCE" = "6" ]]
	then
		echo "Bye bye..."
		exit;
	fi
	RESOURCE=7
	MANAGEMENT=7
	while [ $MANAGEMENT != "5" ];
	do
		until [ $MANAGEMENT -gt 0 -a $MANAGEMENT -lt 6 ]
		do 
		    ask_management 
		done

		if [[ "$MANAGEMENT" = "1" ]]
		then
			# List VMs
			if [[ "$INSECURE" == "yes" ]]
			then
				CURL=$( { curl --sslv3 --insecure --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${ENDPOINT}/compute/; } &)
			else
				CURL=$( { curl --sslv3 --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${ENDPOINT}/compute/ --capath ${CAPATH}; } &)
			fi
			echo
			echo
			echo "List of machines in this resource:"
		#        echo $CURL | sed 's/X-OCCI-Location:/\nMachine:/g' | sed 's/http/https/g' | sed 's/3201/3202/g'
			echo $CURL | sed 's/X-OCCI-Location:/\nMachine:/g'
			echo
			echo

		elif [[ "$MANAGEMENT" = "2" ]]
		then

			# Create a new VM
			if [[ "$INSECURE" == "yes" ]]
			then
				CURL=$( { curl --sslv3 --insecure --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X POST -v ${ENDPOINT}/compute/ --header "Link: $COM_LINK" --header "X-OCCI-Attribute: $COM_ATTRIBUTE" --header "Category: $COM_CATEGORY"; } &)
			else
				CURL=$( { curl --sslv3 --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X POST -v ${ENDPOINT}/compute/ --capath ${CAPATH} --header "Link: $COM_LINK" --header "X-OCCI-Attribute: $COM_ATTRIBUTE" --header "Category: $COM_CATEGORY"; } &)
			fi
			echo
			#echo $CURL | sed 's/http/https/g' | sed 's/3201/3202/g'
			echo $CURL
			echo
			echo
		elif [[ "$MANAGEMENT" = "3" ]]
		then
			# List VMs
			if [[ "$INSECURE" == "yes" ]]
			then
				CURL=$( { curl -s --sslv3 --insecure --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${ENDPOINT}/compute/; } &) 
			else
				CURL=$( { curl -s --sslv3 --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${ENDPOINT}/compute/ --capath ${CAPATH}; } &)
			fi
			echo
			echo
			echo "List of machines to delete in this resource:"
			#echo $CURL | sed 's/X-OCCI-Location:/\nMachine:/g' | sed 's/http/https/g' | sed 's/3201/3202/g'
			echo $CURL | sed 's/X-OCCI-Location:/\nMachine:/g'
			# Remove VM 
			echo
			echo Please write the VM OCCI id to remove it:
			echo -n ${ENDPOINT}"/compute/"
			read ID
			OCCI_ID=${ENDPOINT}"/compute/"${ID}
			echo
			echo You typed: "$OCCI_ID" 
			echo -n "This machine will be removed, are you sure? '(y/n)': "
			read ANSWER
			if [[ "$ANSWER" == "y" ]]
			then
				# Remove VM
				if [[ "$INSECURE" == "yes" ]]
				then
					curl --sslv3 --insecure --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X DELETE -v ${OCCI_ID} 
				else
					curl --sslv3 --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X DELETE -v ${OCCI_ID} --capath ${CAPATH}
				fi
				echo
				echo
			else
				echo OK exiting... 
				exit
			fi


		elif [[ "$MANAGEMENT" = "4" ]]
		then
			# List VMs
			if [[ "$INSECURE" == "yes" ]]
			then
				CURL=$( { curl -s --sslv3 --insecure --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${ENDPOINT}/compute/; } &)
			else
				CURL=$( { curl -s --sslv3 --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${ENDPOINT}/compute/ --capath ${CAPATH}; } &)
			fi
			echo
			echo
			echo "List of machines to view in this resource:"
			#echo $CURL | sed 's/X-OCCI-Location:/\nMachine:/g' | sed 's/http/https/g' | sed 's/3201/3202/g'
			echo $CURL | sed 's/X-OCCI-Location:/\nMachine:/g'
			# View VM status
			echo
			echo Please write the VM OCCI id to view status:
			echo -n ${ENDPOINT}"/compute/"
			read ID
			OCCI_ID=${ENDPOINT}"/compute/"${ID}
			echo
			if [[ "$INSECURE" == "yes" ]]
			then
				CURL=$( { curl --sslv3 --insecure --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${OCCI_ID}; } &)
			else
				CURL=$( { curl --sslv3 --cert ${CERTPATH}/usercert.pem --key ${CERTPATH}/userkey.pem -X GET -v ${OCCI_ID} --capath ${CAPATH}; } &)
			fi
			echo $CURL | grep "X-OCCI-Attribute:" |sed 's/X-OCCI-Attribute:/\n/g'| sed 's/occi.compute.cores=/\n\n CORES: /g'| sed 's/occi.core.title=/TITLE: /g'| sed 's/occi.core.summary=/SUMMARY: /g'| sed 's/opennebula.vm.web_vnc=/WEB VNC LINK: /g'| sed 's/occi.core.id=/ID: /g'| sed 's/opennebula.vm.cpu_reservation=/CPU RESERVATION: /g'| sed 's/opennebula.vm.ip=/IP: /g'| sed 's/occi.compute.memory=/MEMORY: /g'| sed 's/opennebula.vm.vnc=/VNC: /g'| sed 's/occi.compute.state=/STATE: /g'| sed 's/occi.compute.architecture=/ARCHITECTURE: /g'| sed 's/\"//g' | sed 's/opennebula.vm.boot=/BOOT: /g'
			echo
			echo

		elif [[ "$MANAGEMENT" = "5" ]]
		then
		    RESOURCE=7
		    break;
		fi
		echo "Press enter to continue..."
		read
		MANAGEMENT=7 
	done
done

