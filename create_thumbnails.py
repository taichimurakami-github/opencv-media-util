import math
import os
import cv2

class CV2VideoCapture:
  _WRITE_THUMBNAIL_DIRPATH = os.path.join(os.getcwd(), '_data')

  # Private methods
  def __init__(self, mediaFilePath:str):
    # save required parameters
    self._cap = cv2.VideoCapture(mediaFilePath)
    self._mediaFilePath = mediaFilePath
    self._mediaFrameCount = self._cap.get(cv2.CAP_PROP_FRAME_COUNT)
    self._mediaFPS = self._cap.get(cv2.CAP_PROP_FPS)

    if self._mediaFPS == 0.0 or self._mediaFrameCount == 0.0:
      raise Exception('E_FAILED_TO_LOAD_MEDIA')

    self._mediaTimeSec = self._get_media_time_sec(self._mediaFrameCount, self._mediaFPS)


  def _get_media_time_sec(self, frameCount, fps):
    return math.floor(frameCount / fps)


  def _get_thumbnail_filename(self, writeFileDirPath: str, thumbnailId: int, writeFileExt: str):
    dirpath = writeFileDirPath

    if os.path.exists(dirpath) == False:
      print(f"creating new directory: '{dirpath}'")
      os.makedirs(dirpath)

    return os.path.join(dirpath, f'{thumbnailId}.{writeFileExt}') 


  # Public methods
  def write_thumbnails_every_sec(self, writeFileDirPath:str, writeFileExtension:str = "jpg"):
    for i in range(self._mediaTimeSec + 1): # range : use "<", not "<="
      self._cap.set(cv2.CAP_PROP_POS_MSEC, i * 1000)
      res, img = self._cap.read()
      thumbnailFilename = self._get_thumbnail_filename(writeFileDirPath, i, writeFileExtension)
      cv2.imwrite(thumbnailFilename, img)



if __name__ == '__main__':
  MEDIA_FILE_NAME = "Edan-Meyer_stable-diffusion_edited.mp4"

  mediaFileNameWithoutExt, ext = MEDIA_FILE_NAME.split('.')
  mediaFilepath = os.path.join(os.getcwd(), '_assets', MEDIA_FILE_NAME)
  writeDirpath = os.path.join(os.getcwd(), '_data', mediaFileNameWithoutExt)

  capture = CV2VideoCapture(mediaFilepath)
  capture.write_thumbnails_every_sec(writeDirpath + "/jpg")
  capture.write_thumbnails_every_sec(writeDirpath + "/png", "png")