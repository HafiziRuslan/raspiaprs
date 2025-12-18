#!/bin/bash

echo -n "Modem: "
IFS='/ ' read -r _ _ _ mm _ mn mt < <(mmcli -L)
echo $mt

echo -n "Latitude: "
lat=$(mmcli -m $mn --location-get -J | jq .modem.location.gps.latitude | sed 's/\"//g')
echo $lat

echo -n "Longitude: "
lon=$(mmcli -m $mn --location-get -J | jq .modem.location.gps.longitude | sed 's/\"//g')
echo $lon

echo -n "Altitude: "
alt=$(mmcli -m $mn --location-get -J | jq .modem.location.gps.altitude | sed 's/\"//g')
echo $alt

echo -n "UTC: "
utc=$(mmcli -m $mn --location-get -J | jq .modem.location.gps.utc | sed 's/\"//g')
echo $utc

exit 1