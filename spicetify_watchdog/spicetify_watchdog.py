# ##############################################################################
# [Descrição]:
#   Script que serve de watchdog pro comando spicetify [https://github.com/khanhas/spicetify-cli]
#
# [Dependencias]:
#   - Spicetify: [https://github.com/khanhas/spicetify-cli]
#   - watchdog: pip3 install watchdog --user
#
# [Uso]:
#   ./spicetify_watchdog.py
#
# ##############################################################################

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        # Aqui eu rodo o comando que eu quiser, quando houver alguma alteração
        # recursiva ness diretório.
        os.system('spicetify update')

class Watcher:
    homedir = os.environ['HOME']
    DIRECTORY_TO_WATCH = homedir + "/.config/spicetify"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print ("Error")

        self.observer.join()

if __name__ == '__main__':
    watcher = Watcher()
    watcher.run()
