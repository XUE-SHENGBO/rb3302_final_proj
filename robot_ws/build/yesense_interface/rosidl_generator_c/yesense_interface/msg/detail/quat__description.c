// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/Quat.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/quat__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__Quat__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xdd, 0x13, 0xc8, 0x45, 0xe4, 0x86, 0xd1, 0x18,
      0x9b, 0x5c, 0x6a, 0x93, 0xa1, 0x6b, 0x29, 0x43,
      0x0f, 0x55, 0x99, 0xc8, 0x5e, 0x43, 0x45, 0x98,
      0x10, 0xe0, 0x88, 0x6a, 0x90, 0xf1, 0x85, 0xf0,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__Quat__TYPE_NAME[] = "yesense_interface/msg/Quat";

// Define type names, field names, and default values
static char yesense_interface__msg__Quat__FIELD_NAME__q0[] = "q0";
static char yesense_interface__msg__Quat__FIELD_NAME__q1[] = "q1";
static char yesense_interface__msg__Quat__FIELD_NAME__q2[] = "q2";
static char yesense_interface__msg__Quat__FIELD_NAME__q3[] = "q3";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__Quat__FIELDS[] = {
  {
    {yesense_interface__msg__Quat__FIELD_NAME__q0, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Quat__FIELD_NAME__q1, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Quat__FIELD_NAME__q2, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Quat__FIELD_NAME__q3, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__Quat__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
      {yesense_interface__msg__Quat__FIELDS, 4, 4},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float64 q0\n"
  "float64 q1\n"
  "float64 q2\n"
  "float64 q3";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__Quat__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 44, 44},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__Quat__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__Quat__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
