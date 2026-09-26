#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to yesense_interface__msg__Tid

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Tid {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: u16,

}



impl Default for Tid {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Tid::default())
  }
}

impl rosidl_runtime_rs::Message for Tid {
  type RmwMsg = super::msg::rmw::Tid;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: msg.tid,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      tid: msg.tid,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tid: msg.tid,
    }
  }
}


// Corresponds to yesense_interface__msg__ThreeAxis

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ThreeAxis::default())
  }
}

impl rosidl_runtime_rs::Message for ThreeAxis {
  type RmwMsg = super::msg::rmw::ThreeAxis;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        x: msg.x,
        y: msg.y,
        z: msg.z,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      x: msg.x,
      y: msg.y,
      z: msg.z,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      x: msg.x,
      y: msg.y,
      z: msg.z,
    }
  }
}


// Corresponds to yesense_interface__msg__SensorTemp

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SensorTemp {

    // This member is not documented.
    #[allow(missing_docs)]
    pub temp: f32,

}



impl Default for SensorTemp {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SensorTemp::default())
  }
}

impl rosidl_runtime_rs::Message for SensorTemp {
  type RmwMsg = super::msg::rmw::SensorTemp;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        temp: msg.temp,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      temp: msg.temp,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      temp: msg.temp,
    }
  }
}


// Corresponds to yesense_interface__msg__Pressure

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Pressure {

    // This member is not documented.
    #[allow(missing_docs)]
    pub val: f32,

}



impl Default for Pressure {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Pressure::default())
  }
}

impl rosidl_runtime_rs::Message for Pressure {
  type RmwMsg = super::msg::rmw::Pressure;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        val: msg.val,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      val: msg.val,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      val: msg.val,
    }
  }
}


// Corresponds to yesense_interface__msg__EulerAngle

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::EulerAngle::default())
  }
}

impl rosidl_runtime_rs::Message for EulerAngle {
  type RmwMsg = super::msg::rmw::EulerAngle;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pitch: msg.pitch,
        roll: msg.roll,
        yaw: msg.yaw,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      pitch: msg.pitch,
      roll: msg.roll,
      yaw: msg.yaw,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pitch: msg.pitch,
      roll: msg.roll,
      yaw: msg.yaw,
    }
  }
}


// Corresponds to yesense_interface__msg__Quat

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Quat::default())
  }
}

impl rosidl_runtime_rs::Message for Quat {
  type RmwMsg = super::msg::rmw::Quat;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        q0: msg.q0,
        q1: msg.q1,
        q2: msg.q2,
        q3: msg.q3,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      q0: msg.q0,
      q1: msg.q1,
      q2: msg.q2,
      q3: msg.q3,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      q0: msg.q0,
      q1: msg.q1,
      q2: msg.q2,
      q3: msg.q3,
    }
  }
}


// Corresponds to yesense_interface__msg__GnssPos

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::GnssPos::default())
  }
}

impl rosidl_runtime_rs::Message for GnssPos {
  type RmwMsg = super::msg::rmw::GnssPos;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        longitude: msg.longitude,
        latitude: msg.latitude,
        altitude: msg.altitude,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      longitude: msg.longitude,
      latitude: msg.latitude,
      altitude: msg.altitude,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      longitude: msg.longitude,
      latitude: msg.latitude,
      altitude: msg.altitude,
    }
  }
}


// Corresponds to yesense_interface__msg__NavStatus

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::NavStatus::default())
  }
}

impl rosidl_runtime_rs::Message for NavStatus {
  type RmwMsg = super::msg::rmw::NavStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        fusion_status: msg.fusion_status,
        gnss_status: msg.gnss_status,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      fusion_status: msg.fusion_status,
      gnss_status: msg.gnss_status,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      fusion_status: msg.fusion_status,
      gnss_status: msg.gnss_status,
    }
  }
}


// Corresponds to yesense_interface__msg__Vel

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Vel::default())
  }
}

impl rosidl_runtime_rs::Message for Vel {
  type RmwMsg = super::msg::rmw::Vel;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        vel_e: msg.vel_e,
        vel_n: msg.vel_n,
        vel_u: msg.vel_u,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      vel_e: msg.vel_e,
      vel_n: msg.vel_n,
      vel_u: msg.vel_u,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      vel_e: msg.vel_e,
      vel_n: msg.vel_n,
      vel_u: msg.vel_u,
    }
  }
}


