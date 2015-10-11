#!/usr/bin/python

import json
import argparse
import requests


def upload(archive, metadata, catalogRootUri):
    '''
    Upload an archived bundle on the shuttleOFX DB.
    '''

    headerJson= {'Content-type': 'application/json'}

    resp = requests.post(catalogRootUri + "/bundle", data = json.dumps(metadata), headers = headerJson)
    if resp.status_code != 200:
        print "Error when creating a new bundle"
        print resp.text
        return

    resp = resp.json()
    bundleId = str(resp.get('bundleId'))

    print "Bundle ID:", bundleId

    multiple_files = [('file', (archive, open(archive, 'rb'), 'application/gzip'))]

    resp = requests.post(catalogRootUri + '/bundle/' + bundleId + '/archive', files = multiple_files)
    if resp.status_code != 200:
        print "Error when uploading the archive"
        print resp.text
        return

    print "Upload: done"

    resp = requests.post(catalogRootUri + "/bundle/" + bundleId + "/analyse", data = metadata, headers = headerJson)
    if resp.status_code != 200:
        print "Error when analyse the bundle"
        print resp.text
        return
    print "Bundle", resp.json()["name"], "loaded with", len( resp.json()["plugins"] ), "plugins"

if __name__ == "__main__":
    '''
    Parse commande line arguments and call the upload function with the arguments.
    '''
    parser = argparse.ArgumentParser(description='Upload an OpenFX bundle to the ShuttleOFX platform.')
    parser.add_argument('-n', '--name', metavar='BUNDLE_NAME', type=str,
                       help='')
    parser.add_argument('-u', '--userId', metavar='USER', type=int,
                       help='')
    parser.add_argument('-c', '--companyId', metavar='COMPANY', type=int,
                       help='')
    parser.add_argument('--uri', metavar='CATALOG_URI', type=str,
                       help='')
    parser.add_argument('file', metavar='FILEPATH', type=str,
                       help='')

    args = parser.parse_args()

    metadata = {
        "bundleName": args.name,
        "userId": args.userId,
        "companyId" : args.companyId,
    }

    upload(args.file, metadata, args.uri)
