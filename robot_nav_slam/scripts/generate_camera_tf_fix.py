#!/usr/bin/env python3
import os
import re
import rospy
from sensor_msgs.msg import CameraInfo


def wait_camera_info(topic):
    rospy.loginfo("Waiting for %s ...", topic)
    msg = rospy.wait_for_message(topic, CameraInfo, timeout=10.0)

    frame_id = msg.header.frame_id.strip()
    if not frame_id:
        raise RuntimeError(topic + " has empty header.frame_id")

    rospy.loginfo("%s frame_id = %s", topic, frame_id)
    return frame_id


def safe_name(frame_id):
    return re.sub(r"[^A-Za-z0-9_]", "_", frame_id)


def main():
    rospy.init_node("generate_camera_tf_fix", anonymous=True)

    rgb_frame = wait_camera_info("/camera/rgb/camera_info")
    depth_frame = wait_camera_info("/camera/depth/camera_info")

    # 如果 RGB 和 Depth 的 frame_id 相同，只发布一次，避免 TF 重复冲突。
    frames = []
    for frame in [rgb_frame, depth_frame]:
        if frame not in frames:
            frames.append(frame)

    nodes = []
    for frame in frames:
        node_name = "base_to_" + safe_name(frame)

        # 这里直接连接 base_footprint 到实际 camera_info frame_id。
        # 使用 tf2_ros 发布 /tf_static，比旧 tf 更稳定。
        node = '''  <node pkg="tf2_ros"
        type="static_transform_publisher"
        name="%s"
        args="0.08 0.0 0.18 0 0 0 base_footprint %s" />''' % (
            node_name,
            frame,
        )

        nodes.append(node)

    launch_path = os.path.expanduser(
        "~/robot_nav_ws/src/robot_nav_slam/launch/camera_tf_fix.launch"
    )

    content = """<launch>
  <!-- Auto-generated TF fix for RTAB-Map RGB-D input. -->
  <!-- Generated from /camera/rgb/camera_info and /camera/depth/camera_info. -->
  <!-- RGB frame_id: %s -->
  <!-- Depth frame_id: %s -->
%s
</launch>
""" % (
        rgb_frame,
        depth_frame,
        "\n".join(nodes),
    )

    with open(launch_path, "w") as f:
        f.write(content)

    print("")
    print("Generated:", launch_path)
    print("RGB frame_id:", rgb_frame)
    print("Depth frame_id:", depth_frame)
    print("")
    print("Content:")
    print(content)


if __name__ == "__main__":
    main()
