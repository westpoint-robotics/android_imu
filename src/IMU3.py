#!/usr/bin/python2
import socket, traceback

host = ''
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
while 1:
    try:
        message, address = s.recvfrom(8192)
        var_list=message.split(',')
        message_len=len(var_list)
        if message_len==17:
            acc_x=var_list[2]
            acc_y=var_list[3]
            acc_z=var_list[4]
            gyr_x=var_list[6]
            gyr_y=var_list[7]
            gyr_z=var_list[8]
            mag_x=var_list[10]
            mag_y=var_list[11]
            mag_z=var_list[12]
            ori_x=var_list[14]
            ori_y=var_list[15]
            ori_z=var_list[16]
            num_acc_x=float(acc_x)
            num_acc_y=float(acc_y)
            num_acc_z=float(acc_z)
            num_gyr_x=float(gyr_x)
            num_gyr_y=float(gyr_y)
            num_gyr_z=float(gyr_z)
            num_mag_x=float(mag_x)
            num_mag_y=float(mag_y)
            num_mag_z=float(mag_z)
            num_ori_x=float(ori_x)
            num_ori_y=float(ori_y)
            num_ori_z=float(ori_z)
            print 'ax=%s.,ay=%s.,az=%s.,gx=%s.,gy=%s.,gz=%s.,mx=%s.,my=%s.,mz=%s.,ox=%s.,oy=%s.,oz=%s.' %(acc_x,acc_y,acc_z,gyr_x,gyr_y,gyr_z,mag_x,mag_y,mag_z,ori_x,ori_y,ori_z)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        traceback.print_exc()
