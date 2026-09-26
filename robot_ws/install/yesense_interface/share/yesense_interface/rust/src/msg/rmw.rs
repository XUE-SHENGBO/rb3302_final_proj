#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Tid() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__Tid__init(msg: *mut Tid) -> bool;
    fn yesense_interface__msg__Tid__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Tid>, size: usize) -> bool;
    fn yesense_interface__msg__Tid__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Tid>);
    fn yesense_interface__msg__Tid__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Tid>, out_seq: *mut rosidl_runtime_rs::Sequence<Tid>) -> bool;
}

// Corresponds to yesense_interface__msg__Tid
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Tid {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: u16,

}



impl Default for Tid {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__Tid__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__Tid__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Tid {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Tid__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Tid__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Tid__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Tid {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Tid where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/Tid";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Tid() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__ThreeAxis() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__ThreeAxis__init(msg: *mut ThreeAxis) -> bool;
    fn yesense_interface__msg__ThreeAxis__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ThreeAxis>, size: usize) -> bool;
    fn yesense_interface__msg__ThreeAxis__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ThreeAxis>);
    fn yesense_interface__msg__ThreeAxis__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ThreeAxis>, out_seq: *mut rosidl_runtime_rs::Sequence<ThreeAxis>) -> bool;
}

// Corresponds to yesense_interface__msg__ThreeAxis
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ThreeAxis {

    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f32,

}



impl Default for ThreeAxis {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__ThreeAxis__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__ThreeAxis__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ThreeAxis {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ThreeAxis__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ThreeAxis__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ThreeAxis__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ThreeAxis {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ThreeAxis where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/ThreeAxis";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__ThreeAxis() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__SensorTemp() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__SensorTemp__init(msg: *mut SensorTemp) -> bool;
    fn yesense_interface__msg__SensorTemp__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SensorTemp>, size: usize) -> bool;
    fn yesense_interface__msg__SensorTemp__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SensorTemp>);
    fn yesense_interface__msg__SensorTemp__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SensorTemp>, out_seq: *mut rosidl_runtime_rs::Sequence<SensorTemp>) -> bool;
}

// Corresponds to yesense_interface__msg__SensorTemp
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensorTemp {

    // This member is not documented.
    #[allow(missing_docs)]
    pub temp: f32,

}



impl Default for SensorTemp {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__SensorTemp__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__SensorTemp__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SensorTemp {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__SensorTemp__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__SensorTemp__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__SensorTemp__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SensorTemp {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SensorTemp where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/SensorTemp";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__SensorTemp() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Pressure() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__Pressure__init(msg: *mut Pressure) -> bool;
    fn yesense_interface__msg__Pressure__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Pressure>, size: usize) -> bool;
    fn yesense_interface__msg__Pressure__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Pressure>);
    fn yesense_interface__msg__Pressure__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Pressure>, out_seq: *mut rosidl_runtime_rs::Sequence<Pressure>) -> bool;
}

// Corresponds to yesense_interface__msg__Pressure
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Pressure {

    // This member is not documented.
    #[allow(missing_docs)]
    pub val: f32,

}



impl Default for Pressure {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__Pressure__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__Pressure__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Pressure {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Pressure__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Pressure__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Pressure__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Pressure {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Pressure where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/Pressure";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Pressure() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__EulerAngle() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__EulerAngle__init(msg: *mut EulerAngle) -> bool;
    fn yesense_interface__msg__EulerAngle__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EulerAngle>, size: usize) -> bool;
    fn yesense_interface__msg__EulerAngle__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EulerAngle>);
    fn yesense_interface__msg__EulerAngle__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EulerAngle>, out_seq: *mut rosidl_runtime_rs::Sequence<EulerAngle>) -> bool;
}

// Corresponds to yesense_interface__msg__EulerAngle
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EulerAngle {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pitch: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub roll: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub yaw: f32,

}



