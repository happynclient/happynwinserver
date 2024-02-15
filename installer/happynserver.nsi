Unicode True
!include "MUI2.nsh"
!include "StrFunc.nsh"
!include "WinVer.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"

${StrLoc}

Name "happynserver"
OutFile "happyserver_install.exe"

RequestExecutionLevel admin

BrandingText "HappynServer Installer"
!define PRODUCT_VERSION "0.1.0.0"
!define PRODUCT_PUBLISHER "happyn.net"

InstallDir "$PROGRAMFILES\HappynServer"
InstallDirRegKey HKLM "Software\HappynServer" "Path"

Function finishpageaction
CreateShortcut "$DESKTOP\happynsrever.lnk" "$INSTDIR\happynserver.exe"
FunctionEnd

!define MUI_FINISHPAGE_SHOWREADME ""
!define MUI_FINISHPAGE_SHOWREADME_CHECKED
!define MUI_FINISHPAGE_SHOWREADME_TEXT "创建桌面图标"
!define MUI_FINISHPAGE_SHOWREADME_FUNCTION finishpageaction

!define MUI_FINISHPAGE_RUN "$INSTDIR\happynserver.exe"
!define MUI_FINISHPAGE_RUN_TEXT "现在运行happynserver"
!insertmacro MUI_PAGE_LICENSE "../COPYING"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "simpchinese"
;--------------------------------
;Version Information
VIProductVersion ${PRODUCT_VERSION}
VIAddVersionKey  ProductVersion ${PRODUCT_VERSION}
VIAddVersionKey  ProductName "HappynServer Windows Service"
VIAddVersionKey  Comments "happyn for easy net"
VIAddVersionKey  CompanyName ${PRODUCT_PUBLISHER}
VIAddVersionKey  LegalCopyright "Copyright ${PRODUCT_PUBLISHER}"
VIAddVersionKey  FileDescription "happynserver.exe"
VIAddVersionKey  FileVersion ${PRODUCT_VERSION}


;--------------------------------

Var is64bit

Icon "..\res\happynserver.ico"

Section "happynserver"
  SectionIn RO
  SetOutPath $INSTDIR

  CreateDirectory "$SMPROGRAMS\HappynServer"
  File "..\res\happynserver.ico"

  WriteUninstaller "happyserver_uninst.exe"
  WriteRegStr HKLM "SOFTWARE\HappynServer" "Path" '$INSTDIR'
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "DisplayName" "happynserver"
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "UninstallString" '"$INSTDIR\happynserver_uninst.exe"'
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "QuietUninstallString" '"$INSTDIR\happynserver_uninst.exe" /S'
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "InstallLocation" '"$INSTDIR"'
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "DisplayIcon" '"$INSTDIR\happynserver.ico"'
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\HappynServer" "Publisher" "${PRODUCT_PUBLISHER}"


; --------------------------------------------------------
; happynsupernode.exe
; --------------------------------------------------------
  SetOutPath $INSTDIR
    File "..\utility\happynsupernode.exe"
    File "..\utility\happynssm.exe"
    File "..\utility\happynportfwd.exe"
    File "..\utility\happynroute.exe"
    File "..\res\happynserver.ico"
    File "..\res\icon144.png"
  


; --------------------------------------------------------
; dll files
; --------------------------------------------------------
  SetOutPath "$INSTDIR\platforms"
  File "..\platforms\qwindows.dll"
  File "..\platforms\qoffscreen.dll"
  File "..\platforms\qminimal.dll"

; --------------------------------------------------------
; SERVICE
; --------------------------------------------------------


; --------------------------------------------------------
; GUI TOOL
; --------------------------------------------------------
  SetOutPath $INSTDIR

  CreateShortCut "$SMPrograms\HappynServer\happynserver.lnk" "$INSTDIR\happynserver.exe"
  File "..\dist\happynserver.exe"

; --------------------------------------------------------
; FINAL
; --------------------------------------------------------
  CreateShortCut "$SMPROGRAMS\HappynServer\Uninstall happynserver.lnk" "$INSTDIR\happynserver_uninst.exe"
SectionEnd

Function .onInit
  System::Call "kernel32::GetCurrentProcess() i.s"
  System::Call "kernel32::IsWow64Process(is, *i.s)"
  Pop $is64bit
FunctionEnd

UninstallText "This will uninstall happynserver.  Click 'Uninstall' to continue."

Section "Uninstall"
  ;nsExec::ExecToLog '"$INSTDIR\happynssm.exe" stop HappynServer'
  ;nsExec::ExecToLog '"$INSTDIR\happynssm.exe" remove HappynServer confirm'
  SimpleSC::StopService "HappynServer" 1 30
  SimpleSC::RemoveService "HappynServer"
  Delete "$INSTDIR\platforms\*.*"
  RMDIR "$INSTDIR\platforms"
  Delete "$INSTDIR\*.*"
  Delete "$SMPROGRAMS\HappynServer\*.*"
  Delete "$SMPROGRAMS\HappynServer"
  RMDir "$INSTDIR"
  DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\happynserver"
  DeleteRegKey HKLM "SOFTWARE\HappynServer"
  DeleteRegValue HKCU "SOFTWARE\Microsoft\Windows\CurrentVersion\Run" "happynserver"
  Delete "$DESKTOP\happynserver.lnk"

  ; MAKE SURE DELETE ALL REGITEMS INSTALLED BY OTHER USER
  ;IntOp $0 0 + 0
  ;EnumStart:
  ;  EnumRegKey $R1 HKEY_USERS "" $0
  ;  IntOp $0 $0 + 1
  ;  StrCmp $R1 ".DEFAULT" EnumStart
  ;  StrCmp $R1 "" EnumEnd
  ;  DeleteRegValue HKU "$R1\Software\Microsoft\Windows\CurrentVersion\Run" "happynserver"
  ;  Goto EnumStart
  ;EnumEnd:
SectionEnd
