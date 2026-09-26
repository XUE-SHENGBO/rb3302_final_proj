// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/EulerAngle.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/euler_angle__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__EulerAngle__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x48, 0x24, 0x92, 0x57, 0x50, 0xf9, 0x63, 0x6e,
      0x0b, 0xe3, 0x7d, 0x8d, 0xf3, 0xa7, 0x3c, 0xda,
      0xf8, 0x62, 0xa3, 0x77, 0xb2, 0xc4, 0x5d, 0xb5,
      0x2b, 0x29, 0xa6, 0x81, 0x52, 0x8d, 0xb3, 0x8a,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__EulerAngle__TYPE_NAME[] = "yesense_interface/msg/EulerAngle";

// Define type names, field names, and default values
static char yesense_interface__msg__EulerAngle__FIELD_NAME__pitch[] = "pitch";
static char yesense_interface__msg__EulerAngle__FIELD_NAME__roll[] = "roll";
static char yesense_interface__msg__EulerAngle__FIELD_NAME__yaw[] = "yaw";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__EulerAngle__FIELDS[] = {
  {
    {yesense_interface__msg__EulerAngle__FIELD_NAME__pitch, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__EulerAngle__FIELD_NAME__roll, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__EulerAngle__FIELD_NAME__yaw, 3, 3},
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
yesense_interface__msg__EulerAngle__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
      {yesense_interface__msg__EulerAngle__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 pitch\n"
  "float32 roll\n"
  "float32 yaw";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__EulerAngle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 39, 39},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__EulerAngle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__EulerAngle__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
