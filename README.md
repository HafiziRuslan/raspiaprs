# RasPiAPRS

With this simple python program you can monitor your Pi-Star / WPSD / AllStarLink health using APRS metrics.

You can see an example of the metrics logged by my Pi-Star node [9W4GPA-2](https://aprs.fi/telemetry/a/9W4GPA-2?range=day).

The metrics are:-

1. CPU Temperature
2. CPU load average per 5 min
3. Memory used

## Installation (Pi-Star / WPSD / AllStarLink)

```bash
git clone https://github.com/HafiziRuslan/raspiaprs.git
cd raspiaprs
```

## Configurations

Copy the file `.env.SAMPLE` into `.env`, and edit the informations using your favorite editor.

```bash
cp default.env .env
nano .env
```

## Starting RasPiAPRS

```bash
chmod a+x *.sh
./main.sh
```

## AutoStart RasPiAPRS on StartUp

Copy/Paste this into last line of `/etc/crontab` or any other cron program that you're using.

```bash
@reboot pi-star cd /home/pi-star/raspiaprs && ./main.sh > /tmp/raspiaprs.log 2>&1
```

edit the `pi-star` username into your username

## Update RasPiAPRS

Use this command to update:-

```bash
git pull --autostash
```

## Example

This is the screenshoot from aprs.fi, of _CPU temperature_, _CPU load average_ and _Memory free_ from an Pi-Star node.
![WSPR Picture](misc/metrics.png)

### Source

[0x9900/aprstar](https://github.com/0x9900/aprstar)
