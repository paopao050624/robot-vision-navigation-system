#!/usr/bin/env python3
import math
import rospy
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState


def main():
    rospy.init_node("moving_obstacle_node")

    rospy.wait_for_service("/gazebo/set_model_state")
    set_state = rospy.ServiceProxy("/gazebo/set_model_state", SetModelState)

    rate = rospy.Rate(20)
    start_time = rospy.Time.now().to_sec()

    while not rospy.is_shutdown():
        t = rospy.Time.now().to_sec() - start_time

        state = ModelState()
        state.model_name = "dynamic_box"

        # Dynamic obstacle moving laterally in front of robot
        state.pose.position.x = 1.5
        state.pose.position.y = 1.0 * math.sin(0.5 * t)
        state.pose.position.z = 0.3

        state.pose.orientation.x = 0.0
        state.pose.orientation.y = 0.0
        state.pose.orientation.z = 0.0
        state.pose.orientation.w = 1.0

        state.twist.linear.x = 0.0
        state.twist.linear.y = 0.5 * math.cos(0.5 * t)
        state.twist.linear.z = 0.0

        state.reference_frame = "world"

        try:
            set_state(state)
        except rospy.ServiceException as e:
            rospy.logwarn("Failed to move dynamic obstacle: %s", e)

        rate.sleep()


if __name__ == "__main__":
    main()
