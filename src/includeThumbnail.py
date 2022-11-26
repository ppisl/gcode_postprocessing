import base64
import sys
import os
import io
import pathlib
from PIL import Image


def createStringThumbnail(image, width, height):
  imageNew = image.resize((width, height), Image.BICUBIC)
  imageData = io.BytesIO()
  imageNew.save(imageData, format='PNG')
  stringData = base64.b64encode(imageData.getvalue())
  result = ";\n;Generated with Cura_SteamEngine\n"
  result += f"; thumbnail begin {width} {height} {len(stringData)}\n; "
  modulo = 77
  firstLine = True
  for index in range(len(stringData)):
    result = result + chr(stringData[index])
    if index % modulo == 0 and index > 0:
      result = result + '\n; '
      if index == modulo + 10 and firstLine:
        modulo += 1
        firstLine = False
  result += "\n; thumbnail end\n;\n"
  return result

  
def createThumbnail(gcodeFile, image):

  print(f"Creating thumbnail from {image.filename} and including into {gcodeFile}")
  file = open(gcodeFile, 'rb')
  gcode = file.read().decode("utf-8")
  file.close()

  def removeThumbnail():
    nonlocal gcode
    indexBegin = gcode.find("; thumbnail begin")
    if indexBegin > 0:
      indexEnd = gcode.find("; thumbnail end")
      indexEnd += len("; thumbnail end") + 1
      gcode = gcode[0:indexBegin] + gcode[indexEnd:]
    return indexBegin

  originalStart = removeThumbnail()
  if originalStart > 0:
    removeThumbnail()
  else:
    # find first non comment line
    index = 0
    while gcode[index] == ";" or gcode[index] == '\n':
      index = gcode.find("\n", index)
      if index == -1:
        break;
      else:
        index = index + 1
      
    if index == -1:
      orignalStart = 0
    else: 
      originalStart = index
      
  
  thumbnail = createStringThumbnail(image, 300, 300)
  gcode = gcode[0:originalStart] + thumbnail + gcode[originalStart:]
  
  thumbnail = createStringThumbnail(image, 32, 32)
  gcode = gcode[0:originalStart] + thumbnail + gcode[originalStart:]

  # saving to the original file
  new_file = open(gcodeFile, "w")
  new_file.write(gcode)
  new_file.close()




def print_help():
  print("Script takes path to two files. Image file and gcode file.")
  
if __name__ == "__main__":
  argLen = len(sys.argv)
  #print(argLen)
  #for i, arg in enumerate(sys.argv):
  #      print(f"Argument {i:>6}: {arg}")
  
  if argLen != 3:
    print_help()
  else:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    problem = False
    if not os.path.isfile(file1):
      print(f"{file1} is not a file.")
      problem = True
    if not os.path.isfile(file2):
      print(f"{file2} is not a file.")
      problem = True
    
    gcodeF = None
    imageF = None
    extension = pathlib.Path(file1).suffix
    if extension == '.gcode':
      gcodeF = file1
    if extension == '.png':
      imageF = file1
    extension = pathlib.Path(file2).suffix
    if extension == '.gcode':
      gcodeF = file2
    if extension == '.png':
      imageF = file2
    
    if not gcodeF:
      print("You have to specified a .gcode file.")
      problem = True
    if not imageF:
      print("You have to specified a .png file.")
      problem = True
  
    image = Image.open(imageF, mode='r')

    if image.height < 300 or image.width < 300 :
      print(f"Resolution of the input image has to be bigger then 300x300 pixels. The provided image has resolution {image.width}x{image.height}")
      problem = True

    print(f"{imageF} has resolution {image.width}x{image.height}.")    
        
    if not problem:
      createThumbnail(gcodeF, image)
    
  
