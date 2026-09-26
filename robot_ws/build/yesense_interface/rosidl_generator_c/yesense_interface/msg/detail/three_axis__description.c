// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/ThreeAxis.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/three_axis__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__ThreeAxis__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x85, 0xef, 0x87, 0x51, 0xd8, 0x24, 0xa2, 0xbf,
      0xeb, 0xaf, 0x9a, 0x85, 0x7c, 0xb2, 0xb8, 0x47,
      0x82, 0x32, 0x3a, 0x9a, 0x5d, 0xf7, 0x77, 0x9c,
      0xb9, 0x33, 0x12, 0xa7, 0x3e, 0x54, 0xfd, 0xae,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__ThreeAxis__TYPE_NAME[] = "yesense_interface/msg/ThreeAxis";

// Define type names, field names, and default values
static char yesense_interface__msg__ThreeAxis__FIELD_NAME__x[] = "x";
static char yesense_interface__msg__ThreeAxis__FIELD_NAME__y[] = "y";
static char yesense_interface__msg__ThreeAxis__FIELD_NAME__z[] = "z";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__ThreeAxis__FIELDS[] = {
  {
    {yesense_interface__msg__ThreeAxis__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ThreeAxis__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ThreeAxis__FIELD_NAME__z, 1, 1},
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
yesense_interface__msg__ThreeAxis__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
      {yesense_interface__msg__ThreeAxis__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 x\n"
  "float32 y\n"
  "float32 z";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__ThreeAxis__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 30, 30},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__ThreeAxis__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__ThreeAxis__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
