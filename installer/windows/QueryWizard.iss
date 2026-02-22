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
var
  ConfigPage: TInputQueryWizardPage;

function RuntimeEnvDir: string;
begin
  Result := ExpandConstant('{userprofile}\.querywizard');
end;

function HasAnyInstallInput(): Boolean;
begin
  Result :=
    (Trim(ConfigPage.Values[0]) <> '') or
    (Trim(ConfigPage.Values[1]) <> '') or
    (Trim(ConfigPage.Values[2]) <> '') or
    (Trim(ConfigPage.Values[3]) <> '');
end;

procedure EnsureRuntimeEnvFile();
var
  DirPath, FilePath, Content: string;
begin
  DirPath := RuntimeEnvDir();
  if not DirExists(DirPath) then
    ForceDirectories(DirPath);

  FilePath := DirPath + '\.env';

  { If file exists and user did not enter anything, preserve existing runtime config. }
  if FileExists(FilePath) and (not HasAnyInstallInput()) then
    exit;

  Content :=
    'DB_HOST=' + Trim(ConfigPage.Values[0]) + #13#10 +
    'DB_USER=' + Trim(ConfigPage.Values[1]) + #13#10 +
    'DB_PASSWORD=' + Trim(ConfigPage.Values[2]) + #13#10 +
    'DB_NAME=' + Trim(ConfigPage.Values[3]) + #13#10;
  SaveStringToFile(FilePath, Content, False);
end;

procedure InitializeWizard();
begin
  ConfigPage := CreateInputQueryPage(
    wpSelectTasks,
    'Runtime Configuration',
    'Set QueryWizard database connection',
    'These values will be written to %USERPROFILE%\.querywizard\.env. API key is loaded from Firebase.'
  );

  ConfigPage.Add('DB host:', False);
  ConfigPage.Add('DB user:', False);
  ConfigPage.Add('DB password:', True);
  ConfigPage.Add('DB name:', False);

  ConfigPage.Values[0] := 'localhost';
  ConfigPage.Values[1] := 'root';
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    EnsureRuntimeEnvFile();
end;
