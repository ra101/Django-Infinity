from functools import partial

from dj_database_url import parse as _parse_db_url


def parse_db_url(engine=None):
    return partial(_parse_db_url, engine=engine, conn_max_age=600, ssl_require=True)


class disable_signals:
    def __init__(self, signal_dict):
        """
        signle_dict example: {
            post_save: {eceiver_function_1: [sender_1, sender_2, ...], ...},
            ...
        }
        """
        self.signal_dict = signal_dict

        for signal, signal_map in self.signal_dict.items():
            for receiver, senders in signal_map.items():
                for sender in senders:
                    signal.disconnect(receiver, sender)

    def __enter__(self):
        return self.signal_dict

    def reconnect(self):
        for signal, signal_map in self.signal_dict.items():
            for receiver, senders in signal_map.items():
                for sender in senders:
                    signal.connect(receiver, sender)

    def __exit__(self, type, value, traceback):
        self.reconnect()
