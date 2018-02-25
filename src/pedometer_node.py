#! /usr/bin/env python                                              
import rospy, time, math, numpy                                         #import necessary libraries

from sensor_msgs.msg import Imu, MagneticField                          #import necessary message types and data structures                  
from geometry_msgs.msg import PointStamped
from collections import deque


gyr_z=0                                                                 #initiate global variables
imu_data=Imu()

def callback(data):                                                     #get IMU data from /imu_data topic
    global imu_data
    global gyr_z 
    global last_time
    imu_data=data
    gyr_z=float(data.angular_velocity.z)

def expavg_gyr_z(gyr_z,gyr_z_avg_last):                                 #use exponential average to smooth out gyr_z
    gyr_z_exp_avg=gyr_z*.1+gyr_z_avg_last*.9
    return gyr_z_exp_avg
   
def subscriber_publisher():
    global gyr_z                                                        #initialize local variables for publisher_subscriber
    global imu_data
    global duration_step
    queue=deque([0,0])                                                  #create queue for velocity data
    last_time=0.000                                                     #set up variable for time state machine
    lastup=False                                                        #set up variable for peak state machine
    gyr_z_avg_last=0                                                    #set up variable for gyr_z state machine
    step=0                                                              #initialize step count
    step_length=0.067056                                                #step_length=average step length of a person
    rospy.init_node('pedometer', anonymous=True)                        #initialize pedometer node
    pub=rospy.Publisher('steps_velocity',PointStamped, queue_size=1)    #initialize steps_velocity topic to publish to
    rospy.Subscriber("/imu_data", Imu, callback)                        #subscribe from /imu_data topic
    rate=rospy.Rate(30)                                                 #set rate to 30Hz
    msg=PointStamped()                                                  #define message type for steps_velocity
    start_time=time.time()                                              #initialize timer
    while not rospy.is_shutdown():
        current_time=str(imu_data.header.stamp)                         #get time from /imu_data topic
        if len(current_time)==19:
            current_time=current_time[7]+current_time[8]+current_time[9]+'.'+current_time[10:15]
            current_time=float(current_time)                            #turn parsed current_time into a float
            up=False                                                    #define current peak variable 
            current_gyr_z=expavg_gyr_z(gyr_z,gyr_z_avg_last)            #get exponential average of gyr_z
            if current_gyr_z>0.5:                                       #get in range of steps
                if current_gyr_z>gyr_z_avg_last:                      
                    up=True
                if lastup==False and up==True:                          #check for peak/step has occured
                    step+=1                                             #add to step count    
                    msg.header.stamp=rospy.Time.now()                   #get time of step
                    msg.point.x=step                                 
                    duration_step=current_time-last_time                #get duration of step
                    last_time=current_time                              #finish out time state machine
                    step_velocity=step_length/duration_step             #calculate instant velocity of single step
                    queue.append(step_velocity)                         #append instant velocity into queue
                    queue.popleft()                                     #eject last value from queue
                    start_time=time.time()
                    if step%2==0:                                       #check to see if 5 steps has occured
                        avg_velocity=numpy.cumsum(queue)                #find avg_velocity over 5 steps
                        q1=avg_velocity[0]
                        q2=avg_velocity[1]
                        avg_velocity=(q1+q2)/2
                        msg.point.y=avg_velocity                        #add avg_velocity to msg
            elapsed_time=time.time()-start_time                         #get time since last step
            if elapsed_time>2.000:                                      #if time since last step is less than 2, person is standing still
                step_flag=False
                step=0
                avg_velocity=0
                msg.point.x=step
                msg.point.y=avg_velocity                 
            pub.publish(msg)                                                                                                                       
            lastup=up
            gyr_z_avg_last=current_gyr_z                                #finish out gyroscope 
            rate.sleep()
            
           
if __name__=='__main__':
    subscriber_publisher()                                              #run pedometer node function
