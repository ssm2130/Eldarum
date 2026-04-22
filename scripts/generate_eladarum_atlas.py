#!/usr/bin/env python3
"""
Generates expanded atlas location pages under pages/atlas/.
Run from repo root (Webpage folder): python scripts/generate_eladarum_atlas.py
"""
from __future__ import annotations

import json
import os
import textwrap

WEBROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS_DIR = os.path.join(WEBROOT, "pages", "atlas")


def shell(
    *,
    depth: int,
    section: str,
    bc_labels: list[str],
    bc_hrefs: list[str],
    title: str,
    description: str,
    inner: str,
) -> str:
    root = "../" * depth
    labels = "|".join(bc_labels)
    hrefs = "|".join(bc_hrefs)
    desc_tag = f'<meta name="description" content="{description[:220]}"/>' if description else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  {desc_tag}
  <title>{title} — Eldarum Atlas</title>
  <link rel="stylesheet" href="{root}css/eladarum.css"/>
</head>
<body
  data-root="{root}"
  data-section="{section}"
  data-bc-labels="{labels}"
  data-bc-hrefs="{hrefs}">
  <header class="app-header">
    <button type="button" class="menu-toggle" data-sidebar-toggle aria-expanded="false" aria-label="Open navigation">Menu</button>
    <div class="app-header__brand">
      <a href="{root}index.html" style="color:inherit;text-decoration:none"><strong>Eldarum</strong></a>
      <span>Atlas</span>
    </div>
    <div class="header-search">
      <input id="site-search" type="search" placeholder="Search the atlas…" autocomplete="off" aria-label="Search"/>
      <div id="search-results" class="search-dropdown"></div>
    </div>
  </header>
  <div class="breadcrumb-strip" id="breadcrumb-root"><nav id="breadcrumb-target" aria-label="Breadcrumb"></nav></div>
  <div class="backdrop" data-sidebar-backdrop></div>
  <div class="shell">
    <aside class="sidebar" id="sidebar-target" aria-label="Section navigation"></aside>
    <main class="main">
      <article>
        <header class="article-header">
          <h1>{title}</h1>
          <p class="dek">{description}</p>
        </header>
        <div class="prose">
{inner}
        </div>
      </article>
      <footer class="site-footer">Eldarum setting material — expanded gazetteer. Primary campaign notes centered on Thrennora / Asceveron; other continents developed for global context.</footer>
    </main>
  </div>
  <script src="{root}js/chrome.js" defer></script>
