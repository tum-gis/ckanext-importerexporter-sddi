#import ckan.model as model
#import ckan.plugins.toolkit as toolkit###

#import ckan.plugins.toolkit as toolkit

#context = {
#            'model': model,
#            'session': model.Session,
#            'user': "wdeigele",
#        }

#s = {}
#s[u"q"] = u"*:*"


#package_ids = toolkit.get_action(u"package_search")({},q="tags:karte")
#package_ids = 
#print(len(package_ids))

# This Python program connects to a CKAN server and creates a new dataset
# for each feature in the referenced Shapefile.
#
# The program uses Python 3 and needs to have the ckanapi library installed.
# Install ckanapi by using (from the command line): "pip install ckanapi" (under Windows)
# or "pip3 install ckanapi" (under MacOS and probably Linux)
#
# Author: Thomas H. Kolbe     Last update: 2020-01-21

#import geopandas
#import shapely
#import json
from ckanapi import RemoteCKAN, NotAuthorized
import urllib3
import json

ckanserverURL = 'https://10.162.246.55' # Choose our test CKAN installation
#ckanserverURL = 'https://agrihub.hef.tum.de' # Choose our official HEF CKAN installation

# Secret API key of user thomas_kolbe on our test CKAN installation 
# apikey='c94f560d-2171-4017-9efe-77e15cd0fdf2'
# Secret API key of user thomas_kolbe on the Agrihub CKAN installation 
#apikey='815bb17b-fc6e-423e-b332-5891685da341'
apikey='2768bf58-78c0-4727-9f3f-526df95a7305'

#parcels = geopandas.read_file('/Users/kolbe/Dropbox/Arbeitsdateien/Geodaten/DuernastParcels/daw_494216_area.shp')
# parcels_fc = parcels.__geo_interface__

ckanserver = RemoteCKAN(ckanserverURL, apikey)

#print()
#print('Connecting to CKAN-Server', ckanserverURL)
#print()

# Workaround until the ssl certificate agrihub.hef.tum.de has been corrected / verified
# See https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
# and https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
# and https://github.com/ckan/ckanapi/issues/51#import urllib3
urllib3.disable_warnings()

#pkg = ckanserver.action.package_search(q='*:*')
pkg = ckanserver.call_action('package_search', {'q': '*:*'}, requests_kwargs={'verify': False})

for package in pkg["results"]:
    print(package["id"])
    ckanserver.call_action('package_delete', {"id": package["id"]}, requests_kwargs={'verify': False})


#pkg = ckanserver.call_action('package_search',{{'q'= 'parcel_debyli8497000508' }})
##pkg = ckanserver.action.package_search(q='*:*')
#print(pkg)

#import requests

#response = requests.get("https://10.162.246.55/api/action/package_search", verify=False)
#print(response.json())