impl Default for EulerAngle {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__EulerAngle__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__EulerAngle__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EulerAngle {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__EulerAngle__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__EulerAngle__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__EulerAngle__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EulerAngle {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EulerAngle where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/EulerAngle";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__EulerAngle() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Quat() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__Quat__init(msg: *mut Quat) -> bool;
    fn yesense_interface__msg__Quat__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Quat>, size: usize) -> bool;
    fn yesense_interface__msg__Quat__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Quat>);
    fn yesense_interface__msg__Quat__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Quat>, out_seq: *mut rosidl_runtime_rs::Sequence<Quat>) -> bool;
}

// Corresponds to yesense_interface__msg__Quat
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Quat {

    // This member is not documented.
    #[allow(missing_docs)]
    pub q0: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub q1: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub q2: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub q3: f64,

}



impl Default for Quat {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__Quat__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__Quat__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Quat {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Quat__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Quat__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Quat__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Quat {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Quat where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/Quat";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Quat() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__GnssPos() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__GnssPos__init(msg: *mut GnssPos) -> bool;
    fn yesense_interface__msg__GnssPos__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GnssPos>, size: usize) -> bool;
    fn yesense_interface__msg__GnssPos__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GnssPos>);
    fn yesense_interface__msg__GnssPos__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GnssPos>, out_seq: *mut rosidl_runtime_rs::Sequence<GnssPos>) -> bool;
}

// Corresponds to yesense_interface__msg__GnssPos
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GnssPos {

    // This member is not documented.
    #[allow(missing_docs)]
    pub longitude: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub latitude: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub altitude: f32,

}



impl Default for GnssPos {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__GnssPos__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__GnssPos__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GnssPos {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__GnssPos__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__GnssPos__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__GnssPos__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GnssPos {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GnssPos where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/GnssPos";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__GnssPos() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavStatus() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__NavStatus__init(msg: *mut NavStatus) -> bool;
    fn yesense_interface__msg__NavStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<NavStatus>, size: usize) -> bool;
    fn yesense_interface__msg__NavStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<NavStatus>);
    fn yesense_interface__msg__NavStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<NavStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<NavStatus>) -> bool;
}

// Corresponds to yesense_interface__msg__NavStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub fusion_status: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gnss_status: u8,

}



impl Default for NavStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__NavStatus__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__NavStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for NavStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for NavStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for NavStatus where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/NavStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavStatus() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Vel() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__Vel__init(msg: *mut Vel) -> bool;
    fn yesense_interface__msg__Vel__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Vel>, size: usize) -> bool;
    fn yesense_interface__msg__Vel__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Vel>);
    fn yesense_interface__msg__Vel__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Vel>, out_seq: *mut rosidl_runtime_rs::Sequence<Vel>) -> bool;
}

// Corresponds to yesense_interface__msg__Vel
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Vel {

    // This member is not documented.
    #[allow(missing_docs)]
    pub vel_e: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel_n: f32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel_u: f32,

}



impl Default for Vel {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__Vel__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__Vel__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Vel {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Vel__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Vel__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Vel__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Vel {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Vel where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/Vel";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Vel() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Utc() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__Utc__init(msg: *mut Utc) -> bool;
    fn yesense_interface__msg__Utc__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<Utc>, size: usize) -> bool;
    fn yesense_interface__msg__Utc__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<Utc>);
    fn yesense_interface__msg__Utc__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<Utc>, out_seq: *mut rosidl_runtime_rs::Sequence<Utc>) -> bool;
}

// Corresponds to yesense_interface__msg__Utc
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Utc {

    // This member is not documented.
    #[allow(missing_docs)]
    pub year: u16,


    // This member is not documented.
    #[allow(missing_docs)]
    pub month: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub day: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hour: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub min: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sec: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub ms: u32,

}



impl Default for Utc {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__Utc__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__Utc__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for Utc {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Utc__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Utc__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__Utc__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for Utc {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for Utc where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/Utc";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__Utc() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__SampleTimestamp() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__SampleTimestamp__init(msg: *mut SampleTimestamp) -> bool;
    fn yesense_interface__msg__SampleTimestamp__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SampleTimestamp>, size: usize) -> bool;
    fn yesense_interface__msg__SampleTimestamp__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SampleTimestamp>);
    fn yesense_interface__msg__SampleTimestamp__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SampleTimestamp>, out_seq: *mut rosidl_runtime_rs::Sequence<SampleTimestamp>) -> bool;
}

