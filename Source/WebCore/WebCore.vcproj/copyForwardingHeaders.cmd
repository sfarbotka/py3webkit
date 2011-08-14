rem %1 argument is used for graphics. It can be cg or cairo
rem %2 argument is used for network. It can be cf or curl

mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\bindings"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\parser"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\runtime"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\masm"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\profiler"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\heap"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf\text"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf\unicode"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf\unicode\icu"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\yarr"
mkdir 2>NUL "%CONFIGURATIONBUILDDIR%\include\WebCoreTestSupport"

xcopy /y /d "%ProjectDir%..\config.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%CONFIGURATIONBUILDDIR%\obj\WebCore\DerivedSources\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\accessibility\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\accessibility\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\inspector\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\loader\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\loader\appcache\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\loader\archive\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\loader\archive\cf\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\loader\cache\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\loader\icon\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\history\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\history\cf\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\html\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\html\parser\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\notifications\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\css\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\animation\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\cf\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\cf\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\%1\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\transforms\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\ca\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\ca\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\win\%1\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\graphics\opentype\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\text\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\text\transcoder\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\network\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\network\%2\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\sql\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\platform\cairo\cairo\src\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\bindings\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\bindings\js\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\page\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\page\animation\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\page\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\bridge\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\bridge\jsc\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\plugins\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\plugins\win\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\rendering\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\rendering\style\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\rendering\svg\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\editing\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\dom\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\xml\parser\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\xml\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\svg\animation\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\svg\properties\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\svg\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\storage\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\websockets\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\workers\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\bindings\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\bindings"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\parser\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\parser"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\runtime\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\runtime"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\masm\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\masm"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\profiler\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\profiler"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\heap\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\heap"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\wtf\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\wtf\text\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf\text"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\wtf\unicode\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf\unicode"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\wtf\unicode\icu\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\wtf\unicode\icu"
xcopy /y /d "%ProjectDir%..\ForwardingHeaders\yarr\*.h" "%CONFIGURATIONBUILDDIR%\include\WebCore\ForwardingHeaders\yarr"

xcopy /y /d "%ProjectDir%..\testing\js\WebCoreTestSupport.h" "%CONFIGURATIONBUILDDIR%\include\WebCoreTestSupport"

if exist "%CONFIGURATIONBUILDDIR%\buildfailed" del "%CONFIGURATIONBUILDDIR%\buildfailed"
