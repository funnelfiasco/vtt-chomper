# vtt-chomper

A simple tool for chomping the ends of a VTT file.

## Usage

Uploading a meeting video and want to get rid of the first 5 minutes where you're waiting for everyone to join?
Use the `-b <SECONDS>` argument to chomp that many seconds off the beginning of the VTT file and update the time stamps accordingly.
Want to trim off the end where everyone's just awkwardly saying goodbye to each other?
use the `-e <SECONDS>` argument to chomp that many seconds off the end of the VTT file.
Very tasty!

## Requirements

vtt-chomper requires the following Python libraries:

* argparse
* sys
* [webvtt](https://webvtt-py.readthedocs.io/en/latest/index.html)

## License

This project is licensed under the [GNU General Public License 3.0](LICENSE) or later.

## Contributing

I'll accept contributions if you want.
All contributions are accepted under the project's license.
More to come if this is worth actively developing.