// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/ImuData.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/imu_data__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__ImuData__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x85, 0x0a, 0xfd, 0x1c, 0x00, 0xce, 0x4e, 0x86,
      0x4c, 0x17, 0xf4, 0x29, 0x0e, 0x05, 0x3f, 0xf8,
      0xfa, 0xd4, 0xba, 0xa8, 0xbb, 0x59, 0xe4, 0x01,
      0x5c, 0x71, 0x5e, 0x09, 0xea, 0xd4, 0x43, 0x56,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "yesense_interface/msg/detail/sample_timestamp__functions.h"
#include "yesense_interface/msg/detail/tid__functions.h"
#include "yesense_interface/msg/detail/sensor_temp__functions.h"
#include "yesense_interface/msg/detail/three_axis__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t yesense_interface__msg__SampleTimestamp__EXPECTED_HASH = {1, {
    0x36, 0xe2, 0xa1, 0xb4, 0xa7, 0x4e, 0xbc, 0xe4,
    0xdd, 0x74, 0xad, 0x93, 0xa7, 0x3f, 0xe8, 0xb0,
    0x38, 0x2a, 0xf0, 0x2e, 0xfd, 0x4c, 0x0e, 0xae,
    0xa8, 0x9a, 0xdb, 0x80, 0xd3, 0x62, 0x07, 0xff,
  }};
static const rosidl_type_hash_t yesense_interface__msg__SensorTemp__EXPECTED_HASH = {1, {
    0x00, 0x8f, 0xd1, 0x7a, 0x7f, 0x2e, 0x91, 0xdd,
    0xf8, 0xe8, 0x6e, 0xcb, 0x5e, 0x0a, 0xd8, 0x31,
    0x51, 0x41, 0x86, 0xa6, 0x15, 0xce, 0xfd, 0x31,
    0x33, 0xda, 0xf9, 0xd3, 0x7a, 0xd7, 0x0f, 0x5b,
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

static char yesense_interface__msg__ImuData__TYPE_NAME[] = "yesense_interface/msg/ImuData";
static char yesense_interface__msg__SampleTimestamp__TYPE_NAME[] = "yesense_interface/msg/SampleTimestamp";
static char yesense_interface__msg__SensorTemp__TYPE_NAME[] = "yesense_interface/msg/SensorTemp";
static char yesense_interface__msg__ThreeAxis__TYPE_NAME[] = "yesense_interface/msg/ThreeAxis";
static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";

// Define type names, field names, and default values
static char yesense_interface__msg__ImuData__FIELD_NAME__tid[] = "tid";
static char yesense_interface__msg__ImuData__FIELD_NAME__acc[] = "acc";
static char yesense_interface__msg__ImuData__FIELD_NAME__gyro[] = "gyro";
static char yesense_interface__msg__ImuData__FIELD_NAME__temp[] = "temp";
static char yesense_interface__msg__ImuData__FIELD_NAME__sample_timestamp[] = "sample_timestamp";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__ImuData__FIELDS[] = {
  {
    {yesense_interface__msg__ImuData__FIELD_NAME__tid, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ImuData__FIELD_NAME__acc, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ImuData__FIELD_NAME__gyro, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ImuData__FIELD_NAME__temp, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__SensorTemp__TYPE_NAME, 32, 32},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ImuData__FIELD_NAME__sample_timestamp, 16, 16},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__SampleTimestamp__TYPE_NAME, 37, 37},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription yesense_interface__msg__ImuData__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {yesense_interface__msg__SampleTimestamp__TYPE_NAME, 37, 37},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__SensorTemp__TYPE_NAME, 32, 32},
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
yesense_interface__msg__ImuData__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__ImuData__TYPE_NAME, 29, 29},
      {yesense_interface__msg__ImuData__FIELDS, 5, 5},
    },
    {yesense_interface__msg__ImuData__REFERENCED_TYPE_DESCRIPTIONS, 4, 4},
  };
  if (!constructed) {
    assert(0 == memcmp(&yesense_interface__msg__SampleTimestamp__EXPECTED_HASH, yesense_interface__msg__SampleTimestamp__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = yesense_interface__msg__SampleTimestamp__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__SensorTemp__EXPECTED_HASH, yesense_interface__msg__SensorTemp__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = yesense_interface__msg__SensorTemp__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__ThreeAxis__EXPECTED_HASH, yesense_interface__msg__ThreeAxis__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = yesense_interface__msg__ThreeAxis__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Tid__EXPECTED_HASH, yesense_interface__msg__Tid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = yesense_interface__msg__Tid__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "yesense_interface/Tid\\t\\t\\t\\ttid\n"
  "yesense_interface/ThreeAxis\\t\\t\\tacc\n"
  "yesense_interface/ThreeAxis\\t\\t\\tgyro\n"
  "yesense_interface/SensorTemp \\t\\ttemp\n"
  "yesense_interface/SampleTimestamp\\tsample_timestamp";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__ImuData__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__ImuData__TYPE_NAME, 29, 29},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 185, 185},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__ImuData__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[5];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 5, 5};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__ImuData__get_individual_type_description_source(NULL),
    sources[1] = *yesense_interface__msg__SampleTimestamp__get_individual_type_description_source(NULL);
    sources[2] = *yesense_interface__msg__SensorTemp__get_individual_type_description_source(NULL);
    sources[3] = *yesense_interface__msg__ThreeAxis__get_individual_type_description_source(NULL);
    sources[4] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
