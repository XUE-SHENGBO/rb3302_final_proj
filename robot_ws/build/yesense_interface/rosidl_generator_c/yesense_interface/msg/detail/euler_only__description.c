// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/EulerOnly.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/euler_only__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__EulerOnly__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xa9, 0xd6, 0xf7, 0x6e, 0x8b, 0x8f, 0x58, 0x8b,
      0x60, 0xc5, 0x02, 0x88, 0xd4, 0xcf, 0x47, 0x29,
      0x9f, 0x65, 0x0a, 0xc8, 0x2d, 0x66, 0x5c, 0xf2,
      0xc7, 0x25, 0x85, 0xec, 0x2b, 0x67, 0xe4, 0x30,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "yesense_interface/msg/detail/tid__functions.h"
#include "yesense_interface/msg/detail/euler_angle__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t yesense_interface__msg__EulerAngle__EXPECTED_HASH = {1, {
    0x48, 0x24, 0x92, 0x57, 0x50, 0xf9, 0x63, 0x6e,
    0x0b, 0xe3, 0x7d, 0x8d, 0xf3, 0xa7, 0x3c, 0xda,
    0xf8, 0x62, 0xa3, 0x77, 0xb2, 0xc4, 0x5d, 0xb5,
    0x2b, 0x29, 0xa6, 0x81, 0x52, 0x8d, 0xb3, 0x8a,
  }};
static const rosidl_type_hash_t yesense_interface__msg__Tid__EXPECTED_HASH = {1, {
    0xa1, 0xd0, 0x11, 0x88, 0xff, 0x8f, 0x50, 0x39,
    0x04, 0x69, 0xdb, 0xbf, 0x7b, 0x8e, 0xa1, 0xb7,
    0x29, 0xf0, 0x16, 0xf8, 0x00, 0x3d, 0x5d, 0x1a,
    0xe3, 0x62, 0x3d, 0xe3, 0x8c, 0xf9, 0x5f, 0x58,
  }};
#endif

static char yesense_interface__msg__EulerOnly__TYPE_NAME[] = "yesense_interface/msg/EulerOnly";
static char yesense_interface__msg__EulerAngle__TYPE_NAME[] = "yesense_interface/msg/EulerAngle";
static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";

// Define type names, field names, and default values
static char yesense_interface__msg__EulerOnly__FIELD_NAME__tid[] = "tid";
static char yesense_interface__msg__EulerOnly__FIELD_NAME__euler[] = "euler";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__EulerOnly__FIELDS[] = {
  {
    {yesense_interface__msg__EulerOnly__FIELD_NAME__tid, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__EulerOnly__FIELD_NAME__euler, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription yesense_interface__msg__EulerOnly__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__EulerOnly__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__EulerOnly__TYPE_NAME, 31, 31},
      {yesense_interface__msg__EulerOnly__FIELDS, 2, 2},
    },
    {yesense_interface__msg__EulerOnly__REFERENCED_TYPE_DESCRIPTIONS, 2, 2},
  };
  if (!constructed) {
    assert(0 == memcmp(&yesense_interface__msg__EulerAngle__EXPECTED_HASH, yesense_interface__msg__EulerAngle__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = yesense_interface__msg__EulerAngle__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Tid__EXPECTED_HASH, yesense_interface__msg__Tid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = yesense_interface__msg__Tid__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "yesense_interface/Tid\\t\\t\\ttid\n"
  "yesense_interface/EulerAngle\\teuler";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__EulerOnly__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__EulerOnly__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 63, 63},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__EulerOnly__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[3];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 3, 3};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__EulerOnly__get_individual_type_description_source(NULL),
    sources[1] = *yesense_interface__msg__EulerAngle__get_individual_type_description_source(NULL);
    sources[2] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
