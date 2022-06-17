import os
import json
import re


class ANSICOLORS:
    #  TODO: Support 256bit colors
    #        Add bright colors
    class FG:
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'

    class BG:
        BLACK = '\033[40m'
        RED = '\033[41m'
        GREEN = '\033[42m'
        YELLOW = '\033[43m'
        BLUE = '\033[44m'
        MAGENTA = '\033[45m'
        CYAN = '\033[46m'
        WHITE = '\033[47m'

    class STYLES:
        UNDERLINE = '\033[4m'
        BOLD = '\033[1m'
        REVERSED = '\033[7m'

    class ICONS:
        CRIT = " "
        WARN = " "
        INFO = " "
        DEBUG = " "

    CLEAR = '\033[0m'
    RED = FG.RED
    GREEN = FG.GREEN
    YELLOW = FG.YELLOW
    BLUE = FG.BLUE

    DEBUG = f"{FG.CYAN}{ICONS.DEBUG}{CLEAR}: "
    INFO = f"{FG.GREEN}{ICONS.INFO}{CLEAR}: "
    WARN = f"{FG.YELLOW}{ICONS.WARN}{CLEAR}: "
    CRIT = f"{FG.RED}{ICONS.CRIT}{CLEAR}: "


class MessageSegment(object):
    """
    Wraps a segment in a specific set of ANSI strings
    """
    msg = ""

    def __init__(self, msg):
        if isinstance(msg, str):
            self.msg = msg
        elif isinstance(msg, dict):
            self._dict_parse(msg)
        else:
            self._obj_parse(msg)
        return None

    def _obj_parse(_, obj):
        ancestry = type.mro(obj)
        # The last member is usually the base object which
        # doesn't have a callable __str__ method
        spacing = 2
        ancestry.reverse()
        output = ""
        for idx, ancestor in enumerate(ancestry):
            try:
                friendly_name = ancestor.__str__() + " (" + str(ancestor.__class__) + ')'
            except TypeError:
                friendly_name = ancestor
            spaces = "─" * spacing * idx
            if idx == 0:
                output += f"\n┌{spaces} {friendly_name}"
            elif idx == len(ancestry)-1:
                output += f"\n└{spaces} {friendly_name} {ANSICOLORS.FG.CYAN}⟵ {ANSICOLORS.CLEAR}"
            else:
                output += f"\n├{spaces} {friendly_name}"
        print(output)


    def _dict_parse(_, list_data):
        tab_length = 4
        json_format = json.dumps(list_data)
        level = 0
        title = "Dictionary"
        title = ANSICOLORS.STYLES.REVERSED + title + ANSICOLORS.CLEAR + '\n'
        track_line = title.format()
        for keyval_pair in json_format.split(','):
            if '{' in keyval_pair:
                track_line += ' ' * tab_length * level + '{' + '\n'
                keyval_pair = re.sub(r'\s*{', '', keyval_pair)
                level += 1
            if '}' in keyval_pair:
                level -= 1
                track_line += ' ' * tab_length * level + '}' + '\n'
                keyval_pair = re.sub(r'\s*}', '', keyval_pair)
            print(f"At level {level}")
            print("  " + keyval_pair)
            keyval = keyval_pair.split(":")
            key, val = keyval[0].strip(), keyval[1].strip()
            track_line += ' ' * tab_length * level + f"{key}: {val}\n"
        # for newline in json_format.split('\n'):
        #     print(newline)
        #     keyvals = newline.split(",")
        #     for keyval in keyvals:
        #         if '{' in keyval:
        #             keyval = keyval.split('{')[-1]
        #             track_line = track_line + ' '*(level*tab_length) + '{\n'
        #             level += 1
        #         if '}' in keyval:
        #             level -= 1
        #             keyval = keyval.split('}')[-1]
        #             track_line = track_line + ' '*(level*tab_length) + '}\n'
        #         spaces = len(re.findall(r' ', newline))
        #         if ':' in keyval:
        #             keyval_split = keyval.split(":")
        #             print(keyval)
        #             key = MessageSegment(keyval_split[0])
        #             val = MessageSegment(keyval_split[1])
        #             key.color(ANSICOLORS.BLUE)
        #             val.color(ANSICOLORS.GREEN)
        #             track_line += ' '*spaces + f"{key.format()}: {val.format()}\n"

        print(track_line)

    def color(self, color):
        self.msg = f"{color}{self.msg}"

    def icon(self, icon):
        self.msg = f"{icon}: {self.msg}"

    def style(self, style):
        self.msg = f"{style}{self.msg}"

    def format(self):
        return f"{self.msg}{ANSICOLORS.CLEAR}"


class TailPrinter(object):
    dest = None
    echo = False  # Future use

    def _write(self, msg):
        assert self.dest is not None
        with open(self.dest, 'a') as fh:
            fh.write(msg + "\n")

    def crit(self, msg):
        segment = MessageSegment(msg)
        segment.color(ANSICOLORS.CRIT)
        self._write(segment.format())

    def warn(self, msg):
        segment = MessageSegment(msg)
        segment.color(ANSICOLORS.WARN)
        self._write(segment.format())

    def info(self, msg):
        segment = MessageSegment(msg)
        segment.color(ANSICOLORS.INFO)
        self._write(segment.format())

    def debug(self, msg):
        segment = MessageSegment(msg)
        segment.color(ANSICOLORS.DEBUG)
        self._write(segment.format())

    dbg = debug

    def __init__(self):
        # TODO: Multiple destinations
        self.dest = os.environ.get("PYTHON_DEBUGPRINTER_FILE", None)
