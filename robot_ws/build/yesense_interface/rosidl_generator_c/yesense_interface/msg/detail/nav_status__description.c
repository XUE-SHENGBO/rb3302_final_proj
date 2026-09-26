// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/NavStatus.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/nav_status__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__NavStatus__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb0, 0x8e, 0x05, 0x5a, 0x7f, 0xfe, 0x7e, 0xcd,
      0xe9, 0x17, 0x23, 0xec, 0x3a, 0x3b, 0x13, 0xeb,
      0x89, 0x16, 0x87, 0x3b, 0xf0, 0xbf, 0x52, 0xd1,
      0x05, 0x33, 0x39, 0x82, 0xfd, 0x5c, 0x1f, 0x26,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__NavStatus__TYPE_NAME[] = "yesense_interface/msg/NavStatus";

// Define type names, field names, and default values
static char yesense_interface__msg__NavStatus__FIELD_NAME__fusion_status[] = "fusion_status";
static char yesense_interface__msg__NavStatus__FIELD_NAME__gnss_status[] = "gnss_status";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__NavStatus__FIELDS[] = {
  {
    {yesense_interface__msg__NavStatus__FIELD_NAME__fusion_status, 13, 13},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavStatus__FIELD_NAME__gnss_status, 11, 11},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__NavStatus__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__NavStatus__TYPE_NAME, 31, 31},
      {yesense_interface__msg__NavStatus__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "uint8 \\tfusion_status\n"
  "uint8\\tgnss_status\\t\\t\\t";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__NavStatus__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__NavStatus__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 42, 42},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__NavStatus__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__NavStatus__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
