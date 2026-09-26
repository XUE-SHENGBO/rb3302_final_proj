// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/AttitudeAllData.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/attitude_all_data__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__AttitudeAllData__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x73, 0x19, 0x12, 0x9d, 0x2b, 0x7d, 0x79, 0xd1,
      0xd7, 0xf2, 0x0c, 0x70, 0x57, 0x97, 0xc4, 0xfe,
      0x67, 0xe0, 0xa3, 0x6e, 0x50, 0x40, 0xc1, 0x79,
      0x14, 0xf8, 0x16, 0xcf, 0x39, 0x30, 0x5a, 0x21,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "yesense_interface/msg/detail/attitude_min_ahrs__functions.h"
#include "yesense_interface/msg/detail/tid__functions.h"
#include "yesense_interface/msg/detail/quat__functions.h"
#include "yesense_interface/msg/detail/sample_timestamp__functions.h"
#include "yesense_interface/msg/detail/imu_data__functions.h"
#include "yesense_interface/msg/detail/sensor_temp__functions.h"
#include "yesense_interface/msg/detail/euler_angle__functions.h"
#include "yesense_interface/msg/detail/three_axis__functions.h"
#include "yesense_interface/msg/detail/attitude_min_vru__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t yesense_interface__msg__AttitudeMinAhrs__EXPECTED_HASH = {1, {
    0xc0, 0xf6, 0x9c, 0xb4, 0x77, 0x8a, 0xe3, 0x6d,
    0x0e, 0xf2, 0xe3, 0xb2, 0x85, 0x74, 0x0a, 0xd9,
    0x6e, 0x12, 0x92, 0xf8, 0xe6, 0xc6, 0xd8, 0x11,
    0x2d, 0x4a, 0x4c, 0x2e, 0xcd, 0xb6, 0x98, 0xdb,
  }};
static const rosidl_type_hash_t yesense_interface__msg__AttitudeMinVru__EXPECTED_HASH = {1, {
    0xb0, 0x5e, 0x11, 0x14, 0x5f, 0x06, 0x01, 0x8c,
    0xcc, 0x93, 0xa7, 0xed, 0x18, 0x75, 0x26, 0x62,
    0x6c, 0x3b, 0x59, 0x23, 0xf8, 0xea, 0x1b, 0xaa,
    0x1f, 0xae, 0xfa, 0x8f, 0x00, 0x17, 0xc8, 0x00,
  }};
static const rosidl_type_hash_t yesense_interface__msg__EulerAngle__EXPECTED_HASH = {1, {
    0x48, 0x24, 0x92, 0x57, 0x50, 0xf9, 0x63, 0x6e,
    0x0b, 0xe3, 0x7d, 0x8d, 0xf3, 0xa7, 0x3c, 0xda,
    0xf8, 0x62, 0xa3, 0x77, 0xb2, 0xc4, 0x5d, 0xb5,
    0x2b, 0x29, 0xa6, 0x81, 0x52, 0x8d, 0xb3, 0x8a,
  }};
static const rosidl_type_hash_t yesense_interface__msg__ImuData__EXPECTED_HASH = {1, {
    0x85, 0x0a, 0xfd, 0x1c, 0x00, 0xce, 0x4e, 0x86,
    0x4c, 0x17, 0xf4, 0x29, 0x0e, 0x05, 0x3f, 0xf8,
    0xfa, 0xd4, 0xba, 0xa8, 0xbb, 0x59, 0xe4, 0x01,
    0x5c, 0x71, 0x5e, 0x09, 0xea, 0xd4, 0x43, 0x56,
  }};
static const rosidl_type_hash_t yesense_interface__msg__Quat__EXPECTED_HASH = {1, {
    0xdd, 0x13, 0xc8, 0x45, 0xe4, 0x86, 0xd1, 0x18,
    0x9b, 0x5c, 0x6a, 0x93, 0xa1, 0x6b, 0x29, 0x43,
    0x0f, 0x55, 0x99, 0xc8, 0x5e, 0x43, 0x45, 0x98,
    0x10, 0xe0, 0x88, 0x6a, 0x90, 0xf1, 0x85, 0xf0,
  }};
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

