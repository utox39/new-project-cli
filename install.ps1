pip install -r '.\requirements.txt'

mkdir 'C:\Program Files\new_project_cli'
Copy-Item '.\dist\new_project.exe' 'C:\Program Files\new_project_cli'

# mkdir '~\.config'
mkdir '~\.config\new_project_cli_tool'
Copy-Item '.\new_project_config.json' '~\.config\new_project_cli_tool'

$existingPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$newPath = $existingPath + ";C:\Program Files\new_project_cli"
[Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
