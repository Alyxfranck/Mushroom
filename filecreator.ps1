# Define the list of file names
$fileNames = @("home.html", "Master.html", "ch.html", "tokyo.html", "north_america.html", "south_america.html", "africa.html", "australia.html", "antarctica.html")
$fileNames = @("Master.js", "ch.js", "tokyo.js", "north_america.js", "south_america.js", "africa.js", "australia.js", "antarctica.js")
$directoryPath = "Path\to\directory"


if (-not (Test-Path -Path $directoryPath)) {
    New-Item -ItemType Directory -Path $directoryPath
}


foreach ($fileName in $fileNames) {
    $filePath = Join-Path -Path $directoryPath -ChildPath $fileName
    
    # Check if file already exists, if not, create an empty file
    if (-not (Test-Path -Path $filePath)) {
        New-Item -ItemType File -Path $filePath
    } else {
        Write-Host "already exists: $filePath"
    }
}

Write-Host "All files created"
