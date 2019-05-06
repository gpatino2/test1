#!/bin/sh
dateTime=$(date '+%d/%m/%Y %H:%M:%S')

cd /cloudclient-4.6/bin/

./cloudclient.sh vra content export --path /linux7g --id 236b7b2b-8622-40a5-80a7-38757098720b --content-id 'Linux7g'

cd /linux7g/

git add --all

git commit -m "Added new version of blueprint Linux7g - Modified on: $dateTime"

git push

echo "Done."
