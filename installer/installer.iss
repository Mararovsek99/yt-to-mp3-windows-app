#define MyAppName "YT to MP3"
#ifndef MyAppVersion
  #define MyAppVersion "1.0.0"
#endif
#define MyAppPublisher "Andrej Marovšek"
#define MyAppExeName "YoutubeToMp3.exe"

[Setup]
AppId={{B9A043E8-787F-4A4F-BED7-7A7C18A3E421}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

DefaultDirName={localappdata}\Programs\YT to MP3
DefaultGroupName=YT to MP3

OutputDir=output
OutputBaseFilename=YoutubeToMp3-Setup
SetupIconFile=..\icon.ico

Compression=lzma2
SolidCompression=yes

PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

UninstallDisplayName=YT to MP3
UninstallDisplayIcon={app}\{#MyAppExeName}

WizardStyle=modern

[Files]
Source: "..\dist\YoutubeToMp3\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\YT to MP3"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\YT to MP3"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch YT to MP3"; Flags: nowait postinstall skipifsilent