</body>
</html>
"""


def prose_sections(sections: list[dict]) -> str:
    chunks: list[str] = []
    for sec in sections:
        h2 = sec.get("h2", "")
        if h2:
            chunks.append(f"          <h2>{h2}</h2>")
        for p in sec.get("p", []):
            chunks.append(f"          <p>{p}</p>")
        for ul in sec.get("ul", []):
            chunks.append("          <ul>")
            for li in ul:
                chunks.append(f"            <li>{li}</li>")
            chunks.append("          </ul>")
    return "\n".join(chunks)


CONTINENTS: list[dict] = [
    {
        "id": "thrennora",
        "title": "Thrennora",
        "slug": "thrennora",
        "dek": "The Greywake cradle: Stammont, Zrelia, Asceveron, and the wars that rehearse tomorrow's navy.",
        "keywords": "thrennora northwake stammont zrelia asceveron greywake sea",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "Thrennora is Eldarum's northwestern continent-segment: a tilted shield of peninsulas, storm-scoured narrows, and river arteries feeding Collimar's basin. Most travelers simply call it the Northwake—books use Thrennora when treaties need grander vowels.",
                    "Your campaign has lived here longest: supply columns, frontier forts, Black Tusk raids, and Asceveron's layered intrigues are local weather. Elsewhere in Eldarum reads Thrennora through trade wind and rumor—never through indifference.",
                ],
            },
            {
                "h2": "Nations & tensions",
                "p": [
                    "The Stammont Kingdom anchors the interior with grain law and royal highways; Zrelia watches from across the Greywake with admiralties and auguries; Asceveron sits where charters fray into opportunity. Piracy wears grey wolf colors in ballads; crowns wear denial in council chambers.",
                ],
            },
            {
                "h2": "Canonical touchstones",
                "ul": [
                    "<strong>Stammont</strong> — crown at Collimar; veterans' roads to Minwall, Greiser, Towfort.",
                    "<strong>Zrelia</strong> — rival fleets and prophecy courts across the straits.",
                    "<strong>Asceveron</strong> — frontier march where patronage, Titan talk, and Zehas ash rewrite agendas nightly.",
                    "<strong>Darkshore & Baycliff</strong> — fortresses and listeners; sea keeps its receipts.",
                ],
            },
            {
                "h2": "Travel themes",
                "p": [
                    "Expect mud honest enough to ruin poetry, bells honest enough to ruin sleep, and storm chapels honest enough to ruin excuses. Titan remnants in the Highfold peaks attract scholars, mercenaries, and things that mistake prayer for provocation.",
                ],
            },
        ],
    },
    {
        "id": "sverge",
        "title": "Sverge",
        "slug": "sverge",
        "dek": "Central continent of codified roads, metric ambition, and the Republic whose maps your table once imported wholesale.",
        "keywords": "sverge republic senate roads empire central",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "Sverge rises from warm interior seas like a lesson in geometry: grids where other realms accept curves. The Sverge Republic—named on old expedition maps you preserved—styles itself a federation of charter cities bound by rail, canal, and mercantile clock-time.",
                    "Thrennora traders describe Sverge goods as 'too perfect': identical ceramics, interchangeable officials, opera with identical intermissions. Admirers call it civilization; skeptics call it rehearsal.",
                ],
            },
            {
                "h2": "The Republic",
                "p": [
                    "Power splits between a rotating Senate of Land and a Maritime Syndicate whose admirals wear civilian waistcoats on purpose. Laws export neatly; revolutions import messily—revolutionary pamphlets from Thrennora sometimes arrive water-stained but enthusiastic.",
                ],
            },
            {
                "h2": "At the table",
                "p": [
                    "Use Sverge when you want clockwork intrigue, museum heists, or trains that pretend gods don't matter. Titan Wars strata here are buried under civic foundations—excavation permits require three hymns and a notarized apology.",
                ],
            },
        ],
    },
    {
        "id": "vaelstrom",
        "title": "Vaelstrom Archipelago",
        "slug": "vaelstrom-archipelago",
        "dek": "Ten thousand islands arguing with tides; Kazon's cousins; pirate mathematics; storm-saints on skiffs.",
        "keywords": "vaelstrom archipelago kazon pirates islands greywake",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "West of Thrennora, the Vaelstrom Archipelago scatters across furnace-blue water like shattered mirrors. Navigation relies on reef-lore, lantern grammar, and bribes paid to currents. The free port of Kazon—your voyagers know its name—belongs politically nowhere and practically everywhere.",
                ],
            },
            {
                "h2": "Culture of ropes",
                "p": [
                    "Island republics mint tokens out of crushed coral and nerve. Storm Court chapel-boats tie up beside taverns that serve thunder-clap rum; funeral processions sometimes trail behind hurricanes on purpose—symbolism matters more than dry clothes.",
                ],
            },
            {
                "h2": "Why it matters to Asceveron",
                "p": [
                    "Every embargo Asceveron dodges ends here as gossip. Corsairs rebrand as couriers when letters smell like crowns. Shards sought by wandering philosophers wash up as beach glass that hums—some traders swear oaths on it; others swear at it.",
                ],
            },
        ],
    },
    {
        "id": "orunsul",
        "title": "Orunsul",
        "slug": "orunsul",
        "dek": "Sun-scar wastes, buried aqueducts, and god-markets where dawn lasts until someone pays the bill.",
        "keywords": "orunsul desert oasis salt sun wastes",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "South-central Eldarum dries into Orunsul—dune seas interrupted by kiln cities, salt flats that remember oceans, and oases groomed like temples. Water rights fuel wars lighter than air and heavier than crowns.",
                ],
            },
            {
                "h2": "Faith economies",
                "p": [
                    "Solar aspects of the Veiled Pantheon dominate here: the Forge Twins' forges burn charcoal made from blessed thorns; the Mirror Sovereign's shrines sell reflective tiles said to dupe scorpion spirits.",
                    "Titan Wars left glass deserts where sand fused mid-battle—prospectors mine 'war glass' for lenses that reveal invisible ink or invisible guilt depending on moon phase.",
                ],
            },
        ],
    },
    {
        "id": "kharros",
        "title": "Kharros Mantle",
        "slug": "kharros-mantle",
        "dek": "High steppe, reindeer currencies, and sky burial roads that ignore borders drawn by drunk cartographers.",
        "keywords": "kharros steppe tundra nomad sky burial",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "The Kharros Mantle rolls eastward in grass oceans and black-soil braids—continents of motion more than stone. Khanates rise and fall between festivals; borders last until the next thaw.",
                ],
            },
            {
                "h2": "Spirits of horizon",
                "p": [
                    "Genius loci manifest as persistent winds with names invited into tents. Titan shards surface as meteoric iron worshipped as 'fallen arguments'—smiths forge blades that ring specific notes when justice is nearby (or when drama sells tickets).",
                ],
            },
            {
                "h2": "Foreign boots",
                "p": [
                    "Stammont officers train here against mounted archers when budgets allow; Zrelian admirals pretend they don't hire Kharros navigators who read stars like debt ledgers.",
                ],
            },
        ],
    },
    {
        "id": "meloxis",
        "title": "Meloxis",
        "slug": "meloxis",
        "dek": "Rainforest continent of vertical rivers, ladder-towns, and gods who wear pollen as armor.",
        "keywords": "meloxis jungle river verdant southern",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "Meloxis eats cartographers. Canopies fold sunlight into green libraries; rivers climb cliffs on roots trained over centuries. Nations here measure wealth in seeds, venom catalogs, and callable favors from things older than taxonomy.",
                ],
            },
            {
                "h2": "Cosmology at ground level",
                "p": [
                    "Titan Wars buried themselves in biomass: massive rib-arches become bridges; fungal towers pulse when storms argue offshore. The Silent Arbiter's monks trek Meloxis with sealed masks—not for plague, for sympathy: too many spirits remember mourners' faces.",
                ],
            },
            {
                "h2": "Trade",
                "p": [
                    "Spice runs north; steel runs south; scholars run out of adjectives. Asceveron's intrigues import Meloxis poisons disguised as perfumes—customs dogs sneeze prophecies.",
                ],
            },
        ],
    },
]


def templated_place(
    continent_id: str,
    continent_title: str,
    slug_suffix: str,
    title: str,
    dek: str,
    keywords: str,
    flavor: str,
) -> dict:
    """Auto body sections for bulk-generated locales."""
    return {
        "slug": f"{continent_id}--{slug_suffix}",
        "title": title,
        "continent": continent_id,
        "dek": dek,
        "keywords": keywords,
        "sections": [
            {
                "h2": "Snapshot",
                "p": [
                    f"{flavor}",
                    f"Situated within {continent_title}, {title} enters foreign correspondence as rumor before it enters ledgers as fact. Merchants tack on surcharges labeled 'story risk.'",
                ],
            },
            {
                "h2": "People & trade",
                "p": [
                    "Guild charters overlap temple leases; inheritance squabbles hire poets before lawyers. Markets smell of metal, citrus peel, and whichever god claims the next holiday.",
                    "Visitors often mistake politeness for surrender—locals mistake optimism for currency. Both sides profit until someone mentions Titans.",
                ],
            },
            {
                "h2": "Secrets under the stones",
                "p": [
                    "Pre-Compact foundations occasionally hum when storms align; cellar taverns sell maps to cellars beneath those cellars. Children dare each other to sleep on certain flagstones—dreamers wake bilingual in languages churches won't ordain.",
                ],
            },
        ],
    }


# Explicit deep entries (canonical + narrative bridges)
SPECIAL_PLACES: list[dict] = [
    {
        "slug": "thrennora--asceveron-marches",
        "title": "Asceveron Marches",
        "continent": "thrennora",
        "dek": "Frontier peninsula where your table's secrets stack like cordwood: patents, prophecies, and Titan rumors.",
        "keywords": "asceveron frontier kul buldar zehas storm court amara",
        "sections": [
            {
                "h2": "Why the world watches",
                "p": [
                    "Asceveron is concentration of story not because Eldarum lacks elsewhere—but because here crowns blur, storms answer petitions, and patrons like Kul Buldar bank expeditions toward Zehas ash and mountain ossuaries alike.",
                    "Divine attention spikes: seekers investigate how gods exert power through Asceveron's temples without owning the deed. Storm Court banners fray faster here; lightning strikes twice as theatrically.",
                ],
            },
            {
                "h2": "Campaign anchors",
                "ul": [
                    "<strong>Kazon routes</strong> — grey-market harbors when guild wars choke nearer ports.",
                    "<strong>Zehas Volcano</strong> — geological priest; ash seasons fertilize plots and lung ailments equally.",
                    "<strong>Titan remains</strong> — patron-financed digs flirt with archaeology and arson.",
                    "<strong>Baycliff listeners</strong> — espionage traded like smoked fish.",
                ],
            },
            {
                "h2": "Atmosphere",
                "p": [
                    "Fog carries brass snares of harbor jazz from illegal clarinets; bureaucrats stamp passports with perfumes meant to repel scrying. Everyone insists they're minor characters—then buys a bigger hat.",
                ],
            },
        ],
    },
    {
        "slug": "thrennora--stammont-realm",
        "title": "Stammont Realm",
        "continent": "thrennora",
        "dek": "Hereditary monarchy seated at Collimar: grain law, sea dread, and bells that ring accusations.",
        "keywords": "stammont kingdom collimar army darkshore julian welles",
        "sections": [
            {
                "h2": "Realm overview",
                "p": [
                    "Stammont maps like a nervous circulatory system—rivers as arteries, forts as clots nobody admits needing. Royal highways pretend order; forest roads pretend romance; supply trains pretend they're not prayer wheels for economists.",
                ],
            },
            {
                "h2": "Sites your players know by heart",
                "ul": [
                    "<strong>Collimar</strong> — capital courts, curse clinics, harbor pilots who negotiate futures.",
                    "<strong>Darkshore</strong> — batteries rehearsing war with Zrelia.",
                    "<strong>Minwall & Greiser</strong> — riverborn towns feeding sagas and logistics.",
                    "<strong>Towfort</strong> — hinge against Black Tusk pressure.",
                    "<strong>Sanfeld</strong> — orchards tied to veterans' softer memories.",
                ],
            },
            {
                "h2": "Foreshadowing",
                "p": [
                    "Spy rings worry Zrelian bells; chapels worry Storm omens; veterans worry dreams where supply fires never cool. Stammont thinks borders—Titans think seams.",
                ],
            },
        ],
    },
    {
        "slug": "thrennora--zrelian-coalition",
        "title": "Zrelian Coalition Shores",
        "continent": "thrennora",
        "dek": "Across the Greywake: admiralties, tide-clocks, and prophecies sold by the crate.",
        "keywords": "zrelia fleet admiral prophecy mirror reach",
        "sections": [
            {
                "h2": "Overview",
                "p": [
                    "Zrelia speaks in naval cadence—sentences crest and break. Harbor magnates share power with storm-temple colleges whose lightning readers charge consultation fees competitive with torture.",
                ],
            },
            {
                "h2": "Friction with Stammont",
                "p": [
                    "Fishing rights masquerade as destiny; tariffs masquerade as theology. Everyone trains boarding parties against everyone else's boarding parties—peace becomes a breathing exercise performed between disasters.",
                ],
            },
        ],
    },
    {
        "slug": "vaelstrom--kazon-free-harbor",
        "title": "Kazon Free Harbor",
        "continent": "vaelstrom",
        "dek": "Grey-market island city where jurisdiction is rented by the tide.",
        "keywords": "kazon harbor pirates sazi asnaes greywake",
        "sections": [
            {
                "h2": "Harbor logic",
                "p": [
                    "Kazon stacks jurisdictions like chips—Stammont law Monday, Zrelian admiralty Tuesday, independent absurdity weekends. Payment houses like Asnaes underwrite risky manifests; captains rename ships between moorings to spite creditors.",
                ],
            },
            {
                "h2": "Stories nested here",
                "p": [
                    "Former voyages paired with figures such as Sazi linger in dockside verses—routes shift, but Kazon remains the place you go when 'forward' means 'off the record.'",
                ],
            },
        ],
    },
    {
        "slug": "thrennora--zehas-volcanic-arc",
        "title": "Zehas Volcanic Arc",
        "continent": "thrennora",
        "dek": "Ash seasons, lava theology, and climbs patronized by anyone who mistakes adrenaline for destiny.",
        "keywords": "zehas volcano ash climb kul buldar titans",
        "sections": [
            {
                "h2": "Fire geography",
                "p": [
                    "Zehas anchors a chain of cones stewing cloud color into apocalyptic romance. Vineyards gamble on ash; lungs gamble on masks; shrines gamble on synchronized hymns during tremors.",
                ],
            },
            {
                "h2": "Expedition culture",
                "p": [
                    "Financiers bundle climbs with relic insurance and poets-for-hire who translate terror into investor updates. Every summit argues with the last about what counts as 'neutral' Titan behavior.",
                ],
            },
        ],
    },
]


# Bulk templates — mix titles per continent
BULK: dict[str, list[tuple[str, str, str]]] = {
    "thrennora": [
        ("collimar-crown-district", "Collimar Crown District", "Palace lattice, cipher vaults, and lawyers who quote thunder."),
        ("velen-barge-measure", "Velen Barge Measure", "Floating market courts where grain futures smell like river rain."),
        ("ostro-timber-barony", "Ostro Timber Barony", "Axe-bitumen roads; logging saints; debts measured in trees."),
        ("mir-river-oracles", "Mir River Oracle Steps", "Fog stairs where petitioners mishear omens productively."),
        ("highfold-titan-stairs", "Highfold Titan Stairs", "Switchback shrines debating whether peaks are sculptures or sentences."),
        ("greywake-signal-chain", "Greywake Signal Chain", "Island towers whose lantern grammar predates admiralties."),
        ("mirror-reach-silt", "Mirror Reach Silt Banks", "Shallow gold where dredgers find crowns and conscience."),
        ("timberwild-ranger-mark", "Timberwild Ranger Marks", "Blaze codes argued over by rangers, orcs, and poets."),
        ("fiadh-march", "Fiadh March", "Misty border cantons named in traveler songs—watchers favor wolves."),
        ("duinn-sleibhe-barrows", "Duinn Sléibhe Barrows", "Hill tombs where shepherds swear shadows rehearse verse."),
        ("stilicho-exchange", "Stilicho Exchange", "Marble arcade where mercantile drama imports opera budgets."),
        ("vishran-bazaar-stairs", "Vishran Bazaar Stairs", "Spice tiers selling silence alongside cardamom."),
    ],
    "sverge": [
        ("republic-senate-spire", "Senate Spire of Varn", "Glass dome debates; echo policies until populists cough."),
        ("canal-ledger-district", "Canal Ledger District", "Tax barges pulled by choir-trained horses—allegedly."),
        ("metric-glassworks", "Metric Glassworks", "Standard lenses; standardized lies; gorgeous windows."),
        ("old-sverge-cathedral-arc", "Old Sverge Cathedral Arc", "Pre-Republic arches wearing modern shame."),
        ("saltmarsh-automata-yard", "Saltmarsh Automata Yard", "Clock guardians rusting politely near tourist queues."),
        ("express-rails-east", "Eastern Express Rails", "Lines sprinting toward frontiers engineers deny emotionally."),
        ("museum-of-compacts", "Museum of Imperial Compacts", "Treaties displayed as art; thieves steal definitions."),
        ("citadel-of-weights", "Citadel of Weights", "Brass scales big enough to judge nations metaphorically."),
        ("veldt-silk-exchange", "Veldt Silk Exchange", "Worms pampered like royalty; silk priced like prophecy."),
        ("obsidian-arbitration-hall", "Obsidian Arbitration Hall", "Black glass tables; white gloves; red outcomes."),
        ("seventh-canal-hospice", "Seventh Canal Hospice", "Patients healed by regimented kindness and barged sunlight."),
        ("republic-marine-atelier", "Republic Marine Atelier", "Ship models tested in miniature wars—fish volunteer."),
    ],
    "vaelstrom": [
        ("storm-saint-skerry", "Storm Saint Skerry", "Rock chapel where lightning leaves benedictions scorched into stone."),
        ("coral-notary-ring", "Coral Notary Ring", "Reefs hosting contracts barnacle-sealed."),
        ("grey-market-lagoon", "Grey Market Lagoon", "Floating stalls selling identities damp but legal-ish."),
        ("salt-abbey-chain", "Salt Abbey Chain", "Monks who pray brine into bread—results vary by tide."),
        ("petrel-throne-isles", "Petrel Throne Isles", "Democracies of seabirds taken seriously by locals."),
        ("kelp-scriptorium", "Kelp Scriptorium", "Archives woven underwater; readers hold breath and grudges."),
        ("mirage-auction-cay", "Mirage Auction Cay", "Sales occur twice—once in heat, once in regret."),
        ("blackwake-dive-shrine", "Blackwake Dive Shrine", "Priests greet leviathan dreams with brass bells."),
        ("ember-tide-foundry", "Ember Tide Foundry", "Volcanic vents rented to smiths seasonally."),
        ("chartwright-guildhall", "Chartwright Guildhall", "Maps sold with apologies attached as appendices."),
    ],
    "orunsul": [
        ("qalam-basin-cities", "Qalam Basin Cities", "Stepwell palaces; poetry duels; water knives."),
        ("glass-desert-ledger", "Glass Desert Ledger Markets", "War-glass coins that cut palms when lies trade hands."),
        ("sunforge-anvil-dome", "Sunforge Anvil Dome", "Forge Twins cathedral where dawn is smelted."),
        ("salt-serpent-canals", "Salt Serpent Canals", "Brine locks engineered by stubborn mathematicians."),
        ("mirage-court-tents", "Mirage Court Tents", "Judges wear veils thicker than law."),
        ("ossuary-dune-stairs", "Ossuary Dune Stairs", "Spiral climbs where bones narrate Titan retreats."),
        ("cinder-library-wells", "Cinder Library Wells", "Scrolls lowered for cooling; wisdom tastes like ash."),
        ("azure-sink-harbors", "Azure Sink Harbors", "Ports in sinkholes where ships descend politely."),
        ("obsidian-saint-procession", "Obsidian Saint Procession", "Annual march leaving glass footprints tourists mimic."),
    ],
    "kharros": [
        ("sky-burial-road", "Sky Burial Road", "Elevated causeways where offerings ride wind instead of hearses."),
        ("meteor-anvil-khanate", "Meteor Anvil Khanate", "Smith-khans forge from sky-iron 'arguments.'"),
        ("reed-sea-nomad-fairs", "Reed Sea Nomad Fairs", "Temporary cities stitched from grass and gossip."),
        ("white-wolf-calendar-stone", "White Wolf Calendar Stone", "Menhir courts scheduling raids like harvests."),
        ("throat-singing-citadel", "Throat-Singing Citadel", "Keeps where resonance shatters dishonest armor."),
        ("glacier-merchant-tunnels", "Glacier Merchant Tunnels", "Ice highways maintaining trade during spiteful winters."),
        ("steppe-oracle-knot", "Steppe Oracle Knot", "Rope libraries predicting weather via tension."),
        ("bone-bridge-estates", "Bone Bridge Estates", "Arches of ancient beasts repurposed as tax offices."),
        ("black-soil-compact", "Black Soil Compact Markets", "Grain futures mixed with blood oaths—literally."),
    ],
    "meloxis": [
        ("ladder-town-vines", "Ladder Town of Vines", "Vertical streets; lawsuits about altitude."),
        ("poison-perfume-houses", "Poison Perfume Houses", "Assassins and aesthetes share consultants."),
        ("river-root-cathedrals", "River Root Cathedrals", "Sanctuary roots drinking theology from water."),
        ("mosquito-crown-arena", "Mosquito Crown Arena", "Duels staged when insects eclipse sun—symbolism brutal."),
        ("verdant-necropolis", "Verdant Necropolis", "Tombs blooming rare orchids fertilized by epitaphs."),
        ("amber-spire-archive", "Amber Spire Archive", "Sap-sealed texts; scholars allergic to nostalgia."),
        ("jungle-compass-order", "Jungle Compass Order", "Monks who navigate by pollen ethics."),
        ("scaled-market-canals", "Scaled Market Canals", "Fishmongers bargain with river spirits openly."),
        ("sunfall-orchid-war", "Sunfall Orchid War Memorial", "Flowers tied to battles botanists still debate."),
    ],
}


def build_bulk() -> list[dict]:
    out: list[dict] = []
    for cid, entries in BULK.items():
        ctitle = next(c["title"] for c in CONTINENTS if c["id"] == cid)
        for slug_suf, title, flavor in entries:
            out.append(
                templated_place(
                    cid,
                    ctitle,
                    slug_suf,
                    title,
                    f"{title} — regional notes from the {ctitle} gazetteer.",
                    f"{slug_suf.replace('-', ' ')} {cid} eldarum atlas",
                    flavor,
                )
            )
    return out


def write_page(path: str, html: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def continent_bc(c: dict) -> tuple[list[str], list[str]]:
    labels = ["Home", "Atlas", c["title"]]
    hrefs = ["index.html", "pages/atlas/index.html"]
    return labels, hrefs


def place_bc(title: str) -> tuple[list[str], list[str]]:
    labels = ["Home", "Atlas", title]
    hrefs = ["index.html", "pages/atlas/index.html"]
    return labels, hrefs


def main() -> None:
    search_pages: list[dict] = []

    # Atlas index
    labels = ["Home", "Atlas"]
    hrefs = ["index.html"]
    continents_cards = "".join(
        f"""
      <a class="card" href="{c['slug']}.html">
        <div class="card__meta">{c['title']}</div>
        <h3>{c['title']}</h3>
        <p>{c['dek']}</p>
      </a>"""
        for c in CONTINENTS
    )
    atlas_index_inner = f"""
          <p class="lead" style="font-size:1.15rem;color:var(--muted);margin-bottom:2rem">
            Six continental visions structure Eldarum. Thrennora holds your longest-running story; the others widen the lens—trade winds, Titan strata, and wars fought in heaven with mortal receipts.
          </p>
          <div class="card-grid">
            {continents_cards}
          </div>
          <h2>Reading this atlas</h2>
          <p>Use the sticky breadcrumb trail and left navigation (desktop) or menu button (narrow screens) to stay oriented. Search spans generated locales, faith articles, and the legacy Northwake gazetteer.</p>
          <blockquote>Every pin on a map pays rent to whoever tells the story loudest.</blockquote>
    """
    atlas_index_html = shell(
        depth=1,
        section="atlas",
        bc_labels=labels,
        bc_hrefs=hrefs,
        title="Continental Atlas",
        description="Six continents of Eldarum with linked regional articles.",
        inner=atlas_index_inner,
    )
    write_page(os.path.join(ATLAS_DIR, "index.html"), atlas_index_html)
    search_pages.append(
        {
            "title": "Continental Atlas",
            "href": "pages/atlas/index.html",
            "keywords": "atlas continents eldarum map overview six",
        }
    )

    # Continent hubs
    for c in CONTINENTS:
        labs, hrefs = continent_bc(c)
        inner = (
            prose_sections(c["sections"])
            + '\n          <div class="tag-row"><span class="tag">Continent</span><span class="tag">'
            + c["title"]
            + "</span></div>"
        )
        html = shell(
            depth=1,
            section="atlas",
            bc_labels=labs,
            bc_hrefs=hrefs,
            title=c["title"],
            description=c["dek"],
            inner=inner,
        )
        write_page(os.path.join(ATLAS_DIR, f"{c['slug']}.html"), html)
        search_pages.append(
            {
                "title": c["title"],
                "href": f"pages/atlas/{c['slug']}.html",
                "keywords": c["keywords"],
            }
        )

    all_places = SPECIAL_PLACES + build_bulk()
    for place in all_places:
        labs, hrefs = place_bc(place["title"])
        inner = prose_sections(place["sections"])
        inner += '\n          <div class="tag-row"><span class="tag">Locale</span><span class="tag">' + place[
            "continent"
        ].title() + "</span></div>"
        fname = place["slug"] + ".html"
        html = shell(
            depth=1,
            section="atlas",
            bc_labels=labs,
            bc_hrefs=hrefs,
            title=place["title"],
            description=place["dek"],
            inner=inner,
        )
        write_page(os.path.join(ATLAS_DIR, fname), html)
        search_pages.append(
            {
                "title": place["title"],
                "href": f"pages/atlas/{fname}",
                "keywords": place["keywords"],
            }
        )

    # write partial search json for merge
    out_path = os.path.join(WEBROOT, "data", "search-index.generated.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"pages": search_pages}, f, indent=2)
    print(f"Wrote {len(search_pages)} pages into data/search-index.generated.json")
    print(f"Atlas HTML in {ATLAS_DIR}")


if __name__ == "__main__":
    main()
