import numpy as np
import math as m
  
def t_r(degrees):
  return degrees * m.pi / 180

def f_r(radians):
  return radians * 180 / m.pi

def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, m.cos(theta),-m.sin(theta)],
                   [ 0, m.sin(theta), m.cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ m.cos(theta), 0, m.sin(theta)],
                   [ 0           , 1, 0           ],
                   [-m.sin(theta), 0, m.cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ m.cos(theta), -m.sin(theta), 0 ],
                   [ m.sin(theta), m.cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

# phi = t_r(0)
# theta = t_r(25)
# psi = t_r(45)
# # print("phi =", phi)
# # print("theta  =", theta)
# # print("psi =", psi)
  
  
# R = Rz(psi) * Ry(theta) * Rx(phi)
# # print((np.round(R, decimals=2)))
# # print(np.round(R , decimals=2))
# # print(f_r(np.round(R * np.transpose([[  0  , t_r(25)  ,   t_r(90)  ]]), decimals=2)))

# x = m.asin(R[0,2])
# y = m.atan2(-R[0,1], R[0,0])
# z = m.atan2(-R[1,2], R[2,2])

# print(f_r(np.matrix([x,y,z])).round(2))

def calc(roll, pitch, yaw):
  phi = t_r(roll)
  theta = t_r(pitch)
  psi = t_r(yaw)
    
  R = Rz(psi) * Ry(theta) * Rx(phi)

  x = m.asin(R[0,2])
  y = m.atan2(-R[0,1], R[0,0])
  z = m.atan2(-R[1,2], R[2,2])

  return [z, -x, t_r(yaw)] # x, y, z






