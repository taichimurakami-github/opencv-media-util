from common.FileResolver import FileResolver
from create_thumbnails import CV2VideoCapture
from srt_to_json import SrtFileConverter

if(__name__ == '__main__'):
  # (sourceFilePath, outputDirPath) =  FileResolver.get_asset_file_and_result_dir_path('Edan-Meyer_vpt-edited.mp4')
  # capture = CV2VideoCapture(sourceFilePath)
  # capture.write_thumbnails_every_sec(outputDirPath)

  (sourceFilePath, outputDirPath) =  FileResolver.get_asset_file_and_result_dir_path('Edan-Meyer_vpt.srt', 'text')
  converter = SrtFileConverter()
  converter.convert_to_json(sourceFilePath, outputDirPath)

  (sourceFilePath, outputDirPath) =  FileResolver.get_asset_file_and_result_dir_path('Edan-Meyer_gym-mu-rts.srt', 'text')
  converter.convert_to_json(sourceFilePath, outputDirPath)




