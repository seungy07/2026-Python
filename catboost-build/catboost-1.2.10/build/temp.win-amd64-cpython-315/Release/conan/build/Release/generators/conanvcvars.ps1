if (-not $env:VSCMD_ARG_VCVARS_VER){
    Push-Location "$PSScriptRoot"
    cmd /c "conanvcvars.bat&set" |
    foreach {
      if ($_ -match "=") {
        $v = $_.split("=", 2); set-item -force -path "ENV:\$($v[0])"  -value "$($v[1])"
      }
    }
    Pop-Location
    write-host conanvcvars.ps1: Activated environment}