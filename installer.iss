[Setup]
; Thông tin chung về ứng dụng
AppName=ScholarScore
AppVersion=1.0
AppPublisher=Khoa CNTT
AppPublisherURL=https://example.com/
AppSupportURL=https://example.com/
AppUpdatesURL=https://example.com/
DefaultDirName={autopf}\ScholarScore
DisableProgramGroupPage=yes
; Tên file cài đặt đầu ra
OutputBaseFilename=Setup_ScholarScore
; Thêm icon cho file Setup
SetupIconFile=assets\app_icon.ico
; Thư mục lưu file cài đặt (để vào thư mục dist)
OutputDir=dist
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Thư mục bản GUI
Source: "dist\ScholarScore\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Thư mục bản CLI (ghi đè các thư viện trùng lặp vào cùng bộ cài)
Source: "dist\ScholarScore_CLI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Tạo shortcut ở Start Menu cho cả GUI và CLI
Name: "{autoprograms}\ScholarScore"; Filename: "{app}\ScholarScore.exe"
Name: "{autoprograms}\ScholarScore (CLI)"; Filename: "{app}\ScholarScore_CLI.exe"
; Tạo shortcut ở Desktop cho bản GUI nếu user tick chọn
Name: "{autodesktop}\ScholarScore"; Filename: "{app}\ScholarScore.exe"; Tasks: desktopicon

[Run]
; Chạy ứng dụng sau khi cài đặt xong
Filename: "{app}\ScholarScore.exe"; Description: "{cm:LaunchProgram,ScholarScore}"; Flags: nowait postinstall skipifsilent
