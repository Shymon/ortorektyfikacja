import re
import exiftool
import orthorectification
import boundings
import geotiff
import config
import srt_handler

import numpy as np
import os
import argparse
from PIL import Image
from multiprocessing import Process, Queue
import time
import cv2


###################
## Parsing input ##
###################

parser = argparse.ArgumentParser(description="""Program realizujący uproszczoną ortorektyfikację. Część pracy 
                                                inżynierskiej "Uproszczone techniki ortorektyfikacji zdjęć lotniczych". 
                                                Wykonał Szymon Ruta""")
parser.add_argument('-f' , type=str, help='Plik wejściowy z obrazem, wymagany przy niepodaniu folderu z obrazami wejściowymi lub wideo')
parser.add_argument('-d' , type=str, help="""Folder z obrazami wejściowymi, wymagany przy niepodaniu pliku wejściowego z obrazem.
                                              Tylko jedna opcja wejściowa powinna być podana: plik (-f) lub folder (-d).""")
parser.add_argument('-v' , type=str, help="""Plik wejściowy wideo, wymagany przy niepodaniu folderu z obrazami wejściowymi 
                                              oraz pliku wejściowego z obrazem. Dodatkowo wymaga podania pliku srt""")
parser.add_argument('-s' , type=str, help='Plik wejściowy SRT związany z wideo. Wymagany przy podaniu pliku wideo.')
parser.add_argument('--skipFrames' , type=int, help='Ile klatek przy przetwarzaniu wideo pomijać.')
parser.add_argument('--maxFrames' , type=int, help='Maksymalna liczba przetworzonych klatek po której program kończy działanie.')
parser.add_argument('--focalLength' , type=str, help="""Wartość ogniskowej kamery w mm (domyślnie 4.5). Jeżeli brauje informacji w
                                                      pliku to brana jest ta wartość""", default=4.5)
parser.add_argument('-o', type=str, help='Folder na obrazy wyjściowe (domyślnie \'.\')', default='.')
parser.add_argument('-i', type=str, help='Metoda interpolacji (domyślnie \'none\')', default='none',
                          choices=['none', 'neighbours_avg', 'bilinear'])
parser.add_argument('-t', type=int, help='Liczba wątków używanych do przeprowadzania ortorektyfikacji (domyślnie 6)', default=6)
parser.add_argument('--debug', help='Czy wyświetlać informacje debugowania (domyślnie false)', action='store_true')
parser.add_argument('--sensorWidth', type=float, help='Wysokość sensora kamery w mm (domyślnie 6.1)', default=6.1)
parser.add_argument('--sensorHeight', type=float, help='Szerokość sensora kamery w mm (domyślnie 4.7)', default=4.7)
parser.add_argument('--step', type=float, help="""Domyślny krok ortorektyfikacji (rzeczywista długość 
                                                  w metrach przypadająca na 1 piksel) (domyślnie 0.15)""", default=0.15)
parser.add_argument('--altitude', type=float, help='Średnia wysokość terenu na zdjęciach względem wysokości drona (domyślnie 0)',
                                  default=0)
parser.add_argument('--singleThread', help='Czy wymusić używanie tylko jednego wątku', action='store_true')

args = parser.parse_args()

multiprocess = not(args.singleThread)
processes_count = args.t
output_folder = args.o
input_folder = args.d
input_file = args.f
video_path = args.v
srt_file_path = args.s
skip_frames = args.skipFrames
max_frames = args.maxFrames
focal_length = args.focalLength
interpolation_method = args.i
sensor_width = args.sensorWidth
sensor_height = args.sensorHeight
step = args.step
common_altitude = args.altitude
config.print_debugs = args.debug

if not(input_folder or input_file or video_path):
  print('Wymagane jest podanie pliku wejściowego (-f) lub folderu z obrazami wejściowymi (-d) lub pliku wideo (-v)', '\n')
  parser.print_help()
  exit(1)
elif video_path and (input_folder or input_file):
  print('Został podany plik z wideo (-v) oraz folder z obrazami wejściowymi (-d) lub plik z obrazem (-f). Tylko jedna opcja może zostać uzyta!', '\n')
  parser.print_help()
  exit(1)
elif input_folder and input_file:
  print('Został podany plik wejściowy (-f) oraz folder z obrazami wejściowymi (-d). Tylko jedna opcja może zostać uzyta!', '\n')
  parser.print_help()
  exit(1)

if video_path and not(srt_file_path):
  print('Wymagane jest podanie pliku srt (-s) przy podaniu pliku wideo (-v)', '\n')
  parser.print_help()
  exit(1)

