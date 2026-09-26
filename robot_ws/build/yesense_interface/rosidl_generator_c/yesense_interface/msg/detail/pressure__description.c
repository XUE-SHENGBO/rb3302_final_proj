// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/Pressure.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/pressure__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__Pressure__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x62, 0x94, 0x3f, 0x5a, 0x83, 0x15, 0x9d, 0x96,
      0x60, 0x86, 0x8b, 0xe7, 0x99, 0x3a, 0xa7, 0x90,
      0xa3, 0xfe, 0xd6, 0xd4, 0x08, 0xe6, 0xa2, 0xf6,
      0xe9, 0x17, 0x98, 0xba, 0xd3, 0x45, 0x8b, 0x6e,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__Pressure__TYPE_NAME[] = "yesense_interface/msg/Pressure";

// Define type names, field names, and default values
static char yesense_interface__msg__Pressure__FIELD_NAME__val[] = "val";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__Pressure__FIELDS[] = {
  {
    {yesense_interface__msg__Pressure__FIELD_NAME__val, 3, 3},
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
yesense_interface__msg__Pressure__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__Pressure__TYPE_NAME, 30, 30},
      {yesense_interface__msg__Pressure__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 val";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__Pressure__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__Pressure__TYPE_NAME, 30, 30},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 12, 12},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__Pressure__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__Pressure__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
