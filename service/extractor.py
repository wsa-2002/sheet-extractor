import cv2
from pytube import YouTube


class SheetExtractor:
    def __init__(self, url, interval: int = 3):
        yt = YouTube(url)
        self.filename = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download()

        self.interval = interval

    def extract(self):
        file = cv2.VideoCapture(self.filename)
        while True:
            # Capture frame-by-frame
            ret, frame = file.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame', gray)
            if cv2.waitKey(1) == ord('q'):
                break
        file.release()
        pass