// Corresponds to yesense_interface__msg__Utc

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Utc::default())
  }
}

impl rosidl_runtime_rs::Message for Utc {
  type RmwMsg = super::msg::rmw::Utc;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        year: msg.year,
        month: msg.month,
        day: msg.day,
        hour: msg.hour,
        min: msg.min,
        sec: msg.sec,
        ms: msg.ms,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      year: msg.year,
      month: msg.month,
      day: msg.day,
      hour: msg.hour,
      min: msg.min,
      sec: msg.sec,
      ms: msg.ms,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      year: msg.year,
      month: msg.month,
      day: msg.day,
      hour: msg.hour,
      min: msg.min,
      sec: msg.sec,
      ms: msg.ms,
    }
  }
}


// Corresponds to yesense_interface__msg__SampleTimestamp

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SampleTimestamp {

    // This member is not documented.
    #[allow(missing_docs)]
    pub timestamp: u32,

}



impl Default for SampleTimestamp {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SampleTimestamp::default())
  }
}

impl rosidl_runtime_rs::Message for SampleTimestamp {
  type RmwMsg = super::msg::rmw::SampleTimestamp;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        timestamp: msg.timestamp,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      timestamp: msg.timestamp,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      timestamp: msg.timestamp,
    }
  }
}


// Corresponds to yesense_interface__msg__ImuData

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ImuData {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::msg::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gyro: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub temp: super::msg::SensorTemp,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sample_timestamp: super::msg::SampleTimestamp,

}



impl Default for ImuData {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ImuData::default())
  }
}

impl rosidl_runtime_rs::Message for ImuData {
  type RmwMsg = super::msg::rmw::ImuData;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Owned(msg.tid)).into_owned(),
        acc: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.acc)).into_owned(),
        gyro: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.gyro)).into_owned(),
        temp: super::msg::SensorTemp::into_rmw_message(std::borrow::Cow::Owned(msg.temp)).into_owned(),
        sample_timestamp: super::msg::SampleTimestamp::into_rmw_message(std::borrow::Cow::Owned(msg.sample_timestamp)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Borrowed(&msg.tid)).into_owned(),
        acc: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.acc)).into_owned(),
        gyro: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.gyro)).into_owned(),
        temp: super::msg::SensorTemp::into_rmw_message(std::borrow::Cow::Borrowed(&msg.temp)).into_owned(),
        sample_timestamp: super::msg::SampleTimestamp::into_rmw_message(std::borrow::Cow::Borrowed(&msg.sample_timestamp)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tid: super::msg::Tid::from_rmw_message(msg.tid),
      acc: super::msg::ThreeAxis::from_rmw_message(msg.acc),
      gyro: super::msg::ThreeAxis::from_rmw_message(msg.gyro),
      temp: super::msg::SensorTemp::from_rmw_message(msg.temp),
      sample_timestamp: super::msg::SampleTimestamp::from_rmw_message(msg.sample_timestamp),
    }
  }
}


// Corresponds to yesense_interface__msg__ImuDataTenAxis

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ImuDataTenAxis {

    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_basic: super::msg::ImuData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_norm: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_raw: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pressure: super::msg::Pressure,

}



impl Default for ImuDataTenAxis {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ImuDataTenAxis::default())
  }
}

impl rosidl_runtime_rs::Message for ImuDataTenAxis {
  type RmwMsg = super::msg::rmw::ImuDataTenAxis;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        imu_basic: super::msg::ImuData::into_rmw_message(std::borrow::Cow::Owned(msg.imu_basic)).into_owned(),
        mag_norm: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.mag_norm)).into_owned(),
        mag_raw: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.mag_raw)).into_owned(),
        pressure: super::msg::Pressure::into_rmw_message(std::borrow::Cow::Owned(msg.pressure)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        imu_basic: super::msg::ImuData::into_rmw_message(std::borrow::Cow::Borrowed(&msg.imu_basic)).into_owned(),
        mag_norm: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mag_norm)).into_owned(),
        mag_raw: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mag_raw)).into_owned(),
        pressure: super::msg::Pressure::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pressure)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      imu_basic: super::msg::ImuData::from_rmw_message(msg.imu_basic),
      mag_norm: super::msg::ThreeAxis::from_rmw_message(msg.mag_norm),
      mag_raw: super::msg::ThreeAxis::from_rmw_message(msg.mag_raw),
      pressure: super::msg::Pressure::from_rmw_message(msg.pressure),
    }
  }
}


