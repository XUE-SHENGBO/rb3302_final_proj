// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/Vel.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/vel__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__Vel__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x5b, 0x99, 0xe2, 0xeb, 0x7d, 0xe8, 0xdd, 0xb9,
      0xb6, 0x94, 0xd8, 0x58, 0x5c, 0xa3, 0x3a, 0xe4,
      0xbf, 0x39, 0xff, 0x62, 0xfd, 0x61, 0xd2, 0xdc,
      0x52, 0x74, 0xab, 0xdb, 0x0c, 0xf0, 0xde, 0xe8,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char yesense_interface__msg__Vel__TYPE_NAME[] = "yesense_interface/msg/Vel";

// Define type names, field names, and default values
static char yesense_interface__msg__Vel__FIELD_NAME__vel_e[] = "vel_e";
static char yesense_interface__msg__Vel__FIELD_NAME__vel_n[] = "vel_n";
static char yesense_interface__msg__Vel__FIELD_NAME__vel_u[] = "vel_u";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__Vel__FIELDS[] = {
  {
    {yesense_interface__msg__Vel__FIELD_NAME__vel_e, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Vel__FIELD_NAME__vel_n, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Vel__FIELD_NAME__vel_u, 5, 5},
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
yesense_interface__msg__Vel__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__Vel__TYPE_NAME, 25, 25},
      {yesense_interface__msg__Vel__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "float32 vel_e\n"
  "float32 vel_n\n"
  "float32 vel_u";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__Vel__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__Vel__TYPE_NAME, 25, 25},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 42, 42},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__Vel__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__Vel__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
