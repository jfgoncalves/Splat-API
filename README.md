# splat-API
A simple Splatoon API written in Python. Powering [Splat-Rotations](https://github.com/jfgoncalves/splat-rotations).

## Requirements
- Python 3
- [Requests](https://github.com/kennethreitz/requests)
- _wag_session values, that can be obtained in cookies when logged in with an US, EU and JP NNID credentials

## What it does
- Log into [SplatNet](splatoon.nintendo.net), scrape the rotations and write the json files for each region.

##Important
Make sure to make api.py executable with:

    chmod +x /my/path/to/api.py
