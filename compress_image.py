from asyncio.windows_events import NULL
import cv2
import os
from common.FileResolver import FileResolver

class ImageCompressor:
  def __resize_img(self, sourceImg, width:int, height:int):
    return cv2.resize(sourceImg, dsize=(width, height))


  def __compress_img(self, sourceImg, sourceImgExt:str, quality: int): 
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encordedImg = cv2.imencode('.' + sourceImgExt, sourceImg, encode_params) # (bool値,エンコードしたImageオブジェクト)のタプルが返ってくる

    return cv2.imdecode(encordedImg, cv2.IMREAD_UNCHANGED)


  def __output_img(self, img, outputPath):
    cv2.imwrite(outputPath , img)


  def compress_all_images_in_directory(self, inputDirPath: str, outputDirPath: str):
    inputFiles = [os.path.join(inputDirPath, f) for f in os.listdir(inputDirPath) if os.path.isfile(os.path.join(inputDirPath, f))]

    FileResolver.resolve_dir_exists(outputDirPath)

    for imgSrc in inputFiles:
      img = cv2.imread(imgSrc)
      compressedImg = self.__compress_img(self.__resize_img(img, 640, 360), 'jpg', 80)
      self.__output_img(compressedImg, outputDirPath + '/' + imgSrc)



if __name__ == '__main__':
  compressor = ImageCompressor()
  inputDirPath = os.path.join(os.getcwd(), '_data','_images', 'Edan-Meyer_stable-diffusion_edited','jpg')
  outputDirPath = os.path.join(os.getcwd(), '_data','_images', 'Edan-Meyer_stable-diffusion_edited','_compressed', 'jpg')
  compressor.compress_all_images_in_directory(inputDirPath, outputDirPath)