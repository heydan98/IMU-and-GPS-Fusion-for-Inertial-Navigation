# import scipy.io
# import numpy as np
# np.set_printoptions(suppress=True)
# data = scipy.io.loadmat(r"C:\Users\20134\Downloads\madgwick_algorithm_matlab/ExampleData.mat")

# np.savetxt(("Magnetometer.csv"),np.array(data['Magnetometer']),delimiter=',')
# import ctypes
# fun = ctypes.CDLL("magwick_c.so")
# fun.MadgwickAHRSupdate.argtypes = [ctypes.c_,ctypes.c_,ctypes.c_,ctypes.c_,ctypes.c_,ctypes.c_,ctypes.c_,ctypes.c_,ctypes.c_]
# #  gx,  gy,  gz,  ax,  ay,  az,  mx,  my,  mz

import numpy as np
import math as m
  



from math import sqrt, pi
sampleFreq=100.0
betaDef = 0.4
beta = betaDef
q0 = 1.0
q1 = 0.0
q2 = 0.0
q3 = 0.0

def invSqrt(x):
    return 1/sqrt(x)
def MadgwickAHRSupdate( gx,  gy,  gz,  ax,  ay,  az,  mx,  my,  mz) :
    global q0, q1, q2, q3
    if((mx == 0.0) and (my == 0.0) and (mz == 0.0)) :
        MadgwickAHRSupdateIMU(gx, gy, gz, ax, ay, az)
        return 1


    qDot1 = 0.5 * (-q1 * gx - q2 * gy - q3 * gz)
    qDot2 = 0.5 * (q0 * gx + q2 * gz - q3 * gy)
    qDot3 = 0.5 * (q0 * gy - q1 * gz + q3 * gx)
    qDot4 = 0.5 * (q0 * gz + q1 * gy - q2 * gx)

    
    if(not ((ax == 0.0) and (ay == 0.0) and (az == 0.0))) :

        recipNorm = invSqrt(ax * ax + ay * ay + az * az)
        ax *= recipNorm
        ay *= recipNorm
        az *= recipNorm   

        recipNorm = invSqrt(mx * mx + my * my + mz * mz)
        mx *= recipNorm
        my *= recipNorm
        mz *= recipNorm

        _2q0mx = 2. * q0 * mx
        _2q0my = 2. * q0 * my
        _2q0mz = 2. * q0 * mz
        _2q1mx = 2. * q1 * mx
        _2q0 = 2. * q0
        _2q1 = 2. * q1
        _2q2 = 2. * q2
        _2q3 = 2. * q3
        _2q0q2 = 2. * q0 * q2
        _2q2q3 = 2. * q2 * q3
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        hx = mx * q0q0 - _2q0my * q3 + _2q0mz * q2 + mx * q1q1 + _2q1 * my * q2 + _2q1 * mz * q3 - mx * q2q2 - mx * q3q3
        hy = _2q0mx * q3 + my * q0q0 - _2q0mz * q1 + _2q1mx * q2 - my * q1q1 + my * q2q2 + _2q2 * mz * q3 - my * q3q3
        _2bx = sqrt(hx * hx + hy * hy)
        _2bz = -_2q0mx * q2 + _2q0my * q1 + mz * q0q0 + _2q1mx * q3 - mz * q1q1 + _2q2 * my * q3 - mz * q2q2 + mz * q3q3
        _4bx = 2. * _2bx
        _4bz = 2. * _2bz

        s0 = -_2q2 * (2. * q1q3 - _2q0q2 - ax) + _2q1 * (2. * q0q1 + _2q2q3 - ay) - _2bz * q2 * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q3 + _2bz * q1) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q2 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        s1 = _2q3 * (2. * q1q3 - _2q0q2 - ax) + _2q0 * (2. * q0q1 + _2q2q3 - ay) - 4. * q1 * (1 - 2. * q1q1 - 2. * q2q2 - az) + _2bz * q3 * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q2 + _2bz * q0) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q3 - _4bz * q1) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        s2 = -_2q0 * (2. * q1q3 - _2q0q2 - ax) + _2q3 * (2. * q0q1 + _2q2q3 - ay) - 4. * q2 * (1 - 2. * q1q1 - 2. * q2q2 - az) + (-_4bx * q2 - _2bz * q0) * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (_2bx * q1 + _2bz * q3) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + (_2bx * q0 - _4bz * q2) * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        s3 = _2q1 * (2. * q1q3 - _2q0q2 - ax) + _2q2 * (2. * q0q1 + _2q2q3 - ay) + (-_4bx * q3 + _2bz * q1) * (_2bx * (0.5 - q2q2 - q3q3) + _2bz * (q1q3 - q0q2) - mx) + (-_2bx * q0 + _2bz * q2) * (_2bx * (q1q2 - q0q3) + _2bz * (q0q1 + q2q3) - my) + _2bx * q1 * (_2bx * (q0q2 + q1q3) + _2bz * (0.5 - q1q1 - q2q2) - mz)
        recipNorm = invSqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3) 
        s0 *= recipNorm
        s1 *= recipNorm
        s2 *= recipNorm
        s3 *= recipNorm

        qDot1 -= beta * s0
        qDot2 -= beta * s1
        qDot3 -= beta * s2
        qDot4 -= beta * s3
    q0 += qDot1 * (1. / sampleFreq)
    q1 += qDot2 * (1. / sampleFreq)
    q2 += qDot3 * (1. / sampleFreq)
    q3 += qDot4 * (1. / sampleFreq)

    recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
    q0 *= recipNorm
    q1 *= recipNorm
    q2 *= recipNorm
    q3 *= recipNorm
    return q0,q1,q2,q3


