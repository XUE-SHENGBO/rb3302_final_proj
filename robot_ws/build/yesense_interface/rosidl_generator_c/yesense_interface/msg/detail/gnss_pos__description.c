// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/GnssPos.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/gnss_pos__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__GnssPos__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xc6, 0x85, 0xb6, 0x95, 0xfe, 0x24, 0xb8, 0x56,
      0x40, 0x27, 0xb0, 0x55, 0xdb, 0xd5, 0x3c, 0xfc,
      0x85, 0x60, 0x8b, 0x64, 0x47, 0xd4, 0xc5, 0x93,
      0x3e, 0x8c, 0xed, 0x50, 0x1c, 0xa6, 0x08, 0xb6,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__GnssPos__TYPE_NAME[] = "yesense_interface/msg/GnssPos";

// Define type names, field names, and default values
static char yesense_interface__msg__GnssPos__FIELD_NAME__longitude[] = "longitude";
static char yesense_interface__msg__GnssPos__FIELD_NAME__latitude[] = "latitude";
static char yesense_interface__msg__GnssPos__FIELD_NAME__altitude[] = "altitude";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__GnssPos__FIELDS[] = {
  {
    {yesense_interface__msg__GnssPos__FIELD_NAME__longitude, 9, 9},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__GnssPos__FIELD_NAME__latitude, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__GnssPos__FIELD_NAME__altitude, 8, 8},
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
yesense_interface__msg__GnssPos__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__GnssPos__TYPE_NAME, 29, 29},
      {yesense_interface__msg__GnssPos__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float64 longitude\n"
  "float64 latitude\n"
  "float32 altitude";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__GnssPos__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__GnssPos__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 52, 52},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__GnssPos__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__GnssPos__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
