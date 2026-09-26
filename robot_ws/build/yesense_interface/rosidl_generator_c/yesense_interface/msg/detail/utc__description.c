// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/Utc.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/utc__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__Utc__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xa1, 0x81, 0xfc, 0x33, 0x61, 0x99, 0x32, 0x4a,
      0xa7, 0x64, 0x7a, 0x71, 0x91, 0xcc, 0x5b, 0x14,
      0x5b, 0xe6, 0x3c, 0xb0, 0x88, 0x2e, 0x07, 0x0c,
      0x02, 0x83, 0x47, 0x92, 0x8f, 0x7b, 0xad, 0x2c,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__Utc__TYPE_NAME[] = "yesense_interface/msg/Utc";

// Define type names, field names, and default values
static char yesense_interface__msg__Utc__FIELD_NAME__year[] = "year";
static char yesense_interface__msg__Utc__FIELD_NAME__month[] = "month";
static char yesense_interface__msg__Utc__FIELD_NAME__day[] = "day";
static char yesense_interface__msg__Utc__FIELD_NAME__hour[] = "hour";
static char yesense_interface__msg__Utc__FIELD_NAME__min[] = "min";
static char yesense_interface__msg__Utc__FIELD_NAME__sec[] = "sec";
static char yesense_interface__msg__Utc__FIELD_NAME__ms[] = "ms";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__Utc__FIELDS[] = {
  {
    {yesense_interface__msg__Utc__FIELD_NAME__year, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT16,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Utc__FIELD_NAME__month, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Utc__FIELD_NAME__day, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Utc__FIELD_NAME__hour, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Utc__FIELD_NAME__min, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Utc__FIELD_NAME__sec, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Utc__FIELD_NAME__ms, 2, 2},
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
yesense_interface__msg__Utc__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__Utc__TYPE_NAME, 25, 25},
      {yesense_interface__msg__Utc__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint16 \\tyear\n"
  "uint8 \\tmonth\n"
  "uint8 \\tday\n"
  "uint8 \\thour\n"
  "uint8 \\tmin\n"
  "uint8 \\tsec\n"
  "uint32 \\tms";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__Utc__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__Utc__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 82, 82},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__Utc__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__Utc__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