// Corresponds to yesense_interface__msg__SampleTimestamp
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SampleTimestamp {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: u32,

}



impl Default for SampleTimestamp {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__SampleTimestamp__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__SampleTimestamp__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SampleTimestamp {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__SampleTimestamp__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__SampleTimestamp__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__SampleTimestamp__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SampleTimestamp {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SampleTimestamp where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/SampleTimestamp";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__SampleTimestamp() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__ImuData() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__ImuData__init(msg: *mut ImuData) -> bool;
    fn yesense_interface__msg__ImuData__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ImuData>, size: usize) -> bool;
    fn yesense_interface__msg__ImuData__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ImuData>);
    fn yesense_interface__msg__ImuData__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ImuData>, out_seq: *mut rosidl_runtime_rs::Sequence<ImuData>) -> bool;
}

// Corresponds to yesense_interface__msg__ImuData
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ImuData {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::super::msg::rmw::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gyro: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub temp: super::super::msg::rmw::SensorTemp,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sample_timestamp: super::super::msg::rmw::SampleTimestamp,

}



impl Default for ImuData {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__ImuData__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__ImuData__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ImuData {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ImuData__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ImuData__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ImuData__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ImuData {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ImuData where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/ImuData";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__ImuData() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__ImuDataTenAxis() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__ImuDataTenAxis__init(msg: *mut ImuDataTenAxis) -> bool;
    fn yesense_interface__msg__ImuDataTenAxis__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ImuDataTenAxis>, size: usize) -> bool;
    fn yesense_interface__msg__ImuDataTenAxis__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ImuDataTenAxis>);
    fn yesense_interface__msg__ImuDataTenAxis__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ImuDataTenAxis>, out_seq: *mut rosidl_runtime_rs::Sequence<ImuDataTenAxis>) -> bool;
}

// Corresponds to yesense_interface__msg__ImuDataTenAxis
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ImuDataTenAxis {

    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_basic: super::super::msg::rmw::ImuData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_norm: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_raw: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pressure: super::super::msg::rmw::Pressure,

}



impl Default for ImuDataTenAxis {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__ImuDataTenAxis__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__ImuDataTenAxis__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ImuDataTenAxis {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ImuDataTenAxis__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ImuDataTenAxis__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__ImuDataTenAxis__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ImuDataTenAxis {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ImuDataTenAxis where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/ImuDataTenAxis";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__ImuDataTenAxis() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__EulerOnly() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__EulerOnly__init(msg: *mut EulerOnly) -> bool;
    fn yesense_interface__msg__EulerOnly__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<EulerOnly>, size: usize) -> bool;
    fn yesense_interface__msg__EulerOnly__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<EulerOnly>);
    fn yesense_interface__msg__EulerOnly__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<EulerOnly>, out_seq: *mut rosidl_runtime_rs::Sequence<EulerOnly>) -> bool;
}

// Corresponds to yesense_interface__msg__EulerOnly
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EulerOnly {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::super::msg::rmw::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::super::msg::rmw::EulerAngle,

}



impl Default for EulerOnly {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__EulerOnly__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__EulerOnly__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for EulerOnly {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__EulerOnly__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__EulerOnly__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__EulerOnly__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for EulerOnly {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for EulerOnly where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/EulerOnly";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__EulerOnly() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__RobotLord() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__RobotLord__init(msg: *mut RobotLord) -> bool;
    fn yesense_interface__msg__RobotLord__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotLord>, size: usize) -> bool;
    fn yesense_interface__msg__RobotLord__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotLord>);
    fn yesense_interface__msg__RobotLord__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotLord>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotLord>) -> bool;
}