static char yesense_interface__msg__AttitudeAllData__TYPE_NAME[] = "yesense_interface/msg/AttitudeAllData";
static char yesense_interface__msg__AttitudeMinAhrs__TYPE_NAME[] = "yesense_interface/msg/AttitudeMinAhrs";
static char yesense_interface__msg__AttitudeMinVru__TYPE_NAME[] = "yesense_interface/msg/AttitudeMinVru";
static char yesense_interface__msg__EulerAngle__TYPE_NAME[] = "yesense_interface/msg/EulerAngle";
static char yesense_interface__msg__ImuData__TYPE_NAME[] = "yesense_interface/msg/ImuData";
static char yesense_interface__msg__Quat__TYPE_NAME[] = "yesense_interface/msg/Quat";
static char yesense_interface__msg__SampleTimestamp__TYPE_NAME[] = "yesense_interface/msg/SampleTimestamp";
static char yesense_interface__msg__SensorTemp__TYPE_NAME[] = "yesense_interface/msg/SensorTemp";
static char yesense_interface__msg__ThreeAxis__TYPE_NAME[] = "yesense_interface/msg/ThreeAxis";
static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";

// Define type names, field names, and default values
static char yesense_interface__msg__AttitudeAllData__FIELD_NAME__att_min_ahrs[] = "att_min_ahrs";
static char yesense_interface__msg__AttitudeAllData__FIELD_NAME__quat[] = "quat";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__AttitudeAllData__FIELDS[] = {
  {
    {yesense_interface__msg__AttitudeAllData__FIELD_NAME__att_min_ahrs, 12, 12},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__AttitudeMinAhrs__TYPE_NAME, 37, 37},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__AttitudeAllData__FIELD_NAME__quat, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription yesense_interface__msg__AttitudeAllData__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {yesense_interface__msg__AttitudeMinAhrs__TYPE_NAME, 37, 37},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__AttitudeMinVru__TYPE_NAME, 36, 36},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__ImuData__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
    {NULL, 0, 0},
  },
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
yesense_interface__msg__AttitudeAllData__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__AttitudeAllData__TYPE_NAME, 37, 37},
      {yesense_interface__msg__AttitudeAllData__FIELDS, 2, 2},
    },
    {yesense_interface__msg__AttitudeAllData__REFERENCED_TYPE_DESCRIPTIONS, 9, 9},
  };
  if (!constructed) {
    assert(0 == memcmp(&yesense_interface__msg__AttitudeMinAhrs__EXPECTED_HASH, yesense_interface__msg__AttitudeMinAhrs__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = yesense_interface__msg__AttitudeMinAhrs__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__AttitudeMinVru__EXPECTED_HASH, yesense_interface__msg__AttitudeMinVru__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = yesense_interface__msg__AttitudeMinVru__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__EulerAngle__EXPECTED_HASH, yesense_interface__msg__EulerAngle__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = yesense_interface__msg__EulerAngle__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__ImuData__EXPECTED_HASH, yesense_interface__msg__ImuData__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = yesense_interface__msg__ImuData__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Quat__EXPECTED_HASH, yesense_interface__msg__Quat__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = yesense_interface__msg__Quat__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__SampleTimestamp__EXPECTED_HASH, yesense_interface__msg__SampleTimestamp__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = yesense_interface__msg__SampleTimestamp__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__SensorTemp__EXPECTED_HASH, yesense_interface__msg__SensorTemp__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = yesense_interface__msg__SensorTemp__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__ThreeAxis__EXPECTED_HASH, yesense_interface__msg__ThreeAxis__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[7].fields = yesense_interface__msg__ThreeAxis__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Tid__EXPECTED_HASH, yesense_interface__msg__Tid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[8].fields = yesense_interface__msg__Tid__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "yesense_interface/AttitudeMinAhrs\\tatt_min_ahrs\n"
  "yesense_interface/Quat\\t\\t\\t\\tquat";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__AttitudeAllData__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__AttitudeAllData__TYPE_NAME, 37, 37},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 78, 78},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__AttitudeAllData__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[10];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 10, 10};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__AttitudeAllData__get_individual_type_description_source(NULL),
    sources[1] = *yesense_interface__msg__AttitudeMinAhrs__get_individual_type_description_source(NULL);
    sources[2] = *yesense_interface__msg__AttitudeMinVru__get_individual_type_description_source(NULL);
    sources[3] = *yesense_interface__msg__EulerAngle__get_individual_type_description_source(NULL);
    sources[4] = *yesense_interface__msg__ImuData__get_individual_type_description_source(NULL);
    sources[5] = *yesense_interface__msg__Quat__get_individual_type_description_source(NULL);
    sources[6] = *yesense_interface__msg__SampleTimestamp__get_individual_type_description_source(NULL);
    sources[7] = *yesense_interface__msg__SensorTemp__get_individual_type_description_source(NULL);
    sources[8] = *yesense_interface__msg__ThreeAxis__get_individual_type_description_source(NULL);
    sources[9] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
