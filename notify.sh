#!/bin/bash

curl -X POST  \
     -H "X-Parse-Application-Id: HQrMLZDevpTv2J1raSC6KATvlpNqqePPecUE0EgG" \
     -H "X-Parse-REST-API-Key: ivgV8ZoA0kyOOLWKms3M0wxYUxyUw4tfGgbj6DFd" \
     -H "Content-Type: application/json" \
     -d "{\"key\":\"$KEY\", \"text\": \"socket switch \"}"  \
     https://api.parse.com/1/functions/notify
