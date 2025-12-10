# CHANGELOG

All notable changes to this project will be documented in this file.

## [unreleased]

### 💼 Other

- Update CHANGELOG

### 📚 Documentation

- 📝 docs(changelog): update release note
- 📝 docs(changelog): update release note

## [beta] - 2025-12-10

### 🚀 Features

- ✨ feat(deps): update project dependencies and tooling

- [build] update release workflow to target v0.1-beta.2 for all assets
- [build] update project version in pyproject.toml to v0.1-beta.2
- [build] regenerate requirements.txt using uv, locking dependencies
- [chore] update main.sh to use uv for environment management and dependency sync
- [chore] replace venv with .venv directory for uv managed environment
- [chore] install uv if not present in main.sh initialization script
- ✨ feat(ci): change changelog file extension to md

- update pre-release workflow to use CHANGELOG.md instead of CHANGELOG.txt
- this ensures the changelog file is correctly interpreted by release tools
- ✨ feat(ci): add merge schedule workflow

- implement scheduled merging for pull requests
- use `gr2m/merge-schedule-action` for automation
- configure workflow to trigger on PR open/edit/sync and daily schedule
- ✨ feat(ci): add changelog generation workflow

- introduce changelog-ci configuration file
- set up GitHub Actions workflow for automated changelog generation on PR open and push events
- ✨ feat(config): consolidate APRS sleep time and update GPSD settings

- rename APRS_SLEEP to SLEEP in .env.SAMPLE and Config
- add GPSD_HOST and GPSD_PORT to .env.SAMPLE and use them in GPSD client initialization
- set default APRSIS_FILTER to "m/50" in Config and add it to .env.SAMPLE
- update GPSD data fetching logic to check for TPV class and improve logging messages
- update APRS-IS connection to use set_filter method
- ✨ feat(telegram): enhance telegram message link previews

- disable web page previews in telegram messages
- add options to prefer small media and show link previews above text for cleaner presentation
- ✨ feat(telegram): enhance telegram logging with location support

- update get_osinfo to parse multiple os release file fields
- add lat/lon parameters to logs_to_telegram function
- add location sending functionality to telegram messages
- update send_position to pass lat/lon to logs_to_telegram
- remove disable_web_page_preview and use link_preview_options instead
- update status message in main function
- ✨ feat(gps): enhance gps data handling and aprs message

- add logging for gpsd position availability
- include comment in telegram position message
- ✨ feat(main): enhance application lifecycle logging
- add logging for application startup, shutdown, and errors【main.py】
- add script loop【main.sh】
- ✨ feat(deps): add aprslib and gpsdclient dependencies

- add aprslib for APRS protocol handling
- add gpsdclient for GPS data access
- ♻️ refactor(core): migrate from configparser to dotenv for config management
- migrate configuration from `raspiaprs.conf` to `.env` file
- update code to use environment variables for settings
- remove configparser library dependency
- improve configuration management with dotenv
- simplify configuration loading and access
- generate sample .env file

✨ feat(build): add virtual environment and requirements management
- introduce `venv` for dependency isolation
- add `requirements.txt` for dependency tracking
- create `main.sh` to manage venv activation and script execution

♻️ refactor(gps): improve gpsd integration and env usage
- refactor gpsd coordinate retrieval and update .env
- reduce code duplication and improve readability
- improve error handling and logging for gpsd data

🐛 fix(deps): resolve import errors and update dependencies
- update imports and dependency versions
- fix import errors and ensure compatibility

✨ feat(telemetry): add dynamic time to status message
- add dynamic time to status message for better tracking

♻️ refactor(mmdvm): refactor MMDVM info retrieval
- remove configparser dependency
- improve DMR master connection logic
- improve code readability and maintainability

⚡️ perf(coords): improve coordinate retrieval
- improve coordinate retrieval logic
- enhance error handling and logging

✨ feat(config): enhance configuration loading and handling
- improve configuration handling
- enhance error handling and logging
- improve flexibility and maintainability
- ✨ feat(gps): add gpsd socket configuration and improve data handling

- add the ability to specify a custom socket path for GPSD
- enhance GPSD data handling by ensuring values are updated even on errors
- ✨ feat(telegram): add telegram bot integration for notifications

- add telegram configuration section to raspiaprs.conf
- add logs_to_telegram function to send messages to telegram
- send position, telemetry, and status updates to telegram
- ✨ feat(gps): integrate modemmanager coordinates

- add function to get coordinates from modemmanager
- implement fallback to modemmanager if gpsd fails
- ✨ feat(gps): persist gpsd coordinates to config

- add functionality to save latitude, longitude, and altitude from gpsd
- update the config file with the latest gps coordinates
- update the Config object with the latest gps coordinates
- ✨ feat(gps): integrate gpsdclient for gps data

- add gpsdclient dependency to requirements
- replace gps module with gpsdclient for improved gps data retrieval
- remove unused gps module
- ✨ feat(gps): integrate gpsd for precise location data

- replace dummy gpsdata function with get_gpsd_coordinate
- fetch coordinates from gpsd and update aprs config
- add get_modemmanager_coordinates function
- improve logging for coordinate retrieval methods
- ✨ feat(raspiaprs): add gpsd support

- add gpsd configuration to config file
- implement get_gpsdata function to retrieve gps data
- integrate gpsd data into aprs transmission
- update logging for gps status
- 📦 build(ci): update gitlab sync action version to v2.1.0

- update gitlab sync action to v2.1.0
- ensure compatibility and access to the latest features and fixes
- ✨ feat(aprs): enhance telemetry and status reporting

- add voltage monitoring
- include uptime and voltage in aprs status message
- update aprs status format with current date and time
- ✨ feat(position): add altitude support to APRS position reports

- convert altitude from meters to feet
- format altitude string for APRS compatibility
- include altitude in the APRS position payload
- ✨ feat(position): enhance aprs position reporting

- add timestamp to position reports for improved tracking
- include altitude in the uncompressed aprs position format
- ✨ feat(aprs): add AX.25 support to APRS

- include AX.25 mode in the `get_mmdvmmode` function
- add AX.25 to the PARM, UNIT, and EQNS lines for APRS telemetry
- update the telemetry string format to accommodate the new AX.25 mode
- ✨ feat(mmdvm): add POCSAG support and update telemetry

- add POCSAG mode to get_mmdvmmode function
- update telemetry header to include POCSAG parameter
- adjust telemetry data format for POCSAG and other modes
- remove redundant YSF check in get_mmdvmmode
- ✨ feat(mmdvm): add mmdvm mode reporting

- implement get_mmdvmmode function to check enabled protocols in mmdvmd.conf
- report enabled modes in the APRS telemetry string
- ✨ feat(uptime): include local time in uptime string

- add local time to the uptime string for more comprehensive information
- include timezone information in the local time string
- ✨ feat(dmr): Add DMR master connection status to status output

- Check DMR configuration to determine if DMR master status should be retrieved.
- If DMR is enabled, parse log files to identify current DMR master connections.
- Handle cases where log files might not exist for the current or previous day.
- Extract and process connection information for DMR masters and reflectors.
- Deduplicate the list of connected masters.
- Format the DMR master connection status string.
- If DMR is not enabled, the status will be an empty string.
- ✨ feat(system): add DMRGateway status and master info

- add DMRGateway log parsing to get connected masters
- include DMRGateway master status in the APRS comment
- improve system information reporting
- ✨ feat(main): add network traffic monitoring

- Add daily average network traffic monitoring
- Update aprs message to include new metric
- Update readme to include the new metric
- ✨ feat(config): enhance configuration management and data handling

- introduce Config class for structured configuration management
- add server and port properties to Config class for connection settings
- implement error handling for port value to ensure correct type
- improve uptime formatting in get_uptime function for clarity
- ✨ feat(main): add github link to position comment

- add github link to position comment
- remove github link from uptime message
- ✨ feat(aprs): add modem firmware version to aprs comment

- include modem firmware version in the aprs comment
- get modem firmware version from mmdvm logs
- ✨ feat(readme): add disk usage metric

- add disk usage metric to the list of monitored metrics
- ✨ feat(telemetry): add disk usage to APRS telemetry

