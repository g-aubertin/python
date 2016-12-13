
default: tools

tools:
	gcc 433_send.c -o 433_send -lwiringPi

install: tools
	# create directories
	mkdir /opt/beer_machine
	mkdir /opt/beer_machine/web

	# copy binaries
	cp 433_send  /opt/beer_machine/
	cp beer_machine.py /opt/beer_machine
	cp webui.py /opt/beer_machine
	cp config.ini /opt/beer_machine

	# systemd service
	cp beer_machine.service /lib/systemd/system/

	# web folder
	cp -a web/* /opt/beer_machine/web

	# symlinks for webpage
	rm /var/www/html/index.html
	rm /var/www/html/main.css
	ln -s /opt/beer_machine/index.html /var/www/html/
	ln -s /opt/beer_machine/web/main.css /var/www/html/

	echo "install complete."
	echo "to enable the beer_machine, use the following command :"
	echo "systemctl enable beer_machine"
