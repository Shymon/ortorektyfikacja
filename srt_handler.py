import srt
import parse
import gps_coordinates

def parse_file(file_path):
  with open(file_path, 'r') as file:
      data = file.read()
      subs = list(srt.parse(data))

  frames_data = {}

  for sub in subs:

    data = parse_sub(sub.content)
    # Frame cnt => frame data
    frames_data[data['frame']] = data.named

  return frames_data

def parse_sub(sub):
  """
    Returns dict as follows:
    {
      'frame': frame,
      'latitude': latitude,
      'longtitude': longtitude,
      'altitude': altitude,
      'yaw': yaw,
      'pitch': pitch,
      'roll': roll
    }
  """

  # This parses string for MAVIC 2ED Fir srt files
  fir = parse.parse(
    '<font size="36">FrameCnt : {frame:d}, DiffTime : {diff_time:d}ms\n{date}\n[color_md : default] [latitude: {latitude:f}] [longtitude: {longtitude:f}] [altitude: {altitude:f}] [Drone: Yaw:{yaw:f}, Pitch:{pitch:f}, Roll:{roll:f}] </font>', 
    sub
  )

  if fir:
    return fir

  # This parses string for MAVIC 2ED rgb srt files
  rgb = parse.parse(
    '<font size="36">FrameCnt : {frame:d}, DiffTime : {diff_time:d}ms\n{date}\n[iso : {iso}] [shutter : {shutter}] [fnum : {fnum}] [ev : {ev}] [ct : {ct}] [color_md : default] [focal_len : {focal_len}] [latitude: {latitude:f}] [longtitude: {longtitude:f}] [altitude: {altitude:f}] [Drone: Yaw:{yaw:f}, Pitch:{pitch:f}, Roll:{roll:f}] </font>',
    sub
  )

  return rgb

def with_normalized_values(file_path):
  frames_data = parse_file(file_path)

  for key in frames_data:
    frame_data = frames_data[key]

    lat, long, *_ = gps_coordinates.to_utm(frame_data['latitude'], frame_data['longtitude'])

    frame_data['latitude'] = lat
    frame_data['longitude'] = long
    frame_data['altitude'] = frame_data['altitude']

    frame_data['pitch'] = -90 # Pitch is not from gimbal
    frame_data['roll']  = 0 # Roll is not from gimbal

  return frames_data
