# splat-API
A simple Splatoon API written in Python. Powering [Splat-Rotations](https://github.com/jfgoncalves/splat-rotations) and [Splat-Rotations-Discord](https://github.com/jfgoncalves/splat-rotations-discord).

## Requirements
- Python 3
- [Requests](https://github.com/kennethreitz/requests)
- NNID Credentials

## What it does
- Log into [SplatNet](splatoon.nintendo.net), scrape the rotations and write the json files for each region.

You can automate the script every hour with cron.

##Important
Make sure to make api.py executable with:

    chmod +x /my/path/to/api.py
