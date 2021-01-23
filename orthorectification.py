import angles
import rotation_matrix
import gps_coordinates

import numpy as np

class Data:
  def __init__(self, data_source, photo_exif_data, frame_srt_data, sensor_width, sensor_height):
    """
      data_source - 'srt' or 'exif' - describes data source

      photo_exif_data - dictionary with entries from exiftool

      srt_data - dictionary with entries from srt file

      sensor_width in meters, e. g. (4.7 / 1000) that is (4.7 mm)  

      sensor_height in meters  
    """
    if data_source == 'exif':
      self.focal_length_mm = float(photo_exif_data.get('Focal Length').split(' ')[0])
      self.focal_length = self.focal_length_mm / 1000

      self.relative_pitch = (90 + float(photo_exif_data.get('Gimbal Pitch Degree')))
      self.relative_yaw = -float(photo_exif_data.get('Gimbal Yaw Degree'))
      self.roll, self.pitch, self.yaw = angles.from_exif(photo_exif_data)
      self.rotation_matrix = rotation_matrix.create(self.roll, self.pitch, self.yaw)

      self.gps_altitude = float(photo_exif_data.get('GPS Altitude').split(' ')[0])
      self.utm_latitude, self.utm_longtitude, self.zone, self.zone_letter = gps_coordinates.to_utm(
        float(photo_exif_data.get('Latitude')),
        float(photo_exif_data.get('Longitude'))
      )
      self.X0 = self.utm_latitude
      self.Y0 = self.utm_longtitude
      self.Z0 = self.gps_altitude

      self.sensor_size_x = sensor_width
      self.sensor_size_y = sensor_height

      self.resolution_x = int(photo_exif_data.get('Image Width'))
      self.resolution_y = int(photo_exif_data.get('Image Height'))

      self.sensor_middle_x = int(self.resolution_x / 2)
      self.sensor_middle_y = int(self.resolution_y / 2)

      self.pixels_per_m_x = self.resolution_x / self.sensor_size_x
      self.pixels_per_m_y = self.resolution_y / self.sensor_size_y
    elif data_source == 'srt':
      self.focal_length = frame_srt_data['focal_length']

      self.relative_pitch = frame_srt_data['pitch']
      self.relative_yaw = -frame_srt_data['yaw']
      self.roll, self.pitch, self.yaw = angles.from_exif({
        'Gimbal Yaw Degree': frame_srt_data['yaw'],
        'Gimbal Roll Degree': frame_srt_data['roll'],
        'Gimbal Pitch Degree': frame_srt_data['pitch']
      })
      self.rotation_matrix = rotation_matrix.create(self.roll, self.pitch, self.yaw)

      self.gps_altitude = frame_srt_data['altitude']
      self.utm_latitude = frame_srt_data['latitude']
      self.utm_longtitude = frame_srt_data['longitude']
      self.X0 = self.utm_latitude
      self.Y0 = self.utm_longtitude
      self.Z0 = self.gps_altitude

      self.sensor_size_x = sensor_width
      self.sensor_size_y = sensor_height

      self.resolution_x = frame_srt_data['image_width']
      self.resolution_y = frame_srt_data['image_height']

      self.sensor_middle_x = int(self.resolution_x / 2)
      self.sensor_middle_y = int(self.resolution_y / 2)

      self.pixels_per_m_x = self.resolution_x / self.sensor_size_x
      self.pixels_per_m_y = self.resolution_y / self.sensor_size_y
    else:
      raise Exception('Invalid data source', data_source)

def calc_position_on_image(X, Y, Z, data: Data):
    # Old slow method
    x_diff = (X - data.X0)
    y_diff = (Y - data.Y0)
    z_diff = (Z - data.Z0)
    nominator_x = (   data.rotation_matrix[0, 0] * x_diff
                    + data.rotation_matrix[1, 0] * y_diff
                    + data.rotation_matrix[2, 0] * z_diff)
    nominator_y = (   data.rotation_matrix[0, 1] * x_diff
                    + data.rotation_matrix[1, 1] * y_diff
                    + data.rotation_matrix[2, 1] * z_diff)
    denominator = (   data.rotation_matrix[0, 2] * x_diff
                    + data.rotation_matrix[1, 2] * y_diff
                    + data.rotation_matrix[2, 2] * z_diff)
    x = - data.focal_length * (nominator_x / denominator)
    y = - data.focal_length * (nominator_y / denominator)


    x_pos = x * data.pixels_per_m_x
    y_pos = y * data.pixels_per_m_y

    img_x_pos = data.sensor_middle_x + x_pos
    img_y_pos = data.sensor_middle_y - y_pos

    return img_x_pos, img_y_pos

def outside_image(x, y, data : Data, interpolation_margin=2):
  return (
    y >= data.resolution_y - interpolation_margin 
      or y < interpolation_margin 
        or x >= data.resolution_x  - interpolation_margin
          or x < interpolation_margin
  )

