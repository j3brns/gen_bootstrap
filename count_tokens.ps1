# Define exclusion patterns based on .gitignore and standard exclusions
$excludePatterns = @(
    '__pycache__/'
    '*.pyc'
    '*.pyo'
    '*.pyd'
    '.Python'
    'env/'
    '.venv/'
    'venv/'
    'build/'
    'dist/'
    '*.egg-info/'
    '.tox/'
    '.nox/'
    '.mypy_cache/'
    '.pytest_cache/'
    '.ipynb_checkpoints/'
    '.env'
    '.env.*'
    '.vscode/'
    '*.log'
    '*.sublime-project'
    '*.sublime-workspace'
    '.poetry/'
    'poetry.lock'
    '*.py[cod]'
    '*.so'
    'develop-eggs/'
    'eggs/'
    '.eggs/'
    'lib/'
    'lib64/'
    'parts/'
    'sdist/'
    'var/'
    'wheels/'
    'share/python-wheels/'
    '.installed.cfg'
    '*.search.json'
    '*.dist-info/'
    '.coverage'
    '.coverage.*'
    '.hypothesis/'
    '.pytest_cache/'
    '*.mo'
    '*.po'
    'node_modules/'
    'npm-debug.log'
    'yarn-error.log'
    'yarn-debug.log'
    '.idea/'
    '*.swp'
    '*.swo'
    '*~'
    '.DS_Store'
    '.localized'
    'Thumbs.db'
    'ehthumbs.db'
    'ehthumbs_vista.db'
    '$RECYCLE.BIN'
    'Desktop.ini'
    '.gcloud/'
    '.config/gcloud/'
    '.weave/'
    'weave.sqlite'
    'evaluation/results/'
    # Add patterns for any files containing secrets not managed by Secret Manager
    # e.g., '*.env', 'credentials.json' - template.env is included by default
    '.git/' # Standard Git metadata exclusion
)

# Read .clineignore if it exists and add its patterns to exclusions
$clineignorePath = Join-Path $PSScriptRoot ".clineignore"
if (Test-Path $clineignorePath) {
    Write-Host "Reading .clineignore for additional exclusions..."
    Get-Content $clineignorePath | ForEach-Object {
        $line = $_.Trim()
        if (-not [string]::IsNullOrEmpty($line) -and -not $line.StartsWith('#')) {
            $excludePatterns += $line
        }
    }
}

# Define inclusion file extensions and specific files
$includeExtensions = @(
    '.py'
    '.md'
    '.yaml'
    '.yml'
    '.json'
    '.txt'
)
$includeSpecificFiles = @(
    '.coveragerc'
    '.flake8'
    '.gitignore'
    '.pre-commit-config.yaml'
    'Procfile'
    'template.env'
    'pyproject.toml' # Include pyproject.toml as it's a key config file
)

# Get all files recursively
$allFiles = Get-ChildItem -Path . -Recurse -File

# Filter files based on exclusion patterns and inclusion extensions/specific files
$includedFiles = $allFiles | Where-Object {
    $filePath = $_.FullName -replace "$([regex]::Escape($PSScriptRoot))\\", "" # Get path relative to script root

    # Exclude based on patterns
    $isExcluded = $false
    foreach ($pattern in $excludePatterns) {
        # Convert glob pattern to regex for -like operator
        $regexPattern = "^$([regex]::Escape($pattern).Replace('\*', '.*').Replace('\?', '.'))$"
        if ($filePath -like $pattern) {
             $isExcluded = $true
             break
        }
    }

    if ($isExcluded) {
        return $false
    }

    # Include based on extensions or specific files
    $isIncluded = $false
    if ($includeExtensions -contains $_.Extension.ToLower()) {
        $isIncluded = $true
    } elseif ($includeSpecificFiles -contains $_.Name.ToLower()) {
        $isIncluded = $true
    } elseif ($includeSpecificFiles -contains $filePath.ToLower()) {
         # Handle specific files with paths if needed, though current list is root level
         $isIncluded = $true
    }

    # Special case for notebooks: include the file if it's in the notebooks directory
    if ($_.Extension.ToLower() -eq '.ipynb' -and $filePath.ToLower().StartsWith('notebooks\')) {
         $isIncluded = $true
    } elseif ($_.Extension.ToLower() -eq '.ipynb') {
         # Exclude other ipynb files
         $isIncluded = $false
    }


    return $isIncluded
}

# Read content of included files and join them
$combinedContent = $includedFiles | ForEach-Object { Get-Content $_.FullName -Raw } | Out-String

# Get the number of included files
$fileCount = $includedFiles.Count

# Pipe combined content to ttok and capture output
$tokenCountOutput = $combinedContent | poetry run ttok

# Output results
Write-Host "Total files included: $fileCount"
Write-Host "Total token count: $tokenCountOutput"

# Optional: List included files (can be verbose)
# Write-Host "`nIncluded files:"
# $includedFiles | ForEach-Object { Write-Host $_.FullName }
