param(
    [Parameter(Mandatory = $true)]
    [string]$BaseUrl
)

$BaseUrl = $BaseUrl.TrimEnd("/")

$paths = @(
    "/health",
    "/dashboard",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/v1/agents",
    "/v1/scenarios",
    "/v1/metrics",
    "/v1/incidents",
    "/v1/audit"
)

$failed = $false

foreach ($path in $paths) {
    $url = "$BaseUrl$path"

    try {
        $response = Invoke-WebRequest `
            -Uri $url `
            -UseBasicParsing `
            -TimeoutSec 30

        if ($response.StatusCode -eq 200) {
            Write-Host "PASS $($response.StatusCode) $url" `
                -ForegroundColor Green
        }
        else {
            Write-Host "FAIL $($response.StatusCode) $url" `
                -ForegroundColor Red

            $failed = $true
        }
    }
    catch {
        Write-Host "FAIL $url" -ForegroundColor Red
        Write-Host $_.Exception.Message -ForegroundColor DarkRed

        $failed = $true
    }
}

if ($failed) {
    exit 1
}

Write-Host ""
Write-Host "All public endpoints passed." `
    -ForegroundColor Green