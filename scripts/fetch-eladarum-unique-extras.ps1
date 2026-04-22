# Downloads 17 additional CC / PD images for unique <img> usage across the Eldarum site.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$dest = Join-Path $root "assets\images\photo"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

function Get-CommonsDownloadUrl([string]$fileTitle) {
  $enc = [uri]::EscapeDataString($fileTitle)
  # Prefer scaled thumbnail (lighter request; fewer 429s than full originals).
  $uri = "https://commons.wikimedia.org/w/api.php?action=query&titles=$enc&prop=imageinfo&iiprop=url&iiurlwidth=1400&format=json"
  $r = Invoke-RestMethod -Uri $uri -UserAgent "EldarumWikiFetch/1.0 (local D&D wiki)"
  foreach ($prop in $r.query.pages.PSObject.Properties) {
    $page = $prop.Value
    if (-not $page.missing -and $page.imageinfo -and $page.imageinfo.Count -gt 0) {
      $ii = $page.imageinfo[0]
      if ($ii.thumburl) { return $ii.thumburl }
      return $ii.url
    }
  }
  return $null
}

$pairs = @(
  @{ out = "eld-extra-01.jpg"; title = "File:West Hoe Harbour (1).jpg" },
  @{ out = "eld-extra-02.jpg"; title = "File:2017-Halemaumau-lava-lake.jpg" },
  @{ out = "eld-extra-03.jpg"; title = "File:Plymouth , Hoe Road and Plymouth Sound - geograph.org.uk - 1178288.jpg" },
  @{ out = "eld-extra-04.jpg"; title = "File:Tikal Temple IV, 2022 01.jpg" },
  @{ out = "eld-extra-05.jpg"; title = "File:Lothar Path - Black Forest National Park - Root plate 01.jpg" },
  @{ out = "eld-extra-06.jpg"; title = "File:Lightning over Oradea Romania 3.jpg" },
  @{ out = "eld-extra-07.jpg"; title = "File:Panorama Monte Rosa Hut 1.jpg" },
  @{ out = "eld-extra-08.jpg"; title = "File:Morocco Africa Flickr Rosino December 2005 84514010 edited by Buchling.jpg" },
  @{ out = "eld-extra-09.jpg"; title = "File:Halong Bay in Vietnam.jpg" },
  @{ out = "eld-extra-10.jpg"; title = "File:Iceberg in the Arctic with its underside exposed.jpg" },
  @{ out = "eld-extra-11.jpg"; title = "File:Iceland - 2017-02-22 - Gullfoss - 3684.jpg" },
  @{ out = "eld-extra-12.jpg"; title = "File:Tromso banner Aurora Borealis.jpg" },
  @{ out = "eld-extra-13.jpg"; title = "File:Markus Tower, Rothenburg ob der Tauber.jpg" },
  @{ out = "eld-extra-14.jpg"; title = "File:Schloss Neuschwanstein 2013.jpg" },
  @{ out = "eld-extra-15.jpg"; title = "File:GoldenGateBridge BakerBeach MC.jpg" },
  @{ out = "eld-extra-16.jpg"; title = "File:Panorama der Reisterrassen von Banaue, Philippinen.jpg" },
  @{ out = "eld-extra-17.jpg"; title = "File:Petra Jordan BW 21.JPG" }
)

foreach ($p in $pairs) {
  $outPath = Join-Path $dest $p.out
  if (Test-Path -LiteralPath $outPath) {
    Write-Host "Skip existing $($p.out)"
    continue
  }
  Write-Host "Resolve $($p.title) ..."
  $url = Get-CommonsDownloadUrl $p.title
  if (-not $url) {
    Write-Warning "Missing on Commons: $($p.title)"
    continue
  }
  Start-Sleep -Seconds 45
  Invoke-WebRequest -Uri $url -OutFile $outPath -UserAgent "EldarumWikiFetch/1.0 (local D&D wiki)" -TimeoutSec 180
  Write-Host "Saved $($p.out)"
}

Write-Host "Done."
