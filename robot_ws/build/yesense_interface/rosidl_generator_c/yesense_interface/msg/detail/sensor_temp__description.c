// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/SensorTemp.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/sensor_temp__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__SensorTemp__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x00, 0x8f, 0xd1, 0x7a, 0x7f, 0x2e, 0x91, 0xdd,
      0xf8, 0xe8, 0x6e, 0xcb, 0x5e, 0x0a, 0xd8, 0x31,
      0x51, 0x41, 0x86, 0xa6, 0x15, 0xce, 0xfd, 0x31,
      0x33, 0xda, 0xf9, 0xd3, 0x7a, 0xd7, 0x0f, 0x5b,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__SensorTemp__TYPE_NAME[] = "yesense_interface/msg/SensorTemp";

// Define type names, field names, and default values
static char yesense_interface__msg__SensorTemp__FIELD_NAME__temp[] = "temp";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__SensorTemp__FIELDS[] = {
  {
    {yesense_interface__msg__SensorTemp__FIELD_NAME__temp, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__SensorTemp__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__SensorTemp__TYPE_NAME, 32, 32},
      {yesense_interface__msg__SensorTemp__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 \\ttemp";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__SensorTemp__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__SensorTemp__TYPE_NAME, 32, 32},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 14, 14},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__SensorTemp__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__SensorTemp__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
