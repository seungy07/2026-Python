@echo off
chcp 65001 > nul
@echo off


setlocal
echo @echo off > "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
echo echo Restoring environment for conanbuildenv-release-x86_64.bat >> "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
for %%v in (PATH SWIG_LIB) do (
    set foundenvvar=
    for /f "delims== tokens=1,2" %%a in ('set') do (
        if /I "%%a" == "%%v" (
            echo set "%%a=%%b">> "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
            set foundenvvar=1
        )
    )
    if not defined foundenvvar (
        echo set %%v=>> "%~dp0/deactivate_conanbuildenv-release-x86_64.bat"
    )
)
endlocal




if defined PATH (
    set "PATH=C:\Users\ksyki\.conan2\p\yasm0f3a271ce58b4\p\bin;C:\Users\ksyki\.conan2\p\b\swige12fb856b9b4b\p\bin;C:\Users\ksyki\.conan2\p\ragel83efe87fd3acd\p\bin;%PATH%"
) else (
    set "PATH=C:\Users\ksyki\.conan2\p\yasm0f3a271ce58b4\p\bin;C:\Users\ksyki\.conan2\p\b\swige12fb856b9b4b\p\bin;C:\Users\ksyki\.conan2\p\ragel83efe87fd3acd\p\bin"
)
set "SWIG_LIB=C:\Users\ksyki\.conan2\p\b\swige12fb856b9b4b\p\bin\swiglib"