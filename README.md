# Botty

A Telegram bot born to work on a RaspberryPi. 
It allows you to add torrents in Transmission BitTorrent Client. 
You can also check downloading status of whichever torrent. 

## Installation

Just run the setup.sh script with sudo privileges, it will create a virtual environment and install the requirements needed.
Copy settings.json.example into settings.json and edit it with your credentials, now you should be able to run your Botty!

## Commands

```
/download <TORRENT-URL> ; Downloading provided torrent.
/status <TORRENT-ID>    ; Show torrent status. Replace <TORRENT-ID> with -1 to have information about the last download.
```

## Contribution

Feel free to contribute. We accept every idea or improvements.

## License

This software is released under BEER-WARE LICENSE.
