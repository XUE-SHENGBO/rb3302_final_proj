// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/Tid.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/tid__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__Tid__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xa1, 0xd0, 0x11, 0x88, 0xff, 0x8f, 0x50, 0x39,
      0x04, 0x69, 0xdb, 0xbf, 0x7b, 0x8e, 0xa1, 0xb7,
      0x29, 0xf0, 0x16, 0xf8, 0x00, 0x3d, 0x5d, 0x1a,
      0xe3, 0x62, 0x3d, 0xe3, 0x8c, 0xf9, 0x5f, 0x58,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";

// Define type names, field names, and default values
static char yesense_interface__msg__Tid__FIELD_NAME__tid[] = "tid";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__Tid__FIELDS[] = {
  {
    {yesense_interface__msg__Tid__FIELD_NAME__tid, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__Tid__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
      {yesense_interface__msg__Tid__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint16 \\ttid\\t";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__Tid__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 13, 13},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__Tid__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
