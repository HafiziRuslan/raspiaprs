#!/usr/bin/python3

"""RasPiAPRS: Send APRS position and telemetry from Raspberry Pi to APRS-IS."""

import asyncio
import datetime as dt
import json
import logging
import os
import psutil
import subprocess
import sys
import time
from urllib.request import urlopen

import aprslib
import dotenv
import humanize
import telegram
from aprslib.exceptions import ConnectionError as APRSConnectionError
from dotenv import set_key
from gpsdclient import GPSDClient

# Default paths for system files
OS_RELEASE_FILE = "/etc/os-release"
PISTAR_RELEASE_FILE = "/etc/pistar-release"
WPSD_RELEASE_FILE = "/etc/WPSD-release"
MMDVMHOST_FILE = "/etc/mmdvmhost"
MMDVMLOGPATH = "/var/log/pi-star"
MMDVMLOGPREFIX = "MMDVM"
DMRGATEWAYLOGPREFIX = "DMRGateway"


# Set up logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        datefmt="%Y-%m-%dT%H:%M:%S",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


# Configuration class to handle settings
class Config(object):
    """Class to handle configuration settings."""

    def __init__(self):
        dotenv.load_dotenv(".env")

        call = os.getenv("APRS_CALL", "N0CALL")
        ssid = os.getenv("APRS_SSID", "0")
        self.call = f"{call}-{ssid}"
        self.sleep = int(os.getenv("SLEEP", 600))
        self.symbol_table = os.getenv("APRS_SYMBOL_TABLE", "/")
        self.symbol = os.getenv("APRS_SYMBOL", "n")

        lat = os.getenv("APRS_LATITUDE", "0.0")
        lon = os.getenv("APRS_LONGITUDE", "0.0")
        alt = os.getenv("APRS_ALTITUDE", "0.0")

        if os.getenv("GPSD_ENABLE"):
            (
                self.timestamp,
                self.latitude,
                self.longitude,
                self.altitude,
                self.speed,
                self.course,
            ) = get_gpspos()
        else:
            if lat == "0.0" and lon == "0.0":
                self.latitude, self.longitude = get_coordinates()
                self.altitude = alt
            else:
                self.latitude, self.longitude, self.altitude = lat, lon, alt
        self.server = os.getenv("APRSIS_SERVER", "rotate.aprs2.net")
        self.port = int(os.getenv("APRSIS_PORT", 14580))
        self.filter = os.getenv("APRSIS_FILTER", "m/10")

        passcode = os.getenv("APRS_PASSCODE")
        if passcode:
            self.passcode = passcode
        else:
            logging.warning("Generating passcode")
            self.passcode = aprslib.passcode(call)

    def __repr__(self):
        return (
            "<Config> call: {0.call}, passcode: {0.passcode} - {0.latitude}/{0.longitude}/{0.altitude}"
        ).format(self)

    @property
    def call(self):
        return self._call

    @call.setter
    def call(self, val):
        self._call = str(val)

    @property
    def sleep(self):
        return self._sleep

    @sleep.setter
    def sleep(self, val):
        try:
            self._sleep = int(val)
        except ValueError:
            logging.warning("Sleep value error, using 600")
            self._sleep = 600

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, val):
        self._latitude = val

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, val):
        self._longitude = val

    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, val):
        self._altitude = val

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, val):
        self._symbol = str(val)

    @property
    def symbol_table(self):
        return self._symbol_table

    @symbol_table.setter
    def symbol_table(self, val):
        self._symbol_table = str(val)

    @property
    def server(self):
        return self._server

    @server.setter
    def server(self, val):
        self._server = str(val)

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, val):
        try:
            self._port = int(val)
        except ValueError:
            logging.warning("Port value error, using 14580")
            self._port = 14580

    @property
    def passcode(self):
        return self._passcode

    @passcode.setter
    def passcode(self, val):
        self._passcode = str(val)


class Sequence(object):
    """Class to manage APRS sequence."""

    _count = 0

    def __init__(self):
        self.sequence_file = os.path.join("/tmp", "raspiaprs.seq")
        try:
            with open(self.sequence_file) as fds:
                self._count = int(fds.readline())
        except (IOError, ValueError):
            self._count = 0

    def flush(self):
        try:
            with open(self.sequence_file, "w") as fds:
                fds.write("{0:d}".format(self._count))
        except IOError:
            pass

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        self._count = (1 + self._count) % 999
        self.flush()
        return self._count


