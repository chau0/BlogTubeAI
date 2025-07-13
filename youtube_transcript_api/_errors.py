class TranscriptsDisabled(Exception):
    pass

class NoTranscriptFound(Exception):
    def __init__(self, video_id=None, languages=None, message=None):
        super().__init__(message or "No transcript")

class VideoUnavailable(Exception):
    pass
