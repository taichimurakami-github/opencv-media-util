from asyncio.windows_events import NULL
import cv2
import glob
import os

class ImageCompressor:


  def _resize_img(self, sourceImg, width:int, height:int):

    return cv2.resize(sourceImg, dsize=(width, height))


  def _compress_img(self, sourceImg, sourceImgExt:str, quality: int): 

    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]

    result, encordedImg = cv2.imencode('.' + sourceImgExt, sourceImg, encode_params) # (bool値,エンコードしたImageオブジェクト)のタプルが返ってくる

    return cv2.imdecode(encordedImg, cv2.IMREAD_UNCHANGED)


  def _output_img(self, img, outputPath):
    cv2.imwrite(outputPath , img)

  def compress_all_images_in_directory(self, inputDirpath: str, outputDirpath: str):
    inputFiles = [os.path.join(inputDirpath, f) for f in os.listdir(inputDirpath) if os.path.isfile(os.path.join(inputDirpath, f))]

    if os.path.exists(outputDirpath) == False:
      print(f"creating new directory: '{outputDirpath}'")
      os.makedirs(outputDirpath)

    for imgSrc in inputFiles:
      img = cv2.imread(imgSrc)
      compressedImg = self._compress_img(self._resize_img(img, 640, 360), 'jpg', 80)
      self._output_img(compressedImg, outputDirpath + '/' + imgSrc)

if __name__ == '__main__':
  compressor = ImageCompressor()
  inputDirpath = os.path.join(os.getcwd(), '_data','_images', 'Edan-Meyer_stable-diffusion_edited','jpg')
  outputDirpath = os.path.join(os.getcwd(), '_data','_images', 'Edan-Meyer_stable-diffusion_edited','_compressed', 'jpg')
  compressor.compress_all_images_in_directory(inputDirpath, outputDirpath)