// Corresponds to yesense_interface__msg__EulerOnly

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct EulerOnly {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::msg::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::msg::EulerAngle,

}



impl Default for EulerOnly {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::EulerOnly::default())
  }
}

impl rosidl_runtime_rs::Message for EulerOnly {
  type RmwMsg = super::msg::rmw::EulerOnly;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Owned(msg.tid)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Owned(msg.euler)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Borrowed(&msg.tid)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Borrowed(&msg.euler)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tid: super::msg::Tid::from_rmw_message(msg.tid),
      euler: super::msg::EulerAngle::from_rmw_message(msg.euler),
    }
  }
}


// Corresponds to yesense_interface__msg__RobotLord

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotLord {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::msg::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gyro: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quat: super::msg::Quat,

}



impl Default for RobotLord {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotLord::default())
  }
}

impl rosidl_runtime_rs::Message for RobotLord {
  type RmwMsg = super::msg::rmw::RobotLord;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Owned(msg.tid)).into_owned(),
        acc: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.acc)).into_owned(),
        gyro: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.gyro)).into_owned(),
        quat: super::msg::Quat::into_rmw_message(std::borrow::Cow::Owned(msg.quat)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Borrowed(&msg.tid)).into_owned(),
        acc: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.acc)).into_owned(),
        gyro: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.gyro)).into_owned(),
        quat: super::msg::Quat::into_rmw_message(std::borrow::Cow::Borrowed(&msg.quat)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tid: super::msg::Tid::from_rmw_message(msg.tid),
      acc: super::msg::ThreeAxis::from_rmw_message(msg.acc),
      gyro: super::msg::ThreeAxis::from_rmw_message(msg.gyro),
      quat: super::msg::Quat::from_rmw_message(msg.quat),
    }
  }
}


// Corresponds to yesense_interface__msg__AttitudeMinVru

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttitudeMinVru {

    // This member is not documented.
    #[allow(missing_docs)]
    pub imu_basic: super::msg::ImuData,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::msg::EulerAngle,

}



impl Default for AttitudeMinVru {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AttitudeMinVru::default())
  }
}

impl rosidl_runtime_rs::Message for AttitudeMinVru {
  type RmwMsg = super::msg::rmw::AttitudeMinVru;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        imu_basic: super::msg::ImuData::into_rmw_message(std::borrow::Cow::Owned(msg.imu_basic)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Owned(msg.euler)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        imu_basic: super::msg::ImuData::into_rmw_message(std::borrow::Cow::Borrowed(&msg.imu_basic)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Borrowed(&msg.euler)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      imu_basic: super::msg::ImuData::from_rmw_message(msg.imu_basic),
      euler: super::msg::EulerAngle::from_rmw_message(msg.euler),
    }
  }
}


// Corresponds to yesense_interface__msg__AttitudeMinAhrs

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttitudeMinAhrs {

    // This member is not documented.
    #[allow(missing_docs)]
    pub att_min_vru: super::msg::AttitudeMinVru,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_norm: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mag_raw: super::msg::ThreeAxis,

}



impl Default for AttitudeMinAhrs {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AttitudeMinAhrs::default())
  }
}

impl rosidl_runtime_rs::Message for AttitudeMinAhrs {
  type RmwMsg = super::msg::rmw::AttitudeMinAhrs;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        att_min_vru: super::msg::AttitudeMinVru::into_rmw_message(std::borrow::Cow::Owned(msg.att_min_vru)).into_owned(),
        mag_norm: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.mag_norm)).into_owned(),
        mag_raw: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.mag_raw)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        att_min_vru: super::msg::AttitudeMinVru::into_rmw_message(std::borrow::Cow::Borrowed(&msg.att_min_vru)).into_owned(),
        mag_norm: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mag_norm)).into_owned(),
        mag_raw: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mag_raw)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      att_min_vru: super::msg::AttitudeMinVru::from_rmw_message(msg.att_min_vru),
      mag_norm: super::msg::ThreeAxis::from_rmw_message(msg.mag_norm),
      mag_raw: super::msg::ThreeAxis::from_rmw_message(msg.mag_raw),
    }
  }
}


