configure_file(bhdouglass-indicator-weather.py ${CMAKE_CURRENT_BINARY_DIR}/bhdouglass-indicator-weather.py)

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/bhdouglass-indicator-weather.py DESTINATION ${DATA_DIR}indicator)
install(FILES "bhdouglass-indicator-weather.conf" DESTINATION ${DATA_DIR}indicator)
install(FILES "install.sh" DESTINATION ${DATA_DIR}indicator)
install(FILES "com.bhdouglass.indicator.weather" DESTINATION ${DATA_DIR}indicator)
install(FILES "uninstall.sh" DESTINATION ${DATA_DIR}indicator)
