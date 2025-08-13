# RPi-APRS

With this simple python program you can monitor your Allstar or
pi-star health using APRS metrics.  You can see an example of the
metrics logged by my allstar node. https://aprs.fi/telemetry/a/9W4GPA-4

The metrics are temperature, CPU load average, and Available memory.

## Installation (Pi-Star)

I have try to limit the number of dependencies in other python package
but there is still a few that need to be installed.

The following instructions for installing `RPi-APRS` on Pi-Star.

On the Pi-Star image a very minimal version of python has been
installed make sure the main python libraries are installed by running
the following commands.

```
rpi-rw
sudo apt update
sudo apt install python3-pip -y
```

The following packages are the 3 dependencies used by `RPi-APRS`. They
can be installed using the command pip.

```
sudo pip install ConfigParser aprslib humanize --break-system-packages
```

The module `ConfigParser` should be already installed but I have found
some instances where it is not.

### Installing RPi-APRS.py

```
sudo cp rpiaprs.py /usr/local/bin/rpiaprs
sudo chmod a+x /usr/local/bin/rpiaprs
```

### Installing the RPi-APRS service

```
sudo cp rpiaprs.service /lib/systemd/system/rpiaprs.service
sudo chmod 0644 /lib/systemd/system/rpiaprs.service
```

## Configurations

Create the file `/etc/rpiaprs.conf`, using your favorite editor. For example:

```
sudo nano /etc/rpiaprs.conf
```

And add the following lines, replacing `N0CALL` with your call
sign. The `1` is the id of your device. If you have several device,
replace the 1 by your device number.

```
[APRS]
call: N0CALL-1
```

Use Ctrl-X to save and exit.

This is the minimal configuration. You can also add the keywords
`longitude` and `latitude`, with the lat, lon in decimal form. If you
don't indicate the position the program will use the ip-address to
determine where you are.

## Starting the service

```
sudo systemctl enable rpiaprs.service
sudo systemctl start rpiaprs.service
```

You can now run the status command to see if everything is running
smoothly and you have no errors.

```
sudo systemctl status rpiaprs.service
```

## Example

This is the screenshoot from aprs.fi, of the _temperature_ and _load average_ from an Pi-Star node.

![WSPR Picture](misc/Telemetry.png)