- add `get_diskused` function to retrieve disk usage percentage
- include disk usage in telemetry string and header
- update telemetry format string to include disk usage parameter
- update telemetry header to include disk usage parameter and units
- update telemetry header equations to include disk usage

### 🐛 Bug Fixes

- ♻️ refactor(ci): streamline release asset upload process

- 📦 build(ci): split large upload step into multiple, focused actions for clarity
  - Upload default.env separately
  - Upload requirements.txt separately
  - Upload main.py separately
- 🔧 chore(ci): remove explicit file list from the main upload step in release workflow
- 🔧 chore(ci): update release workflow to use explicit file uploads for assets
- 🔧 chore(ci): correct file paths in release workflow to use correct context prefix
- 🔧 chore(cliff): update changelog header to uppercase "CHANGELOG"
- 🔧 chore(cliff): update changelog footer template for consistency
- 🔧 chore(config): update cliff configuration and release workflow

- update cliff.toml header formatting for changelog generation
- move changelog commit logic to the end of the release workflow
- remove redundant commit step from older location in release workflow
- add newline to unreleased section header in cliff.toml
- set `conventional_commits` to `false` in `.github/cliff.toml`
- set `filter_unconventional` to `true` to only process matching commits
- update file paths in the release workflow to use `${{ github.workspace }}` prefix
- reorder file list in release action for consistency
- migrate release workflow to use `git-cliff` for changelog generation
- clean up outdated release workflow steps and configurations
- upgrade GitHub Actions versions in the release workflow
- update changelog generation to use `git-cliff-action`
- remove deprecated changelog actions and configuration files
- update cliff configuration to use standard grouping for other changes
- remove unnecessary `args: --verbose` from git-cliff step
- update file paths in release workflow to use relative paths without leading './'
- add footer template to cliff configuration
- update cliff header to include project details
- update cliff commit parsers to use simple type matching without regex prefixes
- remove unnecessary file list from release workflow
- update release workflow trigger to include 'edited' release event
- update file paths in release workflow to use relative paths starting from root (./)
- update file paths in release workflow to use `${{ github.workspace }}` prefix
- remove unnecessary file list from release workflow
- update cliff configuration to use standard grouping for other changes
- update cliff header to include project details
- update cliff commit parsers to use simple type matching without regex prefixes
- remove unnecessary `args: --verbose` from git-cliff step
- update file paths in release workflow to use relative paths without leading './'
- add footer template to cliff configuration
- update cliff header to include project details
- update cliff commit parsers to use simple type matching without regex prefixes
- remove unnecessary `args: --verbose` from git-cliff step
- update file paths in release workflow to use relative paths without leading './'
- add footer template to cliff configuration
- update cliff header to include project details
- update cliff commit parsers to use simple type matching without regex prefixes
- 🐛 fix(ci): adjust git-cliff checkout depth and file paths

- remove unnecessary fetch-depth: 0 from checkout step
- update file paths in release step to use relative paths without leading './'
- 👷 ci(cliff): disable conventional commits parsing

- set `conventional_commits` to `false` in `.github/cliff.toml`
- set `filter_unconventional` to `true` to only process matching commits
- update file paths in the release workflow to use `${{ github.workspace }}` prefix
- reorder file list in release action for consistency
- migrate release workflow to use `git-cliff` for changelog generation
- clean up outdated release workflow steps and configurations
- upgrade GitHub Actions versions in the release workflow
- update changelog generation to use `git-cliff-action`
- remove deprecated changelog actions and configuration files
- update cliff configuration to use standard grouping for other changes
- 📦 build(ci): update file paths in release workflow

- prefix file paths with './' in the release step for clarity and robustness
- 🐛 fix(telemetry): correct CPU load calculation in telegram logs

- change divisor for cpu load from 100 to 10 in log formatting string
- Fix: remove files error for the moment
- Fix: files error
- Fix: * doesn't match any files in actions
- Fix: * doesn't match any files in actions
- Fix: sync cpuload precision to 0.1
- Fix: sync all precision to 0.1
- Fix: type-error
- Fix: type-error in telemetry
- 🐛 fix(aprs): correct parameter names for memory units

- change PARM.MemUsed to PARM.RAMUsed in header transmission
- change UNIT.Mb to UNIT.MB for consistency in header transmission
- update telegram log message to reflect RAM Used in MB
- 🐛 fix(ais): move filter setting after successful connection

- set_filter was being called before ais.connect()
- this caused the filter to potentially not be applied if the initial connection attempt failed and retried
- 🐛 fix(aprs): ensure filter is set after connection attempt

- move filter setting to after connection attempt in `ais_connect`
- this prevents potential issues if the filter is applied before the connection is fully established or if retries are involved
- 🐛 fix(gps): correct gpsd position handling

- handle gpsd position errors
- return (0, 0, 0) on error instead of "n/a"
- ensure fallback to .env config when gpsd data is unavailable
- 🐛 fix(main): correct telemetry and status timing

- move telemetry and status updates after position sending
- ensures consistent reporting in each sequence
- 🐛 fix(main): fix async call in send_position

- await the send_position function to ensure proper execution
- 🐛 fix(main): correct telemetry and status sending logic

- remove conditional check for sending telemetry and status messages
- ensure telemetry and status are sent every loop iteration
- 🐛 fix(dmr): correct dmr master list creation

- convert list of dicts to list to avoid type errors
- 🐛 fix(main): correct telemetry sequence and logging

- 【Telemetry Sequence】
  - corrected sequence number in telemetry message
  - changed sequence variable name from sequence to seq
- 【Logging】
  - corrected memory usage unit in telegram logs from MBytes to Mb
- 🐛 fix(dmr): correct dmrmaster extraction from logs

- fix parsing logic to accurately identify connected DMR masters
- ensure only unique masters are reported in the status
- 🐛 fix(main): correct header sending frequency

- fix header being sent too often
- adjust the modulo operator to send less frequently
- 🐛 fix(main): correct aprs reporting loop

- fix sequence logic for sending position and header information
- temporarily disable sending position to debug header sending
- 🐛 fix(gpsd): correct gpsd position and add satellite data

- fix typo in `get_gpsd_coordinate` function name, renaming it to `get_gpsd_position`
- add `get_gpsd_sat` to retrieve satellite count from gpsd
- include satellite count in telemetry data sent to aprs-is and telegram
- update aprs header to include gps satellite information
- use `os.cpu_count()` instead of parsing `/proc/cpuinfo` to determine cpu core count
- Fix identation
- 🐛 fix(osinfo): correct os name parsing in get_osinfo

- improve os name extraction from /etc/os-release
- fix the location of `id_like`
- 🐛 fix(osinfo): improve os information retrieval
- correct logic errors in parsing `/etc/os-release` for accurate OS information
- handle cases where certain fields are missing
- 🐛 fix(dmr): correct master callsign retrieval

- fix parsing logic to accurately extract master callsigns
- handle instances where callsigns contain underscores by replacing them with spaces
- 🐛 fix(telegram): correct telegram message id logging

- fix error when logging telegram message ID after sending a message
- 🐛 fix(osinfo): correct osname parsing in get_osinfo

- fix parsing logic to correctly split the line by "="
- ensure the osname format is correct by using "-" between id_like and version_codename
- 🐛 fix(telegram): correct link_preview_options format

- the 'link_preview_options' parameter requires a dictionary, not a list
- 🐛 fix(telegram): fix telegram location sending logic

- fix logic to only send location if lat and lon are not 0
- set default value of lat and lon to 0
- 🐛 fix(position): correct coordinate conversion in send_position

- fix the coordinate conversion in the `send_position` function
- convert latitude, longitude, and altitude to float before conversion
- 🐛 fix(position): correct lat/lon to integer for aprs

- fixed latitude and longitude values to be integers before conversion
- ensures proper formatting for aprs transmission
- 🐛 fix(telegram): improve telegram message logging

- add chat_id, message_thread_id and message_id to the log
- 🐛 fix(gps): handle gpsd errors and fallback to env vars

