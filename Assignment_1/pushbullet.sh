#!/bin/bash

API="o.dc1Td1Mkjo5P99GmRxbNFBLNyfoMViJ5"
MSG="$@"

curl -u $API: https://api.pushbullet.com/v2/pushes -d type=note -d title="Weather Notification" -d body="$MSG"