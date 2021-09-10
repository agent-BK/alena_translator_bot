import platform


class FfmpegConfig:

    @staticmethod
    def get_path():
        try:
            ffmpeg = r'bin/ffmpeg.exe' if platform.system() == "Windows" else 'ffmpeg'
        except FileNotFoundError:
            ffmpeg = 'ffmpeg'
        return ffmpeg

    def setup_command(self, file, ogg=None):
        ffmpeg = self.get_path()
        if ogg:
            command = [ffmpeg, '-i', file, '-f', 'wav', '-ar', '44100', '-']
        else:
            command = [ffmpeg, '-i', file, '-f', 'ogg', '-acodec', 'libopus', '-']
        return command
