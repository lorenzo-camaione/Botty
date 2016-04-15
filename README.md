# Botty

A Telegram bot born to work on a RaspberryPi. 
It allows you to add torrents in BitTorrent Client. 
You can also check downloading status of whichever torrent. 

## Installation

Just run the setup.sh script with sudo privileges, it will create a virtual environment and install the requirements needed.
Update the settings.json file with your credentials and you should be able to run your Botty!

## Commands

```
/download <TORRENT-URL> ; It start downloading torrent you provide it
/status <TORRENT-ID>    ; It provides you information about some download. It keeps an integer. Replace <TORRENT-ID> with -1 to have information about the last download.
```

## Contribution

Feel free to contribute. We accept every idea or improvements.

## License

This software is released under MIT license.
