include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
)

set(PLUGIN_DIR com/ubuntu/PamAuthentication)

set(pamauthentication_SRCS
    pamauthentication.cpp
    pamauthentication.h
    pamauthentication_plugin.cpp
    pamauthentication_plugin.h
)

add_library(PamAuthentication MODULE
    ${pamauthentication_SRCS}
)

target_link_libraries(PamAuthentication pam)

qt5_use_modules(PamAuthentication Gui Qml Quick Widgets DBus)

# Copy the plugin, the qmldir file and other assets to the build dir for running in QtCreator
if(NOT "${CMAKE_CURRENT_SOURCE_DIR}" STREQUAL "${CMAKE_CURRENT_BINARY_DIR}")
    add_custom_command(TARGET PamAuthentication POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_BINARY_DIR}/../${PLUGIN_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/qmldir ${CMAKE_CURRENT_BINARY_DIR}/../${PLUGIN_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/AuthenticationDialog.qml ${CMAKE_CURRENT_BINARY_DIR}/../${PLUGIN_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/AuthenticationService.qml ${CMAKE_CURRENT_BINARY_DIR}/../${PLUGIN_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/NotifyDialog.qml ${CMAKE_CURRENT_BINARY_DIR}/../${PLUGIN_DIR}
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:PamAuthentication> ${CMAKE_CURRENT_BINARY_DIR}/../${PLUGIN_DIR}
    )
endif(NOT "${CMAKE_CURRENT_SOURCE_DIR}" STREQUAL "${CMAKE_CURRENT_BINARY_DIR}")

# Install plugin file
install(TARGETS PamAuthentication DESTINATION ${QT_IMPORTS_DIR}/${PLUGIN_DIR})
install(FILES qmldir DESTINATION ${QT_IMPORTS_DIR}/${PLUGIN_DIR})
install(FILES AuthenticationDialog.qml DESTINATION ${QT_IMPORTS_DIR}/${PLUGIN_DIR})
install(FILES AuthenticationService.qml DESTINATION ${QT_IMPORTS_DIR}/${PLUGIN_DIR})
install(FILES NotifyDialog.qml DESTINATION ${QT_IMPORTS_DIR}/${PLUGIN_DIR})

