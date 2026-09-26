// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/RobotLord.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/robot_lord__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__RobotLord__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xf5, 0xee, 0xa8, 0x26, 0xbc, 0xd4, 0x97, 0x5a,
      0xec, 0x78, 0xa8, 0x0d, 0x00, 0x2e, 0xe5, 0x5f,
      0xee, 0x4d, 0xd9, 0xa1, 0xdb, 0x6a, 0x17, 0xd3,
      0x1c, 0x8a, 0x98, 0xbd, 0x25, 0xaf, 0x60, 0x39,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "yesense_interface/msg/detail/quat__functions.h"
#include "yesense_interface/msg/detail/tid__functions.h"
#include "yesense_interface/msg/detail/three_axis__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t yesense_interface__msg__Quat__EXPECTED_HASH = {1, {
    0xdd, 0x13, 0xc8, 0x45, 0xe4, 0x86, 0xd1, 0x18,
    0x9b, 0x5c, 0x6a, 0x93, 0xa1, 0x6b, 0x29, 0x43,
    0x0f, 0x55, 0x99, 0xc8, 0x5e, 0x43, 0x45, 0x98,
    0x10, 0xe0, 0x88, 0x6a, 0x90, 0xf1, 0x85, 0xf0,
  }};
static const rosidl_type_hash_t yesense_interface__msg__ThreeAxis__EXPECTED_HASH = {1, {
    0x85, 0xef, 0x87, 0x51, 0xd8, 0x24, 0xa2, 0xbf,
    0xeb, 0xaf, 0x9a, 0x85, 0x7c, 0xb2, 0xb8, 0x47,
    0x82, 0x32, 0x3a, 0x9a, 0x5d, 0xf7, 0x77, 0x9c,
    0xb9, 0x33, 0x12, 0xa7, 0x3e, 0x54, 0xfd, 0xae,
  }};
static const rosidl_type_hash_t yesense_interface__msg__Tid__EXPECTED_HASH = {1, {
    0xa1, 0xd0, 0x11, 0x88, 0xff, 0x8f, 0x50, 0x39,
    0x04, 0x69, 0xdb, 0xbf, 0x7b, 0x8e, 0xa1, 0xb7,
    0x29, 0xf0, 0x16, 0xf8, 0x00, 0x3d, 0x5d, 0x1a,
    0xe3, 0x62, 0x3d, 0xe3, 0x8c, 0xf9, 0x5f, 0x58,
  }};
#endif

static char yesense_interface__msg__RobotLord__TYPE_NAME[] = "yesense_interface/msg/RobotLord";
static char yesense_interface__msg__Quat__TYPE_NAME[] = "yesense_interface/msg/Quat";
static char yesense_interface__msg__ThreeAxis__TYPE_NAME[] = "yesense_interface/msg/ThreeAxis";
static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";

// Define type names, field names, and default values
static char yesense_interface__msg__RobotLord__FIELD_NAME__tid[] = "tid";
static char yesense_interface__msg__RobotLord__FIELD_NAME__acc[] = "acc";
static char yesense_interface__msg__RobotLord__FIELD_NAME__gyro[] = "gyro";
static char yesense_interface__msg__RobotLord__FIELD_NAME__quat[] = "quat";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__RobotLord__FIELDS[] = {
  {
    {yesense_interface__msg__RobotLord__FIELD_NAME__tid, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__RobotLord__FIELD_NAME__acc, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__RobotLord__FIELD_NAME__gyro, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__RobotLord__FIELD_NAME__quat, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription yesense_interface__msg__RobotLord__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__RobotLord__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__RobotLord__TYPE_NAME, 31, 31},
      {yesense_interface__msg__RobotLord__FIELDS, 4, 4},
    },
    {yesense_interface__msg__RobotLord__REFERENCED_TYPE_DESCRIPTIONS, 3, 3},
  };
  if (!constructed) {
    assert(0 == memcmp(&yesense_interface__msg__Quat__EXPECTED_HASH, yesense_interface__msg__Quat__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = yesense_interface__msg__Quat__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__ThreeAxis__EXPECTED_HASH, yesense_interface__msg__ThreeAxis__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = yesense_interface__msg__ThreeAxis__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Tid__EXPECTED_HASH, yesense_interface__msg__Tid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = yesense_interface__msg__Tid__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "yesense_interface/Tid\\t\\t\\t\\ttid\n"
  "yesense_interface/ThreeAxis\\t\\t\\tacc\n"
  "yesense_interface/ThreeAxis\\t\\t\\tgyro\n"
  "yesense_interface/Quat\\t\\t\\t\\tquat";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__RobotLord__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__RobotLord__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 129, 129},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__RobotLord__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[4];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 4, 4};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__RobotLord__get_individual_type_description_source(NULL),
    sources[1] = *yesense_interface__msg__Quat__get_individual_type_description_source(NULL);
    sources[2] = *yesense_interface__msg__ThreeAxis__get_individual_type_description_source(NULL);
    sources[3] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
