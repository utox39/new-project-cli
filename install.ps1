pip install -r '.\requirements.txt'

mkdir 'C:\Program Files\new_project'
Copy-Item '.\dist\newproject.exe' 'C:\Program Files\newproject'

# mkdir '~\.config'
mkdir '~\.config\new_project_cli_tool'
Copy-Item '.\newproject_config.yaml' '~\.config\newproject_cli_tool'

$existingPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$newPath = $existingPath + ";C:\Program Files\new_project_cli"
[Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
