[Setup]
AppName=QueryWizard
AppVersion=1.0.0
DefaultDirName={autopf}\QueryWizard
DefaultGroupName=QueryWizard
DisableProgramGroupPage=yes
OutputDir=..\..\dist\installer
OutputBaseFilename=QueryWizard-Setup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\QueryWizard.exe
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional tasks:"

[Files]
Source: "..\..\dist\QueryWizard.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\QueryWizard"; Filename: "{app}\QueryWizard.exe"
Name: "{autodesktop}\QueryWizard"; Filename: "{app}\QueryWizard.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\QueryWizard.exe"; Description: "Launch QueryWizard"; Flags: nowait postinstall skipifsilent

[Code]
function RuntimeEnvDir: string;
begin
  Result := ExpandConstant('{userprofile}\.querywizard');
end;

procedure EnsureRuntimeEnvFile();
var
  DirPath, FilePath, Content: string;
begin
  DirPath := RuntimeEnvDir();
  if not DirExists(DirPath) then
    ForceDirectories(DirPath);

  FilePath := DirPath + '\.env';
  if not FileExists(FilePath) then
  begin
    Content :=
      'GOOGLE_API_KEY=' + #13#10 +
      'DB_HOST=localhost' + #13#10 +
      'DB_USER=root' + #13#10 +
      'DB_PASSWORD=' + #13#10 +
      'DB_NAME=' + #13#10;
    SaveStringToFile(FilePath, Content, False);
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    EnsureRuntimeEnvFile();
end;
