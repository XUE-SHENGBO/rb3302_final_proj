// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from yesense_interface:msg/ImuData.idl
// generated code does not contain a copyright notice
#include "yesense_interface/msg/detail/imu_data__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "yesense_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "yesense_interface/msg/detail/imu_data__struct.h"
#include "yesense_interface/msg/detail/imu_data__functions.h"
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

#include "yesense_interface/msg/detail/sample_timestamp__functions.h"  // sample_timestamp
#include "yesense_interface/msg/detail/sensor_temp__functions.h"  // temp
#include "yesense_interface/msg/detail/three_axis__functions.h"  // acc, gyro
#include "yesense_interface/msg/detail/tid__functions.h"  // tid

// forward declare type support functions

bool cdr_serialize_yesense_interface__msg__SampleTimestamp(
  const yesense_interface__msg__SampleTimestamp * ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool cdr_deserialize_yesense_interface__msg__SampleTimestamp(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__SampleTimestamp * ros_message);

size_t get_serialized_size_yesense_interface__msg__SampleTimestamp(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_yesense_interface__msg__SampleTimestamp(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

bool cdr_serialize_key_yesense_interface__msg__SampleTimestamp(
  const yesense_interface__msg__SampleTimestamp * ros_message,
  eprosima::fastcdr::Cdr & cdr);

size_t get_serialized_size_key_yesense_interface__msg__SampleTimestamp(
  const void * untyped_ros_message,
  size_t current_alignment);

size_t max_serialized_size_key_yesense_interface__msg__SampleTimestamp(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, SampleTimestamp)();

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


using _ImuData__ros_msg_type = yesense_interface__msg__ImuData;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_yesense_interface__msg__ImuData(
  const yesense_interface__msg__ImuData * ros_message,
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

  // Field name: temp
  {
    cdr_serialize_yesense_interface__msg__SensorTemp(
      &ros_message->temp, cdr);
  }

  // Field name: sample_timestamp
  {
    cdr_serialize_yesense_interface__msg__SampleTimestamp(
      &ros_message->sample_timestamp, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_deserialize_yesense_interface__msg__ImuData(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__ImuData * ros_message)
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

  // Field name: temp
  {
    cdr_deserialize_yesense_interface__msg__SensorTemp(cdr, &ros_message->temp);
  }

  // Field name: sample_timestamp
  {
    cdr_deserialize_yesense_interface__msg__SampleTimestamp(cdr, &ros_message->sample_timestamp);
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_yesense_interface__msg__ImuData(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ImuData__ros_msg_type * ros_message = static_cast<const _ImuData__ros_msg_type *>(untyped_ros_message);
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

  // Field name: temp
  current_alignment += get_serialized_size_yesense_interface__msg__SensorTemp(
    &(ros_message->temp), current_alignment);

  // Field name: sample_timestamp
  current_alignment += get_serialized_size_yesense_interface__msg__SampleTimestamp(
    &(ros_message->sample_timestamp), current_alignment);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_yesense_interface__msg__ImuData(
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

  // Field name: sample_timestamp
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_yesense_interface__msg__SampleTimestamp(
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
    using DataType = yesense_interface__msg__ImuData;
    is_plain =
      (
      offsetof(DataType, sample_timestamp) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_key_yesense_interface__msg__ImuData(
  const yesense_interface__msg__ImuData * ros_message,
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

  // Field name: temp
  {
    cdr_serialize_key_yesense_interface__msg__SensorTemp(
      &ros_message->temp, cdr);
  }

  // Field name: sample_timestamp
  {
    cdr_serialize_key_yesense_interface__msg__SampleTimestamp(
      &ros_message->sample_timestamp, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_key_yesense_interface__msg__ImuData(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ImuData__ros_msg_type * ros_message = static_cast<const _ImuData__ros_msg_type *>(untyped_ros_message);
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

  // Field name: temp
  current_alignment += get_serialized_size_key_yesense_interface__msg__SensorTemp(
    &(ros_message->temp), current_alignment);

  // Field name: sample_timestamp
  current_alignment += get_serialized_size_key_yesense_interface__msg__SampleTimestamp(
    &(ros_message->sample_timestamp), current_alignment);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_key_yesense_interface__msg__ImuData(
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

  // Field name: sample_timestamp
  {
    size_t array_size = 1;
    last_member_size = 0;
    for (size_t index = 0; index < array_size; ++index) {
      bool inner_full_bounded;
      bool inner_is_plain;
      size_t inner_size;
      inner_size =
        max_serialized_size_key_yesense_interface__msg__SampleTimestamp(
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
    using DataType = yesense_interface__msg__ImuData;
    is_plain =
      (
      offsetof(DataType, sample_timestamp) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _ImuData__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const yesense_interface__msg__ImuData * ros_message = static_cast<const yesense_interface__msg__ImuData *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_yesense_interface__msg__ImuData(ros_message, cdr);
}

static bool _ImuData__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  yesense_interface__msg__ImuData * ros_message = static_cast<yesense_interface__msg__ImuData *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_yesense_interface__msg__ImuData(cdr, ros_message);
}

static uint32_t _ImuData__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_yesense_interface__msg__ImuData(
      untyped_ros_message, 0));
}

static size_t _ImuData__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_yesense_interface__msg__ImuData(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ImuData = {
  "yesense_interface::msg",
  "ImuData",
  _ImuData__cdr_serialize,
  _ImuData__cdr_deserialize,
  _ImuData__get_serialized_size,
  _ImuData__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _ImuData__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ImuData,
  get_message_typesupport_handle_function,
  &yesense_interface__msg__ImuData__get_type_hash,
  &yesense_interface__msg__ImuData__get_type_description,
  &yesense_interface__msg__ImuData__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, ImuData)() {
  return &_ImuData__type_support;
}

#if defined(__cplusplus)
}
#endif
