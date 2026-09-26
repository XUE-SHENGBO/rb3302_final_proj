// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/SampleTimestamp.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/sample_timestamp__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__SampleTimestamp__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x36, 0xe2, 0xa1, 0xb4, 0xa7, 0x4e, 0xbc, 0xe4,
      0xdd, 0x74, 0xad, 0x93, 0xa7, 0x3f, 0xe8, 0xb0,
      0x38, 0x2a, 0xf0, 0x2e, 0xfd, 0x4c, 0x0e, 0xae,
      0xa8, 0x9a, 0xdb, 0x80, 0xd3, 0x62, 0x07, 0xff,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__SampleTimestamp__TYPE_NAME[] = "yesense_interface/msg/SampleTimestamp";

// Define type names, field names, and default values
static char yesense_interface__msg__SampleTimestamp__FIELD_NAME__timestamp[] = "timestamp";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__SampleTimestamp__FIELDS[] = {
  {
    {yesense_interface__msg__SampleTimestamp__FIELD_NAME__timestamp, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__SampleTimestamp__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__SampleTimestamp__TYPE_NAME, 37, 37},
      {yesense_interface__msg__SampleTimestamp__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint32 \\ttimestamp\\t";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__SampleTimestamp__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__SampleTimestamp__TYPE_NAME, 37, 37},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 19, 19},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__SampleTimestamp__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__SampleTimestamp__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