- return "n/a" on gpsd error instead of 0
- fallback to env vars if gpsd data is unavailable
- 🐛 fix(gps): ensure gpsd coordinates are set before return

- fix a bug where the coordinates were being set regardless of gpsd availability
- 🐛 fix(gps): increase gpsdclient timeout

- increase timeout to 15 seconds to prevent connection issues
- 🐛 fix(main): correct ais header sending frequency

- adjust ais header sending frequency to every 6 sequences
- 🐛 fix(telemetry): correct cpu temp decimal places

- fix cpu temp decimal places from 2 to 3
- change position telegram message to single line format
- 🐛 fix(telemetry): improve telegram logs format

- enhance readability of position, telemetry, and status logs on telegram
- include labels and units for better understanding of data
- 🐛 fix(telemetry): fix telemetry sending without await

- remove await to prevent blocking
- improve non-blocking send telemetry and status
- 🐛 fix(main): correct async call for send_position

- remove await for send_position to prevent blocking
- 🐛 fix(telegram): correct telegram token env variable name

- fix telegram integration by renaming TELEGRAM_BOT_TOKEN to TELEGRAM_TOKEN
- 🐛 fix(gps): correct .env quoting for gps coordinates

- change `quote_mode` from `"none"` to `"never"` when setting GPS coordinates in `.env` file
- resolves issue where coordinates were not being correctly read due to unintended quoting
- 🐛 fix(position): correct lat/lon conversion in send_position

- fix issue where lat/lon were converted to integers, causing inaccuracy
- use the original float values for _lat_to_aprs and _lon_to_aprs
- 🐛 fix(gps): correct return type for get_gpsd_coordinate

- change return type from str to float for latitude, longitude, and altitude
- 🐛 fix(position): correct lat/lon to integer

- fix lat/lon to integer to avoid type errors
- 🐛 fix(config): correct data type for aprs coordinates

- ensure that latitude, longitude, and altitude are strings
- update .env file with unquoted values from gpsd
- update config class with new values after gpsd update
- 🐛 fix(gpsd): correct gpsd coordinate retrieval and handling

- fix: correct boolean check for GPSD_ENABLE environment variable
- fix: ensure gpsd coordinates are properly retrieved and handled
- refactor: change lat/lon/alt defaults from 0.0 to "0.0" to avoid type errors
- 🐛 fix(gpsd): improve gpsd coordinate retrieval logic

- ensure valid gps fix (mode 2 or 3) before processing data
- log gpsd fix type (2d or 3d)
- only update .env file if valid coordinates are obtained
- 🐛 fix(gps): ensure valid gpsd data before processing

- check for valid 'TPV' class and sufficient mode
- handle missing 'lat', 'lon', 'alt' keys gracefully
- log warnings for insufficient or incomplete data
- 🐛 fix(cli): exit gracefully on keyboard interrupt

- ensure the program exits cleanly when Ctrl+C is pressed
- 🐛 fix(gps): handle gpsd coordinate retrieval

- fix: remove fallback to previous coordinates when GPSD is enabled but no fix is available
- the program should use the last known coordinates from GPSD or the default values instead
- fix: remove timeout from GPSDClient to prevent blocking
- 🐛 fix(deps): update gpsdclient import

- fix import statement for gpsdclient to resolve module not found error
- 🐛 fix(gps): correct latitude and longitude type in gpsd
- fix type for latitude, longitude, and altitude to prevent errors
- remove unnecessary float conversion when setting env variables
- 🐛 fix(gps): increase GPSDClient timeout

- increase GPSDClient timeout to 10 seconds to fix connection issues
- avoid program crash when GPSD is unavailable
- 🐛 fix(main): correct log and sequence file paths

- update log and sequence file paths to /tmp
- resolve permission issues in restricted environments
- 🐛 fix(config): correct logging call in config class

- correct the logging call from logger.info to logging.info
- 🐛 fix(logging): correct log file path

- fix log file path to be in the "tmp" directory
- avoid permission issues in "var/log" on some systems
- 🐛 fix(gps): correct conditional statement in coordinate validation

- fix the conditional statement to use != instead of is not to properly validate the gpsd coordinates
- 🐛 fix(gps): handle gpsd no fix scenario

- prevent script from crashing when gpsd has no fix
- log warning message when gpsd is enabled but no fix available
- use previous coordinates when gpsd has no fix
- 🐛 fix(config): correct logging configuration

- remove incorrect logger call
- add logging of environment variables
- 🐛 fix(modemmanager): handle missing return

- fix issue where lat, lon, alt are not returned when an exception is caught
- 🐛 fix(gps): fix coordinate return on exception
- ensure coordinates are returned even when GPSD data retrieval fails
- 🐛 fix(mmcli): correct modem index usage in location retrieval

- use modem index from `mmcli -L` output instead of hardcoded `0`
- ensures correct location retrieval when multiple modems are present
- 🐛 fix(aprs): correct modemmanager coordinates and aprs position

- fix modemmanager coordinates to validate lat, lon, alt values
- fix aprs position to get coordinates from gpsd or config file
- 🐛 fix(gps): correct return statement indentation

- fix indentation of return statement in get_gpsd_coordinate function
- ensure proper execution flow and prevent potential errors
- 🐛 fix(gps): fix gpsd coordinate return

- correct return statement indentation
- 🐛 fix(gps): correct coordinate handling when GPSD data is invalid

- avoid overwriting valid GPS data with default values
- return the last known valid coordinates if GPSD data is invalid
- 🐛 fix(gps): fix return statement in get_gpsd_coordinate function

- fix indentation of return statement to ensure it is properly executed
- 🐛 fix(gps): fix config write when gpsd data is valid

- correct the logic to write GPSD coordinates to the config file only when valid GPS data is received
- 🐛 fix(gps): correct typo in gpsd coordinate retrieval

- fix typo in `lon =result.get("lon", "n/a")`
- ♻️ refactor(gps): improve gps data retrieval

- replace subprocess.getoutput with subprocess.run for better error handling
- fix to return lat, lon, alt after parsing all lines
- 🐛 fix(gps): correct return statement placement

- fix return statement placement to ensure gps data is returned
- avoid returning default values when altitude is missing
- 🐛 fix(gps): correct mmcli execution path

- fix issue with gps data retrieval in certain environments
- ensures reliable gps location updates
- 🐛 fix(gps): correct gps data retrieval

- fix gps data retrieval by using subprocess.getoutput
- remove 'text=True' argument as it is not compatible with check_output
- 🐛 fix(gps): correct script execution path in gps data retrieval

- correct shell script execution path
- ensure proper execution of mmcli_loc_get.sh script for accurate GPS data retrieval
- 🐛 fix(gps): correct mmcli execution path

- resolve gps failing to get location due to incorrect path
- 🐛 fix(gps): correct gps data retrieval script execution
- use sudo to execute mmcli_loc_get.sh for proper permissions
- 🐛 fix(gps): correct path for mmcli_loc_get.sh execution

- correct path for mmcli_loc_get.sh execution
- ensure script runs from the correct directory
- 🐛 fix(logging): enable timed rotating file handler for logs

- resolve issue where log rotation was not functioning as intended
- activate TimedRotatingFileHandler to manage log file size and retention
- 🐛 fix(logging): disable log rotation to resolve file permission issue

- remove TimedRotatingFileHandler to avoid permission errors on log files
- 🐛 fix(gps): improve gps data logging format

