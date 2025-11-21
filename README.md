# raspiaprs

With this simple python program you can monitor your Pi-Star / WPSD / AllStarLink health using APRS metrics.

You can see an example of the metrics logged by my Pi-Star node [9W4GPA-4](https://aprs.fi/telemetry/a/9W4GPA-4?range=day).

The metrics are:-

1. CPU Temperature
2. CPU load average per 5 min
3. Memory used

## Installation (Pi-Star / WPSD / AllStarLink)

I have try to limit the number of dependencies in other python package but there is still a few that need to be installed.

The following instructions for installing `raspiaprs` on Pi-Star.

On the Pi-Star / WPSD / AllStarLink image, a very minimal version of python has been installed.

Make sure the main python libraries are installed by running the following commands:-

```bash
rpi-rw
sudo apt update
sudo apt install python3-pip -y
```

The following packages are the 5 dependencies used by `raspiaprs`.

They can be installed using the command pip:-

```bash
sudo pip install ConfigParser aprslib humanize gpsdclient python-telegram-bot --break-system-packages
```

The module `ConfigParser` should be already installed but I have found some instances where it is not.

Clone this repo and move into directory:-

```bash
git clone https://github.com/HafiziRuslan/raspiaprs.git
cd raspiaprs
```

### Installing raspiaprs script

```bash
sudo cp usr/bin/raspiaprs.py /usr/bin/raspiaprs
sudo chmod a+x /usr/bin/raspiaprs
```

### Installing the raspiaprs service

```bash
sudo cp lib/systemd/system/raspiaprs.service /lib/systemd/system/raspiaprs.service
sudo chmod 0644 /lib/systemd/system/raspiaprs.service
```

## Configurations

Copy the file `raspiaprs.conf` into `/etc`, and edit the informations using your favorite editor.

```bash
sudo cp etc/raspiaprs.conf /etc/raspiaprs.conf
sudo nano /etc/raspiaprs.conf
```

## Starting the service

```bash
sudo systemctl enable raspiaprs
sudo systemctl start raspiaprs
```

You can now run the status command to see if everything is running smoothly and you have no errors.

```bash
systemctl status raspiaprs
```

If any error upon start, you may look into `journalctl` for more info.

```bash
journalctl -u raspiaprs
```

## Update raspiaprs

Use this command to update:-

```bash
sudo systemctl stop raspiaprs
sudo systemctl disable raspiaprs
git pull
sudo cp usr/bin/raspiaprs.py /usr/bin/raspiaprs
sudo chmod a+x /usr/bin/raspiaprs
sudo cp lib/systemd/system/raspiaprs.service /lib/systemd/system/raspiaprs.service
sudo chmod 0644 /lib/systemd/system/raspiaprs.service
sudo systemctl enable raspiaprs
sudo systemctl start raspiaprs
```

## Example

This is the screenshoot from aprs.fi, of _CPU temperature_, _CPU load average_ and _Memory free_ from an Pi-Star node.
![WSPR Picture](misc/metrics.png)

### Source

[0x9900/aprstar](https://github.com/0x9900/aprstar)
