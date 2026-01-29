from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QObject, pyqtSignal


class SoundManager(QObject):

    sound_enabled_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._enabled = True
        self._sounds = {}

    def set_enabled(self, enabled: bool):
        if self._enabled != enabled:
            self._enabled = enabled
            self.sound_enabled_changed.emit(enabled)

    def is_enabled(self) -> bool:
        return self._enabled

    def toggle(self):
        self.set_enabled(not self._enabled)

    def register_sound(self, name: str, sound: QSound):
        self._sounds[name] = sound

    def play(self, name: str = None, sound: QSound = None):
        if not self._enabled:
            return False

        if name and name in self._sounds:
            self._sounds[name].play()
            return True
        elif sound:
            sound.play()
            return True

        return False

    def play_click(self):
        return self.play('click')

    def play_notify(self):
        return self.play('notify')

    def play_error(self):
        return self.play('error')

    def play_about(self):
        return self.play('about')