##########################################
## Function processing one file / frame ##
##########################################

def process_image(orthorectification_data, image_data, file_name):
  tic = time.time()
  # Wyznaczanie rozmaru 
  start_x, end_x, start_y, end_y = boundings.calc_boundings(
    orthorectification_data,
    step,
    common_altitude
  )

  if config.print_debugs:
    print('Drone at: ', round(orthorectification_data.utm_latitude, 2), round(orthorectification_data.utm_longtitude, 2))
    print('Boundary coords: ', round(start_x, 2), round(end_x, 2), round(start_y, 2), round(end_y, 2))

  x_range = np.arange(start_x, end_x, step)
  y_range = np.arange(end_y, start_y, -step)

  x_count = len(x_range)
  y_count = len(y_range)

  if config.print_debugs:
    print('Resolution: ', x_count, ' x ', y_count)

  if x_count == 0 or y_count == 0:
    print(("Wystąpił błąd w programie, podczas obliczania krawędzi (nie znaleziono ich, "
          "powstał obraz o boku 0 długości). Sprawdź zgodność współrzędnych."))
    exit()

  new_image = None
  transparency_mask = None

  if multiprocess:
    x_ranges = np.array_split(x_range, processes_count)
    processes = []
    images_queue = Queue()

    # Each process processes it's range and pushes result to queue with index as tuple (index, image, transparency_mask)
    for i, mini_x_range in enumerate(x_ranges, start=0):
      args = (mini_x_range, y_range, common_altitude, image_data, orthorectification_data, interpolation_method)
      p = Process(target=orthorectification.async_process_image, args=(images_queue, i, args))
      processes.append(p)
     
    for p in processes:
      p.start()

    images_array = []
    for p in processes:
      images_array.append(images_queue.get())

    for p in processes:
      p.join()

    # Mini images come in (index, image, transparency_mask) tuple so they must be processed
    # First sort mini images in proper order then remove index and finally concatenate them
    new_image = np.concatenate(list(map(lambda x: x[1], sorted(images_array))), axis=0)
    transparency_mask = np.concatenate(list(map(lambda x: x[2], sorted(images_array))), axis=0)

  else:
    new_image, transparency_mask = orthorectification.process_image(x_range, y_range, common_altitude, image_data, orthorectification_data, interpolation_method)

  toc = time.time()
  print('Przetworzono obraz w: ', round(toc - tic, 3), 's')
  # Save resulting image to png file
  # Image.fromarray(new_image).save('result/result.png')

  # Save resulting image as tif file
  geotiff.write(
    os.path.join(output_folder, f'{file_name}.tif'),
    new_image,
    transparency_mask,
    start_x,
    end_y,
    step
  )


#######################
## Processing videos ##
#######################
if video_path:
  cap = cv2.VideoCapture(video_path) 
  srt_data = srt_handler.with_normalized_values(srt_file_path)

  # Loop untill the end of the video 
  current_frame = 0
  frames_processed = 0
  if config.print_debugs:
    print('Video open: ', cap.isOpened())

  while (cap.isOpened()): 
      # Capture frame-by-frame 
      ret, frame = cap.read() 
      current_frame += 1

      if not(ret) or (max_frames and max_frames <= frames_processed):
        break

      if skip_frames and (current_frame - 1) % skip_frames != 0:
        continue

      print('Przetwadzanie klatki nr', current_frame)

      current_frame_data = srt_data[current_frame]
      current_frame_data.update({
        'focal_length': focal_length,
        'image_width': frame.shape[1],
        'image_height': frame.shape[0]
      })

      orthorectification_data = orthorectification.Data('srt', {}, current_frame_data, sensor_width, sensor_height, focal_length)
      process_image(orthorectification_data, frame, f'Frame {current_frame}')
      frames_processed += 1

  cap.release() 
  print('Wideo zostało przetworzone')


##############################
## Processing file or files ##
##############################
else:
  if input_folder:
    files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    files = map(lambda f: os.path.join(input_folder, f), files)
  elif input_file:
    files = [input_file]
  else:
    files = []

  for file_path in files:
    file_name = os.path.basename(file_path).split('.')[0]

    photo_data = exiftool.process(file_path)
    orthorectification_data = orthorectification.Data(
      'exif',
      photo_data,
      {},
      sensor_width / 1000,
      sensor_height / 1000,
      focal_length
    )

    image = Image.open(file_path)
    image_data = np.asarray(image)

    process_image(orthorectification_data, image_data, file_name)

  print('Wszystkie obrazy zostały przetworzone')


