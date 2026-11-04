// Exercise the installed Nav2 BT plugins against synthetic services/actions only.
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <thread>
#include <vector>
#include "nav2_behavior_tree/behavior_tree_engine.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "nav2_msgs/action/compute_path_to_pose.hpp"
#include "nav2_msgs/action/follow_path.hpp"
#include "nav2_msgs/action/wait.hpp"
#include "nav2_msgs/srv/clear_entire_costmap.hpp"

using Plan = nav2_msgs::action::ComputePathToPose;
using Follow = nav2_msgs::action::FollowPath;
using Wait = nav2_msgs::action::Wait;
using Clear = nav2_msgs::srv::ClearEntireCostmap;
using namespace std::chrono_literals;

void require(bool ok, const std::string & message) {
  if (!ok) {throw std::runtime_error(message);}
}

template<class T, class F>
auto server(rclcpp::Node::SharedPtr node, const std::string & name, F execute) {
  return rclcpp_action::create_server<T>(node, name,
    [](const rclcpp_action::GoalUUID &, std::shared_ptr<const typename T::Goal>) {
      return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    },
    [](std::shared_ptr<rclcpp_action::ServerGoalHandle<T>>) {
      return rclcpp_action::CancelResponse::ACCEPT;
    }, execute);
}

int main(int argc, char ** argv) {
  require(argc == 2, "usage: check path/to/navigate_refresh_local.xml");
  require(std::string(std::getenv("ROS_DOMAIN_ID") ? std::getenv("ROS_DOMAIN_ID") : "") == "217",
    "test must run on isolated domain 217");
  require(std::string(std::getenv("ROS_AUTOMATIC_DISCOVERY_RANGE") ?
    std::getenv("ROS_AUTOMATIC_DISCOVERY_RANGE") : "") == "LOCALHOST",
    "test must use localhost discovery");
  rclcpp::init(argc, argv);
  auto fake = std::make_shared<rclcpp::Node>("synthetic_navigation");
  auto node = std::make_shared<rclcpp::Node>("recovery_bt_test");
  int mode = 0, plans = 0, follows = 0, global_clears = 0, local_clears = 0, waits = 0;
  std::vector<std::string> events;
  auto planner = server<Plan>(fake, "compute_path_to_pose", [&](auto handle) {
    ++plans; events.push_back("plan");
    auto result = std::make_shared<Plan::Result>();
    if ((mode == 0 && plans == 1) || mode == 1 || mode == 2) {
      result->error_code = mode == 2 ? Plan::Result::INVALID_PLANNER : Plan::Result::NO_VALID_PATH;
      handle->abort(result);
    } else {
      result->path.header.frame_id = "map";
      geometry_msgs::msg::PoseStamped pose;
      pose.header.frame_id = "map"; pose.pose.orientation.w = 1.;
      result->path.poses.push_back(pose);
      handle->succeed(result);
    }
  });
  auto controller = server<Follow>(fake, "follow_path", [&](auto handle) {
    ++follows; events.push_back("follow");
    auto result = std::make_shared<Follow::Result>();
    if (mode == 3 && follows == 1) {
      result->error_code = Follow::Result::NO_VALID_CONTROL;
      handle->abort(result);
    } else {handle->succeed(result);}
  });
  auto waiter = server<Wait>(fake, "wait", [&](auto handle) {
    ++waits; events.push_back("wait");
    const auto duration = rclcpp::Duration(handle->get_goal()->time);
    require(duration.seconds() >= 1., "recovery must wait at least one second");
    std::this_thread::sleep_for(std::chrono::nanoseconds(duration.nanoseconds()));
    handle->succeed(std::make_shared<Wait::Result>());
  });
  auto global = fake->create_service<Clear>("global_costmap/clear_entirely_global_costmap",
    [&](std::shared_ptr<Clear::Request>, std::shared_ptr<Clear::Response>) {
      ++global_clears; events.push_back("global_clear");
    });
  auto local = fake->create_service<Clear>("local_costmap/clear_entirely_local_costmap",
    [&](std::shared_ptr<Clear::Request>, std::shared_ptr<Clear::Response>) {
      ++local_clears; events.push_back("local_clear");
    });
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(fake);
  std::thread thread([&]() {executor.spin();});
  int status = 0;
  try {
    nav2_behavior_tree::BehaviorTreeEngine engine({
      "nav2_compute_path_to_pose_action_bt_node", "nav2_follow_path_action_bt_node",
      "nav2_wait_action_bt_node", "nav2_clear_costmap_service_bt_node",
      "nav2_would_a_planner_recovery_help_condition_bt_node",
      "nav2_would_a_controller_recovery_help_condition_bt_node",
      "nav2_rate_controller_bt_node", "nav2_pipeline_sequence_bt_node",
      "nav2_recovery_node_bt_node"}, node);
    for (mode = 0; mode < 4; ++mode) {
      plans = follows = global_clears = local_clears = waits = 0; events.clear();
      auto blackboard = BT::Blackboard::create(); blackboard->set("node", node);
      for (auto key : {"server_timeout", "cancel_timeout", "wait_for_service_timeout"}) {
        blackboard->set(key, 3000ms);
      }
      blackboard->set("bt_loop_duration", 10ms);
      blackboard->set("number_recoveries", 0);
      geometry_msgs::msg::PoseStamped goal;
      goal.header.frame_id = "map"; goal.pose.orientation.w = 1.;
      blackboard->set("goal", goal);
      auto tree = engine.createTreeFromFile(argv[1], blackboard);
      auto start = std::chrono::steady_clock::now();
      auto result = engine.run(&tree, []() {}, [&]() {
        return std::chrono::steady_clock::now() - start > 12s;
      });
      if (mode == 0) {
        require(result == nav2_behavior_tree::BtStatus::SUCCEEDED, "208 did not recover");
        require(plans == 2 && global_clears == 1 && waits == 1 && local_clears == 0,
          "wrong planner recovery counts");
        require(events == std::vector<std::string>{"plan", "global_clear", "wait", "plan", "follow"},
          "planning recovery order incorrect");
      } else if (mode == 1) {
        require(result == nav2_behavior_tree::BtStatus::FAILED && plans == 3 &&
          global_clears == 2 && waits == 2 && follows == 0 && local_clears == 0,
          "persistent obstacle must stop after bounded planning retries");
      } else if (mode == 2) {
        require(result == nav2_behavior_tree::BtStatus::FAILED && plans == 1 &&
          global_clears == 0 && local_clears == 0 && waits == 0,
          "invalid planner must not clear maps");
      } else {
        require(result == nav2_behavior_tree::BtStatus::SUCCEEDED && follows == 2 &&
          global_clears == 0 && local_clears == 1 && waits == 1,
          "controller/local recovery regressed");
      }
      engine.haltAllActions(tree);
      std::cout << "PASS mode=" << mode << " plans=" << plans << " global=" << global_clears
                << " local=" << local_clears << " waits=" << waits << " follows=" << follows << '\n';
    }
  } catch (const std::exception & error) {std::cerr << error.what() << '\n'; status = 1;}
  executor.cancel(); thread.join(); rclcpp::shutdown();
  return status;
}
