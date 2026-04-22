$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$outPath = Join-Path $here "journal.html"

$digest = Get-Content (Join-Path $here "_journal_digest_fragment.html") -Raw -Encoding UTF8

$head = @'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <meta name="description" content="Asceveron campaign journal — full narrative chronicle: arcs, scenes, and tier roadmap in readable prose."/>
  <title>Campaign journal - Asceveron - Eldarum</title>
  <link rel="stylesheet" href="../../css/eladarum.css"/>
  <style>
    .journal-toc ol { column-width: 18em; column-gap: 2em; }
    .prose .journal-dl dt { font-weight: 600; margin-top: 0.75em; }
    .prose .journal-dl dd { margin: 0.25em 0 0 1em; }
  </style>
</head>
<body data-root="../../" data-section="campaign" data-bc-labels="Home|Campaign archive|Campaign journal" data-bc-hrefs="index.html|pages/campaign/index.html">
  <header class="app-header">
    <button type="button" class="menu-toggle" data-sidebar-toggle aria-expanded="false" aria-label="Open navigation">Menu</button>
    <div class="app-header__brand"><a href="../../index.html" style="color:inherit;text-decoration:none"><strong>Eldarum</strong></a><span>Campaign</span></div>
    <div class="header-search"><input id="site-search" type="search" placeholder="Search..." aria-label="Search"/><div id="search-results" class="search-dropdown"></div></div>
  </header>
  <div class="breadcrumb-strip"><nav id="breadcrumb-target"></nav></div>
  <div class="backdrop" data-sidebar-backdrop></div>
  <div class="shell">
    <aside class="sidebar" id="sidebar-target"></aside>
    <main class="main" id="main">
      <article>
        <header class="article-header">
          <h1>Campaign journal — Asceveron</h1>
          <p class="dek">Narrative chronicle from integrated session prep and planning notes: scene-level prose for major arcs (not bullet summaries). Mechanics appear inline where they clarify stakes. Companions: <a href="index.html">Roll20 archive hub</a> · ordered <a href="../history/asceveron-grand-chronicle.html">Grand chronicle</a> (timeline spine).</p>
          <div class="callout"><strong>Note:</strong> Third-party <em>Critical Role</em> pacing notes are not reproduced. Spellings vary across drafts (Anoceth/Anocheth, Flavious/Flavius).</div>
        </header>

'@

$foot = @'

          <p>Return to <a href="index.html">Campaign archive hub</a> &middot; <a href="../npcs-notable.html">Notable people</a> &middot; <a href="../../index.html">Site home</a></p>

          <div class="tag-row"><span class="tag">Journal</span><span class="tag">Asceveron</span><span class="tag">GM notes</span></div>
        </div>
      </article>
      <footer class="site-footer"></footer>
    </main>
  </div>
  <script src="../../js/chrome.js" defer></script>
</body>
</html>
'@

$middle = $digest.TrimEnd() + "`n"

$full = $head + $middle + $foot
[IO.File]::WriteAllText($outPath, $full, [Text.UTF8Encoding]::new($false))

$c = [IO.File]::ReadAllText($outPath, [Text.Encoding]::UTF8)
$triple = "$([char]0x00E2)$([char]0x20AC)$([char]0x201D)"
if ($c.Contains($triple)) {
  $em = [string][char]0x2014
  $c = $c.Replace($triple, $em)
  [IO.File]::WriteAllText($outPath, $c, [Text.UTF8Encoding]::new($false))
}

Write-Host "Wrote" $outPath ((Get-Item $outPath).Length) "bytes"