def process_image(x_range, y_range, common_altitude, image_data, orthorectification_data : Data, interpolation_method):
  # new_image = np.zeros((len(x_range), len(y_range), 3), dtype=np.uint8)
  # transparency_mask = np.full((len(x_range), len(y_range)), 255, dtype=np.uint8)

  new_image = np.zeros((len(x_range), len(y_range), 3), dtype=np.uint8)
  transparency_mask = np.full((len(x_range), len(y_range)), 255, dtype=np.uint8)

  mesh = np.array(np.meshgrid(y_range, x_range))
  x_diffs = (mesh[1] - np.ones((len(x_range),len(y_range))) * orthorectification_data.X0)
  y_diffs = (mesh[0] - np.ones((len(x_range),len(y_range))) * orthorectification_data.Y0)
  z_diffs = np.ones((len(x_range),len(y_range))) * (common_altitude - orthorectification_data.Z0)

  x_nominators = (  x_diffs * orthorectification_data.rotation_matrix[0, 0] 
                  + y_diffs * orthorectification_data.rotation_matrix[1, 0] 
                  + z_diffs * orthorectification_data.rotation_matrix[2, 0]) 
  y_nominators = (  x_diffs * orthorectification_data.rotation_matrix[0, 1] 
                  + y_diffs * orthorectification_data.rotation_matrix[1, 1] 
                  + z_diffs * orthorectification_data.rotation_matrix[2, 1]) 
  denominators = (  x_diffs * orthorectification_data.rotation_matrix[0, 2] 
                  + y_diffs * orthorectification_data.rotation_matrix[1, 2] 
                  + z_diffs * orthorectification_data.rotation_matrix[2, 2]) 
  xes = - orthorectification_data.focal_length * (x_nominators / denominators)
  yes = - orthorectification_data.focal_length * (y_nominators / denominators)

  x_poses = xes * orthorectification_data.pixels_per_m_x
  y_poses = yes * orthorectification_data.pixels_per_m_y

  img_x_poses = orthorectification_data.sensor_middle_x + x_poses
  img_y_poses = orthorectification_data.sensor_middle_y - y_poses

  interpolation_margin = 2
  lower_bound = 0 + interpolation_margin
  upper_bound_x = orthorectification_data.resolution_x - interpolation_margin
  upper_bound_y = orthorectification_data.resolution_y - interpolation_margin
  x_mask = (img_x_poses < lower_bound) | (img_x_poses > upper_bound_x)
  y_mask = (img_y_poses < lower_bound) | (img_y_poses > upper_bound_y)

  new_image[x_mask | y_mask] = [255, 255, 255]
  transparency_mask[x_mask | y_mask] = 0

  img_x_poses[x_mask | y_mask] = -1
  img_y_poses[x_mask | y_mask] = -1

  for ix,iy in np.ndindex(img_x_poses.shape):
      x_pos = img_x_poses[ix][iy]
      if x_pos == -1:
        continue

      y_pos = img_y_poses[ix][iy]
      if y_pos == -1:
        continue

      if interpolation_method == 'none':
        new_image[ix][iy] = image_data[int(y_pos)][int(x_pos)]
      elif interpolation_method == 'neighbours_avg':
        # 8 neightbours average
        y_pos = int(y_pos)
        x_pos = int(x_pos)
        new_image[ix][iy] = [
          int(np.mean(image_data[y_pos-1:y_pos+2, x_pos-1:x_pos+2, 0])),
          int(np.mean(image_data[y_pos-1:y_pos+2, x_pos-1:x_pos+2, 1])),
          int(np.mean(image_data[y_pos-1:y_pos+2, x_pos-1:x_pos+2, 2]))
        ]
      elif interpolation_method == 'bilinear':
        # Bilinear interpolation
        new_image[ix][iy] = _bilinear_interpolate(image_data, x_pos, y_pos)
      else:
        raise Exception('Invalid interpolation method')
      

  return new_image, transparency_mask

def async_process_image(queue, index, args):
  image, transparency_mask = process_image(*args)
  queue.put((index, image, transparency_mask))

def _bilinear_interpolate(im, x, y):
  x = np.asarray(x)
  y = np.asarray(y)

  x0 = np.floor(x).astype(int)
  x1 = x0 + 1
  y0 = np.floor(y).astype(int)
  y1 = y0 + 1

  x0 = np.clip(x0, 0, im.shape[1]-1)
  x1 = np.clip(x1, 0, im.shape[1]-1)
  y0 = np.clip(y0, 0, im.shape[0]-1)
  y1 = np.clip(y1, 0, im.shape[0]-1)

  Ia = im[ y0, x0 ]
  Ib = im[ y1, x0 ]
  Ic = im[ y0, x1 ]
  Id = im[ y1, x1 ]

  wa = (x1-x) * (y1-y)
  wb = (x1-x) * (y-y0)
  wc = (x-x0) * (y1-y)
  wd = (x-x0) * (y-y0)

  return wa*Ia + wb*Ib + wc*Ic + wd*Id