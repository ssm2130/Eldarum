$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$dir = Join-Path $root "assets\images"
New-Item -ItemType Directory -Force -Path $dir | Out-Null

$pairs = @(
  @{ Name = "medieval-city-walls.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/f/f9/Walls_of_Dubrovnik%2C_Croatia_-_Diliff.jpg" }
  @{ Name = "mountain-peaks.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/4/4f/Monte_Rosa_summit.jpg" }
  @{ Name = "storm-coast.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/e/e9/Lightning_over_Oradea_Romania_3.jpg" }
  @{ Name = "volcano-crater.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/7/7e/Halemaumau_crater_lava_lake_with_Kilauea_caldera_and_Mauna_Loa.jpg" }
  @{ Name = "ancient-ruins.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/5/54/Tikal_Temple_IV.jpg" }
  @{ Name = "forest-road.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/8/84/Forest_path_near_Schwilper_Germany.jpg" }
  @{ Name = "harbor-ships.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/6/6d/Plymouth_Devon_UK_harbour_from_the_Hoe.jpg" }
  @{ Name = "parchment-map-bg.jpg"; Url = "https://upload.wikimedia.org/wikipedia/commons/5/5c/Old_map_of_the_world.jpg" }
)

foreach ($p in $pairs) {
  $out = Join-Path $dir $p.Name
  try {
    Start-Sleep -Seconds 2
    $client = New-Object System.Net.WebClient
    $client.Headers.Add("User-Agent", "EldarumWikiSetup/1.0 (local campaign wiki; educational)")
    $client.DownloadFile($p.Url, $out)
    Write-Host "OK $($p.Name)"
  } catch {
    Write-Host "FAIL $($p.Name): $_"
  }
}
