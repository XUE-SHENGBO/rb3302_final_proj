// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from yesense_interface:msg/NavAll.idl
// generated code does not contain a copyright notice

#include "yesense_interface/msg/detail/nav_all__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_yesense_interface
const rosidl_type_hash_t *
yesense_interface__msg__NavAll__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xb0, 0x83, 0xae, 0x4c, 0xf3, 0xea, 0x91, 0x1c,
      0x3b, 0xb9, 0xfe, 0x0a, 0x78, 0x38, 0xdc, 0x1c,
      0xc7, 0x2e, 0x3f, 0xd5, 0x90, 0xe7, 0x23, 0x4f,
      0xfa, 0x2a, 0xf8, 0xf6, 0xcc, 0x1f, 0x5c, 0xc8,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types
#include "yesense_interface/msg/detail/tid__functions.h"
#include "yesense_interface/msg/detail/gnss_pos__functions.h"
#include "yesense_interface/msg/detail/pressure__functions.h"
#include "yesense_interface/msg/detail/nav_status__functions.h"
#include "yesense_interface/msg/detail/quat__functions.h"
#include "yesense_interface/msg/detail/utc__functions.h"
#include "yesense_interface/msg/detail/sensor_temp__functions.h"
#include "yesense_interface/msg/detail/euler_angle__functions.h"
#include "yesense_interface/msg/detail/vel__functions.h"
#include "yesense_interface/msg/detail/three_axis__functions.h"

// Hashes for external referenced types
#ifndef NDEBUG
static const rosidl_type_hash_t yesense_interface__msg__EulerAngle__EXPECTED_HASH = {1, {
    0x48, 0x24, 0x92, 0x57, 0x50, 0xf9, 0x63, 0x6e,
    0x0b, 0xe3, 0x7d, 0x8d, 0xf3, 0xa7, 0x3c, 0xda,
    0xf8, 0x62, 0xa3, 0x77, 0xb2, 0xc4, 0x5d, 0xb5,
    0x2b, 0x29, 0xa6, 0x81, 0x52, 0x8d, 0xb3, 0x8a,
  }};
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
static const rosidl_type_hash_t yesense_interface__msg__Pressure__EXPECTED_HASH = {1, {
    0x62, 0x94, 0x3f, 0x5a, 0x83, 0x15, 0x9d, 0x96,
    0x60, 0x86, 0x8b, 0xe7, 0x99, 0x3a, 0xa7, 0x90,
    0xa3, 0xfe, 0xd6, 0xd4, 0x08, 0xe6, 0xa2, 0xf6,
    0xe9, 0x17, 0x98, 0xba, 0xd3, 0x45, 0x8b, 0x6e,
  }};