// Corresponds to yesense_interface__msg__RobotLord
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotLord {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::super::msg::rmw::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gyro: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quat: super::super::msg::rmw::Quat,

}



impl Default for RobotLord {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__RobotLord__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__RobotLord__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotLord {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__RobotLord__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__RobotLord__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__RobotLord__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotLord {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotLord where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/RobotLord";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__RobotLord() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__AttitudeMinVru() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__AttitudeMinVru__init(msg: *mut AttitudeMinVru) -> bool;
    fn yesense_interface__msg__AttitudeMinVru__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AttitudeMinVru>, size: usize) -> bool;
    fn yesense_interface__msg__AttitudeMinVru__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AttitudeMinVru>);
    fn yesense_interface__msg__AttitudeMinVru__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AttitudeMinVru>, out_seq: *mut rosidl_runtime_rs::Sequence<AttitudeMinVru>) -> bool;
}

// Corresponds to yesense_interface__msg__AttitudeMinVru
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttitudeMinVru {

    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_basic: super::super::msg::rmw::ImuData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::super::msg::rmw::EulerAngle,

}



impl Default for AttitudeMinVru {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__AttitudeMinVru__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__AttitudeMinVru__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AttitudeMinVru {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeMinVru__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeMinVru__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeMinVru__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AttitudeMinVru {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AttitudeMinVru where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/AttitudeMinVru";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__AttitudeMinVru() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__AttitudeMinAhrs() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__AttitudeMinAhrs__init(msg: *mut AttitudeMinAhrs) -> bool;
    fn yesense_interface__msg__AttitudeMinAhrs__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AttitudeMinAhrs>, size: usize) -> bool;
    fn yesense_interface__msg__AttitudeMinAhrs__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AttitudeMinAhrs>);
    fn yesense_interface__msg__AttitudeMinAhrs__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AttitudeMinAhrs>, out_seq: *mut rosidl_runtime_rs::Sequence<AttitudeMinAhrs>) -> bool;
}

// Corresponds to yesense_interface__msg__AttitudeMinAhrs
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttitudeMinAhrs {

    // This member is not documented.
    #[allow(missing_docs)]
    pub att_min_vru: super::super::msg::rmw::AttitudeMinVru,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_norm: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_raw: super::super::msg::rmw::ThreeAxis,

}



impl Default for AttitudeMinAhrs {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__AttitudeMinAhrs__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__AttitudeMinAhrs__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AttitudeMinAhrs {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeMinAhrs__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeMinAhrs__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeMinAhrs__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AttitudeMinAhrs {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AttitudeMinAhrs where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/AttitudeMinAhrs";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__AttitudeMinAhrs() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__AttitudeAllData() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__AttitudeAllData__init(msg: *mut AttitudeAllData) -> bool;
    fn yesense_interface__msg__AttitudeAllData__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AttitudeAllData>, size: usize) -> bool;
    fn yesense_interface__msg__AttitudeAllData__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AttitudeAllData>);
    fn yesense_interface__msg__AttitudeAllData__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AttitudeAllData>, out_seq: *mut rosidl_runtime_rs::Sequence<AttitudeAllData>) -> bool;
}

// Corresponds to yesense_interface__msg__AttitudeAllData
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttitudeAllData {

    // This member is not documented.
    #[allow(missing_docs)]
    pub att_min_ahrs: super::super::msg::rmw::AttitudeMinAhrs,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quat: super::super::msg::rmw::Quat,

}



impl Default for AttitudeAllData {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__AttitudeAllData__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__AttitudeAllData__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AttitudeAllData {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeAllData__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeAllData__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__AttitudeAllData__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AttitudeAllData {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AttitudeAllData where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/AttitudeAllData";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__AttitudeAllData() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__PosOnly() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__PosOnly__init(msg: *mut PosOnly) -> bool;
    fn yesense_interface__msg__PosOnly__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PosOnly>, size: usize) -> bool;
    fn yesense_interface__msg__PosOnly__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PosOnly>);
    fn yesense_interface__msg__PosOnly__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PosOnly>, out_seq: *mut rosidl_runtime_rs::Sequence<PosOnly>) -> bool;
}

