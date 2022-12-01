import json
import os
from common.FileResolver import FileResolver

class SrtFileConverter:
  _roundMillisec = True

  # Private methods
  def __convert_timeformat_to_integers(self, timeFormatStr: str):
    hours, minutes, secondsAndMilliseconds = timeFormatStr.split(":")
    seconds, milliseconds = secondsAndMilliseconds.split(",")
    return (int(hours), int(minutes), int(seconds), int(milliseconds))
    

  def __convert_timeformat_to_sec(self, timeFormatStr: str):
    hours, minutes, seconds, milliseconds = self.__convert_timeformat_to_integers(timeFormatStr)

    return hours * 60 * 60 + minutes * 60 + seconds + round(milliseconds / 1000)


  def __get_timeformat_tupple_from_second_line(self, secondLineStr: str):
    startTimeStr, endTimeStr = secondLineStr.split(" --> ")

    return (
      self.__convert_timeformat_to_sec(startTimeStr),
      self.__convert_timeformat_to_sec(endTimeStr)
    )
  

  def __get_output_file_path(self, outputDirPath: str):
    fileName = os.path.join(outputDirPath, 'subtitle.json')
    return fileName


  # Public methods
  def convert_to_json(self, srtFilePath: str, outputDirPath: str, enableRoundMillisec = True):
    self._roundMillisec = enableRoundMillisec
    convertedDictList = []

    with open(srtFilePath, 'r', encoding="utf-8") as f:
      srtRawStr = f.read()

      for paragraph in srtRawStr.split('\n\n'):
        # print(paragraph)
        lines = paragraph.split("\n")

        if lines[0] == '': break

        firstLine, secondLine, thirdLine = lines
        startTimeStr, endTimeStr = self.__get_timeformat_tupple_from_second_line(secondLine)

        convertedDictList.append({
          'id': int(firstLine),
          'startAt': startTimeStr,
          'endAt': endTimeStr,
          'subtitle': thirdLine
        })

    FileResolver.resolve_dir_exists(outputDirPath)

    outputFilePath = self.__get_output_file_path(outputDirPath)

    with open(outputFilePath , 'w') as wf:
      resultJsonStr = json.dumps(convertedDictList)
      wf.write(resultJsonStr)



if __name__ == '__main__':
    converter = SrtFileConverter()
    srtFilePath = os.path.join(os.getcwd(), "_assets", "edan-meyer_vpt.srt")
    outputFilePath = os.path.join(os.getcwd(), "_data", "Edan-Meyer_vpt/subtitles.json")
    converter.convert_to_json(srtFilePath, outputFilePath)