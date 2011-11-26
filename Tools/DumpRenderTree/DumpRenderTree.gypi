{
    'variables': {
        'drt_files': [
            'chromium/AccessibilityController.cpp',
            'chromium/AccessibilityController.h',
            'chromium/AccessibilityUIElement.cpp',
            'chromium/AccessibilityUIElement.h',
            'chromium/CppBoundClass.cpp',
            'chromium/CppBoundClass.h',
            'chromium/CppVariant.cpp',
            'chromium/CppVariant.h',
            'chromium/DRTDevToolsAgent.cpp',
            'chromium/DRTDevToolsAgent.h',
            'chromium/DRTDevToolsClient.cpp',
            'chromium/DRTDevToolsClient.h',
            'chromium/DumpRenderTree.cpp',
            'chromium/EventSender.cpp',
            'chromium/EventSender.h',
            'chromium/GamepadController.cpp',
            'chromium/GamepadController.h',
            'chromium/LayoutTestController.cpp',
            'chromium/LayoutTestController.h',
            'chromium/MockSpellCheck.cpp',
            'chromium/MockSpellCheck.h',
            'chromium/NotificationPresenter.h',
            'chromium/NotificationPresenter.cpp',
            'chromium/PlainTextController.cpp',
            'chromium/PlainTextController.h',
            'chromium/Task.h',
            'chromium/Task.cpp',
            'chromium/TestEventPrinter.h',
            'chromium/TestEventPrinter.cpp',
            'chromium/TestNavigationController.cpp',
            'chromium/TestNavigationController.h',
            'chromium/TestShell.cpp',
            'chromium/TestShell.h',
            'chromium/TestShellAndroid.cpp',
            'chromium/TestShellGtk.cpp',
            'chromium/TestShellMac.mm',
            'chromium/TestShellWin.cpp',
            'chromium/TestWebPlugin.cpp',
            'chromium/TestWebPlugin.h',
            'chromium/TextInputController.cpp',
            'chromium/TextInputController.h',
            'chromium/WebPermissions.cpp',
            'chromium/WebPermissions.h',
            'chromium/WebPreferences.cpp',
            'chromium/WebPreferences.h',
            'chromium/WebViewHost.cpp',
            'chromium/WebViewHost.h',
        ],
        'test_plugin_files': [
            'TestNetscapePlugIn/PluginObject.cpp',
            'TestNetscapePlugIn/PluginObject.h',
            'TestNetscapePlugIn/PluginObjectMac.mm',
            'TestNetscapePlugIn/PluginTest.cpp',
            'TestNetscapePlugIn/PluginTest.h',
            'TestNetscapePlugIn/TestObject.cpp',
            'TestNetscapePlugIn/TestObject.h',
            'TestNetscapePlugIn/Tests/DocumentOpenInDestroyStream.cpp',
            'TestNetscapePlugIn/Tests/EvaluateJSAfterRemovingPluginElement.cpp',
            'TestNetscapePlugIn/Tests/FormValue.cpp',
            'TestNetscapePlugIn/Tests/GetURLNotifyWithURLThatFailsToLoad.cpp',
            'TestNetscapePlugIn/Tests/GetURLWithJavaScriptURL.cpp',
            'TestNetscapePlugIn/Tests/GetURLWithJavaScriptURLDestroyingPlugin.cpp',
            'TestNetscapePlugIn/Tests/GetUserAgentWithNullNPPFromNPPNew.cpp',
            'TestNetscapePlugIn/Tests/NPRuntimeObjectFromDestroyedPlugin.cpp',
            'TestNetscapePlugIn/Tests/NPRuntimeRemoveProperty.cpp',
            'TestNetscapePlugIn/Tests/NullNPPGetValuePointer.cpp',
            'TestNetscapePlugIn/Tests/PassDifferentNPPStruct.cpp',
            'TestNetscapePlugIn/Tests/PluginScriptableNPObjectInvokeDefault.cpp',
            'TestNetscapePlugIn/Tests/PrivateBrowsing.cpp',
            'TestNetscapePlugIn/main.cpp',
        ],
        'conditions': [
            ['OS=="win"', {
                'drt_files': [
                    'chromium/WebThemeControlDRTWin.cpp',
                    'chromium/WebThemeControlDRTWin.h',
                    'chromium/WebThemeEngineDRTWin.cpp',
                    'chromium/WebThemeEngineDRTWin.h',
                ],
            }],
            ['OS=="mac"', {
                'drt_files': [
                    'chromium/WebThemeEngineDRTMac.mm',
                    'chromium/WebThemeEngineDRTMac.h',
                ],
            }],            
        ],
    }
}
