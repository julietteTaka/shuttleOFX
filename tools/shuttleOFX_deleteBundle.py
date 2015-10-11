#!/usr/bin/python

import json
import argparse
import requests


def deleteBundle(bundleId, catalogRootUri):
    '''
    delete a bundle from the database
    '''
    print(catalogRootUri + "/bundle/"+bundleId)

    resp = requests.delete(catalogRootUri + "/bundle/"+bundleId)

    if resp.status_code != 200:
        print "Error when deleting the bundle with bundle id "+bundleId
        print resp.text
        return

    print "Bundle "+bundleId+" has been successfully deleted."

if __name__ == "__main__":
    '''
    Parse commande line arguments and call the deleteBundle function with the arguments.
    '''
    parser = argparse.ArgumentParser(description='Upload an OpenFX bundle to the ShuttleOFX platform.')
    parser.add_argument('-i', '--id', metavar='BUNDLE_ID', type=str,
                        help='')
    parser.add_argument('--uri', metavar='CATALOG_URI', type=str,
                        help='')

    args = parser.parse_args()
    deleteBundle(args.id, args.uri)
