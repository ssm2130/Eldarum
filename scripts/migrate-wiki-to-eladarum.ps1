# Wraps legacy wiki.css gazetteer pages in the same chrome as index.html (app-header, sidebar chrome.js, shell).
# Preserves inner <article class="main-article"> markup (infoboxes, grid-top). Styles: css/eladarum.css ".main article.main-article".
param(
    [switch]$WhatIf
)
$ErrorActionPreference = 'Stop'
$pagesRoot = Resolve-Path (Join-Path (Join-Path $PSScriptRoot '..') 'pages')
$htmlFiles = Get-ChildItem -LiteralPath $pagesRoot.Path -Filter '*.html' -Recurse -File

function Get-RootPrefix([string]$dirAbs) {
    $rel = $dirAbs.Substring($pagesRoot.Path.Length).Trim('\')
    if (-not $rel) { return '../' }
    $depth = ($rel.Split('\') | Where-Object { $_ }).Count
    return '../' * ($depth + 1)
}

foreach ($f in $htmlFiles) {
    $raw = Get-Content -LiteralPath $f.FullName -Raw -Encoding UTF8
    if ($raw -notmatch 'wiki\.css') { continue }

    $mArt = [regex]::Match($raw, '(?s)<article class="main-article">(.*)</article>')
    if (-not $mArt.Success) {
        Write-Warning "No main-article: $($f.Name)"
        continue
    }
    $inner = $mArt.Groups[1].Value.TrimEnd()

    $mTi = [regex]::Match($raw, '<title>([^<]+)</title>')
    $fullTitle = if ($mTi.Success) { $mTi.Groups[1].Value.Trim() } else { 'Eldarum' }
    if ($fullTitle -match '^(.*)\s[\u2014\u2013-]\s*Eldarum\s*$') { $shortTitle = $matches[1].Trim() } else { $shortTitle = $fullTitle }
    $desc = 'Eldarum gazetteer: ' + $shortTitle + '.'

    $rp = Get-RootPrefix $f.DirectoryName
    $descEsc = $desc.Replace('&', '&amp;').Replace('"', '&quot;')

    $out = @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="description" content="$descEsc"/>
  <title>$fullTitle</title>
  <link rel="stylesheet" href="${rp}css/eladarum.css"/>
</head>
<body data-root="$rp" data-section="gazetteer" data-bc-labels="Home|$shortTitle" data-bc-hrefs="index.html">
  <header class="app-header">
    <button type="button" class="menu-toggle" data-sidebar-toggle aria-expanded="false" aria-label="Open navigation">Menu</button>
    <div class="app-header__brand"><a href="${rp}index.html" style="color:inherit;text-decoration:none"><strong>Eldarum</strong></a><span>Gazetteer</span></div>
    <div class="header-search"><input id="site-search" type="search" placeholder="Search..." autocomplete="off" aria-label="Search"/><div id="search-results" class="search-dropdown"></div></div>
  </header>
  <div class="breadcrumb-strip"><nav id="breadcrumb-target" aria-label="Breadcrumb"></nav></div>
  <div class="backdrop" data-sidebar-backdrop></div>
  <div class="shell">
    <aside class="sidebar" id="sidebar-target" aria-label="Section navigation"></aside>
    <main class="main" id="main">
      <article class="main-article">
$inner
      </article>
      <footer class="site-footer"></footer>
    </main>
  </div>
  <script src="${rp}js/chrome.js" defer></script>
</body>
</html>
"@
    if ($WhatIf) {
        Write-Host "Would migrate: $($f.FullName)"
        continue
    }
    [System.IO.File]::WriteAllText($f.FullName, $out, [System.Text.UTF8Encoding]::new($false))
    Write-Host "Migrated $($f.Name)"
}