// Corresponds to yesense_interface__msg__AttitudeAllData

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AttitudeAllData {

    // This member is not documented.
    #[allow(missing_docs)]
    pub att_min_ahrs: super::msg::AttitudeMinAhrs,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quat: super::msg::Quat,

}



impl Default for AttitudeAllData {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AttitudeAllData::default())
  }
}

impl rosidl_runtime_rs::Message for AttitudeAllData {
  type RmwMsg = super::msg::rmw::AttitudeAllData;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        att_min_ahrs: super::msg::AttitudeMinAhrs::into_rmw_message(std::borrow::Cow::Owned(msg.att_min_ahrs)).into_owned(),
        quat: super::msg::Quat::into_rmw_message(std::borrow::Cow::Owned(msg.quat)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        att_min_ahrs: super::msg::AttitudeMinAhrs::into_rmw_message(std::borrow::Cow::Borrowed(&msg.att_min_ahrs)).into_owned(),
        quat: super::msg::Quat::into_rmw_message(std::borrow::Cow::Borrowed(&msg.quat)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      att_min_ahrs: super::msg::AttitudeMinAhrs::from_rmw_message(msg.att_min_ahrs),
      quat: super::msg::Quat::from_rmw_message(msg.quat),
    }
  }
}


// Corresponds to yesense_interface__msg__PosOnly

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PosOnly {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::msg::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: super::msg::GnssPos,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: super::msg::NavStatus,

}



impl Default for PosOnly {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::PosOnly::default())
  }
}

impl rosidl_runtime_rs::Message for PosOnly {
  type RmwMsg = super::msg::rmw::PosOnly;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Owned(msg.tid)).into_owned(),
        pos: super::msg::GnssPos::into_rmw_message(std::borrow::Cow::Owned(msg.pos)).into_owned(),
        status: super::msg::NavStatus::into_rmw_message(std::borrow::Cow::Owned(msg.status)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Borrowed(&msg.tid)).into_owned(),
        pos: super::msg::GnssPos::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pos)).into_owned(),
        status: super::msg::NavStatus::into_rmw_message(std::borrow::Cow::Borrowed(&msg.status)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tid: super::msg::Tid::from_rmw_message(msg.tid),
      pos: super::msg::GnssPos::from_rmw_message(msg.pos),
      status: super::msg::NavStatus::from_rmw_message(msg.status),
    }
  }
}


// Corresponds to yesense_interface__msg__NavMin

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavMin {

    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: super::msg::PosOnly,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::msg::EulerAngle,

}



impl Default for NavMin {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::NavMin::default())
  }
}

impl rosidl_runtime_rs::Message for NavMin {
  type RmwMsg = super::msg::rmw::NavMin;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: super::msg::PosOnly::into_rmw_message(std::borrow::Cow::Owned(msg.pos)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Owned(msg.euler)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        pos: super::msg::PosOnly::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pos)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Borrowed(&msg.euler)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      pos: super::msg::PosOnly::from_rmw_message(msg.pos),
      euler: super::msg::EulerAngle::from_rmw_message(msg.euler),
    }
  }
}


// Corresponds to yesense_interface__msg__NavMinUtc

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavMinUtc {

    // This member is not documented.
    #[allow(missing_docs)]
    pub nav_basic: super::msg::NavMin,


    // This member is not documented.
    #[allow(missing_docs)]
    pub utc: super::msg::Utc,

}



impl Default for NavMinUtc {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::NavMinUtc::default())
  }
}

impl rosidl_runtime_rs::Message for NavMinUtc {
  type RmwMsg = super::msg::rmw::NavMinUtc;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        nav_basic: super::msg::NavMin::into_rmw_message(std::borrow::Cow::Owned(msg.nav_basic)).into_owned(),
        utc: super::msg::Utc::into_rmw_message(std::borrow::Cow::Owned(msg.utc)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        nav_basic: super::msg::NavMin::into_rmw_message(std::borrow::Cow::Borrowed(&msg.nav_basic)).into_owned(),
        utc: super::msg::Utc::into_rmw_message(std::borrow::Cow::Borrowed(&msg.utc)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      nav_basic: super::msg::NavMin::from_rmw_message(msg.nav_basic),
      utc: super::msg::Utc::from_rmw_message(msg.utc),
    }
  }
}


