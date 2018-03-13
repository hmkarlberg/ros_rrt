#!/usr/bin/env python

import rospy
import baxter_interface

from baxter_interface import CHECK_VERSION

def run_velocity_loop():

    left = baxter_interface.Limb('left')
    right = baxter_interface.Limb('right')

    grip_left = baxter_interface.Gripper('left', CHECK_VERSION)
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)

    joints_left = left.joint_names()
    joints_right = right.joint_names()

    vel_right = {}
    vel_left = {}
    for curr_joint in joints_right:
        vel_right.update({curr_joint: 0})
    for curr_joint in joints_left:
        vel_left.update({curr_joint: 0})

    done = False
    r_side = True
    i = 0

    while not done and not rospy.is_shutdown():
        if r_side:
            limb = right
            joints = joints_right
            vel = vel_right
        else:
            limb = left
            joints = joints_left
            vel = vel_left
        for j in range(0, 7):
            vel[joints[j]] = 0.0
        vel[joints[i]] = 5.0

#        print("endpoint angular velocity: \n x:%f y:%f z:%f " %
#             (endpoint_vel['angular'][0], endpoint_vel['angular'][1], endpoint_vel['angular'][2]))
#        endpoint_pos = limb.endpoint_pose()
#        print("endpoint position: \n x:%f y:%f z:%f " %
#             (endpoint_pos['position'][0], endpoint_pos['position'][1], endpoint_pos['position'][2]))

        for k in range(0,50):
            print("setting joint %s" % (joints[i]) )
            endpoint_vel = limb.endpoint_velocity()
            limb.set_joint_velocities(vel)
            rospy.sleep(0.1)

        i += 1

        if i == 7:
            i = 0
            r_side = not r_side

        rospy.sleep(0.1)

def run_path_loop():


def main():

    rospy.init_node("rsdk_test")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled

    def clean_shutdown():
        if not init_state:
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    rs.enable()

    print('1. velocity \n 2. path')
    c = raw_input()
    if c == 1:
        run_velocity_loop()
    else if c == 2:
        run_path_loop()

if __name__ == '__main__':
    main()
