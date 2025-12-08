# Version: ae1c38ed31d5d068814908845ff28e5e766d8146

* [ae1c38e](https://github.com/HafiziRuslan/raspiaprs/commit/ae1c38ed31d5d068814908845ff28e5e766d8146): 👷 ci(workflow): use commit hash as fallback release version

- set default release_version to head commit ID if not provided in inputs
- ensures changelog generation works even without explicit version input during CI runs
* [575bdab](https://github.com/HafiziRuslan/raspiaprs/commit/575bdab2192c94101f30ca66948740b7f2fd654d): 🔧 chore(ci): update changelog workflow inputs

- remove default release version fallback to head commit
- explicitly pass github_token to the action
* [19f15a3](https://github.com/HafiziRuslan/raspiaprs/commit/19f15a32518a4182efebc9def32fd3942f7271e1): 🔧 chore(ci): enable manual release version input in changelog workflow

- uncommented and configured `release_version` input for `workflow_dispatch` event
- default `release_version` to `github.event.head_commit` if not provided during manual dispatch
* [2ead7fd](https://github.com/HafiziRuslan/raspiaprs/commit/2ead7fd002f9a253b04b087d0faa237261a9c5d4): 🔧 chore(ci): disable manual release version input in workflow

- remove `release_version` input from `workflow_dispatch` trigger
- comment out usage of `release_version` in build job step
* [aa3d3e2](https://github.com/HafiziRuslan/raspiaprs/commit/aa3d3e2930a02595bb103ed1550d39c9eaf3a664): 🔧 chore(ci): remove redundant changelog step

- remove unused step for generating changelog in CI pipeline
* [e2a22c0](https://github.com/HafiziRuslan/raspiaprs/commit/e2a22c0eb5890c7fe234cfd8467157f1235f3f10): ✨ feat(ci): add changelog generation workflow

- introduce changelog-ci configuration file
- set up GitHub Actions workflow for automated changelog generation on PR open and push events
* [5ba959c](https://github.com/HafiziRuslan/raspiaprs/commit/5ba959c1cebca0d9ca5ba214bcdc91ea41527f21): 📝 docs(readme): rename README to README.md
* [1abc4e9](https://github.com/HafiziRuslan/raspiaprs/commit/1abc4e9a187daed4b2f3953de8954802e523fbac): 📝 docs(readme): update license file reference

- rename LICENSE.md to LICENSE for standard practice
- update README to reflect license file name change
* [d5775f3](https://github.com/HafiziRuslan/raspiaprs/commit/d5775f3ba577adec43b77b3868bf58e0c46cd22a): ♻️ refactor(config): improve readability and adhere to Python conventions

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
* [3ccf7ff](https://github.com/HafiziRuslan/raspiaprs/commit/3ccf7ff2b8762049e1282db10bdd23e3649c8603): 🐛 fix(aprs): correct parameter names for memory units

- change PARM.MemUsed to PARM.RAMUsed in header transmission
- change UNIT.Mb to UNIT.MB for consistency in header transmission
- update telegram log message to reflect RAM Used in MB
* [9678e72](https://github.com/HafiziRuslan/raspiaprs/commit/9678e721a859b3c3a523bd58c0fe54ce130e5a9b): 🐛 fix(ais): move filter setting after successful connection

- set_filter was being called before ais.connect()
- this caused the filter to potentially not be applied if the initial connection attempt failed and retried
* [7554c3c](https://github.com/HafiziRuslan/raspiaprs/commit/7554c3c92cd7550e0f821d3d58eae7f4cccba55b): 🐛 fix(aprs): ensure filter is set after connection attempt

- move filter setting to after connection attempt in `ais_connect`
- this prevents potential issues if the filter is applied before the connection is fully established or if retries are involved
* [8659f3a](https://github.com/HafiziRuslan/raspiaprs/commit/8659f3a9f9239c20042f32601fb7fc07115c8a4f): ✨ feat(config): consolidate APRS sleep time and update GPSD settings

- rename APRS_SLEEP to SLEEP in .env.SAMPLE and Config
- add GPSD_HOST and GPSD_PORT to .env.SAMPLE and use them in GPSD client initialization
- set default APRSIS_FILTER to "m/50" in Config and add it to .env.SAMPLE
- update GPSD data fetching logic to check for TPV class and improve logging messages
- update APRS-IS connection to use set_filter method
* [d35371d](https://github.com/HafiziRuslan/raspiaprs/commit/d35371d51471c2ba0ecc71b4b39c948b9eb931c4): 🐛 fix(gps): correct gpsd position handling

- handle gpsd position errors
- return (0, 0, 0) on error instead of "n/a"
- ensure fallback to .env config when gpsd data is unavailable
* [a50a151](https://github.com/HafiziRuslan/raspiaprs/commit/a50a151a4fe6716e609ccc3f62c901d1a3b7e068): 🐛 fix(main): correct telemetry and status timing

- move telemetry and status updates after position sending
- ensures consistent reporting in each sequence
* [a7d6853](https://github.com/HafiziRuslan/raspiaprs/commit/a7d6853854bec97454efbfa618e190108b4f9285): 🐛 fix(main): fix async call in send_position

- await the send_position function to ensure proper execution
* [caceab1](https://github.com/HafiziRuslan/raspiaprs/commit/caceab19e64a3fb5c22970fe90f11e06b977f0f4): ⚡️ perf(main): improve ais message sending efficiency

- change await send_position to send_position to prevent blocking
* [e1b7600](https://github.com/HafiziRuslan/raspiaprs/commit/e1b7600c2b69e271bc6bda8735fcc1a30120e60c): ♻️ refactor(main): simplify header sending logic

- move send_header to synchronous function
- call send_header directly instead of awaiting it
- reduce redundant await calls
* [2897474](https://github.com/HafiziRuslan/raspiaprs/commit/2897474d32e99e41e6b4de5b8ba836c73644763f): 🐛 fix(main): correct telemetry and status sending logic

- remove conditional check for sending telemetry and status messages
- ensure telemetry and status are sent every loop iteration
* [d77d6d7](https://github.com/HafiziRuslan/raspiaprs/commit/d77d6d79bebb8bfc3033dd2ade8e9dde47231d8f): 🐛 fix(dmr): correct dmr master list creation

- convert list of dicts to list to avoid type errors
* [379e938](https://github.com/HafiziRuslan/raspiaprs/commit/379e9380e180742655a2a25a8ca4d03ba2d1d4d7): ♻️ refactor(dmr): improve dmr master retrieval logic

- add type hints for clarity and maintainability
- initialize variables with explicit types
* [cb6edcb](https://github.com/HafiziRuslan/raspiaprs/commit/cb6edcb6432e462b00bf18db966ec0f7775228d7): 🐛 fix(main): correct telemetry sequence and logging

- 【Telemetry Sequence】
  - corrected sequence number in telemetry message
  - changed sequence variable name from sequence to seq
- 【Logging】
  - corrected memory usage unit in telegram logs from MBytes to Mb
* [95ef291](https://github.com/HafiziRuslan/raspiaprs/commit/95ef29144bd1b60efbd241907f7d4c96aa909055): ♻️ refactor(main): change send_header to async

- rename send_header to async function
- call async send_header instead of sync
* [e67c6d1](https://github.com/HafiziRuslan/raspiaprs/commit/e67c6d12ea46972bb7ff6f8c2434e34c92930f68): 🐛 fix(dmr): correct dmrmaster extraction from logs

- fix parsing logic to accurately identify connected DMR masters
- ensure only unique masters are reported in the status
* [4bf064f](https://github.com/HafiziRuslan/raspiaprs/commit/4bf064f0aafc5fc76d0c75d4615aac1fcb2b0767): 🐛 fix(main): correct header sending frequency

- fix header being sent too often
- adjust the modulo operator to send less frequently
* [70b0f5c](https://github.com/HafiziRuslan/raspiaprs/commit/70b0f5c2bffeb38aec8c4b5d304ee49d75314aaa): 🐛 fix(main): correct aprs reporting loop

- fix sequence logic for sending position and header information
- temporarily disable sending position to debug header sending
* [c19c9c5](https://github.com/HafiziRuslan/raspiaprs/commit/c19c9c54c12b6049be9154f2ff9c5fcb1d172dd3): 🐛 fix(gpsd): correct gpsd position and add satellite data

- fix typo in `get_gpsd_coordinate` function name, renaming it to `get_gpsd_position`
- add `get_gpsd_sat` to retrieve satellite count from gpsd
- include satellite count in telemetry data sent to aprs-is and telegram
- update aprs header to include gps satellite information
- use `os.cpu_count()` instead of parsing `/proc/cpuinfo` to determine cpu core count
* [63297d1](https://github.com/HafiziRuslan/raspiaprs/commit/63297d16fa1694389d41c7d07a568e178bd31c4c): 👷 ci(pylint): remove pylint workflow

- remove pylint workflow as it's no longer needed
* [fb7c43b](https://github.com/HafiziRuslan/raspiaprs/commit/fb7c43b9da5956fc8a94cd85abb90390724dbada): ♻️ refactor(location): remove modemmanager coordinates function

- remove the get_modemmanager_coordinates function
- this function is no longer needed
* [519de53](https://github.com/HafiziRuslan/raspiaprs/commit/519de532f31462fbe0373d2c060fe80a585d2e45): Update Python versions in pylint workflow
* [16814c5](https://github.com/HafiziRuslan/raspiaprs/commit/16814c59d1024414b6a5cac59234f4c82f459318): fix identation
* [adcdb56](https://github.com/HafiziRuslan/raspiaprs/commit/adcdb56936f31652a715b22b3cec7810aa269497): Set package-ecosystem to 'pip' in dependabot config
* [19c5d22](https://github.com/HafiziRuslan/raspiaprs/commit/19c5d22c87a202a1bc7834f5feb5c93e7d282b0c): Delete .github/workflows/pylint.yml
* [065dad5](https://github.com/HafiziRuslan/raspiaprs/commit/065dad532b7a12c9e97f046c35c985e590b330d9): ♻️ refactor(deps): move urllib import

- move urllib import to be with other urllib related imports
* [5dfb1be](https://github.com/HafiziRuslan/raspiaprs/commit/5dfb1be18f38831130010e8c389d142acbbf5626): ♻️ refactor(main): consolidate imports and update dependencies

- group imports by category for better readability
- update dependencies to the latest versions for security and performance improvements
* [3b53229](https://github.com/HafiziRuslan/raspiaprs/commit/3b53229f7b7bec39129b6678934a371c5211e4d8): Add Pylint workflow for Python code analysis
* [238ef20](https://github.com/HafiziRuslan/raspiaprs/commit/238ef20de14356408e09f1e74a9e2e081c7a8263): 🐛 fix(osinfo): correct os name parsing in get_osinfo

- improve os name extraction from /etc/os-release
- fix the location of `id_like`
* [7661508](https://github.com/HafiziRuslan/raspiaprs/commit/766150813d90df2a553f9fd405eea36f241b0595): 🐛 fix(osinfo): improve os information retrieval
- correct logic errors in parsing `/etc/os-release` for accurate OS information
- handle cases where certain fields are missing
* [ff43ce8](https://github.com/HafiziRuslan/raspiaprs/commit/ff43ce8294626fa87ccc98453b4b7ab41041f2d9): 🐛 fix(dmr): correct master callsign retrieval

- fix parsing logic to accurately extract master callsigns
- handle instances where callsigns contain underscores by replacing them with spaces
* [f61bb0b](https://github.com/HafiziRuslan/raspiaprs/commit/f61bb0bd56e428f4564bdf093e4f1ec728edefa1): 🐛 fix(telegram): correct telegram message id logging

- fix error when logging telegram message ID after sending a message
* [afcd413](https://github.com/HafiziRuslan/raspiaprs/commit/afcd4130de37d1d02119b838b99a207f5129f3d8): 🐛 fix(osinfo): correct osname parsing in get_osinfo

- fix parsing logic to correctly split the line by "="
- ensure the osname format is correct by using "-" between id_like and version_codename
* [62dd184](https://github.com/HafiziRuslan/raspiaprs/commit/62dd18428aec983cac04d5319cb815392741b4cf): 🐛 fix(telegram): correct link_preview_options format

- the 'link_preview_options' parameter requires a dictionary, not a list
* [57d3ea6](https://github.com/HafiziRuslan/raspiaprs/commit/57d3ea6b8f35583f9784d0ae87706e4fc885a6b9): 🐛 fix(telegram): fix telegram location sending logic

- fix logic to only send location if lat and lon are not 0
- set default value of lat and lon to 0
* [9f3271b](https://github.com/HafiziRuslan/raspiaprs/commit/9f3271b99263839f089e17e97fda3926ef352441): 📝 docs(readme): update instructions for RasPiAPRS

- add execute permission for shell scripts
- use autostash option to prevent merge conflicts
* [81c1894](https://github.com/HafiziRuslan/raspiaprs/commit/81c1894df99def065ef69733db0fa4f617b9e431): 🔧 chore(main): enhance logging and venv management

- add timestamped logging for better monitoring
- ensure venv is activated before running main.py
- loop main.py execution with a 15-second delay
* [110103b](https://github.com/HafiziRuslan/raspiaprs/commit/110103bcef4e04caff570f633632c9869463fc54): 📝 docs(README): improve installation and configuration instructions

- update example aprs.fi link
- simplify installation instructions
- replace ConfigParser with .env for configuration
- update autostart instructions
- remove unnecessary commands
* [4e3dba8](https://github.com/HafiziRuslan/raspiaprs/commit/4e3dba8d29168c6aafb33746ea858991689f6a2c): ✨ feat(telegram): enhance telegram message link previews

- disable web page previews in telegram messages
- add options to prefer small media and show link previews above text for cleaner presentation
* [ca4c11e](https://github.com/HafiziRuslan/raspiaprs/commit/ca4c11ef49c4e0371b3b9c43cfde02e3b038df92): ✨ feat(telegram): enhance telegram logging with location support

- update get_osinfo to parse multiple os release file fields
- add lat/lon parameters to logs_to_telegram function
- add location sending functionality to telegram messages
- update send_position to pass lat/lon to logs_to_telegram
- remove disable_web_page_preview and use link_preview_options instead
- update status message in main function
* [a44a609](https://github.com/HafiziRuslan/raspiaprs/commit/a44a60987b773c107146ec071e1dcfbdfdebaadb): 🐛 fix(position): correct coordinate conversion in send_position

- fix the coordinate conversion in the `send_position` function
- convert latitude, longitude, and altitude to float before conversion
* [8fdd294](https://github.com/HafiziRuslan/raspiaprs/commit/8fdd294e8e016cbded9b0ebe80f9fde5443eacf0): 🐛 fix(position): correct lat/lon to integer for aprs

- fixed latitude and longitude values to be integers before conversion
- ensures proper formatting for aprs transmission
* [258a4e4](https://github.com/HafiziRuslan/raspiaprs/commit/258a4e4e4277625026de47edcc6262491091570f): 🐛 fix(telegram): improve telegram message logging

- add chat_id, message_thread_id and message_id to the log
* [9b4cd78](https://github.com/HafiziRuslan/raspiaprs/commit/9b4cd780bcffe07c29571d41c6fd001f02644c0b): 🐛 fix(gps): handle gpsd errors and fallback to env vars

- return "n/a" on gpsd error instead of 0
- fallback to env vars if gpsd data is unavailable
* [6ebaa41](https://github.com/HafiziRuslan/raspiaprs/commit/6ebaa4103c9850030ed432bfa368ecd8322f5392): 🐛 fix(gps): ensure gpsd coordinates are set before return

- fix a bug where the coordinates were being set regardless of gpsd availability
* [f5e6f93](https://github.com/HafiziRuslan/raspiaprs/commit/f5e6f93b407d7fe0b3675db583fd0665707bf27a): 🔧 chore(config): remove logging of environment variables

- remove logging of environment variables for security reasons
* [132dbd6](https://github.com/HafiziRuslan/raspiaprs/commit/132dbd6b7e377dd94d20ff0a321bfaee5850d19e): 🐛 fix(gps): increase gpsdclient timeout

- increase timeout to 15 seconds to prevent connection issues
* [ff89b9c](https://github.com/HafiziRuslan/raspiaprs/commit/ff89b9c2604e32a55bb9b566cb353621ded91155): ✨ feat(gps): enhance gps data handling and aprs message

- add logging for gpsd position availability
- include comment in telegram position message
* [4d79f68](https://github.com/HafiziRuslan/raspiaprs/commit/4d79f6884b1d75624e65ed6bd1d137253b8438ec): 🐛 fix(main): correct ais header sending frequency

- adjust ais header sending frequency to every 6 sequences
* [44fc04c](https://github.com/HafiziRuslan/raspiaprs/commit/44fc04c0e27b0688025dee5edf7c9312d9b670c5): ✨ feat(main): enhance application lifecycle logging
- add logging for application startup, shutdown, and errors【main.py】
- add script loop【main.sh】
* [a400895](https://github.com/HafiziRuslan/raspiaprs/commit/a40089530e17ac02436b1ed7170c84dec2d940a7): 🐛 fix(telemetry): correct cpu temp decimal places

- fix cpu temp decimal places from 2 to 3
- change position telegram message to single line format
* [ac68302](https://github.com/HafiziRuslan/raspiaprs/commit/ac683029f5c63b749183a2fd9f827d0091d44703): 🐛 fix(telemetry): improve telegram logs format

- enhance readability of position, telemetry, and status logs on telegram
- include labels and units for better understanding of data
* [721e3d9](https://github.com/HafiziRuslan/raspiaprs/commit/721e3d941401254f19b5cbae1ef43c82f6b81762): 🐛 fix(telemetry): fix telemetry sending without await

- remove await to prevent blocking
- improve non-blocking send telemetry and status
* [5a16621](https://github.com/HafiziRuslan/raspiaprs/commit/5a166218f5d7a90e9e5170e783db4f6945de2a4d): ♻️ refactor(main): convert send_header to async

- convert send_header to async function
- use await for send_position in send_header
- use await for send_header, send_position, and ais.sendall in main
* [fd248be](https://github.com/HafiziRuslan/raspiaprs/commit/fd248be40c070623359a5cef33b8d57943191e43): 🐛 fix(main): correct async call for send_position

- remove await for send_position to prevent blocking
* [850a290](https://github.com/HafiziRuslan/raspiaprs/commit/850a290356b517bccd1a80f8e7767d571d5907de): 🐛 fix(telegram): correct telegram token env variable name

- fix telegram integration by renaming TELEGRAM_BOT_TOKEN to TELEGRAM_TOKEN
* [63bf076](https://github.com/HafiziRuslan/raspiaprs/commit/63bf0760ee7267f3928bb6a1c5090bfa45741cdd): ♻️ refactor(main): migrate Telegram logging to asynchronous

- Switch from synchronous telegram library to asynchronous
- Update logs_to_telegram to be an async function
- Update send_position and main to call logs_to_telegram with await
- Use asyncio.run to run the main function
- Read telegram config from environment variables
* [36bd2a3](https://github.com/HafiziRuslan/raspiaprs/commit/36bd2a3230bddb512849ac479d2af81352632555): 🐛 fix(gps): correct .env quoting for gps coordinates

- change `quote_mode` from `"none"` to `"never"` when setting GPS coordinates in `.env` file
- resolves issue where coordinates were not being correctly read due to unintended quoting
* [03e2f1f](https://github.com/HafiziRuslan/raspiaprs/commit/03e2f1f9f923f981e0d64c1ad65ad458370277dd): 🐛 fix(position): correct lat/lon conversion in send_position

- fix issue where lat/lon were converted to integers, causing inaccuracy
- use the original float values for _lat_to_aprs and _lon_to_aprs
* [70f11dd](https://github.com/HafiziRuslan/raspiaprs/commit/70f11dd1e0b341b1168ff4129d41d19f581acae0): 🐛 fix(gps): correct return type for get_gpsd_coordinate

- change return type from str to float for latitude, longitude, and altitude
* [740c6ff](https://github.com/HafiziRuslan/raspiaprs/commit/740c6ff91de79a65746eb25e7f12d31e921a8baf): 🐛 fix(position): correct lat/lon to integer

- fix lat/lon to integer to avoid type errors
* [ed9e2d9](https://github.com/HafiziRuslan/raspiaprs/commit/ed9e2d9f6d2a7f9dbed14b2ff9aa749f1c2286b8): 🐛 fix(config): correct data type for aprs coordinates

- ensure that latitude, longitude, and altitude are strings
- update .env file with unquoted values from gpsd
- update config class with new values after gpsd update
* [26d2d72](https://github.com/HafiziRuslan/raspiaprs/commit/26d2d725110749ba0a607e093f682a73f9ab0111): 🐛 fix(gpsd): correct gpsd coordinate retrieval and handling

- fix: correct boolean check for GPSD_ENABLE environment variable
- fix: ensure gpsd coordinates are properly retrieved and handled
- refactor: change lat/lon/alt defaults from 0.0 to "0.0" to avoid type errors
* [ab27a85](https://github.com/HafiziRuslan/raspiaprs/commit/ab27a85094151e4a17a5a83d4eb93166aa283228): 🐛 fix(gpsd): improve gpsd coordinate retrieval logic

- ensure valid gps fix (mode 2 or 3) before processing data
- log gpsd fix type (2d or 3d)
- only update .env file if valid coordinates are obtained
* [0067e5d](https://github.com/HafiziRuslan/raspiaprs/commit/0067e5db771c171e041c1c3cd5052f5e9340abb3): 🐛 fix(gps): ensure valid gpsd data before processing

- check for valid 'TPV' class and sufficient mode
- handle missing 'lat', 'lon', 'alt' keys gracefully
- log warnings for insufficient or incomplete data
* [e36e154](https://github.com/HafiziRuslan/raspiaprs/commit/e36e15480bc9a387ba497203a57150c44294f3ae): 🐛 fix(cli): exit gracefully on keyboard interrupt

- ensure the program exits cleanly when Ctrl+C is pressed
* [15841c3](https://github.com/HafiziRuslan/raspiaprs/commit/15841c369637c6ba6dc0f093583f06111cfec2c2): 🐛 fix(gps): handle gpsd coordinate retrieval

- fix: remove fallback to previous coordinates when GPSD is enabled but no fix is available
- the program should use the last known coordinates from GPSD or the default values instead
- fix: remove timeout from GPSDClient to prevent blocking
* [243205a](https://github.com/HafiziRuslan/raspiaprs/commit/243205a42d71ae252d57f816ec71631698b50fb5): 🐛 fix(deps): update gpsdclient import

- fix import statement for gpsdclient to resolve module not found error
* [5bbf948](https://github.com/HafiziRuslan/raspiaprs/commit/5bbf94816372cbace65b07fd7bd7543e8589d3b0): 🐛 fix(gps): correct latitude and longitude type in gpsd
- fix type for latitude, longitude, and altitude to prevent errors
- remove unnecessary float conversion when setting env variables
* [c64b31b](https://github.com/HafiziRuslan/raspiaprs/commit/c64b31b4c57465528e2fde53a13384c25829f5fc): 🐛 fix(gps): increase GPSDClient timeout

- increase GPSDClient timeout to 10 seconds to fix connection issues
- avoid program crash when GPSD is unavailable
* [8f547a6](https://github.com/HafiziRuslan/raspiaprs/commit/8f547a6808792db48a102d77d407b4f5cafc4ac7): 🐛 fix(main): correct log and sequence file paths

- update log and sequence file paths to /tmp
- resolve permission issues in restricted environments
* [fd9006b](https://github.com/HafiziRuslan/raspiaprs/commit/fd9006b2587935c2676e713d01caac8eedf1cd77): 🐛 fix(config): correct logging call in config class

- correct the logging call from logger.info to logging.info
* [4607c79](https://github.com/HafiziRuslan/raspiaprs/commit/4607c79183445e6dcabb30236669c734318ba7cf): 🐛 fix(logging): correct log file path

- fix log file path to be in the "tmp" directory
- avoid permission issues in "var/log" on some systems
* [d739a6b](https://github.com/HafiziRuslan/raspiaprs/commit/d739a6b7eb8c6333c3421d5de1954b6fabc30f51): ♻️ refactor(gps): improve gps coordinate handling
- store sequence file in tmp directory
- change lat, lon, alt type to float

🔧 chore(main): update log file path and remove unused directory

- change log file path to /var/log/raspiaprs.log
- remove unused /logs/* entry from .gitignore
- remove placeholder log file
* [14d0b89](https://github.com/HafiziRuslan/raspiaprs/commit/14d0b894d585648bbec4ead5608481e7baabdb24): 🐛 fix(gps): correct conditional statement in coordinate validation

- fix the conditional statement to use != instead of is not to properly validate the gpsd coordinates
* [de74caf](https://github.com/HafiziRuslan/raspiaprs/commit/de74caf4b168cae07da8f4339ce0cfda1948aad9): 🔧 chore(gitignore): update gitignore file

- add .env file to gitignore to prevent sensitive information from being committed
- ignore vscode files
- ignore log files
- ignore /sample
* [2ff9cf5](https://github.com/HafiziRuslan/raspiaprs/commit/2ff9cf554d310a60a1d1d3f130ee862a61c8eefb): 🔧 chore(gitignore): add log folder to gitignore

- prevent the logs folder from being tracked by git
* [8d8c391](https://github.com/HafiziRuslan/raspiaprs/commit/8d8c39170492e3cbecc5d631767527ba02b2fc14): 🐛 fix(gps): handle gpsd no fix scenario

- prevent script from crashing when gpsd has no fix
- log warning message when gpsd is enabled but no fix available
- use previous coordinates when gpsd has no fix
* [1451518](https://github.com/HafiziRuslan/raspiaprs/commit/145151848e4fefc8871ed1c7f1503acded7aada5): 🐛 fix(config): correct logging configuration

- remove incorrect logger call
- add logging of environment variables
* [ebe40ad](https://github.com/HafiziRuslan/raspiaprs/commit/ebe40addae2ebe9c573904f25c679b7042ef2d80): 🔧 chore(gitignore): update .gitignore file

- remove unnecessary vscode folder
- add logs folder to ignore list
* [b1a997b](https://github.com/HafiziRuslan/raspiaprs/commit/b1a997b01608fdcff11232e644b4c8234cd5d092): 🔧 chore(gitignore): add vscode and logs to gitignore

- ignore vscode settings and logs to prevent committing local ide settings and log files
* [129248e](https://github.com/HafiziRuslan/raspiaprs/commit/129248ecf63f4ac93c2a5e5bfbb19f0b16374e49): 🔧 chore(config): enhance logging and file path

- configure logging to output to a file in the ./logs directory
- add detailed configuration logging to track settings
* [9575256](https://github.com/HafiziRuslan/raspiaprs/commit/9575256bd40be6c4a18de306caa9a1f0aa2612d7): ✨ feat(deps): add aprslib and gpsdclient dependencies

- add aprslib for APRS protocol handling
- add gpsdclient for GPS data access
* [278fc85](https://github.com/HafiziRuslan/raspiaprs/commit/278fc8504705ca3e3637bf338b9473a2ff41da98): ♻️ refactor(core): migrate from configparser to dotenv for config management
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
* [30ad5ed](https://github.com/HafiziRuslan/raspiaprs/commit/30ad5edc044e909ddacf4000c7174ee6f7f909b5): 🐛 fix(modemmanager): handle missing return

- fix issue where lat, lon, alt are not returned when an exception is caught
* [bf705fe](https://github.com/HafiziRuslan/raspiaprs/commit/bf705fe024e41614bed5af207b0d1d7116e69a47): 🐛 fix(gps): fix coordinate return on exception
- ensure coordinates are returned even when GPSD data retrieval fails
* [a56e64d](https://github.com/HafiziRuslan/raspiaprs/commit/a56e64d0a8a693bca616520fbcc19f5a90f3714a): ✨ feat(gps): add gpsd socket configuration and improve data handling

- add the ability to specify a custom socket path for GPSD
- enhance GPSD data handling by ensuring values are updated even on errors
* [e709a16](https://github.com/HafiziRuslan/raspiaprs/commit/e709a16e4005f8e51e7042ddbd6d70c6671db0a6): 🔧 chore(systemd): configure service restart behavior

- set restart to on-failure for automatic recovery
- configure restart interval and burst limits
- set restart time to 45 seconds
* [84d7ba5](https://github.com/HafiziRuslan/raspiaprs/commit/84d7ba54e8f87631a311167473994ca690fb385d): ♻️ refactor(aprs): disable telegram integration

- comment out telegram functionality to remove dependency
- remove telegram import
- comment out logs_to_telegram calls
* [0870ee5](https://github.com/HafiziRuslan/raspiaprs/commit/0870ee52ffb457bd00c22f5abeb511da12babd56): ✨ chore(script): remove raspiaprs.py

- remove the script as it's no longer needed
