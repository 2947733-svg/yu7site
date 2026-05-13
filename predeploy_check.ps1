#requires -Version 5.0
<#
.SYNOPSIS
    Pre-deploy проверка yu7.site перед заливкой на хостинг.
.DESCRIPTION
    Прогоняет: html-validate, cspell, проверку SEO-метаданных, проверку битых ссылок.
    Запускать из C:\claude-test\yu7-digest\site_live\
.EXAMPLE
    .\predeploy_check.ps1
    .\predeploy_check.ps1 -Strict   # выйдет с кодом 1 при любом warning
#>
param(
    [switch]$Strict
)

$ErrorActionPreference = 'Continue'
$startTime = Get-Date

Write-Host "`n========== YU7.SITE PRE-DEPLOY CHECK ==========" -ForegroundColor Cyan
Write-Host "Запуск: $startTime`n" -ForegroundColor Gray

$problems = 0
$warnings = 0

# 1. html-validate
Write-Host "[1/5] html-validate..." -ForegroundColor Yellow
if (Get-Command html-validate -ErrorAction SilentlyContinue) {
    $hvOutput = & html-validate *.html 2>&1
    $hvProblems = $hvOutput | Select-String "problems" | Select-Object -Last 1
    if ($hvProblems -and $hvProblems.ToString() -match "(\d+) errors?, (\d+) warnings?") {
        $errs = [int]$matches[1]
        $wrns = [int]$matches[2]
        if ($errs -gt 0) {
            Write-Host "    ❌ $errs ошибок, $wrns предупреждений" -ForegroundColor Red
            $hvOutput | Where-Object { $_ -match "error" } | ForEach-Object { Write-Host "       $_" -ForegroundColor Red }
            $problems += $errs
        } else {
            Write-Host "    ✅ 0 ошибок, $wrns предупреждений" -ForegroundColor Green
            $warnings += $wrns
        }
    } else {
        Write-Host "    ✅ Без замечаний" -ForegroundColor Green
    }
} else {
    Write-Host "    ⚠️  html-validate не установлен. Поставь: npm i -g html-validate" -ForegroundColor Yellow
}

# 2. cspell (опционально)
Write-Host "`n[2/5] cspell (русский+английский)..." -ForegroundColor Yellow
if (Get-Command cspell -ErrorAction SilentlyContinue) {
    $cs = & cspell "**/*.html" --no-progress --quiet 2>&1
    $csCount = ($cs | Where-Object { $_ -match ":\d+:\d+" }).Count
    if ($csCount -eq 0) {
        Write-Host "    ✅ Опечаток не найдено" -ForegroundColor Green
    } else {
        Write-Host "    ⚠️  Найдено $csCount возможных опечаток (см. полный лог: cspell '**/*.html')" -ForegroundColor Yellow
        $warnings += $csCount
    }
} else {
    Write-Host "    ⚠️  cspell не установлен. Поставь: npm i -g cspell" -ForegroundColor Yellow
}

# 3. SEO checks - canonical, og:url, JSON-LD
Write-Host "`n[3/5] SEO-метаданные..." -ForegroundColor Yellow
$noCanonical = @()
$noOgUrl = @()
$htmlFiles = Get-ChildItem -Filter *.html | Where-Object { $_.Name -notmatch "^(yandex_|google[a-f0-9]+\.html$)" }
foreach ($f in $htmlFiles) {
    $content = Get-Content $f.FullName -Raw
    if ($content -notmatch 'rel="canonical"') { $noCanonical += $f.Name }
    if ($content -notmatch 'property="og:url"') { $noOgUrl += $f.Name }
}
if ($noCanonical.Count -eq 0) {
    Write-Host "    ✅ Все страницы имеют canonical" -ForegroundColor Green
} else {
    Write-Host "    ⚠️  Без canonical ($($noCanonical.Count)): $($noCanonical -join ', ')" -ForegroundColor Yellow
    $warnings += $noCanonical.Count
}
if ($noOgUrl.Count -gt 0) {
    Write-Host "    ⚠️  Без og:url ($($noOgUrl.Count) шт.)" -ForegroundColor Yellow
}

# 4. Internal links
Write-Host "`n[4/5] Внутренние ссылки..." -ForegroundColor Yellow
$existing = $htmlFiles.Name + (Get-ChildItem -Filter *.html | ForEach-Object { "/$($_.Name)" })
$broken = @()
foreach ($f in $htmlFiles) {
    $content = Get-Content $f.FullName -Raw
    $matches = [regex]::Matches($content, 'href="(/[^"]+\.html)"')
    foreach ($m in $matches) {
        $target = $m.Groups[1].Value.TrimStart('/')
        if (-not (Test-Path $target)) {
            $broken += "$($f.Name) → $($m.Groups[1].Value)"
        }
    }
}
if ($broken.Count -eq 0) {
    Write-Host "    ✅ Битых ссылок нет" -ForegroundColor Green
} else {
    Write-Host "    ❌ Битые ссылки ($($broken.Count)):" -ForegroundColor Red
    $broken | ForEach-Object { Write-Host "       $_" -ForegroundColor Red }
    $problems += $broken.Count
}

# 5. search-index.json sanity
Write-Host "`n[5/5] search-index.json..." -ForegroundColor Yellow
if (Test-Path "search-index.json") {
    try {
        $idx = Get-Content "search-index.json" -Raw | ConvertFrom-Json
        $idxCount = $idx.Count
        $htmlCount = $htmlFiles.Count
        if ($idxCount -lt $htmlCount - 5) {
            Write-Host "    ⚠️  В индексе $idxCount записей, на сайте $htmlCount страниц" -ForegroundColor Yellow
            $warnings++
        } else {
            Write-Host "    ✅ $idxCount записей в индексе, $htmlCount HTML-файлов" -ForegroundColor Green
        }
    } catch {
        Write-Host "    ❌ search-index.json повреждён: $_" -ForegroundColor Red
        $problems++
    }
} else {
    Write-Host "    ⚠️  search-index.json не найден" -ForegroundColor Yellow
}

# Сводка
$elapsed = (Get-Date) - $startTime
Write-Host "`n========== ИТОГ ==========" -ForegroundColor Cyan
Write-Host "Время: $([math]::Round($elapsed.TotalSeconds, 1))s" -ForegroundColor Gray
Write-Host "Ошибок: $problems" -ForegroundColor $(if ($problems -gt 0) { 'Red' } else { 'Green' })
Write-Host "Предупреждений: $warnings" -ForegroundColor $(if ($warnings -gt 0) { 'Yellow' } else { 'Green' })

if ($problems -gt 0) {
    Write-Host "`n❌ ДЕПЛОИТЬ НЕЛЬЗЯ — есть ошибки`n" -ForegroundColor Red
    exit 1
} elseif ($Strict -and $warnings -gt 0) {
    Write-Host "`n⚠️  Strict mode: есть предупреждения`n" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "`n✅ ГОТОВ К ДЕПЛОЮ`n" -ForegroundColor Green
    exit 0
}
