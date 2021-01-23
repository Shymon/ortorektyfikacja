import orthorectification
import numpy as np
import config

def calc_boundings(
  orthorectification_data : orthorectification.Data,
  step,
  common_altitude
):
  beginning_x = orthorectification_data.utm_latitude
  beginning_y = orthorectification_data.utm_longtitude

  # Non nadir test
  if orthorectification_data.relative_pitch > 5:
    distance = orthorectification_data.gps_altitude / np.tan((90 - orthorectification_data.relative_pitch) * np.pi / 180)
    x_distance = distance * np.sin(-orthorectification_data.relative_yaw * np.pi / 180)
    y_distance = distance * np.cos(-orthorectification_data.relative_yaw * np.pi / 180)

    beginning_x = orthorectification_data.utm_latitude + x_distance
    beginning_y = orthorectification_data.utm_longtitude + y_distance

  start_x = None
  end_x = None
  start_y = None
  end_y = None

  multiplier = 10

  start_x = _move_until_outside_of_image(beginning_x, beginning_y, step, common_altitude, True, False, multiplier, orthorectification_data)
  end_x = _move_until_outside_of_image(beginning_x, beginning_y, step, common_altitude, True, True, multiplier, orthorectification_data)
  start_y = _move_until_outside_of_image(beginning_x, beginning_y, step, common_altitude, False, False, multiplier, orthorectification_data)
  end_y = _move_until_outside_of_image(beginning_x, beginning_y, step, common_altitude, False, True, multiplier, orthorectification_data)

  if config.print_debugs:
    print('Calulated inital bounds', round(start_x, 2), round(end_x, 2), round(start_y, 2), round(end_y, 2))

  for y_line in np.arange(start_y, end_y, step * multiplier):
    new_x = _move_until_outside_of_image(beginning_x, y_line, step, common_altitude, True, True, multiplier, orthorectification_data)
    if new_x > end_x:
      end_x = new_x

    new_x = _move_until_outside_of_image(beginning_x, y_line, step, common_altitude, True, False, multiplier, orthorectification_data)
    if new_x < start_x:
      start_x = new_x

  for x_line in np.arange(start_x, end_x, step*10):
    new_y = _move_until_outside_of_image(x_line, beginning_y, step, common_altitude, False, True, multiplier, orthorectification_data)
    if new_y > end_y:
      end_y = new_y

    new_y = _move_until_outside_of_image(x_line, beginning_y, step, common_altitude, False, False, multiplier, orthorectification_data)
    if new_y < start_x:
      start_x = new_y

  if config.print_debugs:
    print('Calulated advanced bounds x', round(start_x, 2), round(end_x, 2), 'y', round(start_y, 2), round(end_y, 2))

  return start_x, end_x, start_y, end_y

def _move_until_outside_of_image(
  start_x,
  start_y,
  step,
  common_altitude,
  move_x,
  move_positive,
  multiplier,
  data : orthorectification.Data
):
  current_x = start_x
  current_y = start_y

  while 1:
    img_x_pos, img_y_pos = orthorectification.calc_position_on_image(current_x, current_y, common_altitude, data)

    if orthorectification.outside_image(int(img_x_pos), int(img_y_pos), data):
      break
    if move_x:
      current_x += step * multiplier if move_positive else - step * multiplier
    else:
      current_y += step * multiplier if move_positive else - step * multiplier
        
  return current_x if move_x else current_y











  # while 1:
  #     x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #     x_pos = x * pixels_per_m_x
  #     y_pos = y * pixels_per_m_y

  #     img_x_pos = middle_x + int(x_pos)
  #     img_y_pos = middle_y - int(y_pos)
  #     if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #       break
  #     current_x += step * 10
  # end_x = current_x

  # current_x = beginning_x
  # current_y = beginning_y
  # while 1:
  #     x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #     x_pos = x * pixels_per_m_x
  #     y_pos = y * pixels_per_m_y

  #     img_x_pos = middle_x + int(x_pos)
  #     img_y_pos = middle_y - int(y_pos)
  #     if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #       break
  #     current_x -= step * 10
  # start_x = current_x

  # current_x = beginning_x
  # current_y = beginning_y
  # while 1:
  #     x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #     x_pos = x * pixels_per_m_x
  #     y_pos = y * pixels_per_m_y

  #     img_x_pos = middle_x + int(x_pos)
  #     img_y_pos = middle_y - int(y_pos)
  #     if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #       break
  #     current_y += step * 10
  # end_y = current_y

  # current_x = beginning_x
  # current_y = beginning_y
  # while 1:
  #     x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #     x_pos = x * pixels_per_m_x
  #     y_pos = y * pixels_per_m_y

  #     img_x_pos = middle_x + int(x_pos)
  #     img_y_pos = middle_y - int(y_pos)
  #     if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #       break
  #     current_y -= step * 10
  # start_y = current_y


  # for y_line in np.arange(start_x - 10, end_x + 10, step*10):
  #   current_x = y_line
  #   current_y = beginning_y
  #   while 1:
  #       x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #       x_pos = x * pixels_per_m_x
  #       y_pos = y * pixels_per_m_y

  #       img_x_pos = middle_x + int(x_pos)
  #       img_y_pos = middle_y - int(y_pos)
  #       if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #         break

  #       current_y += step * 10
  #   if end_y < current_y:
  #     end_y = current_y

  #   current_x = beginning_x
  #   current_y = beginning_y
  #   while 1:
  #       x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #       x_pos = x * pixels_per_m_x
  #       y_pos = y * pixels_per_m_y

  #       img_x_pos = middle_x + int(x_pos)
  #       img_y_pos = middle_y - int(y_pos)
  #       if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #         break
  #       current_y -= step * 10
  #   if start_y > current_y:
  #     start_y = current_y

  # for x_line in np.arange(start_y, end_y, step*10):
  #   current_x = x_line
  #   current_y = beginning_y
  #   while 1:
  #       x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #       x_pos = x * pixels_per_m_x
  #       y_pos = y * pixels_per_m_y

  #       img_x_pos = middle_x + int(x_pos)
  #       img_y_pos = middle_y - int(y_pos)
  #       if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #         break
  #       current_y += step * 10
  #   if end_y < current_y:
  #     end_y = current_y

  #   current_x = beginning_x
  #   current_y = beginning_y
  #   while 1:
  #       x, y = orthorectification.calc_points(current_x, current_y, h, utm_latitude, utm_longtitude, gps_altitude, r_matrix, focal_length)
  #       x_pos = x * pixels_per_m_x
  #       y_pos = y * pixels_per_m_y

  #       img_x_pos = middle_x + int(x_pos)
  #       img_y_pos = middle_y - int(y_pos)
  #       if img_y_pos >= res_y or img_y_pos < 0 or img_x_pos >= res_x or img_x_pos < 0:
  #         break
  #       current_y -= step * 10
  #   if start_y > current_y:
  #     start_y = current_y

  


  # return start_x, end_x, start_y, end_y