// Corresponds to yesense_interface__msg__NavAll

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct NavAll {

    // This member is not documented.
    #[allow(missing_docs)]
    pub tid: super::msg::Tid,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acc: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub gyro: super::msg::ThreeAxis,


    // This member is not documented.
    #[allow(missing_docs)]
    pub euler: super::msg::EulerAngle,


    // This member is not documented.
    #[allow(missing_docs)]
    pub quat: super::msg::Quat,


    // This member is not documented.
    #[allow(missing_docs)]
    pub temp: super::msg::SensorTemp,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pos: super::msg::GnssPos,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: super::msg::NavStatus,


    // This member is not documented.
    #[allow(missing_docs)]
    pub vel: super::msg::Vel,


    // This member is not documented.
    #[allow(missing_docs)]
    pub utc: super::msg::Utc,


    // This member is not documented.
    #[allow(missing_docs)]
    pub pressure: super::msg::Pressure,

}



impl Default for NavAll {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::NavAll::default())
  }
}

impl rosidl_runtime_rs::Message for NavAll {
  type RmwMsg = super::msg::rmw::NavAll;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Owned(msg.tid)).into_owned(),
        acc: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.acc)).into_owned(),
        gyro: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Owned(msg.gyro)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Owned(msg.euler)).into_owned(),
        quat: super::msg::Quat::into_rmw_message(std::borrow::Cow::Owned(msg.quat)).into_owned(),
        temp: super::msg::SensorTemp::into_rmw_message(std::borrow::Cow::Owned(msg.temp)).into_owned(),
        pos: super::msg::GnssPos::into_rmw_message(std::borrow::Cow::Owned(msg.pos)).into_owned(),
        status: super::msg::NavStatus::into_rmw_message(std::borrow::Cow::Owned(msg.status)).into_owned(),
        vel: super::msg::Vel::into_rmw_message(std::borrow::Cow::Owned(msg.vel)).into_owned(),
        utc: super::msg::Utc::into_rmw_message(std::borrow::Cow::Owned(msg.utc)).into_owned(),
        pressure: super::msg::Pressure::into_rmw_message(std::borrow::Cow::Owned(msg.pressure)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        tid: super::msg::Tid::into_rmw_message(std::borrow::Cow::Borrowed(&msg.tid)).into_owned(),
        acc: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.acc)).into_owned(),
        gyro: super::msg::ThreeAxis::into_rmw_message(std::borrow::Cow::Borrowed(&msg.gyro)).into_owned(),
        euler: super::msg::EulerAngle::into_rmw_message(std::borrow::Cow::Borrowed(&msg.euler)).into_owned(),
        quat: super::msg::Quat::into_rmw_message(std::borrow::Cow::Borrowed(&msg.quat)).into_owned(),
        temp: super::msg::SensorTemp::into_rmw_message(std::borrow::Cow::Borrowed(&msg.temp)).into_owned(),
        pos: super::msg::GnssPos::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pos)).into_owned(),
        status: super::msg::NavStatus::into_rmw_message(std::borrow::Cow::Borrowed(&msg.status)).into_owned(),
        vel: super::msg::Vel::into_rmw_message(std::borrow::Cow::Borrowed(&msg.vel)).into_owned(),
        utc: super::msg::Utc::into_rmw_message(std::borrow::Cow::Borrowed(&msg.utc)).into_owned(),
        pressure: super::msg::Pressure::into_rmw_message(std::borrow::Cow::Borrowed(&msg.pressure)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      tid: super::msg::Tid::from_rmw_message(msg.tid),
      acc: super::msg::ThreeAxis::from_rmw_message(msg.acc),
      gyro: super::msg::ThreeAxis::from_rmw_message(msg.gyro),
      euler: super::msg::EulerAngle::from_rmw_message(msg.euler),
      quat: super::msg::Quat::from_rmw_message(msg.quat),
      temp: super::msg::SensorTemp::from_rmw_message(msg.temp),
      pos: super::msg::GnssPos::from_rmw_message(msg.pos),
      status: super::msg::NavStatus::from_rmw_message(msg.status),
      vel: super::msg::Vel::from_rmw_message(msg.vel),
      utc: super::msg::Utc::from_rmw_message(msg.utc),
      pressure: super::msg::Pressure::from_rmw_message(msg.pressure),
    }
  }
}


