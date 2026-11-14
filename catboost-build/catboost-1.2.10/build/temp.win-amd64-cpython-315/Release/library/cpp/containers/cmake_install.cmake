# Install script for directory: C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/catboost_all_src/library/cpp/containers

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files (x86)/CATBOOST")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/paged_vector/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/stack_array/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/absl_flat_hash/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/2d_array/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/dense_hash/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/flat_hash/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/comptrie/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/compact_vector/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/stack_vector/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/ring_buffer/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/intrusive_rb_tree/cmake_install.cmake")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for the subdirectory.
  include("C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/disjoint_interval_tree/cmake_install.cmake")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "C:/Users/ksyki/Desktop/2026 Python/catboost-build/catboost-1.2.10/build/temp.win-amd64-cpython-315/Release/library/cpp/containers/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
