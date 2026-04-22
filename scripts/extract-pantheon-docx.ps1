# Extract plain text from .docx (OOXML) and copy embedded media to output folder.
param(
  [Parameter(Mandatory = $true)][string]$DocxPath,
  [Parameter(Mandatory = $true)][string]$OutTextPath,
  [string]$MediaDestDir = ""
)

Add-Type -AssemblyName System.IO.Compression.FileSystem

function Get-DocxPlainText {
  param([string]$Path)
  $zip = [System.IO.Compression.ZipFile]::OpenRead($Path)
  try {
    $entry = $zip.GetEntry("word/document.xml")
    if (-not $entry) { return "" }
    $sr = New-Object System.IO.StreamReader($entry.Open())
    $xml = $sr.ReadToEnd()
    $sr.Close()
    $doc = [xml]$xml
    $ns = New-Object System.Xml.XmlNamespaceManager($doc.NameTable)
    $ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")
    $paras = $doc.SelectNodes("//w:p", $ns)
    $lines = foreach ($p in $paras) {
      $ts = $p.SelectNodes(".//w:t", $ns)
      if ($ts.Count -eq 0) { continue }
      ($ts | ForEach-Object { $_.InnerText }) -join ""
    }
    return ($lines -join "`n")
  }
  finally {
    $zip.Dispose()
  }
}

function Copy-DocxMedia {
  param([string]$Path, [string]$DestDir)
  if (-not (Test-Path $DestDir)) { New-Item -ItemType Directory -Path $DestDir -Force | Out-Null }
  $zip = [System.IO.Compression.ZipFile]::OpenRead($Path)
  try {
    foreach ($e in $zip.Entries) {
      if ($e.FullName -like "word/media/*" -and $e.FullName -notlike "*/") {
        $name = Split-Path $e.FullName -Leaf
        $target = Join-Path $DestDir $name
        $out = [System.IO.File]::Create($target)
        try {
          $ein = $e.Open()
          try { $ein.CopyTo($out) } finally { $ein.Dispose() }
        }
        finally { $out.Dispose() }
      }
    }
  }
  finally {
    $zip.Dispose()
  }
}

$text = Get-DocxPlainText -Path $DocxPath
$dir = Split-Path $OutTextPath -Parent
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
[System.IO.File]::WriteAllText($OutTextPath, $text, [System.Text.UTF8Encoding]::new($false))

if ($MediaDestDir) {
  Copy-DocxMedia -Path $DocxPath -DestDir $MediaDestDir
}