class Timer(object):
    """Class to manage APRS timer."""

    _count = 0

    def __init__(self):
        self.timer_file = os.path.join("/tmp", "raspiaprs.tmr")
        try:
            with open(self.timer_file) as fds:
                self._count = int(fds.readline())
        except (IOError, ValueError):
            self._count = 0

    def flush(self):
        try:
            with open(self.timer_file, "w") as fds:
                fds.write("{0:d}".format(self._count))
        except IOError:
            pass

    def __iter__(self):
        return self

    def next(self):
        return self.__next__()

    def __next__(self):
        self._count = 1 + self._count
        self.flush()
        return self._count


def get_gpspos():
    """Get position from GPSD."""
    if os.getenv("GPSD_ENABLE"):
        timestamp = dt.datetime.now(dt.timezone.utc)
        logging.info("Trying to figure out position using GPS")
        try:
            with GPSDClient(
                os.getenv("GPSD_HOST", "localhost"),
                int(os.getenv("GPSD_PORT", 2947)),
                15,
            ) as client:
                for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
                    if result["class"] == "TPV":
                        logging.info("GPS fix acquired")
                        utc = result.get("time", timestamp)
                        lat = result.get("lat", 0)
                        lon = result.get("lon", 0)
                        alt = result.get("alt", 0)
                        spd = result.get("speed", 0)
                        cse = result.get("magtrack", 0)
                        # acc = result.get("sep", 0)
                        if lat != 0 and lon != 0 and alt != 0:
                            logging.info(
                                "%s | GPS Position: %s, %s, %s, %s, %s",
                                utc,
                                lat,
                                lon,
                                alt,
                                spd,
                                cse,
                            )
                            set_key(".env", "APRS_LATITUDE", lat, quote_mode="never")
                            set_key(".env", "APRS_LONGITUDE", lon, quote_mode="never")
                            set_key(".env", "APRS_ALTITUDE", alt, quote_mode="never")
                            Config.latitude = lat
                            Config.longitude = lon
                            Config.altitude = alt
                            return utc, lat, lon, alt, spd, cse
                    else:
                        logging.info("GPS Position unavailable")
                        return (timestamp, 0, 0, 0, 0, 0)
        except Exception as e:
            logging.error("Error getting GPS data: %s", e)
            return (timestamp, 0, 0, 0, 0, 0)


def get_gpssat():
    """Get satellite from GPSD."""
    if os.getenv("GPSD_ENABLE"):
        timestamp = dt.datetime.now(dt.timezone.utc)
        logging.info("Trying to figure out satellite using GPS")
        try:
            with GPSDClient(
                os.getenv("GPSD_HOST", "localhost"),
                int(os.getenv("GPSD_PORT", 2947)),
                15,
            ) as client:
                for result in client.dict_stream(convert_datetime=True, filter=["SKY"]):
                    if result["class"] == "SKY":
                        logging.info("GPS Satellite acquired")
                        utc = result.get("time", timestamp)
                        uSat = result.get("uSat", 0)
                        nSat = result.get("nSat", 0)
                        return utc, uSat, nSat
                    else:
                        logging.info("GPS Satellite unavailable")
                        return (timestamp, 0, 0)
        except Exception as e:
            logging.error("Error getting GPS data: %s", e)
            return (timestamp, 0, 0)


def get_coordinates():
    """Get approximate latitude and longitude using IP address lookup."""
    logging.info("Trying to figure out the coordinate using your IP address")
    url = "http://ip-api.com/json/"
    try:
        with urlopen(url) as response:
            _data = response.read()
            data = json.loads(_data.decode())
    except Exception as err:
        logging.error("Failed to fetch coordinates from %s: %s", url, err)
        return (0, 0)
    else:
        try:
            logging.info("IP-Position: %f, %f", data["lat"], data["lon"])
            return data["lat"], data["lon"]
        except (KeyError, TypeError) as err:
            logging.error("Unexpected response format: %s", err)
            return (0, 0)


def get_cpuload():
    """Get CPU load as a percentage of total capacity."""
    try:
        load5 = psutil.getloadavg()[1]
        corecount = psutil.cpu_count()
        return int((load5 / corecount) * 100 * 1000)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return 0


