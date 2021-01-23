# ξ or ω - roll (more like E)
# ψ or φ - pitch
# ζ or κ - yaw (more like C)

import numpy as np
import math as m

# def create(roll, pitch, yaw):
def create(pitch, roll, yaw): # ????????????
  # Polskie
  b = np.array([
    (
      cos(pitch) * cos(yaw),
      -cos(pitch) * sin(yaw),
      sin(pitch)
    ),
    (
      cos(roll) * sin(yaw) + sin(roll) * sin(pitch) * cos(yaw),
      cos(roll) * cos(yaw) - sin(roll) * sin(pitch) * sin(yaw),
      -sin(roll) * cos(pitch)
    ),
    (
      sin(roll) * sin(yaw) - cos(roll) * sin(pitch) * cos(yaw),
      sin(roll) * cos(yaw) + cos(roll) * sin(pitch) * sin(yaw),
      cos(roll) * cos(pitch)
    )
  ])

  # import code; code.interact(local=dict(globals(), **locals()))


  # Near real time
  # a = np.transpose(np.array([
  #   (
  #     cos(pitch) * cos(yaw),
  #     cos(roll) * sin(yaw) + sin(roll) * sin(pitch) * cos(yaw),
  #     sin(roll) * sin(yaw) - cos(roll) * sin(pitch) * sin(yaw)
  #   ),
  #   (
  #     -cos(pitch) * sin(yaw),
  #     cos(roll) * cos(yaw) - sin(roll) * sin(pitch) * sin(yaw),
  #     sin(roll) * cos(yaw) + cos(roll) * sin(pitch) * sin(yaw)
  #   ),
  #   (
  #     sin(pitch),
  #     -sin(roll) * cos(pitch),
  #     cos(roll) * cos(pitch)
  #   )
  # ]))

  # print(b)
  return b


def sin(v):
  return m.sin(v)

def cos(v):
  return m.cos(v)  
  