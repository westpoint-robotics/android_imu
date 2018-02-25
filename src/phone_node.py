#!/usr/bin/python2
import socket, traceback, rospy                                                                     #initiate necessary libraries

from sensor_msgs.msg import Imu, MagneticField                                                      #define message data types
msg1=Imu()
msg2=MagneticField()

def message_parser(raw_msg):                                                                        #define message parser function
    message_len=len(raw_msg)    
    if message_len==17:                                                                             #check to see if sensor is sending full message
        msg1.header.stamp=rospy.Time.now()                                                          #append time stamp to data collected
        msg1.header.frame_id="phone"
        msg2.header.frame_id="phone"
        msg2.header.stamp=rospy.Time.now()
        msg1.orientation.x=float(raw_msg[14])/57.29                                                 #get orientation from in radians
        msg1.orientation.y=float(raw_msg[15])/57.29
        msg1.orientation.z=float(raw_msg[16])/57.29
        msg1.linear_acceleration.x=float(raw_msg[2])                                                #get acceleration
        msg1.linear_acceleration.y=float(raw_msg[3])
        msg1.linear_acceleration.z=float(raw_msg[4])
        msg1.angular_velocity.x=float(raw_msg[6])                                                   #get gyroscope readings
        msg1.angular_velocity.y=float(raw_msg[7])
        msg1.angular_velocity.z=float(raw_msg[8])
        msg2.magnetic_field.x=float(raw_msg[10])*1000000                                            #get magnetometer in teslas
        msg2.magnetic_field.y=float(raw_msg[11])*1000000
        msg2.magnetic_field.z=float(raw_msg[12])*1000000
       


if __name__ == '__main__':
    pub1=rospy.Publisher('imu_data', Imu, queue_size=1)                                             #initialize data topics to pubish to
    pub2=rospy.Publisher('mag_data', MagneticField, queue_size=1)
    rospy.init_node('phone',anonymous=True)                                                         #initilaize phone node
    rate=rospy.Rate(10)
    host=''
    port=5555                                                                                       #set up socket to receive phone data
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))
    while not rospy.is_shutdown():
        message, address = s.recvfrom(8192)                                                         #receive phone data
        var_list=message.split(',')
        message_parser(var_list)
        pub1.publish(msg1)                                                                          #publish information to two topics
        pub2.publish(msg2)
            

