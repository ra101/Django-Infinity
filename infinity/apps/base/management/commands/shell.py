import os

from django.core.management.commands.shell import Command


def ptpython(self, *args, **kwargs):
    from ptpython.repl import embed

    history_filename = os.path.expanduser("~/.ptpython_history")
    embed(globals(), locals(), vi_mode=False, history_filename=history_filename)


Command.ptpython = ptpython
Command.shells.insert(0, "ptpython")
