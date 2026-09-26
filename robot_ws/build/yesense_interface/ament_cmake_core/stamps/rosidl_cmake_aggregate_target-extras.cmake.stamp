# generated from rosidl_cmake/cmake/rosidl_cmake_aggregate_target-extras.cmake.in

# Create a convenience aggregate target yesense_interface::yesense_interface
# that links all generated interface targets, so downstream packages can use
# a single modern CMake target name instead of ${yesense_interface_TARGETS}.
if(yesense_interface_TARGETS AND NOT TARGET yesense_interface::yesense_interface)
  add_library(yesense_interface::yesense_interface INTERFACE IMPORTED)
  set_target_properties(yesense_interface::yesense_interface PROPERTIES
    INTERFACE_LINK_LIBRARIES "${yesense_interface_TARGETS}")
endif()
