Scripts for postprocessing gcode

#### src/includeThumbnail.py

The script requires two inputs. A png file larger than 300x300 pixels and a gcode file. The script will add the 32x32 and 300x300 resolution thumbnails of the image to the gcode. If there are already thumbnails in the gcode, they will be replaced.

**Example usage:**
python includeThumbnail.py picture.png your.gcode
