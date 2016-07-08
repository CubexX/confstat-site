Confstat web
============

Web interface for [confstat-bot](https://github.com/CubexX/confstat-bot)

Installation
-------
**Python >=3.5 required!**
```bash
pip3 install -r requirements.txt
```
Usage
-----
Edit config.json:
```js
"db": {
    "driver": "mysql",
    "host": "localhost",
    "database": "",
    "user": "",
    "password": ""
  },
```
And run with gunicorn:
```bash
gunicorn -w 4 -b serverip:port app:app
```
License
-------
[MIT License](http://www.opensource.org/licenses/MIT)