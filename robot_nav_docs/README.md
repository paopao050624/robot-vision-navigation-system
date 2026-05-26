# Robot Vision & Navigation System

## 1. Project Overview

本项目实现一个基于 ROS1 Noetic、Gazebo、TurtleBot3、Gmapping、AMCL、MoveBase 和 RTAB-Map 的机器人视觉感知与自主导航系统。

系统目标是完成如下闭环：

```text
环境感知 → 地图构建 → 定位 → 路径规划 → 自主导航 → 反馈