static const rosidl_type_hash_t yesense_interface__msg__Quat__EXPECTED_HASH = {1, {
    0xdd, 0x13, 0xc8, 0x45, 0xe4, 0x86, 0xd1, 0x18,
    0x9b, 0x5c, 0x6a, 0x93, 0xa1, 0x6b, 0x29, 0x43,
    0x0f, 0x55, 0x99, 0xc8, 0x5e, 0x43, 0x45, 0x98,
    0x10, 0xe0, 0x88, 0x6a, 0x90, 0xf1, 0x85, 0xf0,
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
static const rosidl_type_hash_t yesense_interface__msg__Utc__EXPECTED_HASH = {1, {
    0xa1, 0x81, 0xfc, 0x33, 0x61, 0x99, 0x32, 0x4a,
    0xa7, 0x64, 0x7a, 0x71, 0x91, 0xcc, 0x5b, 0x14,
    0x5b, 0xe6, 0x3c, 0xb0, 0x88, 0x2e, 0x07, 0x0c,
    0x02, 0x83, 0x47, 0x92, 0x8f, 0x7b, 0xad, 0x2c,
  }};
static const rosidl_type_hash_t yesense_interface__msg__Vel__EXPECTED_HASH = {1, {
    0x5b, 0x99, 0xe2, 0xeb, 0x7d, 0xe8, 0xdd, 0xb9,
    0xb6, 0x94, 0xd8, 0x58, 0x5c, 0xa3, 0x3a, 0xe4,
    0xbf, 0x39, 0xff, 0x62, 0xfd, 0x61, 0xd2, 0xdc,
    0x52, 0x74, 0xab, 0xdb, 0x0c, 0xf0, 0xde, 0xe8,
  }};
#endif

static char yesense_interface__msg__NavAll__TYPE_NAME[] = "yesense_interface/msg/NavAll";
static char yesense_interface__msg__EulerAngle__TYPE_NAME[] = "yesense_interface/msg/EulerAngle";
static char yesense_interface__msg__GnssPos__TYPE_NAME[] = "yesense_interface/msg/GnssPos";
static char yesense_interface__msg__NavStatus__TYPE_NAME[] = "yesense_interface/msg/NavStatus";
static char yesense_interface__msg__Pressure__TYPE_NAME[] = "yesense_interface/msg/Pressure";
static char yesense_interface__msg__Quat__TYPE_NAME[] = "yesense_interface/msg/Quat";
static char yesense_interface__msg__SensorTemp__TYPE_NAME[] = "yesense_interface/msg/SensorTemp";
static char yesense_interface__msg__ThreeAxis__TYPE_NAME[] = "yesense_interface/msg/ThreeAxis";
static char yesense_interface__msg__Tid__TYPE_NAME[] = "yesense_interface/msg/Tid";
static char yesense_interface__msg__Utc__TYPE_NAME[] = "yesense_interface/msg/Utc";
static char yesense_interface__msg__Vel__TYPE_NAME[] = "yesense_interface/msg/Vel";

// Define type names, field names, and default values
static char yesense_interface__msg__NavAll__FIELD_NAME__tid[] = "tid";
static char yesense_interface__msg__NavAll__FIELD_NAME__acc[] = "acc";
static char yesense_interface__msg__NavAll__FIELD_NAME__gyro[] = "gyro";
static char yesense_interface__msg__NavAll__FIELD_NAME__euler[] = "euler";
static char yesense_interface__msg__NavAll__FIELD_NAME__quat[] = "quat";
static char yesense_interface__msg__NavAll__FIELD_NAME__temp[] = "temp";
static char yesense_interface__msg__NavAll__FIELD_NAME__pos[] = "pos";
static char yesense_interface__msg__NavAll__FIELD_NAME__status[] = "status";
static char yesense_interface__msg__NavAll__FIELD_NAME__vel[] = "vel";
static char yesense_interface__msg__NavAll__FIELD_NAME__utc[] = "utc";
static char yesense_interface__msg__NavAll__FIELD_NAME__pressure[] = "pressure";

static rosidl_runtime_c__type_description__Field yesense_interface__msg__NavAll__FIELDS[] = {
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__tid, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Tid__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__acc, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__gyro, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__ThreeAxis__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__euler, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__quat, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__temp, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__SensorTemp__TYPE_NAME, 32, 32},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__pos, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__GnssPos__TYPE_NAME, 29, 29},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__status, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__NavStatus__TYPE_NAME, 31, 31},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__vel, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Vel__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__utc, 3, 3},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Utc__TYPE_NAME, 25, 25},
    },
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavAll__FIELD_NAME__pressure, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_NESTED_TYPE,
      0,
      0,
      {yesense_interface__msg__Pressure__TYPE_NAME, 30, 30},
    },
    {NULL, 0, 0},
  },
};