def get_memused():
    """Get used memory in MB."""
    try:
        totalVmem = psutil.virtual_memory().total
        freeVmem = psutil.virtual_memory().free
        buffVmem = psutil.virtual_memory().buffers
        cacheVmem = psutil.virtual_memory().cached
        return int(((totalVmem - freeVmem - buffVmem - cacheVmem) / 1024**2) * 1000)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return 0


def get_diskused():
    """Get used disk space in GB."""
    try:
        diskused = psutil.disk_usage("/").used
        return int((diskused / 1024**3) * 1000)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return 0


def get_temp():
    """Get CPU temperature in degC."""
    try:
        temperature = psutil.sensors_temperatures()["cpu_thermal"][0].current
        return int(temperature * 10)
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return 0


def get_uptime():
    """Get system uptime in a human-readable format."""
    try:
        uptime_seconds = (
            dt.datetime.now(dt.timezone.utc).timestamp() - psutil.boot_time()
        )
        uptime = dt.timedelta(seconds=uptime_seconds)
        return f"up={humanize.precisedelta(uptime, minimum_unit='seconds', format='%0.0f')}"
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return ""


def get_osinfo():
    """Get operating system information."""
    osname = ""
    try:
        with open(OS_RELEASE_FILE) as osr:
            for line in osr:
                if "ID_LIKE" in line:
                    id_like = line.split("=", 1)[1].strip().title()
                if "DEBIAN_VERSION_FULL" in line:
                    debian_version_full = line.split("=", 1)[1].strip()
                if "VERSION_CODENAME" in line:
                    version_codename = line.split("=", 1)[1].strip()
            osname = f"{id_like} {debian_version_full} ({version_codename})"
    except (IOError, OSError):
        logging.warning("OS release file not found: %s", OS_RELEASE_FILE)
    kernelver = ""
    try:
        kernel = os.uname()
        kernelver = f"[{kernel.sysname}{kernel.release}{kernel.version.split(' ')[0]} ({kernel.machine})]"
    except Exception as e:
        logging.error("Unexpected error: %s", e)
    return f" {osname} {kernelver}"


def get_dmrmaster():
    """Get connected DMR master from DMRGateway log files."""
    with open(MMDVMHOST_FILE, "r") as mmh:
        if "Enable=1" in mmh.read():
            log_dmrgw_previous = os.path.join(
                MMDVMLOGPATH,
                f"{DMRGATEWAYLOGPREFIX}-{(dt.datetime.now(dt.UTC) - dt.timedelta(days=1)).strftime('%Y-%m-%d')}.log",
            )
            log_dmrgw_now = os.path.join(
                MMDVMLOGPATH,
                f"{DMRGATEWAYLOGPREFIX}-{dt.datetime.now(dt.UTC).strftime('%Y-%m-%d')}.log",
            )

            dmr_master: str = ""
            log_master_string = "Logged into the master successfully"
            log_ref_string = "XLX, Linking"
            # log_master_dc_string = "Closing DMR Network"
            master_line: list[str] = []
            # master_dc_line: list[str] = []
            ref_line: list[str] = []
            dmrmaster: list[str] = []
            dmrmasters: list[str] = []
            try:
                master_line = subprocess.check_output(
                    ["grep", log_master_string, log_dmrgw_now], text=True
                ).splitlines()
                # master_dc_line = subprocess.check_output(["grep", log_master_dc_string, log_dmrgw_now], text=True).splitlines()
                ref_line = subprocess.check_output(
                    ["grep", log_ref_string, log_dmrgw_now], text=True
                ).splitlines()
                ref_line = ref_line[-1:] if ref_line else []
            except subprocess.CalledProcessError:
                try:
                    master_line = subprocess.check_output(
                        ["grep", log_master_string, log_dmrgw_previous], text=True
                    ).splitlines()
                    # master_dc_line = subprocess.check_output(["grep", log_master_dc_string, log_dmrgw_previous], text=True).splitlines()
                    ref_line = subprocess.check_output(
                        ["grep", log_ref_string, log_dmrgw_previous], text=True
                    ).splitlines()
                    ref_line = ref_line[-1:] if ref_line else []
                except subprocess.CalledProcessError:
                    pass
            master_line_count = len(master_line)
            # master_dc_line_count = len(master_dc_line)
            ref_line_count = len(ref_line)
            for mascount in range(master_line_count):
                master = (
                    master_line[mascount].split()[3].split(",")[0].replace("_", " ")
                )
                if master == "XLX":
                    for refcount in range(ref_line_count):
                        master = f"{ref_line[refcount].split()[7]} {ref_line[refcount].split()[8]}"
                dmrmaster.append(master)
                # for dccount in range(master_dc_line_count):
                # 	 master_dc = master_dc_line[dccount].split()[3].split(",")[0]
                # 	 if master_dc == "XLX":
                # 		 xlxdcid = dmrmaster.index(re.search(r"^XLX.+", dmrmaster[dccount])[0])
                # 		 dmrmaster.pop(xlxdcid)
                # 	 dmrmaster.remove(master_dc)
            dmrmasters = list(dict.fromkeys(dmrmaster))
            if len(dmrmasters) > 0:
                dmr_master = f" connected via [{', '.join(dmrmasters)}]"
    return dmr_master


