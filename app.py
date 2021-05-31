#!/usr/bin/python
import ispapi  # https://wiki.hexonet.net/wiki/SDKs#PYTHON_Library
import os
import sys
import urllib2
import logging
import time

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)

DDNS_HOSTNAME=os.getenv("DDNS_HOSTNAME","")
SLEEP_TIMER=14400
ISPAPI_API=os.getenv("ISPAPI_API","https://api.ispapi.net/api/call.cgi")
ISPAPI_ENTITY=os.getenv("ISPAPI_ENTITY","1234") # Defaults to 1234 for OT&E
ISPAPI_USER=os.getenv("ISPAPI_USER","test.user")
ISPAPI_PASS=os.getenv("ISPAPI_PASS","test.passw0rd")

# Hostname
if not DDNS_HOSTNAME:
    logging.error('No DynDNS Hostname given. Nothing to do here, mate...')
    sys.exit(1)

def getPublicIP():
    # We're getting our public IP by HTTP GET-ing api.ispapi.net.
    # HEXONET's API is a friendly one and answers our request with
    # the source IP it's coming from.
    try:
        return urllib2.urlopen("%s://%s" % (ISPAPI_API.split("://")[0],ISPAPI_API.split("//")[-1].split("/")[0].split('?')[0])).read().splitlines()[1].split()[4]
    except Exception as e:
        logging.warning('Problem getting public IP: %s' % e)
        sys.exit(1)

def ispapiConnect():
    try:
        api = ispapi.connect(
            url = ISPAPI_API,
            entity = ISPAPI_ENTITY,
            login = ISPAPI_USER,
            password = ISPAPI_PASS
        )
        return api
    except Exception as e:
        logging.warning('Problem connecting to the API: %s' % e)
        sys.exit(1)

def getRRs(api,dnszone):
    # Lookup current IP for your desired hostname
    response = api.call({
       'COMMAND': "QueryDNSZoneRRList",
       'DNSZONE' : dnszone,
       'SHORT': 1
    })

    result = response.as_hash()

    # Shit hit the fan
    if result['CODE'] != 200:
        logging.warning('Settings Problem: %s' % result['DESCRIPTION'])
        sys.exit(1)

    return result

def getDomainParts(DDNS_HOSTNAME):
    parts = {"dnszone":"","subdomain":""}
    host = DDNS_HOSTNAME.split('.')

    if len(host) == 2:
        # Only a domain, no subdomain
        parts['dnszone'] = DDNS_HOSTNAME+"."
        parts['subdomain'] = "@"
    else:
        parts['subdomain'] = host[0]
        host.pop(0)
        parts['dnszone'] = ".".join(host)+"."
    return parts


def main():
    extIP = getPublicIP()
    curIP = "0.0.0.0"
    api = ispapiConnect()
    getDomainParts(DDNS_HOSTNAME)

    # Split Hostname
    p = getDomainParts(DDNS_HOSTNAME)
    print p

    host = DDNS_HOSTNAME.split('.')
    dnszone = host[len(host)-2]+"."+host[len(host)-1]+"."
    subdomain = host[0]

    # Get all the records of this zone
    rrs = getRRs(api,p['dnszone'])

    e = 0
    for rr in rrs['PROPERTY']['RR']:
        data = rr.split(' ')
        print data

        # Check if an A-Record for the given subdomain exists
        if str(data[0]) == p['subdomain'] and str(data[3]) == "A":
            e = 1 # Current IP exists
            logging.info("Given Subdomain '%s' exists in DNS Zone '%s'" % (p['subdomain'],p['dnszone']))

            curIP = data[4].rstrip()
            if (str(curIP) != str(extIP)):
                # Delete Current Record
                response = api.call({
                   'COMMAND': "UpdateDNSZone",
                   'DNSZONE' : dnszone,
                   'DELRR0': str(data[0]+" "+data[1]+" "+data[2]+" "+data[3]+" "+curIP),
                   'ADDRR0': str(data[0]+" "+data[1]+" "+data[2]+" "+data[3]+" "+extIP),
                   'INCSERIAL': 1
                })
                result = response.as_hash()

                if result['CODE'] == 200:
                    logging.info("Updated A-Record '%s' in DNS Zone '%s': %s => %s" % (data[0],p['dnszone'],curIP,extIP))
                else:
                    logging.warning("Update on A-Record '%s' in DNS Zone '%s' failed: %s" % (data[0],p['dnszone'],result['DESCRIPTION']))
            else:
                logging.info("No Update necessary, IPs still match :)")
            break

    if e == 0:
        # Your DynDNS Hostname does not yet exist in this zone
        response = api.call({
           'COMMAND': "UpdateDNSZone",
           'DNSZONE' : p['dnszone'],
           'ADDRR0': p['subdomain']+" 10 IN A "+extIP,
           'INCSERIAL': 1
        })
        result = response.as_hash()

        if result['CODE'] == 200:
            logging.info("Created A-Record '%s' in DNS Zone '%s': %s => %s" % (p['subdomain'],p['dnszone'],curIP,extIP))
        else:
            logging.warning("Creation of A-Record '%s' in DNS Zone '%s' failed: %s" % (p['subdomain'],p['dnszone'],result['DESCRIPTION']))

if __name__ == "__main__":
    while True:
        main()
        time.sleep(SLEEP_TIMER)
