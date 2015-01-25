weechat-intersect
=================

Find people in common between two or more channels.

Installation
------------

1. Make sure weechat is installed with python support. If you're brewing, the
   command is: `brew install weechat --with-python`.
2. Place script into ~/.weechat/python
3. Load it in weechat using `/script load intersect_nicks`
4. To auto-load it, add a symlink in ~/.weechat/python/autoload

Usage
-----

You must join the channels you'd like to intersect.

```
/join #foo,#bar
/intersect #foo #bar
```
