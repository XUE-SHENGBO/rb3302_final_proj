// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from yesense_interface:msg/EulerOnly.idl
// generated code does not contain a copyright notice
#include "yesense_interface/msg/detail/euler_only__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <cstddef>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/serialization_helpers.hpp"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "yesense_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "yesense_interface/msg/detail/euler_only__struct.h"
#include "yesense_interface/msg/detail/euler_only__functions.h"
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
#include "yesense_interface/msg/detail/tid__functions.h"  // tid

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


using _EulerOnly__ros_msg_type = yesense_interface__msg__EulerOnly;


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_yesense_interface__msg__EulerOnly(
  const yesense_interface__msg__EulerOnly * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: tid
  {
    cdr_serialize_yesense_interface__msg__Tid(
      &ros_message->tid, cdr);
  }

  // Field name: euler
  {
    cdr_serialize_yesense_interface__msg__EulerAngle(
      &ros_message->euler, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_deserialize_yesense_interface__msg__EulerOnly(
  eprosima::fastcdr::Cdr & cdr,
  yesense_interface__msg__EulerOnly * ros_message)
{
  // Field name: tid
  {
    cdr_deserialize_yesense_interface__msg__Tid(cdr, &ros_message->tid);
  }

  // Field name: euler
  {
    cdr_deserialize_yesense_interface__msg__EulerAngle(cdr, &ros_message->euler);
  }

  return true;
}  // NOLINT(readability/fn_size)


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_yesense_interface__msg__EulerOnly(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _EulerOnly__ros_msg_type * ros_message = static_cast<const _EulerOnly__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: tid
  current_alignment += get_serialized_size_yesense_interface__msg__Tid(
    &(ros_message->tid), current_alignment);

  // Field name: euler
  current_alignment += get_serialized_size_yesense_interface__msg__EulerAngle(
    &(ros_message->euler), current_alignment);

  return current_alignment - initial_alignment;
}


ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_yesense_interface__msg__EulerOnly(
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


  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = yesense_interface__msg__EulerOnly;
    is_plain =
      (
      offsetof(DataType, euler) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
bool cdr_serialize_key_yesense_interface__msg__EulerOnly(
  const yesense_interface__msg__EulerOnly * ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Field name: tid
  {
    cdr_serialize_key_yesense_interface__msg__Tid(
      &ros_message->tid, cdr);
  }

  // Field name: euler
  {
    cdr_serialize_key_yesense_interface__msg__EulerAngle(
      &ros_message->euler, cdr);
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t get_serialized_size_key_yesense_interface__msg__EulerOnly(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _EulerOnly__ros_msg_type * ros_message = static_cast<const _EulerOnly__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;

  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Field name: tid
  current_alignment += get_serialized_size_key_yesense_interface__msg__Tid(
    &(ros_message->tid), current_alignment);

  // Field name: euler
  current_alignment += get_serialized_size_key_yesense_interface__msg__EulerAngle(
    &(ros_message->euler), current_alignment);

  return current_alignment - initial_alignment;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_yesense_interface
size_t max_serialized_size_key_yesense_interface__msg__EulerOnly(
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

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = yesense_interface__msg__EulerOnly;
    is_plain =
      (
      offsetof(DataType, euler) +
      last_member_size
      ) == ret_val;
  }
  return ret_val;
}


static bool _EulerOnly__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const yesense_interface__msg__EulerOnly * ros_message = static_cast<const yesense_interface__msg__EulerOnly *>(untyped_ros_message);
  (void)ros_message;
  return cdr_serialize_yesense_interface__msg__EulerOnly(ros_message, cdr);
}

static bool _EulerOnly__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  yesense_interface__msg__EulerOnly * ros_message = static_cast<yesense_interface__msg__EulerOnly *>(untyped_ros_message);
  (void)ros_message;
  return cdr_deserialize_yesense_interface__msg__EulerOnly(cdr, ros_message);
}

static uint32_t _EulerOnly__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_yesense_interface__msg__EulerOnly(
      untyped_ros_message, 0));
}

static size_t _EulerOnly__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_yesense_interface__msg__EulerOnly(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_EulerOnly = {
  "yesense_interface::msg",
  "EulerOnly",
  _EulerOnly__cdr_serialize,
  _EulerOnly__cdr_deserialize,
  _EulerOnly__get_serialized_size,
  _EulerOnly__max_serialized_size,
  nullptr
};

static rosidl_message_type_support_t _EulerOnly__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_EulerOnly,
  get_message_typesupport_handle_function,
  &yesense_interface__msg__EulerOnly__get_type_hash,
  &yesense_interface__msg__EulerOnly__get_type_description,
  &yesense_interface__msg__EulerOnly__get_type_description_sources,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, yesense_interface, msg, EulerOnly)() {
  return &_EulerOnly__type_support;
}

#if defined(__cplusplus)
}
#endif
