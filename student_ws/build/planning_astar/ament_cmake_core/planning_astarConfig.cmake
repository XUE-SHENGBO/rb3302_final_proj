# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_planning_astar_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED planning_astar_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(planning_astar_FOUND FALSE)
  elseif(NOT planning_astar_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(planning_astar_FOUND FALSE)
  endif()
  return()
endif()
set(_planning_astar_CONFIG_INCLUDED TRUE)

# output package information
if(NOT planning_astar_FIND_QUIETLY)
  message(STATUS "Found planning_astar: 1.0.0 (${planning_astar_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'planning_astar' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT planning_astar_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(planning_astar_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${planning_astar_DIR}/${_extra}")
endforeach()