// Corresponds to yesense_interface__msg__PosOnly
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PosOnly {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::super::msg::rmw::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: super::super::msg::rmw::GnssPos,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: super::super::msg::rmw::NavStatus,

}



impl Default for PosOnly {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__PosOnly__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__PosOnly__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PosOnly {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__PosOnly__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__PosOnly__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__PosOnly__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PosOnly {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PosOnly where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/PosOnly";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__PosOnly() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavMin() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__NavMin__init(msg: *mut NavMin) -> bool;
    fn yesense_interface__msg__NavMin__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<NavMin>, size: usize) -> bool;
    fn yesense_interface__msg__NavMin__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<NavMin>);
    fn yesense_interface__msg__NavMin__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<NavMin>, out_seq: *mut rosidl_runtime_rs::Sequence<NavMin>) -> bool;
}

// Corresponds to yesense_interface__msg__NavMin
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavMin {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: super::super::msg::rmw::PosOnly,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::super::msg::rmw::EulerAngle,

}



impl Default for NavMin {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__NavMin__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__NavMin__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for NavMin {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavMin__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavMin__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavMin__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for NavMin {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for NavMin where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/NavMin";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavMin() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavMinUtc() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__NavMinUtc__init(msg: *mut NavMinUtc) -> bool;
    fn yesense_interface__msg__NavMinUtc__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<NavMinUtc>, size: usize) -> bool;
    fn yesense_interface__msg__NavMinUtc__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<NavMinUtc>);
    fn yesense_interface__msg__NavMinUtc__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<NavMinUtc>, out_seq: *mut rosidl_runtime_rs::Sequence<NavMinUtc>) -> bool;
}

// Corresponds to yesense_interface__msg__NavMinUtc
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavMinUtc {

    // This member is not documented.
    #[allow(missing_docs)]
    pub nav_basic: super::super::msg::rmw::NavMin,


    // This member is not documented.
    #[allow(missing_docs)]
    pub utc: super::super::msg::rmw::Utc,

}



impl Default for NavMinUtc {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__NavMinUtc__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__NavMinUtc__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for NavMinUtc {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavMinUtc__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavMinUtc__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavMinUtc__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for NavMinUtc {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for NavMinUtc where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/NavMinUtc";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavMinUtc() }
  }
}


#[link(name = "yesense_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavAll() -> *const std::ffi::c_void;
}

#[link(name = "yesense_interface__rosidl_generator_c")]
extern "C" {
    fn yesense_interface__msg__NavAll__init(msg: *mut NavAll) -> bool;
    fn yesense_interface__msg__NavAll__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<NavAll>, size: usize) -> bool;
    fn yesense_interface__msg__NavAll__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<NavAll>);
    fn yesense_interface__msg__NavAll__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<NavAll>, out_seq: *mut rosidl_runtime_rs::Sequence<NavAll>) -> bool;
}

// Corresponds to yesense_interface__msg__NavAll
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavAll {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::super::msg::rmw::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gyro: super::super::msg::rmw::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::super::msg::rmw::EulerAngle,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quat: super::super::msg::rmw::Quat,


    // This member is not documented.
    #[allow(missing_docs)]
    pub temp: super::super::msg::rmw::SensorTemp,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: super::super::msg::rmw::GnssPos,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: super::super::msg::rmw::NavStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel: super::super::msg::rmw::Vel,


    // This member is not documented.
    #[allow(missing_docs)]
    pub utc: super::super::msg::rmw::Utc,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pressure: super::super::msg::rmw::Pressure,

}



impl Default for NavAll {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !yesense_interface__msg__NavAll__init(&mut msg as *mut _) {
        panic!("Call to yesense_interface__msg__NavAll__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for NavAll {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavAll__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavAll__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { yesense_interface__msg__NavAll__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for NavAll {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for NavAll where Self: Sized {
  const TYPE_NAME: &'static str = "yesense_interface/msg/NavAll";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__yesense_interface__msg__NavAll() }
  }
}


