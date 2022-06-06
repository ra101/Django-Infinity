from os.path import expanduser

from django.core.management.commands import shell


class Command(shell.Command):
    """
    Adding ptpython support.

    SideNote:
        I personnaly like bpython, but installing bpython on windows is a hassle,
        so adding the next best thing, ptpython, it is cross-platform and is
        aesthetically pleasing than ipython in my opinion.
    """

    shells = ["bpython", "ptpython", "ipython", "python"]

    def ptpython(self, *args, **kwargs):
        """
        Embed Python Shell and Add History
        """
        from ptpython.repl import embed

        history_filename = expanduser("~/.ptpython_history")
        embed(globals(), locals(), vi_mode=False, history_filename=history_filename)