static rosidl_runtime_c__type_description__IndividualTypeDescription yesense_interface__msg__NavAll__REFERENCED_TYPE_DESCRIPTIONS[] = {
  {
    {yesense_interface__msg__EulerAngle__TYPE_NAME, 32, 32},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__GnssPos__TYPE_NAME, 29, 29},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__NavStatus__TYPE_NAME, 31, 31},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Pressure__TYPE_NAME, 30, 30},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Quat__TYPE_NAME, 26, 26},
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
  {
    {yesense_interface__msg__Utc__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
  {
    {yesense_interface__msg__Vel__TYPE_NAME, 25, 25},
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
yesense_interface__msg__NavAll__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {yesense_interface__msg__NavAll__TYPE_NAME, 28, 28},
      {yesense_interface__msg__NavAll__FIELDS, 11, 11},
    },
    {yesense_interface__msg__NavAll__REFERENCED_TYPE_DESCRIPTIONS, 10, 10},
  };
  if (!constructed) {
    assert(0 == memcmp(&yesense_interface__msg__EulerAngle__EXPECTED_HASH, yesense_interface__msg__EulerAngle__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[0].fields = yesense_interface__msg__EulerAngle__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__GnssPos__EXPECTED_HASH, yesense_interface__msg__GnssPos__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[1].fields = yesense_interface__msg__GnssPos__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__NavStatus__EXPECTED_HASH, yesense_interface__msg__NavStatus__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[2].fields = yesense_interface__msg__NavStatus__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Pressure__EXPECTED_HASH, yesense_interface__msg__Pressure__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[3].fields = yesense_interface__msg__Pressure__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Quat__EXPECTED_HASH, yesense_interface__msg__Quat__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[4].fields = yesense_interface__msg__Quat__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__SensorTemp__EXPECTED_HASH, yesense_interface__msg__SensorTemp__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[5].fields = yesense_interface__msg__SensorTemp__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__ThreeAxis__EXPECTED_HASH, yesense_interface__msg__ThreeAxis__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[6].fields = yesense_interface__msg__ThreeAxis__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Tid__EXPECTED_HASH, yesense_interface__msg__Tid__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[7].fields = yesense_interface__msg__Tid__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Utc__EXPECTED_HASH, yesense_interface__msg__Utc__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[8].fields = yesense_interface__msg__Utc__get_type_description(NULL)->type_description.fields;
    assert(0 == memcmp(&yesense_interface__msg__Vel__EXPECTED_HASH, yesense_interface__msg__Vel__get_type_hash(NULL), sizeof(rosidl_type_hash_t)));
    description.referenced_type_descriptions.data[9].fields = yesense_interface__msg__Vel__get_type_description(NULL)->type_description.fields;
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "yesense_interface/Tid\\t\\t\\t\\ttid\n"
  "yesense_interface/ThreeAxis\\t\\t\\tacc\n"
  "yesense_interface/ThreeAxis\\t\\t\\tgyro\n"
  "yesense_interface/EulerAngle\\t\\teuler\n"
  "yesense_interface/Quat\\t\\t\\t\\tquat\n"
  "yesense_interface/SensorTemp \\t\\ttemp\n"
  "yesense_interface/GnssPos\\t\\t\\tpos\n"
  "yesense_interface/NavStatus\\t\\t\\tstatus\n"
  "yesense_interface/Vel\\t\\t\\t\\tvel\\t\n"
  "yesense_interface/Utc\\t\\t\\t\\tutc\n"
  "yesense_interface/Pressure\\t\\t\\tpressure";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
yesense_interface__msg__NavAll__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {yesense_interface__msg__NavAll__TYPE_NAME, 28, 28},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 367, 367},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
yesense_interface__msg__NavAll__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[11];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 11, 11};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *yesense_interface__msg__NavAll__get_individual_type_description_source(NULL),
    sources[1] = *yesense_interface__msg__EulerAngle__get_individual_type_description_source(NULL);
    sources[2] = *yesense_interface__msg__GnssPos__get_individual_type_description_source(NULL);
    sources[3] = *yesense_interface__msg__NavStatus__get_individual_type_description_source(NULL);
    sources[4] = *yesense_interface__msg__Pressure__get_individual_type_description_source(NULL);
    sources[5] = *yesense_interface__msg__Quat__get_individual_type_description_source(NULL);
    sources[6] = *yesense_interface__msg__SensorTemp__get_individual_type_description_source(NULL);
    sources[7] = *yesense_interface__msg__ThreeAxis__get_individual_type_description_source(NULL);
    sources[8] = *yesense_interface__msg__Tid__get_individual_type_description_source(NULL);
    sources[9] = *yesense_interface__msg__Utc__get_individual_type_description_source(NULL);
    sources[10] = *yesense_interface__msg__Vel__get_individual_type_description_source(NULL);
    constructed = true;
  }
  return &source_sequence;
}
