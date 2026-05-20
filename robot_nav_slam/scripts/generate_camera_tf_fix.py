#!/usr/bin/env python3
import os
import rospy
from sensor_msgs.msg import CameraInfo


def wait_camera_info(topic):
    rospy.loginfo("Waiting for %s ...", topic)
    msg = rospy.wait_for_message(topic, CameraInfo, timeout=10.0)
    frame_id = msg.header.frame_id
    rospy.loginfo("%s frame_id = %s", topic, frame_id)
    return frame_id


def main():
    rospy.init_node("generate_camera_tf_fix", anonymous=True)

    rgb_frame = wait_camera_info("/camera/rgb/camera_info")
    depth_frame = wait_camera_info("/camera/depth/camera_info")

    launch_path = os.path.expanduser(
        "~/robot_nav_ws/src/robot_nav_slam/launch/camera_tf_fix.launch"
    )

    content = f'''<launch>
  <!-- Auto-generated TF fix for RTAB-Map RGB-D input -->

  <!-- RGB camera_info frame_id: {rgb_frame} -->
  <node pkg="tf"
        type="static_transform_publisher"
        name="base_to_rgb_camera_frame"
        args="0.08 0.0 0.18 0 0 0 base_footprint {rgb_frame} 100" />

  <!-- Depth camera_info frame_id: {depth_frame} -->
  <node pkg="tf"
        type="static_transform_publisher"
        name="base_to_depth_camera_frame"
        args="0.08 0.0 0.18 0 0 0 base_footprint {depth_frame} 100" />
</launch>
'''

    with open(launch_path, "w") as f:
        f.write(content)

    print("\nGenerated:", launch_path)
    print("RGB frame_id:", rgb_frame)
    print("Depth frame_id:", depth_frame)
    print("\nContent:\n")
    print(content)


if __name__ == "__main__":
    main()