def get_mmdvminfo():
    """Get MMDVM configured frequency and color code."""
    rx_freq, tx_freq, color_code, dmr_enabled = 0, 0, 0, False
    with open(MMDVMHOST_FILE, "r") as mmh:
        for line in mmh:
            if line.startswith("RXFrequency="):
                rx_freq = int(line.strip().split("=")[1])
            elif line.startswith("TXFrequency="):
                tx_freq = int(line.strip().split("=")[1])
            elif line.startswith("ColorCode="):
                color_code = int(line.strip().split("=")[1])
            elif "[DMR]" in line:
                dmr_enabled = "Enable=1" in next(mmh, "")
    rx = round(rx_freq / 1000000, 6)
    tx = round(tx_freq / 1000000, 6)
    shift = ""
    if tx > rx:
        shift = f" ({round(rx - tx, 6)}MHz)"
    elif tx < rx:
        shift = f" (+{round(rx - tx, 6)}MHz)"
    cc = f" CC{color_code}" if dmr_enabled else ""
    return (str(tx) + "MHz" + shift + cc) + get_dmrmaster() + ","


async def logs_to_telegram(tg_message: str, lat: float = 0, lon: float = 0):
    """Send log message to Telegram channel."""
    if os.getenv("TELEGRAM_ENABLE"):
        tgbot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))
        async with tgbot:
            try:
                botmsg = await tgbot.send_message(
                    chat_id=os.getenv("TELEGRAM_CHAT_ID"),
                    message_thread_id=int(os.getenv("TELEGRAM_TOPIC_ID")),
                    text=tg_message,
                    parse_mode="HTML",
                    link_preview_options={
                        "is_disabled": True,
                        "prefer_small_media": True,
                        "show_above_text": True,
                    },
                )
                logging.info(
                    "Sent message to Telegram: %s/%s/%s",
                    botmsg.chat_id,
                    botmsg.message_thread_id,
                    botmsg.message_id,
                )
                if lat != 0 and lon != 0:
                    botloc = await tgbot.send_location(
                        chat_id=os.getenv("TELEGRAM_CHAT_ID"),
                        message_thread_id=int(os.getenv("TELEGRAM_TOPIC_ID")),
                        latitude=lat,
                        longitude=lon,
                    )
                    logging.info(
                        "Sent location to Telegram: %s/%s/%s",
                        botloc.chat_id,
                        botloc.message_thread_id,
                        botloc.message_id,
                    )
            except Exception as e:
                logging.error("Failed to send message to Telegram: %s", e)


