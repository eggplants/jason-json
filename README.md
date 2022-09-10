# [![jason logo](https://jason.co.jp/favicon.ico)](https://jason.co.jp/) jason-json

[![PyPI version](
  https://badge.fury.io/py/jason-json.svg
  )](
  https://badge.fury.io/py/jason-json
) [![Maintainability](
  https://api.codeclimate.com/v1/badges/20d58be4ccf5c4c8e008/maintainability
  )](
    https://codeclimate.com/github/eggplants/jason-json/maintainability
) [![pre-commit.ci status](
  https://results.pre-commit.ci/badge/github/eggplants/jason-json/master.svg
  )](
  https://results.pre-commit.ci/latest/github/eggplants/jason-json/master
)

[![ghcr latest](
  https://ghcr-badge.herokuapp.com/eggplants/jason-json/latest_tag?trim=major&label=latest
) ![ghcr size](
  https://ghcr-badge.herokuapp.com/eggplants/jason-json/size)
](
  https://github.com/eggplants/jason-json/pkgs/container/getjump
)

[Jason](https://jason.co.jp) JSON Builder

## Install

```bash
pip install git+https://github.com/eggplants/jason-json
# or...
pip install jason-json
```

## CLI Usage

You can run this program as `jason-json` or `jason.json` on CLI.

```shellsession
$ jason.json -i 2
{
  "東京都": [
    {
      "name": "足立鹿浜店",
      "address": "東京都足立区鹿浜6-34-19",
      "link": "http://jason.co.jp/wptest/?p=5079",
      "business_time": {
        "begin_sec": 36000,
        "end_sec": 79200,
        "duration_sec": 43200,
        "duration_str": "10:00～22:00"
      }
    },
    ...
  ],
  "群馬県": [
    ...
  ]
}
```

### Help

```shellsession
$ jason.json -h
usage: jason.json [-h] [-O] [-i NAT] [-s PATH] [-u URL] [-V]

Jason (jason.co.jp) JSON Builder

options:
  -h, --help            show this help message and exit
  -O, --overwrite       overwrite if save path already exists (default: False)
  -i NAT, --indent NAT  indent json (default: None)
  -s PATH, --save PATH  save json to given path (default: None)
  -u URL, --url URL     target url (default: https://jason.co.jp/network)
  -V, --version         show program's version number and exit
```

### from Docker

Try:

```bash
docker run -it ghcr.io/eggplants/jason-json -h
```

## License

MIT
