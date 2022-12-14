import math
import os
import cv2
from common.FileResolver import FileResolver

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

    self._mediaTimeSec = self.__get_media_time_sec(self._mediaFrameCount, self._mediaFPS)


  def __get_media_time_sec(self, frameCount, fps):
    return math.floor(frameCount / fps)


  def __get_thumbnail_filename(self, writeFileDirPath: str, thumbnailId: int, writeFileExt: str):
    dirPath = writeFileDirPath

    FileResolver.resolve_dir_exists(dirPath)

    return os.path.join(dirPath, f'{thumbnailId}.{writeFileExt}') 


  # Public methods
  def write_thumbnails_every_sec(self, writeFileDirPath:str, writeFileExtension:str = "jpg"):
    for i in range(self._mediaTimeSec + 1): # range : use "<", not "<="
      self._cap.set(cv2.CAP_PROP_POS_MSEC, i * 1000)
      res, img = self._cap.read()
      thumbnailFilename = self.__get_thumbnail_filename(writeFileDirPath, i, writeFileExtension)
      cv2.imwrite(thumbnailFilename, img)


  def write_jpg_thumbnails_by_range(self,writeFileDirPath:str,startTime_ms: int,interval_ms:int , endTime_ms: int | None = None):

    ## parse and define endTime_ms
    MEDIA_TIME_MS = endTime_ms
    if endTime_ms is None :
        MEDIA_TIME_MS = self._mediaTimeSec * 1000

    ## define output file extension as jpg
    WRITE_FILE_EXTENSION = "jpg"

    nowTimePtr_ms = startTime_ms

    while(nowTimePtr_ms < MEDIA_TIME_MS):
      self._cap.set(cv2.CAP_PROP_POS_MSEC, nowTimePtr_ms)
      res, img = self._cap.read()
      thumbnailFilename = self.__get_thumbnail_filename(writeFileDirPath, nowTimePtr_ms, WRITE_FILE_EXTENSION)
      cv2.imwrite(thumbnailFilename, img)
      nowTimePtr_ms += interval_ms



if __name__ == '__main__':
  # alpha-code
  MEDIA_FILE_NAME = "Edan-Meyer_vpt-edited.mp4"

  mediaFileNameWithoutExt, ext = MEDIA_FILE_NAME.split('.')
  mediaFilePath = os.path.join(os.getcwd(), '_assets', MEDIA_FILE_NAME)
  writeDirPath = os.path.join(os.getcwd(), '_data', mediaFileNameWithoutExt)

  capture = CV2VideoCapture(mediaFilePath)
  # capture.write_jpg_thumbnails_by_range(writeDirPath + "/jpg", 272 * 1000, 50, 280 * 1000)
  capture.write_thumbnails_every_sec(writeDirPath)

  MEDIA_FILE_NAME = "Edan-Meyer_gym-mu-rts-edited.mp4"

  mediaFileNameWithoutExt, ext = MEDIA_FILE_NAME.split('.')
  mediaFilePath = os.path.join(os.getcwd(), '_assets', MEDIA_FILE_NAME)
  writeDirPath = os.path.join(os.getcwd(), '_data', mediaFileNameWithoutExt)

  capture = CV2VideoCapture(mediaFilePath)
  capture.write_thumbnails_every_sec(writeDirPath)