async def send_position(ais, cfg):
    """Send APRS position packet to APRS-IS."""

    def _lat_to_aprs(lat):
        ns = "N" if lat >= 0 else "S"
        lat = abs(lat)
        deg = int(lat)
        minutes = (lat - deg) * 60
        return f"{deg:02d}{minutes:05.2f}{ns}"

    def _lon_to_aprs(lon):
        ew = "E" if lon >= 0 else "W"
        lon = abs(lon)
        deg = int(lon)
        minutes = (lon - deg) * 60
        return f"{deg:03d}{minutes:05.2f}{ew}"

    def _alt_to_aprs(alt):
        alt /= 0.3048  # to feet
        alt = min(999999, alt)
        alt = max(-99999, alt)
        return "/A={0:06.0f}".format(alt)

    def _spd_to_aprs(spd):
        spd /= 1.9438  # to knots
        spd = min(999, spd)
        spd = max(-999, spd)
        return "{0:03.0f}".format(spd)

    def _cse_to_aprs(cse):
        cse = min(0, cse)
        cse = max(360, cse)
        return "{0:03.0f}".format(cse)

    if os.getenv("GPSD_ENABLE"):
        cur_time, cur_lat, cur_lon, cur_alt, cur_spd, cur_cse = get_gpspos()
        if cur_lat == 0 and cur_lon == 0 and cur_alt == 0:
            cur_lat = os.getenv("APRS_LATITUDE", cfg.latitude)
            cur_lon = os.getenv("APRS_LONGITUDE", cfg.longitude)
            cur_alt = os.getenv("APRS_ALTITUDE", cfg.altitude)
    else:
        cur_lat = os.getenv("APRS_LATITUDE", cfg.latitude)
        cur_lon = os.getenv("APRS_LONGITUDE", cfg.longitude)
        cur_alt = os.getenv("APRS_ALTITUDE", cfg.altitude)
    latstr = _lat_to_aprs(float(cur_lat))
    lonstr = _lon_to_aprs(float(cur_lon))
    altstr = _alt_to_aprs(float(cur_alt))
    spdstr = _spd_to_aprs(float(cur_spd))
    csestr = _cse_to_aprs(float(cur_cse))
    extdatstr = f"{csestr}/{spdstr}"
    mmdvminfo = get_mmdvminfo()
    osinfo = get_osinfo()
    comment = f"{mmdvminfo}{osinfo} https://github.com/HafiziRuslan/RasPiAPRS"
    ztime = dt.datetime.now(dt.timezone.utc)
    timestamp = (
        cur_time.strftime("%d%H%Mz") if cur_time != None else ztime.strftime("%d%H%Mz")
    )
    symbt = cfg.symbol_table
    symb = cfg.symbol
    if os.getenv("SMARTBEACONING_ENABLE"):
        sspd = os.getenv("SMARTBEACONING_SLOWSPEED")
        if spdstr >= sspd:
            symbt = "/"
            symb = ">"
        if spdstr > "000" and spdstr <= sspd:
            symbt = "\\"
            symb = ">"
    payload = f"/{timestamp}{latstr}{symbt}{lonstr}{symb}{extdatstr}{altstr}{comment}"
    packet = f"{cfg.call}>APP642:{payload}"
    try:
        ais.sendall(packet)
        logging.info(packet)
        await logs_to_telegram(
            f"<u>{cfg.call} Position</u>\n\n<b>Time</b>: {timestamp}\n<b>Position</b>:\n\t<b>Latitude</b>: {cur_lat}\n\t<b>Longitude</b>: {cur_lon}\n\t<b>Altitude</b>: {cur_alt} m\n\t<b>Speed</b>: {cur_spd} m/s\n\t<b>Course</b>: {cur_cse} deg\n<b>Comment</b>: {comment}",
            cur_lat,
            cur_lon,
        )
        await send_status(ais, cfg)
    except APRSConnectionError as err:
        logging.error(err)


async def send_header(ais, cfg):
    """Send APRS header information to APRS-IS."""
    parm = "{0}>APP642::{0:9s}:PARM.CPUTemp,CPULoad,RAMUsed,DiskUsed".format(cfg.call)
    unit = "{0}>APP642::{0:9s}:UNIT.deg.C,pcnt,MB,GB".format(cfg.call)
    eqns = "{0}>APP642::{0:9s}:EQNS.0,0.1,0,0,0.001,0,0,0.001,0,0,0.001,0".format(
        cfg.call
    )
    try:
        if os.getenv("GPSD_ENABLE"):
            parm += f",GPSUsed"
            unit += f",sats"
            eqns += f",0,1,0"
        ais.sendall(parm)
        ais.sendall(unit)
        ais.sendall(eqns)
        await send_status(ais, cfg)
    except APRSConnectionError as err:
        logging.error(err)