def MadgwickAHRSupdateIMU( gx,  gy,  gz,  ax,  ay,  az) :


	qDot1 = 0.5 * (-q1 * gx - q2 * gy - q3 * gz)
	qDot2 = 0.5 * (q0 * gx + q2 * gz - q3 * gy)
	qDot3 = 0.5 * (q0 * gy - q1 * gz + q3 * gx)
	qDot4 = 0.5 * (q0 * gz + q1 * gy - q2 * gx)

	if(not((ax == 0.) and (ay == 0.) and (az == 0.))) :

		recipNorm = invSqrt(ax * ax + ay * ay + az * az)
		ax *= recipNorm
		ay *= recipNorm
		az *= recipNorm   

		_2q0 = 2. * q0
		_2q1 = 2. * q1
		_2q2 = 2. * q2
		_2q3 = 2. * q3
		_4q0 = 4. * q0
		_4q1 = 4. * q1
		_4q2 = 4. * q2
		_8q1 = 8. * q1
		_8q2 = 8. * q2
		q0q0 = q0 * q0
		q1q1 = q1 * q1
		q2q2 = q2 * q2
		q3q3 = q3 * q3

		s0 = _4q0 * q2q2 + _2q2 * ax + _4q0 * q1q1 - _2q1 * ay
		s1 = _4q1 * q3q3 - _2q3 * ax + 4. * q0q0 * q1 - _2q0 * ay - _4q1 + _8q1 * q1q1 + _8q1 * q2q2 + _4q1 * az
		s2 = 4. * q0q0 * q2 + _2q0 * ax + _4q2 * q3q3 - _2q3 * ay - _4q2 + _8q2 * q1q1 + _8q2 * q2q2 + _4q2 * az
		s3 = 4. * q1q1 * q3 - _2q1 * ax + 4. * q2q2 * q3 - _2q2 * ay
		recipNorm = invSqrt(s0 * s0 + s1 * s1 + s2 * s2 + s3 * s3) 
		s0 *= recipNorm
		s1 *= recipNorm
		s2 *= recipNorm
		s3 *= recipNorm

		qDot1 -= beta * s0
		qDot2 -= beta * s1
		qDot3 -= beta * s2
		qDot4 -= beta * s3
	

	q0 += qDot1 * (1. / sampleFreq)
	q1 += qDot2 * (1. / sampleFreq)
	q2 += qDot3 * (1. / sampleFreq)
	q3 += qDot4 * (1. / sampleFreq)

	recipNorm = invSqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3)
	q0 *= recipNorm
	q1 *= recipNorm
	q2 *= recipNorm
	q3 *= recipNorm
