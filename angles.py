import math
import euler
import config

def from_exif(exif_data: dict):
  """ Returns pitch, roll, yaw """
  flight_roll = 0 # float(exif_data.get('Flight Roll Degree'))
  flight_pitch = 0 # float(exif_data.get('Flight Pitch Degree'))
  flight_yaw = 0 #360 - float(exif_data.get('Flight Yaw Degree')) 

  gimbal_roll =  float(exif_data.get('Gimbal Roll Degree'))
  gimbal_pitch =  -(90 + float(exif_data.get('Gimbal Pitch Degree'))) * 1.02
  gimbal_yaw = -float(exif_data.get('Gimbal Yaw Degree'))

  # Old code without euler
  # roll = to_radians(gimbal_roll + flight_roll)
  # pitch = to_radians(flight_pitch + gimbal_pitch)
  # yaw =  to_radians(gimbal_yaw + flight_yaw)
  if config.print_debugs:
    print('Pre angles (degrees)', gimbal_roll, gimbal_pitch, gimbal_yaw)
    print('Post angles (radians)', euler.calc(gimbal_roll, gimbal_pitch, gimbal_yaw))

  return euler.calc(gimbal_roll, gimbal_pitch, gimbal_yaw)

def to_radians(degrees):
  return degrees * math.pi / 180