async def send_telemetry(ais, cfg, seq):
    """Send APRS telemetry information to APRS-IS."""
    temp = get_temp()
    cpuload = get_cpuload()
    memused = get_memused()
    diskused = get_diskused()
    telem = "{}>APP642:T#{:03d},{:d},{:d},{:d},{:d}".format(
        cfg.call, seq, temp, cpuload, memused, diskused
    )
    tgtel = f"<u>{cfg.call} Telemetry</u>\n\n<b>Sequence</b>: #{seq}\n\n<b>CPU Temp</b>: {temp / 10:.1f} °C\n<b>CPU Load</b>: {cpuload / 1000:.3f} %\n<b>RAM Used</b>: {memused / 1000:.3f} MB\n<b>Disk Used</b>: {diskused / 1000:.3f} GB"
    if os.getenv("GPSD_ENABLE"):
        nowz, uSat, nSat = get_gpssat()
        telem += ",{:d}".format(uSat)
        tgtel += f"\n<b>GPS Used</b>: {uSat}/{nSat}"
    try:
        ais.sendall(telem)
        await logs_to_telegram(tgtel)
        logging.info(telem)
        await send_status(ais, cfg)
    except APRSConnectionError as err:
        logging.error(err)


async def send_status(ais, cfg):
    """Send APRS status information to APRS-IS."""
    ztime = dt.datetime.now(dt.timezone.utc)
    timestamp = ztime.strftime("%d%H%Mz")
    uptime = get_uptime()
    status = "{0}>APP642:>{1}{2}".format(cfg.call, timestamp, uptime)
    tgstat = f"<u>{cfg.call} Status</u>\n\n{timestamp}, {uptime}"
    if os.getenv("GPSD_ENABLE"):
        timez, uSat, nSat = get_gpssat()
        timestamp = timez if timez != None else ztime.strftime("%d%H%Mz")
        sats = f"sats={uSat}/{nSat}"
        status += f", {sats}"
        tgstat += f", {sats}"
    try:
        ais.sendall(status)
        await logs_to_telegram(tgstat)
        logging.info(status)
    except APRSConnectionError as err:
        logging.error(err)


def ais_connect(cfg):
    """Establish connection to APRS-IS with retries."""
    logging.info(
        "Connecting to APRS-IS server %s:%d as %s", cfg.server, cfg.port, cfg.call
    )
    ais = aprslib.IS(cfg.call, passwd=cfg.passcode, host=cfg.server, port=cfg.port)
    for _ in range(5):
        try:
            ais.connect()
        except APRSConnectionError as err:
            logging.warning("APRS connection error: %s", err)
            time.sleep(20)
            continue
        else:
            ais.set_filter(cfg.filter)
            return ais
    logging.error("Connection error, exiting")
    sys.exit(getattr(os, "EX_NOHOST", 1))


async def main():
    """Main function to run the APRS reporting loop."""
    cfg = Config()
    ais = ais_connect(cfg)
    rate = cfg.sleep
    if os.getenv("SMARTBEACONING_ENABLE"):
        spd = get_gpspos()[4]
        fspd = int(os.getenv("SMARTBEACONING_FASTSPEED"))
        sspd = int(os.getenv("SMARTBEACONING_SLOWSPEED"))
        frate = int(os.getenv("SMARTBEACONING_FASTRATE"))
        srate = int(os.getenv("SMARTBEACONING_SLOWRATE"))
        if spd >= fspd:
            rate = frate
            logging.info("Fast beaconing enabled")
        if spd <= sspd:
            rate = srate
            logging.info("Slow beaconing enabled")
        if spd > sspd and spd < fspd:
            rate = int(frate + srate / 2)
            logging.info("Mixed beaconing enabled")
        if spd == 0:
            rate = cfg.sleep
            logging.info("Smart beaconing disabled")
    for tmr in Timer():
        if tmr % rate == 1:
            await send_position(ais, cfg)
        if tmr % cfg.sleep == 1:
            if tmr % 1800 == 1:
                await send_header(ais, cfg)
            for seq in Sequence():
                await send_telemetry(ais, cfg, seq)
        if tmr == 1:
            await send_position(ais, cfg)
            await send_header(ais, cfg)
            await send_telemetry(ais, cfg, seq)
        # await send_status(ais, cfg)
        # logging.info("Sleeping for %d seconds", rate)
        # time.sleep(rate)


if __name__ == "__main__":
    configure_logging()
    try:
        logging.info("Starting the application...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Stopping application...")
    except Exception as e:
        logging.error("An error occurred: %s", e)
    finally:
        logging.info("Exiting script...")
        sys.exit(0)
