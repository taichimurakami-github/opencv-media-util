import json
import os


class SrtFileConverter:
  _roundMillisec = True

  # Private methods
  def _convert_timeformat_to_integers(self, timeFormatStr: str):
    hours, minutes, secondsAndMilliseconds = timeFormatStr.split(":")
    seconds, milliseconds = secondsAndMilliseconds.split(",")
    return (int(hours), int(minutes), int(seconds), int(milliseconds))
    

  def _convert_timeformat_to_sec(self, timeFormatStr: str):
    hours, minutes, seconds, milliseconds = self._convert_timeformat_to_integers(timeFormatStr)

    return hours * 60 * 60 + minutes * 60 + seconds + round(milliseconds / 1000)


  def _get_timeformat_tupple_from_second_line(self, secondLineStr: str):
    startTimeStr, endTimeStr = secondLineStr.split(" --> ")

    return (
      self._convert_timeformat_to_sec(startTimeStr),
      self._convert_timeformat_to_sec(endTimeStr)
    )


  # Public methods
  def convert_to_json(self, srtFilepath: str, outputFilepath: str, enableRoundMillisec = True):
    self._roundMillisec = enableRoundMillisec
    convertedDictList = []

    with open(srtFilepath, 'r', encoding="utf-8") as f:
      srtRawStr = f.read()

      for paragraph in srtRawStr.split('\n\n'):
        # print(paragraph)
        lines = paragraph.split("\n")

        if lines[0] == '': break

        firstLine, secondLine, thirdLine = lines
        startTimeStr, endTimeStr = self._get_timeformat_tupple_from_second_line(secondLine)

        convertedDictList.append({
          'id': int(firstLine),
          'startAt': startTimeStr,
          'endAt': endTimeStr,
          'subtitle': thirdLine
        })

    outputDir, outputFilename = os.path.split(outputFilepath)

    if os.path.isdir(outputDir) == False:
      os.makedirs(outputDir)

    with open(outputFilepath, 'w') as wf:
      resultJsonStr = json.dumps(convertedDictList)
      wf.write(resultJsonStr)



if __name__ == '__main__':
    converter = SrtFileConverter()
    srtFilepath = os.path.join(os.getcwd(), "_assets", "EdanMeyer_stable-diffusion_edited.srt")
    outputFilepath = os.path.join(os.getcwd(), "_data", "EdanMeyer_stable-diffusion_edited/subtitles.json")
    converter.convert_to_json(srtFilepath, outputFilepath)