// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from yesense_interface:msg/NavAll.idl
// generated code does not contain a copyright notice
#include "yesense_interface/msg/detail/nav_all__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "yesense_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "yesense_interface/msg/detail/nav_all__struct.h"
#include "yesense_interface/msg/detail/nav_all__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "yesense_interface/msg/detail/euler_angle__functions.h"  // euler
#include "yesense_interface/msg/detail/gnss_pos__functions.h"  // pos
#include "yesense_interface/msg/detail/nav_status__functions.h"  // status
#include "yesense_interface/msg/detail/pressure__functions.h"  // pressure
#include "yesense_interface/msg/detail/quat__functions.h"  // quat
#include "yesense_interface/msg/detail/sensor_temp__functions.h"  // temp
#include "yesense_interface/msg/detail/three_axis__functions.h"  // acc, gyro
#include "yesense_interface/msg/detail/tid__functions.h"  // tid
#include "yesense_interface/msg/detail/utc__functions.h"  // utc
#include "yesense_interface/msg/detail/vel__functions.h"  // vel

// forward declare type support functions

bool cdr_serialize_yesense_interface__msg__EulerAngle(
  const yesense_interface__msg__EulerAngle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__EulerAngle(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__EulerAngle * ros_message);

size_t get_serialized_size_yesense_interface__msg__EulerAngle(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__EulerAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__EulerAngle(
  const yesense_interface__msg__EulerAngle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__EulerAngle(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__EulerAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, EulerAngle)();

bool cdr_serialize_yesense_interface__msg__GnssPos(
  const yesense_interface__msg__GnssPos * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__GnssPos(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__GnssPos * ros_message);

size_t get_serialized_size_yesense_interface__msg__GnssPos(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__GnssPos(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__GnssPos(
  const yesense_interface__msg__GnssPos * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__GnssPos(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__GnssPos(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, GnssPos)();

bool cdr_serialize_yesense_interface__msg__NavStatus(
  const yesense_interface__msg__NavStatus * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__NavStatus(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__NavStatus * ros_message);

size_t get_serialized_size_yesense_interface__msg__NavStatus(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__NavStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__NavStatus(
  const yesense_interface__msg__NavStatus * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__NavStatus(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__NavStatus(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, NavStatus)();

bool cdr_serialize_yesense_interface__msg__Pressure(
  const yesense_interface__msg__Pressure * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__Pressure(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__Pressure * ros_message);

size_t get_serialized_size_yesense_interface__msg__Pressure(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__Pressure(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__Pressure(
  const yesense_interface__msg__Pressure * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__Pressure(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__Pressure(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, Pressure)();

bool cdr_serialize_yesense_interface__msg__Quat(
  const yesense_interface__msg__Quat * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__Quat(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__Quat * ros_message);

size_t get_serialized_size_yesense_interface__msg__Quat(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__Quat(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__Quat(
  const yesense_interface__msg__Quat * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__Quat(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__Quat(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, Quat)();

bool cdr_serialize_yesense_interface__msg__SensorTemp(
  const yesense_interface__msg__SensorTemp * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__SensorTemp(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__SensorTemp * ros_message);

size_t get_serialized_size_yesense_interface__msg__SensorTemp(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__SensorTemp(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__SensorTemp(
  const yesense_interface__msg__SensorTemp * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__SensorTemp(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__SensorTemp(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, SensorTemp)();

bool cdr_serialize_yesense_interface__msg__ThreeAxis(
  const yesense_interface__msg__ThreeAxis * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__ThreeAxis(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__ThreeAxis * ros_message);

size_t get_serialized_size_yesense_interface__msg__ThreeAxis(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__ThreeAxis(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__ThreeAxis(
  const yesense_interface__msg__ThreeAxis * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__ThreeAxis(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__ThreeAxis(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, ThreeAxis)();

bool cdr_serialize_yesense_interface__msg__Tid(
  const yesense_interface__msg__Tid * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__Tid(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__Tid * ros_message);

size_t get_serialized_size_yesense_interface__msg__Tid(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__Tid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__Tid(
  const yesense_interface__msg__Tid * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__Tid(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__Tid(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, Tid)();

bool cdr_serialize_yesense_interface__msg__Utc(
  const yesense_interface__msg__Utc * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__Utc(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__Utc * ros_message);

size_t get_serialized_size_yesense_interface__msg__Utc(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__Utc(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__Utc(
  const yesense_interface__msg__Utc * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__Utc(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__Utc(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, Utc)();

bool cdr_serialize_yesense_interface__msg__Vel(
  const yesense_interface__msg__Vel * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__Vel(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__Vel * ros_message);

size_t get_serialized_size_yesense_interface__msg__Vel(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__Vel(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__Vel(
  const yesense_interface__msg__Vel * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__Vel(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__Vel(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, Vel)();


using _NavAll__ros_msg_type = yesense_interface__msg__NavAll;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_yesense_interface__msg__NavAll(
  const yesense_interface__msg__NavAll * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: tid
  {
    cdr_serialize_yesense_interface__msg__Tid(
      &ros_message->tid, cdr);
  }

  // Field name: acc
  {
    cdr_serialize_yesense_interface__msg__ThreeAxis(
      &ros_message->acc, cdr);
  }

  // Field name: gyro
  {
    cdr_serialize_yesense_interface__msg__ThreeAxis(
      &ros_message->gyro, cdr);
  }

  // Field name: euler
  {
    cdr_serialize_yesense_interface__msg__EulerAngle(
      &ros_message->euler, cdr);
  }

  // Field name: quat
  {
    cdr_serialize_yesense_interface__msg__Quat(
      &ros_message->quat, cdr);
  }

  // Field name: temp
  {
    cdr_serialize_yesense_interface__msg__SensorTemp(
      &ros_message->temp, cdr);
  }

  // Field name: pos
  {
    cdr_serialize_yesense_interface__msg__GnssPos(
      &ros_message->pos, cdr);
  }

  // Field name: status
  {
    cdr_serialize_yesense_interface__msg__NavStatus(
      &ros_message->status, cdr);
  }

  // Field name: vel
  {
    cdr_serialize_yesense_interface__msg__Vel(
      &ros_message->vel, cdr);
  }

  // Field name: utc
  {
    cdr_serialize_yesense_interface__msg__Utc(
      &ros_message->utc, cdr);
  }

  // Field name: pressure
  {
    cdr_serialize_yesense_interface__msg__Pressure(
      &ros_message->pressure, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_deserialize_yesense_interface__msg__NavAll(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__NavAll * ros_message)
{
  // Field name: tid
  {
    cdr_deserialize_yesense_interface__msg__Tid(cdr, &ros_message->tid);
  }

  // Field name: acc
  {
    cdr_deserialize_yesense_interface__msg__ThreeAxis(cdr, &ros_message->acc);
  }

  // Field name: gyro
  {
    cdr_deserialize_yesense_interface__msg__ThreeAxis(cdr, &ros_message->gyro);
  }

  // Field name: euler
  {
    cdr_deserialize_yesense_interface__msg__EulerAngle(cdr, &ros_message->euler);
  }

  // Field name: quat
  {
    cdr_deserialize_yesense_interface__msg__Quat(cdr, &ros_message->quat);
  }

  // Field name: temp
  {
    cdr_deserialize_yesense_interface__msg__SensorTemp(cdr, &ros_message->temp);
  }

  // Field name: pos
  {
    cdr_deserialize_yesense_interface__msg__GnssPos(cdr, &ros_message->pos);
  }

  // Field name: status
  {
    cdr_deserialize_yesense_interface__msg__NavStatus(cdr, &ros_message->status);
  }

  // Field name: vel
  {
    cdr_deserialize_yesense_interface__msg__Vel(cdr, &ros_message->vel);
  }

  // Field name: utc
  {
    cdr_deserialize_yesense_interface__msg__Utc(cdr, &ros_message->utc);
  }

  // Field name: pressure
  {
    cdr_deserialize_yesense_interface__msg__Pressure(cdr, &ros_message->pressure);
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_yesense_interface__msg__NavAll(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _NavAll__ros_msg_type * ros_message = static_cast<const _NavAll__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: tid
  current_alignment += get_serialized_size_yesense_interface__msg__Tid(
    &(ros_message->tid), current_alignment);

  // Field name: acc
  current_alignment += get_serialized_size_yesense_interface__msg__ThreeAxis(
    &(ros_message->acc), current_alignment);

  // Field name: gyro
  current_alignment += get_serialized_size_yesense_interface__msg__ThreeAxis(
    &(ros_message->gyro), current_alignment);

  // Field name: euler
  current_alignment += get_serialized_size_yesense_interface__msg__EulerAngle(
    &(ros_message->euler), current_alignment);

  // Field name: quat
  current_alignment += get_serialized_size_yesense_interface__msg__Quat(
    &(ros_message->quat), current_alignment);

  // Field name: temp
  current_alignment += get_serialized_size_yesense_interface__msg__SensorTemp(
    &(ros_message->temp), current_alignment);

  // Field name: pos
  current_alignment += get_serialized_size_yesense_interface__msg__GnssPos(
    &(ros_message->pos), current_alignment);

  // Field name: status
  current_alignment += get_serialized_size_yesense_interface__msg__NavStatus(
    &(ros_message->status), current_alignment);

  // Field name: vel
  current_alignment += get_serialized_size_yesense_interface__msg__Vel(
    &(ros_message->vel), current_alignment);

  // Field name: utc
  current_alignment += get_serialized_size_yesense_interface__msg__Utc(
    &(ros_message->utc), current_alignment);

  // Field name: pressure
  current_alignment += get_serialized_size_yesense_interface__msg__Pressure(
    &(ros_message->pressure), current_alignment);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_yesense_interface__msg__NavAll(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // Field name: tid
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__Tid(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: acc
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__ThreeAxis(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: gyro
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__ThreeAxis(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: euler
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__EulerAngle(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: quat
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__Quat(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: temp
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__SensorTemp(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: pos
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__GnssPos(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: status
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__NavStatus(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: vel
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__Vel(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: utc
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__Utc(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: pressure
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__Pressure(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = yesense_interface__msg__NavAll;
    is_plain =
      (
      offsetof(DataType, pressure) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_key_yesense_interface__msg__NavAll(
  const yesense_interface__msg__NavAll * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: tid
  {
    cdr_serialize_key_yesense_interface__msg__Tid(
      &ros_message->tid, cdr);
  }

  // Field name: acc
  {
    cdr_serialize_key_yesense_interface__msg__ThreeAxis(
      &ros_message->acc, cdr);
  }

  // Field name: gyro
  {
    cdr_serialize_key_yesense_interface__msg__ThreeAxis(
      &ros_message->gyro, cdr);
  }

  // Field name: euler
  {
    cdr_serialize_key_yesense_interface__msg__EulerAngle(
      &ros_message->euler, cdr);
  }

  // Field name: quat
  {
    cdr_serialize_key_yesense_interface__msg__Quat(
      &ros_message->quat, cdr);
  }

  // Field name: temp
  {
    cdr_serialize_key_yesense_interface__msg__SensorTemp(
      &ros_message->temp, cdr);
  }

  // Field name: pos
  {
    cdr_serialize_key_yesense_interface__msg__GnssPos(
      &ros_message->pos, cdr);
  }

  // Field name: status
  {
    cdr_serialize_key_yesense_interface__msg__NavStatus(
      &ros_message->status, cdr);
  }

  // Field name: vel
  {
    cdr_serialize_key_yesense_interface__msg__Vel(
      &ros_message->vel, cdr);
  }

  // Field name: utc
  {
    cdr_serialize_key_yesense_interface__msg__Utc(
      &ros_message->utc, cdr);
  }

  // Field name: pressure
  {
    cdr_serialize_key_yesense_interface__msg__Pressure(
      &ros_message->pressure, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_key_yesense_interface__msg__NavAll(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _NavAll__ros_msg_type * ros_message = static_cast<const _NavAll__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: tid
  current_alignment += get_serialized_size_key_yesense_interface__msg__Tid(
    &(ros_message->tid), current_alignment);

  // Field name: acc
  current_alignment += get_serialized_size_key_yesense_interface__msg__ThreeAxis(
    &(ros_message->acc), current_alignment);

  // Field name: gyro
  current_alignment += get_serialized_size_key_yesense_interface__msg__ThreeAxis(
    &(ros_message->gyro), current_alignment);

  // Field name: euler
  current_alignment += get_serialized_size_key_yesense_interface__msg__EulerAngle(
    &(ros_message->euler), current_alignment);

  // Field name: quat
  current_alignment += get_serialized_size_key_yesense_interface__msg__Quat(
    &(ros_message->quat), current_alignment);

  // Field name: temp
  current_alignment += get_serialized_size_key_yesense_interface__msg__SensorTemp(
    &(ros_message->temp), current_alignment);

  // Field name: pos
  current_alignment += get_serialized_size_key_yesense_interface__msg__GnssPos(
    &(ros_message->pos), current_alignment);

  // Field name: status
  current_alignment += get_serialized_size_key_yesense_interface__msg__NavStatus(
    &(ros_message->status), current_alignment);

  // Field name: vel
  current_alignment += get_serialized_size_key_yesense_interface__msg__Vel(
    &(ros_message->vel), current_alignment);

  // Field name: utc
  current_alignment += get_serialized_size_key_yesense_interface__msg__Utc(
    &(ros_message->utc), current_alignment);

  // Field name: pressure
  current_alignment += get_serialized_size_key_yesense_interface__msg__Pressure(
    &(ros_message->pressure), current_alignment);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_key_yesense_interface__msg__NavAll(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;
  // Field name: tid
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__Tid(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: acc
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__ThreeAxis(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: gyro
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__ThreeAxis(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: euler
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__EulerAngle(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: quat
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__Quat(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: temp
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__SensorTemp(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: pos
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__GnssPos(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: status
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__NavStatus(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: vel
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__Vel(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: utc
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__Utc(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  // Field name: pressure
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__Pressure(
        inner_full_bounded, inner_is_plain, current_alignment);
      last_member_size += inner_size;
      current_alignment += inner_size;
      full_bounded &= inner_full_bounded;
      is_plain &= inner_is_plain;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = yesense_interface__msg__NavAll;
    is_plain =
      (
      offsetof(DataType, pressure) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _NavAll__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const yesense_interface__msg__NavAll * ros_message = static_cast<const yesense_interface__msg__NavAll *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_yesense_interface__msg__NavAll(ros_message, cdr);
}

static bool _NavAll__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  yesense_interface__msg__NavAll * ros_message = static_cast<yesense_interface__msg__NavAll *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_yesense_interface__msg__NavAll(cdr, ros_message);
}

static uint32_t _NavAll__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_yesense_interface__msg__NavAll(
      untyped_ros_message, 0));
}

static size_t _NavAll__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_yesense_interface__msg__NavAll(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_NavAll = {
  "yesense_interface::msg",
  "NavAll",
  _NavAll__cdr_serialize,
  _NavAll__cdr_deserialize,
  _NavAll__get_serialized_size,
  _NavAll__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _NavAll__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_NavAll,
  get_message_typesupport_handle_function,
  &yesense_interface__msg__NavAll__get_type_hash,
  &yesense_interface__msg__NavAll__get_type_description,
  &yesense_interface__msg__NavAll__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, NavAll)() {
  return &_NavAll__type_support;
}

#if defined(__cplusplus)
}
#endif