import math as m

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)
	
def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z
def quaternion_to_euler(w, x, y, z):
        t0 = 2 * (w * x + y * z)
        t1 = 1 - 2 * (x * x + y * y)
        X = m.atan2(t0, t1)
 
        t2 = 2 * (w * y - z * x)
        t2 = 1 if t2 > 1 else t2
        t2 = -1 if t2 < -1 else t2
        Y = m.asin(t2)
         
        t3 = 2 * (w * z + x * y)
        t4 = 1 - 2 * (y * y + z * z)
        Z = m.atan2(t3, t4)
 
        return X, Y, Z

	

# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')


# i=-1

# a_linear_x = []
# a_linear_y = []
# a_linear_z = []
# data_ = data['time'].reshape(1,6959)


# def update(angle):
#     global i
#     i= i+1
#     MadgwickAHRSupdate(data["Gyroscope"][i][0]* (pi/180), data["Gyroscope"][i][1]* (pi/180),data["Gyroscope"][i][2]* (pi/180), data['Accelerometer'][i][0],data['Accelerometer'][i][1],data['Accelerometer'][i][2], data['Magnetometer'][i][0],data['Magnetometer'][i][1],data['Magnetometer'][i][2])       

    
#     v2 = qv_mult([q0,q1,q2,q3],v1)
#     R = Rz(v2[2]) * Ry(v2[1]) * Rx(v2[0])
#     a_linear = R*g- g
#     # print(data['time'][i])
#     # v3 = qv_mult([q0,q1,q2,q3],v4)

#     ax.clear()        
#     # print(angle)

#     # ax.quiver(-1, 0, 0, 3, 0, 0, color='#aaaaaa',linestyle='dashed')
#     # ax.quiver(0, -1, 0, 0,3, 0, color='#aaaaaa',linestyle='dashed')
#     # ax.quiver(0, 0, -1, 0, 0, 3, color='#aaaaaa',linestyle='dashed')
#     # Vector before rotation
#     ax.quiver(0, 0, 0, 1, 0, 0, color='b')
#     # Vector after rotation
#     ax.quiver(0, 0, 0, v2[0], v2[1], v2[2], color='r')
#     # print(a_linear)
#     a_linear_x.append(a_linear[0][0])
#     a_linear_y.append(a_linear[1][0])
#     a_linear_z.append(a_linear[2][0])
    



#     # ax.quiver(0, 0, 0, v3[0], v3[1], v3[2], color='r')

#     ax.set_xlim([-1.5, 1.5])
#     ax.set_ylim([-1.5, 1.5])
#     ax.set_zlim([-1.5, 1.5])

# ani = animation.FuncAnimation(fig=fig, func=update, frames=10, interval=1)
# plt.show()

# g = np.matrix([0, 0, 1])
# g_ = (0,0,1)

# for i in range(6959):
#     MadgwickAHRSupdate(data["Gyroscope"][i][0]* (pi/180), data["Gyroscope"][i][1]* (pi/180),data["Gyroscope"][i][2]* (pi/180), data['Accelerometer'][i][0],data['Accelerometer'][i][1],data['Accelerometer'][i][2], data['Magnetometer'][i][0],data['Magnetometer'][i][1],data['Magnetometer'][i][2])       
#     # v1 = (0,data['Accelerometer'][i][0],data['Accelerometer'][i][1],data['Accelerometer'][i][2])
#     a = np.array([[data['Accelerometer'][i][0]],[data['Accelerometer'][i][1]],[data['Accelerometer'][i][2]]])
    
#     v3 = qv_mult([q0,-q1,-q2,-q3], g_)
    
#     a_linear =  a - np.array(v3).reshape(3,1)
    
#     a_linear_x.append(float(a_linear[0][0]))
#     a_linear_y.append(float(a_linear[1][0]))
#     a_linear_z.append(float(a_linear[2][0]))

    
# fig1, axs = plt.subplots(3, sharex=True, sharey=True)


# axs[0].plot(data_[0], a_linear_x)
# # print( a_linear[1][0])
# axs[1].plot(data_[0], a_linear_y)
# axs[2].plot(data_[0], a_linear_z)
# plt.show()