- change gps data logging format for better readability
- display latitude, longitude, and altitude with labels
- 🐛 fix(main.sh): add virtual environment setup and dependency installation
- 🐛 fix(gpsd): add enable option to GPSD configuration and adjust sleep timing
- Revert [9da0215](https://github.com/HafiziRuslan/raspiaprs/commit/9da02157025d350bb65a93f5dc9bb23fc1a2bb4b)

🐛 fix(gpsd): update configuration with GPSD latitude, longitude, and altitude and save to config file for later use if gpsd failed
- 🐛 fix(config): simplify GPSD enable check in configuration
- 🐛 fix(gpsd): add enable option to GPSD configuration
- 🐛 fix(config): update gps device path

- change device path from /dev/ttyUSB0 to /dev/ttyS0
- correct the serial port used for gps device
- 🐛 fix(raspiaprs): remove unused gpsd device option

- remove unused device option
- fix gps data retrieval
- 🐛 fix: correct telemetry data order

- Fixes telemetry data order to match expected format
- Addresses incorrect data being sent to APRS
- 🐛 fix(raspiaprs): correct telemetry format

- fixed the telemetry format for the APRS data
- removed the extra '00' at the end of the telemetry string
- added an additional parameter to the EQNS string
- 🐛 fix(telemetry): correct time format in telemetry string

- fix the telemetry string to include the current time in UTC format
- the time is now included as a key-value pair (time=DDHHMMz)
- 🐛 fix(aprs): correct uptime format for aprs

- fix "minutes" abbreviation to "mi" to avoid confusion
- remove extra space after comma in uptime string
- 🐛 fix(telemetry): improve uptime formatting and connection stability

- shorten uptime units for brevity
- increase connection retry delay
- add randomness to sleep interval
- 🐛 fix(telemetry): correct status message format

- fix order of variables in status message
- ensure correct information is displayed
- 🐛 fix(position): correct aprs position format

- fix uncompressed aprs position format
- remove the old code for sending position
- 🐛 fix(position): correct altitude formatting in APRS payload

- ensure altitude is formatted as a 4-digit number with leading zeros
- remove unnecessary colon after callsign in packet construction
- 🐛 fix(position): correct altitude formatting in APRS payload

- fix altitude formatting to remove unnecessary ".0f"
- 🐛 fix(position): correct aprs packet format

- remove redundant callsign in packet
- fix aprs packet format to comply with specification
- 🐛 fix(aprs): correct string formatting in aprs script

- use f-strings for modem firmware, dmr master, and uptime information
- improve code readability and maintainability
- 🐛 fix(dmr): correct XLX master identification

- fix logic to correctly identify XLX master in DMR network
- 🐛 fix(raspiaprs): remove redundant pass statements

- Removed unnecessary 'pass' statements in the get_dmrmaster function.
- These statements do not contribute to the logic and can be considered dead code.
- 🐛 fix(dmr): correct dmrmaster count check

- use len() to check the number of items in the dmrmasters list
- dmrmasters.count() is not a valid method for lists
- 🐛 fix(dmr): correct dmr master string formatting

- initialize dmr_master to empty string
- only append connection information if dmrmasters list is not empty
- this prevents adding "connected via []" when no DMR masters are found
- 🐛 fix(raspiaprs): update radio mode names and telemetry format

- rename "YSF" to "C4FM" for clarity and consistency with other radio modes.
- remove "FM" and "Pager" from the telemetry header and data as they are no longer explicitly tracked.
- adjust the telemetry data format to match the updated header, ensuring correct alignment and number of parameters.
- 🐛 fix(raspiaprs): correct telemetry format for modes

- The modes variable was incorrectly formatted as an integer in the telemetry string,
  leading to potential display issues.
- Changed the format specifier for modes from {:d} to {} to ensure it's
  represented as a string, handling cases where modes might not be a simple integer.
- 🐛 fix(config): use fallback for configparser get

- changed `get` method calls to use `fallback` parameter instead of default value
- this ensures consistent behavior when options are missing in the config file
- 🐛 fix(raspiaprs): correct parameter names in header

- Rename "D-Star" to "D*" for consistency.
- Rename "POCSAG" to "Pager" for clarity.
- 🐛 fix(config): simplify MMDVM mode detection

- use getboolean with a default value of 0 to directly retrieve boolean values
- remove redundant checks and assignments for a cleaner and more concise implementation
- 🐛 fix(raspiaprs): remove AX.25 from MMDVM mode check and telemetry

- The AX.25 mode was incorrectly included in the `get_mmdvmmode` function and the telemetry header.
- This commit removes the AX.25 check from `get_mmdvmmode` as it's not a standard MMDVM mode.
- It also removes AX.25 from the telemetry header and data sent to the AIS server.
- 🐛 fix(systemd): ensure network is online before starting service

- change 'Require=network.target' to 'After=network-online.target'
- this ensures the network is fully configured and online before the service attempts to start, preventing potential startup failures.
- 🐛 fix(systemd): ensure network is available before starting service

- change `After=network.target` to `Require=network.target`
- this ensures that the network is fully up and configured before the APRS service attempts to start, preventing potential startup failures.
- 📝 docs(README): simplify systemctl commands

- remove '.service' suffix from systemctl commands for enabling, starting, stopping, and checking status.
- update journalctl command to reflect the simplified service name.
- 🐛 fix(logging): improve reflector log parsing

- update log_ref_string to include "XLX" for better matching
- use tail -1 to get the last matching line for reflector logs
- 🐛 fix(systemd): adjust service restart limits

- increase StartLimitIntervalSec to 300 seconds
- increase RestartSec to 45 seconds
- remove CPU and memory limits to allow for more flexibility
- 🐛 fix(dmr): improve dmr master connection string

- update dmr master connection string to include brackets for clarity
- this change improves the readability of the dmr master connection information
- 🐛 fix(raspiaprs): Correctly parse DMR master and reflector information

- uncommented log_ref_string for reflector linking logs.
- uncommented ref_line for capturing reflector linking log entries.
- added logic to correctly identify XLX reflectors by parsing reflector linking logs.
- previously, XLX reflectors were not correctly identified and processed.
- this change ensures accurate reporting of DMR master and reflector status.
- 🐛 fix(raspiaprs): correct dmr master connection string

- remove unnecessary sort call from dmr_master string formatting
- ensure correct display of connected DMR masters
- 🐛 fix(raspiaprs): correct DMR master log parsing

- uncommented lines related to parsing "Closing DMR Network" log entries
- uncommented lines related to parsing DMR master DC entries
- corrected logic to handle and remove master DC entries from the dmrmaster list
- ensured that XLX entries are correctly identified and handled when processing master DC entries
- 🐛 fix(raspiaprs): correct regex for XLX identification

- update regex in get_dmrmaster to correctly identify XLX lines
- ensure accurate parsing of DMR master data
- 🐛 fix(raspiaprs): remove unused DMR master DC log parsing

- comment out lines related to parsing "Closing DMR Network" logs
- these lines were not being used and were causing unnecessary processing
- this simplifies the code and removes potential future issues
- 🐛 fix(raspiaprs): correct DMR master parsing logic

- rename loop counters to avoid shadowing built-in functions
- fix XLX ID parsing to correctly identify and replace XLX entries in dmrmaster
- 🐛 fix(raspiaprs): Correctly handle DMR master data processing

- addresses an issue where DMR master data was not being processed correctly
- ensures that XLX callsigns are properly replaced with their corresponding reference data
- improves the accuracy of DMR master callsign parsing
- 🐛 fix(uptime): remove timezone specifier from uptime string

- The uptime string format did not include timezone information,
  leading to inconsistent formatting. Removed the %Z specifier
  to align with the expected output.
- 🐛 fix(vnstat): correct parsing of vnstat output

- adjust split indices to accurately capture traffic data
- ensure correct parsing of average speed and units
- 🐛 fix(raspiaprs): correct DMR master connection string and position comment

- fix: ensure DMR master connection string is correctly formatted by adding a preceding space
- fix: remove redundant `get_dmrmaster()` call from `send_position` function's comment as it's already included in `get_mmdvminfo()`
- 🐛 fix(raspiaprs): improve DMR master connection logic

- open MMDVMHOST_FILE using 'with open' for better resource management
- handle potential subprocess.CalledProcessError when grepping logs
- refine logic for extracting and processing DMR master connection strings
- ensure correct handling of XLX connections and reflector links
- improve sorting and joining of connected DMR masters for clarity
- 🐛 fix(dmr): correct config parsing for dmrgw

- use a new ConfigParser instance for checking DMR enable status
- this ensures that the correct configuration is read for the dmrgw functionality
- 🐛 fix(dmr): correctly handle DMR master string formatting

- ensure DMR master string is only returned when DMR is enabled in config
- sort DMR masters before joining them into a string for consistent output
- 🐛 fix(raspiaprs): correct XLX DC identification in dmrmaster

- When searching for "XLX" in dmrmaster, the index was being incorrectly retrieved
  using `dmrmaster.index(re.search("^XLX", dmrmaster[count]))`.
- This has been corrected to use the loop counter `dccount` which corresponds
  to the correct position within the `dmrmaster` list:
  `dmrmaster.index(re.search("^XLX", dmrmaster[dccount]))`.
- 🐛 fix(dmr): ensure cc is empty when dmr is disabled

- In `get_mmdvminfo`, if DMR is disabled, `cc` should be an empty string.
- Previously, `cc` would incorrectly contain " DMRCC" followed by the color code even when DMR was not enabled.
- 🐛 fix(dmr): improve dmrgw master detection and handling

- Added detection for DMRGateway master disconnects and reflector linking.
- Implemented logic to remove disconnected masters from the list and insert linked reflectors.
- Refined master detection to handle different log formats and potential race conditions.
- Utilized regex for more robust parsing of log entries.
- Ensured that XLX masters are correctly handled by removing and re-inserting them with reflector information.
- 🐛 fix(traffic): improve network traffic reporting

- change traffic reporting to use 5-minute intervals for more granular data
- adjust units for network traffic to kbit/s to match vnstat output
- convert Mbit/s and Gbit/s to kbit/s for consistent reporting
- 🐛 fix(raspiaprs): sort dmrmasters correctly

- remove sort from list creation
- sort dmrmasters after creation to avoid incorrect ordering
- 🐛 fix(raspiaprs): improve DMR master display

- sort DMR master list before joining
- use comma-separated string for better readability of multiple DMR masters
- 🐛 fix(raspiaprs): correctly parse DMR master logs

- change log_line from string to list to store multiple grep results
- iterate through log_line list to correctly extract DMR master information
- use splitlines() to handle multiple log entries
- ensure DMR masters are correctly parsed and deduplicated
- 🐛 fix(raspiaprs): correctly assign software version

- initialize softver to " Unknown" to prevent errors
- use pass statement to handle potential IOErrors or ValueErrors gracefully
- 🐛 fix(raspiaprs): improve DMR master parsing

- Correctly parse DMR master from log output.
- Handle cases where log lines might not contain the expected format.
- Ensure unique DMR masters are returned.
- 🐛 fix(raspiaprs): resolve dmrmaster data duplication

- comment out unused dmrmaster list initialization
- comment out duplicate removal for dmrmasters list
- ensure correct data is appended to dmrmasters list
- fix potential data duplication issue by removing unnecessary list conversion
- 🐛 fix(dmr): correct dmrmaster parsing logic

- initialize dmrmaster as an empty list before the loop
- append found masters to dmrmaster list
- ensure unique masters are returned by using dict.fromkeys
- 🐛 fix(raspiaprs): correctly parse DMR master calls

- iterate over log lines to find DMR master calls
- split the line and extract the master callsign
- 🐛 fix(raspiaprs): correct master parsing logic

- fix bug where masters was iterating over a string instead of appending the whole string
- ensure dmrmaster list correctly captures the masters string
- 🐛 fix(raspiaprs): correct DMRS master connection string formatting

- change "connected to ".join(dmrmasters) to "connected to " + "".join(dmrmasters)
- this ensures that the "connected to " prefix is only added once, and all connected masters are listed consecutively without extra spaces.
- 🐛 fix(service): adjust service restart and startup behavior

- reduce restart delay to 15 seconds
- add pre-start sleep of 90 seconds to allow network to initialize
- 🐛 fix(osinfo): correct Pi-Star/WPSD version string format

- reverse version and MMDVMHost order
- change separator from "-" to "#"
- 🐛 fix(osinfo): correct os info formatting

- fix spacing and prefixes in os info string for readability
- standardize version prefixes to "#" for consistency
- 🐛 fix(config): resolve passcode retrieval from config file

- correct the section where the passcode is read from the config file from `APRS-IS` to `APRS`
- 🐛 fix(telemetry): correct formatting of aprs comment field

- remove unnecessary semicolons and adjust spacing in aprs comment to improve readability
- ensure data fields in aprs comment are properly concatenated for better information display
- 🐛 fix(telemetry): correct data type for traffic value

- ensure traffic value is an integer for accurate reporting
- 🐛 fix(config): correct passcode retrieval from config file

- fix the section to get the passcode from the config file
- 🐛 fix(traffic): correct index for traffic statistics

- fix index to retrieve correct average traffic value
- 🐛 fix(traffic): correct traffic data type and add logging for sleep

- correct traffic data type from int to float to handle decimal values
- add logging information for sleep duration
- 🐛 fix(aprs): correct uptime format

- remove trailing semicolon from uptime string
- 🐛 fix(general): correct uptime format

- change uptime format to be compatible with APRS
- 🐛 fix(telemetry): correct uptime string format

- adjust uptime string to meet APRS format
- 🐛 fix(aprs): correct uptime format and add timestamp

- adjust uptime format to include seconds
- add timestamp after uptime
- 🐛 fix(aprs): correct EQNS format in send_header

- remove trailing comma in EQNS string to match expected format
- 🐛 fix(ax.25): correct aprs header equations

- correct aprs header equations to match aprs spec
- 🐛 fix(telemetry): correct callsign format in telemetry string

- fix the callsign format in the telemetry string to ensure correct APRS transmission
- 🐛 fix(telemetry): correct format string in send_header and main

- fix format string to correctly pass the callsign
- 🐛 fix(telemetry): correct callsign formatting in aprs messages

- remove unnecessary curly braces around callsign in telemetry messages
- ensures proper aprs format and transmission
- 🐛 fix(telemetry): correct string formatting in telemetry and uptime messages

- fix string formatting issues in telemetry and uptime messages
- ensure correct variable substitution in the telemetry and uptime strings
- 🐛 fix(main): correct uptime string and randomize sleep

- fix the uptime string to match the specifications
- add randomization to sleep to avoid collisions
- 🐛 fix(aprs): improve uptime format for readability

- replaces " and" with "," in uptime string for better formatting
- Update get_osinfo function: fix kernel and OS version retrieval logic for accurate output
- Merge pull request #2 from 0x9900/fred/senderror

fix connection error
- Fix connection error

### 💼 Other

- Update CHANGELOG
- Update CHANGELOG
- Update changelog
- Update changelog
- Merge branch 'master' of https://github.com/HafiziRuslan/RPi-APRS
- Merge branch 'master' of https://github.com/HafiziRuslan/RPi-APRS
- Run changelog on push
- [Changelog CI] Add Changelog for Version ae1c38ed31d5d068814908845ff28e5e766d8146
- Update Python versions in pylint workflow
- Set package-ecosystem to 'pip' in dependabot config
- Delete .github/workflows/pylint.yml
- Merge branch 'master' of https://github.com/HafiziRuslan/RPi-APRS
- Add Pylint workflow for Python code analysis
- Merge pull request #2 from HafiziRuslan/virtual-env

Refactor configuration management and enhance GPS integration
- Add GitHub Actions workflow to sync with GitLab
- 📦 build(systemd): delay raspiaprs start

- add ExecStartPre to delay the start of raspiaprs service by 90 seconds
- this allows the network to fully initialize before raspiaprs starts
- Fix get_uptime function: move current time retrieval above uptime calculation for accurate display
- Enhance uptime display: prepend current time to uptime string format
- Add source reference to README: include link to aprstar repository
- Add new LICENSE file: include BSD 2-Clause License with updated copyright information
- Fix send_header function: update parameter names for consistency in data transmission
- Fix get_modem function: replace subprocess.run with check_output for improved output handling
- Fix get_modem function: update subprocess.run to capture stdout for better error handling
- Remove ExecStartPre directive for 90-second delay in raspiaprs.service
- Update raspiaprs.service: increase RestartSec to 15 and add ExecStartPre for a 90-second delay
- Fix get_modem function: update datetime usage for log file naming and replace check_output with run for better error handling
- Update SSID configuration: change default SSID from 1 to 10 in raspiaprs.conf and from 1 to 0 in raspiaprs.py
- Update configuration files: standardize call sign format and improve comments in raspiaprs.conf and raspiaprs.py
- Refactor project structure: rename files and update configuration for consistency
- Fix get_freemem function: ensure return value is an integer for accurate free memory percentage
- Fix get_load function: ensure return value is an integer for accurate load percentage
- Update README.md: enhance clarity and formatting in installation and usage instructions
- Refactor memory and load calculations: improve accuracy in get_load and get_freemem functions
- Fix get_freemem function: correct memory calculation by adjusting cache memory division
- Fix get_load function: convert core count to float for accurate CPU load calculation
- Update load and memory functions: improve CPU load calculation and refine memory usage metrics
- Update get_osinfo function: adjust OS version formatting for improved readability
- Update README.md: add update instructions for RPi-APRS service
- Update main function: change telemetry data structure from dictionary to string format for improved clarity
- Refactor main function: replace data structure with individual sends for telemetry and uptime, improve logging
- Update main function: change data structure from list to dictionary for improved clarity and logging
- Update get_osinfo function: refine kernel and OS version retrieval logic for improved accuracy
- Update get_osinfo function: enhance kernel and OS version retrieval, improve error handling for PiStar and WPSD release files
- Update get_osinfo function: improve kernel version retrieval and handle exceptions for PiStar and WPSD release files
- Update rpiaprs.py: correct variable names for PiStar and WPSD release files and enhance version retrieval logic
- Refactor Config class: update server and port properties for clarity
- Update README.md: improve installation commands formatting and add troubleshooting tips
Update rpiaprs.py: change 'host' to 'server' in configuration for clarity
- Update README.md and rpiaprs.conf: improve clarity of installation instructions and configuration comments
- Update rpiaprs.conf: enhance comments for latitude, longitude, and altitude fields to improve clarity
- Update README.md: streamline installation instructions by consolidating commands
- Update README.md: improve installation instructions and clarify configuration steps
- Refactor memory and uptime reporting: simplify freemem return value, update piversion formatting, and enhance position packet comment structure
- Enhance modem firmware detection: update get_modem function to include additional modem descriptions and improve parsing logic
- Enhance modem information retrieval: update get_modem function and modify packet comment to include modem details
- Update packet comment format: change GitHub link to use HTTPS for improved security
- Update APRS-IS configuration: change password placeholder and modify filter setting
- Reorder packet comment format: move GitHub link to the front for better visibility
- Improve DMR frequency shift display: add conditional formatting for TX/RX frequency differences
- Update send_header call frequency: change condition to every 10th sequence
- Enhance rpiaprs configuration: add altitude parameter and improve comments for clarity
- Update README.md formatting and enhance rpiaprs.py comments: improve readability and add GitHub link
- Refactor configuration settings and improve logging: update default values and enhance error handling
- Update rpiaprs.service: remove Type=simple line for service configuration
- Update .gitignore to include aprstar-WIP.py file
- Fix formatting issue in default configuration: separate 'sleep' value from 'pip'
- Update installation instructions and configuration files: streamline pip install command and correct default call sign
- Update send_position function: change tocall from "APP720" to "APP642"
- Fix logging message and adjust indentation in get_uptime function
- Update send_position function: change tocall from "APRS" to "APP720"
- Refactor aprstar.py: streamline imports, enhance logging, and improve configuration handling
- Refactor project structure: rename and update files for RPi-APRS, add configuration and service files
- Merge pull request #3 from 0x9900/fred/senderror

Python 3
- Python 3
- Hardening ais connections
- Let's make it less verbose
- Create LICENSE
- Logging when the position is infered
- Casting the symbol into a string
- Example of telemetry
- Installation notes for pi-star
- Readme...
- Adding the origin of aprstar
- How to install aprstar
- Making the code work on python 2 and 3
- Adding a readme file
- Send the header first when the program starts
Sleep time is part of the config
- Adding FreeMemory metric
Custom iterator for the sequence number
- Initial version

### 🚜 Refactor

- ♻️ refactor(system): clean up type conversions in system metric functions

- remove redundant float/int conversions in get_cpuload
- remove redundant float/int conversions in get_memused
- adjust return calculation for get_memused to divide by 100 instead of casting to int
- simplify temperature reading and return in get_temp
- update EQNS string in send_header for consistency (changed 0.001 to 0.01 for first three params)
- ♻️ refactor(config): improve readability and adhere to Python conventions

- reformat Config class initialization and property setters for better readability
- wrap long lines in __repr__ method for cleaner output
- update memory usage calculation to round to 4 decimal places
- adjust CPU temperature return value to 4 decimal places
- simplify log file processing in get_osinfo by removing unnecessary intermediate variables
- update MMDVM info parsing to correctly handle line reading after setting DMR enabled status
- remove unused `re` import assumption by simplifying DMR master parsing logic
- update APRS header EQNS string to use 0.01 divisor for better precision alignment with other metrics
- simplify `get_memused` return to ensure correct float representation before casting to int (though the cast truncates, rounding is applied before)
- update Telegram logging to correctly pass only the message when location data is absent, avoiding unnecessary arguments
- adjust APRS position packet creation to ensure latitude/longitude/altitude are explicitly cast to float before formatting
- ♻️ refactor(main): simplify header sending logic

- move send_header to synchronous function
- call send_header directly instead of awaiting it
- reduce redundant await calls
- ♻️ refactor(dmr): improve dmr master retrieval logic

- add type hints for clarity and maintainability
- initialize variables with explicit types
- ♻️ refactor(main): change send_header to async

- rename send_header to async function
- call async send_header instead of sync
- ♻️ refactor(location): remove modemmanager coordinates function

- remove the get_modemmanager_coordinates function
- this function is no longer needed
- ♻️ refactor(deps): move urllib import

- move urllib import to be with other urllib related imports
- ♻️ refactor(main): consolidate imports and update dependencies

- group imports by category for better readability
- update dependencies to the latest versions for security and performance improvements
- ♻️ refactor(main): convert send_header to async

- convert send_header to async function
- use await for send_position in send_header
- use await for send_header, send_position, and ais.sendall in main
- ♻️ refactor(main): migrate Telegram logging to asynchronous

- Switch from synchronous telegram library to asynchronous
- Update logs_to_telegram to be an async function
- Update send_position and main to call logs_to_telegram with await
- Use asyncio.run to run the main function
- Read telegram config from environment variables
- ♻️ refactor(gps): improve gps coordinate handling
- store sequence file in tmp directory
- change lat, lon, alt type to float

🔧 chore(main): update log file path and remove unused directory

- change log file path to /var/log/raspiaprs.log
- remove unused /logs/* entry from .gitignore
- remove placeholder log file
- ♻️ refactor(aprs): disable telegram integration

- comment out telegram functionality to remove dependency
- remove telegram import
- comment out logs_to_telegram calls
- ♻️ refactor(main): adjust transmission intervals for efficiency

- adjusted header transmission interval to every 12 sequences
- added position transmission every other sequence to increase position reporting
- ♻️ refactor(gps): switch to modemmanager for gps data
- remove gpsd dependency
- use modemmanager to get gps data
- add mmcli_loc_get.sh script to get location from modemmanager
- remove gpsd code and replace with modemmanager code
- update readme to reflect changes

📝 docs(readme): update dependencies
- removed gpsd from the list of dependencies
- ♻️ refactor(readme): improve documentation clarity and update file paths
- remove unnecessary comments and simplify installation instructions
- update file paths to reflect actual locations, use relative paths
- rename sample config file and script to match actual file names
- enhance readability and provide accurate guidance for users
- ♻️ refactor: improve raspiaprs configuration and usage

- pass config as self to methods for better readability
- update send_position, ais_connect, main functions
- replace config. calls with self. calls for clarity
- ♻️ refactor: remove unused import

- remove unused import statement for re module
- ♻️ refactor(raspiaprs): remove unused mode function and telemetry data

- Remove get_mmdvmmode function, as it is unused.
- Remove DMR, DSTAR, C4FM, P25, NXDN, and POCSAG from telemetry.
- Update telemetry string formatting.
- ♻️ refactor: remove modem firmware retrieval

- Removed the `get_modem` function and its related logic.
- The modem firmware information retrieval was unreliable.
- Simplified the `get_osinfo` function.
- Updated the comment string to reflect the changes.
- ♻️ refactor(main): improve code readability and maintainability

- format code to adhere to PEP 8 guidelines for better readability
- remove redundant variables and simplify calculations
- improve error handling and logging for robustness
- use f-strings for string formatting for clarity and efficiency
- refine logic for determining modem firmware and connected DMR masters
- replace aprslib.packets with manual string formatting for aprs packets
- ♻️ refactor(sequence): simplify sequence file name

- change sequence file name from "raspiaprs.sequence" to "raspiaprs.seq"
- shorter file name for easier handling and less typing
- Update README and refactor functions: clarify metrics terminology and rename functions for CPU load and memory usage

### 📚 Documentation

- 📝 docs(ci): standardize changelog file reference

- change 'changelog' references to 'CHANGELOG' in release workflow
- ensures consistency with generated file name CHANGELOG.md
- 📝 docs(changelog): adjust cliff configuration and release workflow

- update cliff.toml header formatting for changelog generation
- move changelog commit logic to the end of the release workflow
- remove redundant commit step from older location in release workflow
- add newline to unreleased section header in cliff.toml
- Docs: update CHANGELOG.md
- Docs: update CHANGELOG.md
- Docs(CHANGELOG): update release notes
- 👷 ci(workflows): streamline release and changelog generation

- 【build】remove unnecessary file list from pre-release workflow
- 【ci】update changelog workflow trigger to include 'edited' release event
- 【ci】replace changelog updater action with `auto-generate-changelog` for consistency and simplification
- 【docs】remove redundant permissions block from update-changelog workflow
- 📝 docs(readme): rename README to README.md
- 📝 docs(readme): update license file reference

- rename LICENSE.md to LICENSE for standard practice
- update README to reflect license file name change
- 📝 docs(readme): update instructions for RasPiAPRS

- add execute permission for shell scripts
- use autostash option to prevent merge conflicts
- 📝 docs(README): improve installation and configuration instructions

- update example aprs.fi link
- simplify installation instructions
- replace ConfigParser with .env for configuration
- update autostart instructions
- remove unnecessary commands
- 📝 docs(readme): update dependencies in readme

- update dependencies from 4 to 5
- add `python-telegram-bot` dependency
- 📝 docs(README): add gpsd to dependency list

- add gpsd to dependency list
- update dependency count from 3 to 4
- 📝 docs(gitignore): add log folder to gitignore

- prevent log files from being tracked by git
- 📝 docs(config): update GPSD configuration

- add comments for GPSD host
- remove unused GPSD configuration options
- clarify GPSD device path information
- 📝 docs(readme): remove unused metrics

- removed disk used and traffic average from readme
- 📝 docs(main): add docstrings to functions and classes

- add detailed docstrings to classes
- add detailed docstrings to functions
- 📝 docs(README): update traffic metric description

- change "Traffic daily average" to "Traffic average per 5 min" to accurately reflect the metric displayed.
- 📝 docs(readme): update installation path for raspiaprs

- changed installation path from /usr/local/bin to /usr/bin for raspiaprs script
- updated the service file to reflect the new path
- updated installation instructions in README.md and during update process
- renamed raspiaprs.py to reflect the new destination path
- 📝 docs(readme): correct service disable command order

- move the `sudo systemctl disable raspiaprs.service` command to appear before `git pull`
- this ensures the service is stopped and disabled before attempting to pull updates, preventing potential conflicts or errors.
- 📝 docs(readme): correct installation script paths

- update paths in the installation script section to match the actual file locations
- ensure the README accurately reflects the installation process
- 📝 docs(readme): simplify systemctl status command

- remove sudo from systemctl status command to align with standard usage
- 📝 docs(readme): update service installation instructions

- add commands to disable, copy, and enable the systemd service
- ensure the service file has correct permissions

♻️ chore(raspiaprs.service): adjust service restart delay and pre-exec sleep

- increase RestartSec to 30 seconds
- remove ExecStartPre=/bin/sleep 90 as it is no longer necessary
- Update README and rpiaprs.py: enhance documentation clarity and add default APRS-IS server settings

### ⚡ Performance

- ⚡️ perf(aprs): reduce precision for some telegram values
- ⚡️ perf(aprs): reduce precision for some EQNS values

- decreased precision for two values in the EQNS string sent to APRS
- this might slightly improve transmission stability or efficiency
- ⚡️ perf(aprs): reduce precision for some EQNS values

- decreased precision for two values in the EQNS string sent to APRS
- this might slightly improve transmission stability or efficiency
- ⚡️ perf(monitoring): remove unnecessary rounding in system metric calculations

- remove .__round__(4) from get_memused calculation to return integer
- remove .__round__(4) from get_temp calculation to return integer
- ⚡️ perf(main): improve ais message sending efficiency

- change await send_position to send_position to prevent blocking
- ⚡️ perf(raspiaprs): adjust random sleep duration

- increase the upper bound of random sleep duration by 15 seconds
- this change aims to improve the distribution of network traffic and reduce potential congestion
- ⚡️ perf(disk, memory): optimize disk and memory usage calculation

- change disk usage calculation from percentage to gigabytes for better readability
- adjust the disk usage calculation to use integer division by 1000 for efficiency
- change memory usage calculation from percentage to megabytes for better readability
- adjust the memory usage calculation to use integer division by 1000 for efficiency
- Implement code changes to enhance functionality and improve performance

### 🧪 Testing

- 👷 ci(release): update GitHub Actions versions

- upgrade actions/checkout from v6 to main
- upgrade orhun/git-cliff-action from v4 to main
- upgrade svenstaro/upload-release-action from latest to master
- 【chore】remove unused name from changelog job
- 【chore】remove unused git checkout command in commit changelog step

### ⚙️ Miscellaneous Tasks

- 👷 ci(release): restructure workflow jobs

- rename 'changelog' job to 'release' in the main workflow file
- move changelog generation to a separate 'changelog' job
- update 'release' job to use the last commit message as the release body
- ensure changelog generation runs independently after release steps
- 📦 build(ci): include requirements and environment file in release

- update upload-release-action to include requirements.txt and default.env
- ensure necessary files are bundled for the beta release
- 📦 build(ci): simplify release asset upload

- remove requirements.txt and default.env from assets uploaded in release workflow
- 📦 build(ci): adjust file paths in release workflow

- update file paths in release workflow to use relative paths starting from root (./)
- this ensures correct referencing of files during the build and release process
- 📦 build(ci): update release workflow to use workspace path

- use `${{ github.workspace }}` when specifying files for release action
  - ensures correct path resolution within the GitHub Actions runner environment
- 🔧 chore(ci): migrate release workflow to use git-cliff

- delete deprecated `.github/workflows/pre-release.yml`
- create new `.github/workflows/release.yml` using `git-cliff-action` for changelog generation
- configure `git-cliff.toml` for desired changelog format and grouping
- update commit steps in workflow to automatically stage and commit `CHANGELOG.md`
- update release step to use generated changelog content
- 👷 ci(pre-release): switch changelog generation action

- replace saadmk11/changelog-ci with janheinrichmerker/action-github-changelog-generator
- remove deprecated changelog output steps
- update workflow to use the new action consistently
- 👷 ci(pre-release): set explicit release version in workflow

- explicitly set release_version to v0.1-beta.1 in changelog-ci step
- ensures consistent versioning during pre-release workflow execution
- 👷 ci(workflow): switch to changelog-ci action

- replace janheinrichmerker/action-github-changelog-generator with saadmk11/changelog-ci
- add changelog-ci configuration file (.github/changelog-ci-config.yaml)
- configure workflow to use the new action and output summary
- 👷 ci(pre-release): remove redundant body append setting

- remove `append_body: true` from softprops/action-gh-release step
- the default behavior already appends the body path content
- 🔧 chore(ci): remove deprecated changelog configuration

- remove .github/changelog-ci-config.json as it is no longer needed
- update pre-release workflow to remove step for generating changelog via previous action
- 👷 ci(workflow): replace changelog generation action

- switch from requarks/changelog-action to janheinrichmerker/action-github-changelog-generator
- remove outdated 'tag: beta' parameter from previous action
- 👷 ci(pre-release): adjust changelog action input

- switch from 'fromTag/toTag' to 'tag' input for changelog generation
- remove static tag name setting in commit step
- 🔧 chore(ci): adjust changelog action tag range

- set fromTag and toTag to 'master' in requarks/changelog-action
- ensure changelog generation covers the correct commit range for pre-release
- 👷 ci(pre-release): use GITHUB_TOKEN for changelog action

- switch changelog action token from github.token to secrets.GITHUB_TOKEN
  - ensures proper secret usage for GitHub actions authentication
- 👷 ci(pre-release): improve changelog generation workflow

- switch to dedicated changelog action for better integration
- ensure full history is fetched for accurate changelog generation
- update commit step to use file_pattern for CHANGELOG.md
- adjust body_path in release step to reflect correct file location
- 👷 ci(release): adjust pre-release workflow condition

- remove explicit check for `github.ref_type == 'tag'` in release step
- allow release action to proceed based on other workflow triggers
- 🔧 chore(ci): remove changelog workflow and update release process

- removed deprecated `.github/workflows/changelog.yml` file
- updated `.github/workflows/pre-release.yml` to use modern actions and workflow syntax
- updated README to reference `default.env` instead of `.env.SAMPLE`
- renamed `.env.SAMPLE` to `default.env` for better clarity in setup instructions
- 👷 ci(workflows): update changelog flow type
- 👷 ci(workflows): update github actions workflow names and steps

- rename workflow file generate-changelog.yml to changelog.yml
- update workflow names for better clarity (e.g., 'Changelog', 'Auto-Merge', 'Release', 'Sync Repo')
- update checkout action version in changelog workflow to main
- remove redundant steps/names in pre-release workflow
- simplify sync-to-gitlab workflow steps by removing unnecessary comments/renaming job
- 👷 ci(workflow): include published event for changelog generation

- trigger changelog generation workflow on tag publication in addition to creation/editing
- 👷 ci(workflows): update github action versions and release files

- update BobAnkh/auto-generate-changelog action to 'master'
- update gr2m/merge-schedule-action action to 'master'
- update marvinpinto/action-automatic-releases title format in pre-release workflow
- add .env.SAMPLE, requirements.txt, and main.py to pre-release files
- update keninkujovic/gitlab-sync action to 'main'
- 🔧 chore(ci): clean up unused and update GitHub workflows

- remove deprecated changelog-ci workflow
- update pre-release workflow to include necessary files in release artifacts
- ensure correct permissions and environment variables in other workflows
- 👷 ci(release): add pre-release workflow

- create new github actions workflow for pre-releases on master branch
- use action-automatic-releases to create a beta pre-release
- 🔧 chore(ci): clean up obsolete and update workflow triggers

- remove obsolete auto-approve workflow for dependabot/github-actions
- update changelog-ci trigger to only run on pull_request opened event
- add auto_merge_enabled trigger to merge-schedule workflow
- 🔧 chore(ci): adjust changelog workflow configuration

- rename job from build to build-changelog for clarity
- comment out github_token usage in changelog action step
- 👷 ci(workflows): add auto approve workflow for bots

- introduce a new workflow to automatically approve PRs opened by dependabot or github-actions[bot]
- use hmarr/auto-approve-action for the approval process
- Merge pull request #3 from HafiziRuslan/changelog-ci-ae1c38

[Changelog CI] Add Changelog for Version ae1c38e
- 👷 ci(workflow): use commit hash as fallback release version

- set default release_version to head commit ID if not provided in inputs
- ensures changelog generation works even without explicit version input during CI runs
- 🔧 chore(ci): update changelog workflow inputs

- remove default release version fallback to head commit
- explicitly pass github_token to the action
- 🔧 chore(ci): enable manual release version input in changelog workflow

- uncommented and configured `release_version` input for `workflow_dispatch` event
- default `release_version` to `github.event.head_commit` if not provided during manual dispatch
- 🔧 chore(ci): disable manual release version input in workflow

- remove `release_version` input from `workflow_dispatch` trigger
- comment out usage of `release_version` in build job step
- 🔧 chore(ci): remove redundant changelog step

- remove unused step for generating changelog in CI pipeline
- 👷 ci(pylint): remove pylint workflow

- remove pylint workflow as it's no longer needed
- 🔧 chore(main): enhance logging and venv management

- add timestamped logging for better monitoring
- ensure venv is activated before running main.py
- loop main.py execution with a 15-second delay
- 🔧 chore(config): remove logging of environment variables

- remove logging of environment variables for security reasons
- 🔧 chore(gitignore): update gitignore file

- add .env file to gitignore to prevent sensitive information from being committed
- ignore vscode files
- ignore log files
- ignore /sample
- 🔧 chore(gitignore): add log folder to gitignore

- prevent the logs folder from being tracked by git
- 🔧 chore(gitignore): update .gitignore file

- remove unnecessary vscode folder
- add logs folder to ignore list
- 🔧 chore(gitignore): add vscode and logs to gitignore

- ignore vscode settings and logs to prevent committing local ide settings and log files
- 🔧 chore(config): enhance logging and file path

- configure logging to output to a file in the ./logs directory
- add detailed configuration logging to track settings
- 🔧 chore(systemd): configure service restart behavior

- set restart to on-failure for automatic recovery
- configure restart interval and burst limits
- set restart time to 45 seconds
- ✨ chore(script): remove raspiaprs.py

- remove the script as it's no longer needed
- 🔧 chore(gitignore): update .gitignore file

- remove /log from .gitignore
- a new log file was added
- 🔧 chore(gitignore): update .gitignore file

- add venv to .gitignore to exclude virtual environment folder
- 🔧 chore(main): rename raspiaprs.py to main.py
  - rename the main script for clarity
- 📦 build(deps): add new project dependencies

- Add required libraries for project
- Include aprslib, configparser, gpsd and humanize
- 🔧 chore(gitignore): add .vscode to gitignore

- prevent .vscode directory from being committed
- 🔧 chore(raspiaprs): reorganize file path definitions and clean up unused code

- move THERMAL_FILE and LOADAVG_FILE definitions to be grouped with other system file paths
- remove commented-out code related to master DC linking and unlinking in get_dmrmaster function
- use defined constants for file paths (e.g., UPTIME_FILE) instead of hardcoded strings
- ensure consistency in file path definitions for improved readability and maintainability
- 🔧 chore(systemd): improve raspiaprs.service configuration

- add start limit intervals and burst to prevent rapid restarts
- limit cpu and memory usage to prevent resource exhaustion
- enable system and home directory protection for security
- ensure permissions are only checked at startup
- 🔧 chore(scripts): remove unused import

- removed 're' import as it was not being used in the script
- 🔧 chore(raspiaprs.py): simplify DMR master logging

- commented out unused log reference strings and processing logic for "Linking to reflector" and "Closing DMR Network"
- this simplifies the code by removing unnecessary log parsing and analysis, improving readability and maintainability
- 🔧 chore(files): update file paths and remove sleep from service

- update file paths in README.md to reflect new locations
- remove unnecessary sleep command from raspiaprs.service
- adjust .gitignore to exclude the new sample directory
- rename raspiaprs.py to usr/local/bin/raspiaprs.py
- rename raspiaprs.conf to etc/raspiaprs.conf
- rename raspiaprs.service to lib/systemd/system/raspiaprs.service
- Fix formatting in rpiaprs.conf: adjust spacing for password and filter comments
- Fix get_freemem function: adjust memory calculation for more precise free memory percentage
- Update rpiaprs.conf: clarify altitude comment to specify AGL (Above Ground Level)
- Update uptime display format: abbreviate time units and remove unnecessary precision
- Fix send_header function: update EQNS parameter for improved precision
- Remove aprstar.py file: eliminate unused code and dependencies
- The symbol and symbol table can be speicified in the config

### ◀️ Revert

- Revert to ec381c1

---

generated by git-cliff
