INCLUDE(OptionsWindows)

ADD_DEFINITIONS(-DWTF_USE_WINCE_UNICODE=1)
ADD_DEFINITIONS(-DWTF_USE_WININET=1)
ADD_DEFINITIONS(-DWTF_CPU_ARM_TRADITIONAL -DWINCEBASIC)
ADD_DEFINITIONS(-DJS_NO_EXPORT)
ADD_DEFINITIONS(-DHAVE_ACCESSIBILITY=0)
ADD_DEFINITIONS(-DUSE_SYSTEM_MALLOC=1)
ADD_DEFINITIONS(-DJSCCOLLECTOR_VIRTUALMEM_RESERVATION=0x200000)

IF (NOT 3RDPARTY_DIR)
    IF (EXISTS $ENV{WEBKITTHIRDPARTYDIR})
        SET(3RDPARTY_DIR $ENV{WEBKITTHIRDPARTYDIR})
    ELSE ()
        MESSAGE(FATAL_ERROR "You must provide a third party directory for WinCE port.")
    ENDIF ()
ENDIF ()

INCLUDE_DIRECTORIES(${3RDPARTY_DIR}/ce-compat)
ADD_SUBDIRECTORY(${3RDPARTY_DIR} "${CMAKE_CURRENT_BINARY_DIR}/3rdparty")

WEBKIT_FEATURE(ENABLE_BLOB "Enable blob slice" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_CHANNEL_MESSAGING "Enable channel messaging" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_SQL_DATABASE "Enable SQL database" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_DATAGRID "Enable datagrid" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_DATALIST "Enable datalist" DEFAULT OFF HTML)
WEBKIT_FEATURE(ENABLE_DATA_TRANSFER_ITEMS "Enable data transfer items" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_DOM_STORAGE "Enable DOM storage" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_FAST_MOBILE_SCROLLING "Enable fast mobile scrolling" DEFAULT ON)
WEBKIT_FEATURE(ENABLE_FILTERS "Enable SVG filters" DEFAULT OFF SVG)
WEBKIT_FEATURE(ENABLE_FTPDIR "Enable FTP directory support" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_GEOLOCATION "Enable geolocation" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_GLIB_SUPPORT "Enable Glib support" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_ICONDATABASE "Enable icon database" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_INSPECTOR "Enable inspector" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_JAVASCRIPT_DEBUGGER "Enable JavaScript debugger" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_JIT "Enable JIT code" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_MATHML "Enable MathML" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_NETSCAPE_PLUGIN_API "Enable Netscape plugin API" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_NOTIFICATIONS "Enable notifications" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_ORIENTATION_EVENTS "Enable orientation events" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_PROGRESS_TAG "Enable progress tag" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_SHARED_WORKERS "Enable shared workers" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_SVG "Enable SVG" DEFAULT ON)
WEBKIT_FEATURE(ENABLE_SVG_FONTS "Enable SVG fonts" DEFAULT ON SVG)
WEBKIT_FEATURE(ENABLE_TOUCH_EVENTS "Enable Touch Events" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_VIDEO "Enable video" DEFAULT OFF HTML)
WEBKIT_FEATURE(ENABLE_WEB_SOCKETS "Enable web sockets" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_WORKERS "Enable workers" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_XHTMLMP "Enable XHTMLMP" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_XPATH "Enable XPath" DEFAULT OFF)
WEBKIT_FEATURE(ENABLE_XSLT "Enable XSLT" DEFAULT OFF)
