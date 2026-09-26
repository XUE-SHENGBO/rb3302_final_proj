// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/PosOnly.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/pos_only__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__PosOnly__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xa4, 0x58, 0x30, 0x1c, 0x07, 0x06, 0xde, 0xfa,
      0x61, 0x02, 0x35, 0xa4, 0x89, 0xe1, 0x46, 0x62,
      0x6d, 0x34, 0x51, 0x25, 0x0d, 0x1a, 0x24, 0xed,
      0xd9, 0x58, 0x29, 0x3c, 0x18, 0xae, 0xd6, 0xd5,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "yesense_interface/msg/detail/nav_status__functions.h"
#include "yesense_interface/msg/detail/tid__functions.h"
#include "yesense_interface/msg/detail/gnss_pos__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t yesense_interface__msg__GnssPos__EXPECTED_HASH = {1, {
    0xc6, 0x85, 0xb6, 0x95, 0xfe, 0x24, 0xb8, 0x56,
    0x40, 0x27, 0xb0, 0x55, 0xdb, 0xd5, 0x3c, 0xfc,
    0x85, 0x60, 0x8b, 0x64, 0x47, 0xd4, 0xc5, 0x93,
    0x3e, 0x8c, 0xed, 0x50, 0x1c, 0xa6, 0x08, 0xb6,
  }};
static const rosidl_type_hash_t yesense_interface__msg__NavStatus__EXPECTED_HASH = {1, {
    0xb0, 0x8e, 0x05, 0x5a, 0x7f, 0xfe, 0x7e, 0xcd,
    0xe9, 0x17, 0x23, 0xec, 0x3a, 0x3b, 0x13, 0xeb,
    0x89, 0x16, 0x87, 0x3b, 0xf0, 0xbf, 0x52, 0xd1,
    0x05, 0x33, 0x39, 0x82, 0xfd, 0x5c, 0x1f, 0x26,
  }};
static const rosidl_type_hash_t yesense_interface__msg__Tid__EXPECTED_HASH = {1, {
    0xa1, 0xd0, 0x11, 0x88, 0xff, 0x8f, 0x50, 0x39,
    0x04, 0x69, 0xdb, 0xbf, 0x7b, 0x8e, 0xa1, 0xb7,
    0x29, 0xf0, 0x16, 0xf8, 0x00, 0x3d, 0x5d, 0x1a,
    0xe3, 0x62, 0x3d, 0xe3, 0x8c, 0xf9, 0x5f, 0x58,
  }};
#endif

static char yesense_interface__msg__PosOnly__TYPE_NAME[] = "yesense_interface/msg/PosOnly";
static char yesense_interface__msg__GnssPos__TYPE_NAME[] = "yesense_interface/msg/GnssPos";
static char yesense_interface__msg__NavStatus__TYPE_NAME[] = "yesense_interface/msg/NavStatus";
static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";

// Define type names, field names, and default values
static char yesense_interface__msg__PosOnly__FIELD_NAME__tid[] = "tid";
static char yesense_interface__msg__PosOnly__FIELD_NAME__pos[] = "pos";
static char yesense_interface__msg__PosOnly__FIELD_NAME__status[] = "status";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__PosOnly__FIELDS[] = {
  {
    {yesense_interface__msg__PosOnly__FIELD_NAME__tid, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__PosOnly__FIELD_NAME__pos, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__GnssPos__TYPE_NAME, 29, 29},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__PosOnly__FIELD_NAME__status, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__NavStatus__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription yesense_interface__msg__PosOnly__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {yesense_interface__msg__GnssPos__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavStatus__TYPE_NAME, 31, 31},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__PosOnly__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__PosOnly__TYPE_NAME, 29, 29},
      {yesense_interface__msg__PosOnly__FIELDS, 3, 3},
    },
    {yesense_interface__msg__PosOnly__REFERENCED_TYPE_DESCRIPTIONS, 3, 3},
  };
  if (!constructed) {
    assert(0 == memcmp(&yesense_interface__msg__GnssPos__EXPECTED_HASH, yesense_interface__msg__GnssPos__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = yesense_interface__msg__GnssPos__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__NavStatus__EXPECTED_HASH, yesense_interface__msg__NavStatus__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = yesense_interface__msg__NavStatus__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Tid__EXPECTED_HASH, yesense_interface__msg__Tid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = yesense_interface__msg__Tid__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "yesense_interface/Tid\\t\\t\\t\\ttid\n"
  "yesense_interface/GnssPos\\t\\t\\tpos\n"
  "yesense_interface/NavStatus\\t\\t\\tstatus";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__PosOnly__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__PosOnly__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 98, 98},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__PosOnly__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[4];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 4, 4};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__PosOnly__get_individual_type_description_source(NULL),
    sources[1] = *yesense_interface__msg__GnssPos__get_individual_type_description_source(NULL);
    sources[2] = *yesense_interface__msg__NavStatus__get_individual_type_description_source(NULL);
    sources[3] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
