pip install -r '.\requirements.txt'

mkdir 'C:\Program Files\newproject'
Copy-Item '.\dist\newproject.exe' 'C:\Program Files\newproject'

# mkdir '~\.config'
mkdir '~\.config\newproject'
Copy-Item '.\newproject_config.yaml' '~\.config\newproject'

$existingPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$newPath = $existingPath + ";C:\Program Files\newproject"
[Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
