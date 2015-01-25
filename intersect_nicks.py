import weechat as w
import re
import argparse

NAME = "intersect_nicks"
AUTHOR = "Anton Backer <olegov@gmail.com>"
VERSION = "0.2.0"
LICENSE = "ISC"
DESCRIPTION = "Find people in common between two or more channels"
SHUTDOWN_FUNCTION = ""
CHARSET = ""

COMMAND = "intersect"

w.register(NAME, AUTHOR, VERSION, LICENSE, DESCRIPTION, SHUTDOWN_FUNCTION, CHARSET)


def enumerate_nicks(buffer):
    nicklist = w.infolist_get('nicklist', buffer, '')
    while w.infolist_next(nicklist):
        nick_type = w.infolist_string(nicklist, 'type')
        if nick_type == 'nick':
            yield w.infolist_string(nicklist, 'name')
    w.infolist_free(nicklist)


class BufferWrapper(object):
    def __init__(self, buffer):
        self.buffer = buffer

    def __getattr__(self, attr):
        return w.buffer_get_string(self.buffer, "localvar_" + attr)

    def show(self, obj):
        w.prnt(self.buffer, str(obj))


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-summary", action='store_true')
    parser.add_argument("channels", nargs='*')
    argv = re.split(r"\s+", args.strip())
    return parser.parse_args(argv)


def intersection_command(data, buffer_, args_):
    buffer = BufferWrapper(buffer_)
    args = parse_args(args_)
    channels = list(args.channels)
    if len(channels) == 1 and buffer.type == 'channel':
        channels.insert(0, buffer.channel)
    if len(channels) < 2:
        buffer.show("At least two channels need to be supplied")
        return w.WEECHAT_RC_ERROR

    nicks = {}
    for channel in channels:
        chan_buffer = w.buffer_search("", "%s.%s" % (buffer.server, channel))
        nicks[channel] = set(enumerate_nicks(chan_buffer))
    in_common = set.intersection(*nicks.values())

    buffer.show("%s shares %i people with %s" % (
        channels[0], len(in_common), ", ".join(channels[1:])))
    if in_common:
        for channel in channels:
            percentage = 100.0 * len(in_common) / len(nicks[channel])
            buffer.show("Percentage of %s: %.2f%%" % (channel, percentage))
        if not args.summary:
            sorted_names = sorted(in_common, key=lambda n: n.lower())
            buffer.show("People in common: %s" % ", ".join(sorted_names))
    return w.WEECHAT_RC_OK


w.hook_command(
    COMMAND, DESCRIPTION,
    "[-summary] <channel> [channel ...]",
    "Examples:\n"
    "  Find people in common between the current channel and #foo:\n"
    "    /" + COMMAND + " #foo\n"
    "  Find people in common between #foo and #bar:\n"
    "    /" + COMMAND + " #foo #bar"
    "", "", "intersection_command", "")
