import subprocess


def process(path):
  out = subprocess.Popen(['exiftool', path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT)
  stdout, stderr = out.communicate()

  output = list(filter(lambda x: x[0] != '', list(map(lambda x: list(map(lambda y: y.strip(), x.split(':', 1))), stdout.decode().split("\n")))))
  keys = map(lambda x: x[0], output)
  values = map(lambda x: x[1] if x[0] else None, output)

  values_dictionary = dict(zip(keys, values))
  return values_dictionary

# Przykład:
# print(values_dictionary.get('Field Of View'))

# Dostępne dane:
# ExifTool Version Number         : 12.14
# File Name                       : DJI_0647.JPG
# Directory                       : .
# File Size                       : 7.4 MiB
# File Modification Date/Time     : 2021:01:06 20:17:51+01:00
# File Access Date/Time           : 2021:01:12 17:55:53+01:00
# File Creation Date/Time         : 2021:01:06 21:07:30+01:00
# File Permissions                : rw-rw-rw-
# File Type                       : JPEG
# File Type Extension             : jpg
# MIME Type                       : image/jpeg
# Exif Byte Order                 : Little-endian (Intel, II)
# Image Description               : created by dji camera
# Make                            : DJI
# Camera Model Name               : FC2103
# Orientation                     : Horizontal (normal)
# X Resolution                    : 72
# Y Resolution                    : 72
# Resolution Unit                 : inches
# Software                        : 10.00.13.02
# Modify Date                     : 2019:03:28 14:31:31
# Y Cb Cr Positioning             : Centered
# Exposure Time                   : 1/250
# F Number                        : 2.8
# Exposure Program                : Program AE
# ISO                             : 100
# Exif Version                    : 0230
# Date/Time Original              : 2019:03:28 14:31:31
# Create Date                     : 2019:03:28 14:31:31
# Components Configuration        : -, Cr, Cb, Y
# Compressed Bits Per Pixel       : 4.478471141
# Aperture Value                  : 2.8
# Exposure Compensation           : 0
# Max Aperture Value              : 2.8
# Subject Distance                : undef
# Metering Mode                   : Average
# Light Source                    : Unknown
# Flash                           : No flash function
# Focal Length                    : 4.5 mm
# Warning                         : [minor] Bad MakerNotes directory
# Flashpix Version                : 0100
# Color Space                     : sRGB
# Exif Image Width                : 4056
# Exif Image Height               : 3040
# Interoperability Index          : R98 - DCF basic file (sRGB)
# Interoperability Version        : 0100
# Exposure Index                  : 0.25
# File Source                     : Digital Camera
# Scene Type                      : Directly photographed
# Custom Rendered                 : Normal
# Exposure Mode                   : Auto
# White Balance                   : Manual
# Digital Zoom Ratio              : undef
# Focal Length In 35mm Format     : 24 mm
# Scene Capture Type              : Standard
# Gain Control                    : None
# Contrast                        : Normal
# Saturation                      : Normal
# Sharpness                       : Hard
# Device Setting Description      : (Binary data 4 bytes, use -b option to extract)
# Subject Distance Range          : Unknown
# Lens Info                       : 0mm f/2.2
# GPS Version ID                  : 2.3.0.0
# GPS Latitude Ref                : North
# GPS Longitude Ref               : East
# GPS Altitude Ref                : Above Sea Level
# XP Comment                      : 0.9.142
# XP Keywords                     : N
# Compression                     : Unknown (0)
# Thumbnail Offset                : 8902
# Thumbnail Length                : 29871
# About                           : DJI Meta Data
# Format                          : image/jpg
# Latitude                        : 50 deg 25' 16.78" N
# Longitude                       : 18 deg 45' 2.85" E
# Absolute Altitude               : +1.20
# Relative Altitude               : +74.90
# Gimbal Roll Degree              : -0.20
# Gimbal Yaw Degree               : +61.40
# Gimbal Pitch Degree             : -89.50
# Flight Roll Degree              : -2.50
# Flight Yaw Degree               : +78.60
# Flight Pitch Degree             : -15.10
# Cam Reverse                     : 0
# Gimbal Reverse                  : 0
# Self Data                       : DJI Self data
# Version                         : 7.0
# Has Settings                    : False
# Has Crop                        : False
# Already Applied                 : False
# MPF Version                     : 0100
# Number Of Images                : 2
# MP Image Flags                  : Dependent child image
# MP Image Format                 : JPEG
# MP Image Type                   : Large Thumbnail (VGA equivalent)
# MP Image Length                 : 856716
# MP Image Start                  : 6949723
# Dependent Image 1 Entry Number  : 0
# Dependent Image 2 Entry Number  : 0
# Image UID List                  : (Binary data 66 bytes, use -b option to extract)
# Total Frames                    : 1
# Image Width                     : 4056
# Image Height                    : 3040
# Encoding Process                : Baseline DCT, Huffman coding
# Bits Per Sample                 : 8
# Color Components                : 3
# Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
# Aperture                        : 2.8
# Image Size                      : 4056x3040
# Megapixels                      : 12.3
# Scale Factor To 35 mm Equivalent: 5.3
# Shutter Speed                   : 1/250
# Thumbnail Image                 : (Binary data 29871 bytes, use -b option to extract)
# GPS Altitude                    : 74.9 m Above Sea Level
# GPS Latitude                    : 50 deg 25' 16.72" N
# GPS Longitude                   : 18 deg 45' 2.83" E
# Preview Image                   : (Binary data 856716 bytes, use -b option to extract)
# Circle Of Confusion             : 0.006 mm
# Field Of View                   : 73.7 deg
# Focal Length                    : 4.5 mm (35 mm equivalent: 24.0 mm)
# GPS Position                    : 50 deg 25' 16.72" N, 18 deg 45' 2.83" E
# Hyperfocal Distance             : 1.28 m
# Light Value                     : 10.9