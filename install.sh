#!/bin/sh

cd RFSource && make
mkdir /opt/beer_machine
cp -a * /opt/beer_machine
cp beer_machine.service /lib/systemd/system/
