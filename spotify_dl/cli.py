# TODO: move to prompt_toolkit
import readline
import sys
import threading
import time

from spotify_dl.downloader import SpotifyDownloadManager


class CLI:
    def __init__(self, download_manager: SpotifyDownloadManager) -> None:
        self.dm: SpotifyDownloadManager = download_manager
        self.prompting: bool = False

        readline.set_pre_input_hook(self._pre_input_hook)

        self._status_thread: threading.Thread = threading.Thread(
            target=self._status_updater, daemon=True
        )
        self._status_thread.start()
        self.heartbeat: bool = True

    def _pre_input_hook(self):
        _ = sys.stdout.write(
            f"\x1b[s\x1b[1A\r({'*' if self.heartbeat else ' '})[{self._collect_status_lines()}]\x1b[u"
        )
        _ = sys.stdout.flush()
        pass

    def _collect_status_lines(self) -> str:
        active = self.dm.get_active()
        queued = self.dm.get_queued()

        status: list[str] = []
        for dl, _ in active:
            status.append(f"{dl.get_percentage()*100:.0f}%")

        return f"{len(active)}/{len(queued)}{', ' if status else ''}{'|'.join(status)}"

    def _status_updater(self):
        while True:
            time.sleep(0.2)
            if self.prompting:
                readline.redisplay()
                self._pre_input_hook()
            self.heartbeat = not self.heartbeat
