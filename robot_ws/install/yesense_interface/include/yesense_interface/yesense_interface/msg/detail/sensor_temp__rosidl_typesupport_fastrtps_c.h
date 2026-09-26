// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from yesense_interface:msg/SensorTemp.idl
// generated code does not contain a copyright notice
#ifndef YESENSE_INTERFACE__MSG__DETAIL__SENSOR_TEMP__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define YESENSE_INTERFACE__MSG__DETAIL__SENSOR_TEMP__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "yesense_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "yesense_interface/msg/detail/sensor_temp__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_yesense_interface__msg__SensorTemp(
  const yesense_interface__msg__SensorTemp * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_deserialize_yesense_interface__msg__SensorTemp(
  eprosima::fastcdr::Cdr &,
  yesense_interface__msg__SensorTemp * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_yesense_interface__msg__SensorTemp(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_yesense_interface__msg__SensorTemp(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_key_yesense_interface__msg__SensorTemp(
  const yesense_interface__msg__SensorTemp * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_key_yesense_interface__msg__SensorTemp(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_key_yesense_interface__msg__SensorTemp(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, SensorTemp)();

#ifdef __cplusplus
}
#endif

#endif  // YESENSE_INTERFACE__MSG__DETAIL__SENSOR_TEMP__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
