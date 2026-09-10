// DxSkills Typst Executive Briefing Template
// Swiss Typographic Discipline for Spatial & Non-Linear Leaders
// Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).

#let executive-briefing(
  title: "Executive Strategic Briefing",
  subtitle: "Speed-of-Thought Spatial Synthesis",
  author: "DxSkills Compiler",
  date: "2026-09-10",
  classification: "INTERNAL STRATEGY",
  bluf: "Bottom Line Up Front: Key operational conclusion and immediate decision required.",
  takeaways: (),
  action-items: (),
  doc
) = {
  // Page Configuration
  set page(
    paper: "a4",
    margin: (x: 20mm, y: 22mm),
    header: locate(loc => {
      text(9pt, fill: rgb("#71717a"), font: "Liberation Sans")[
        #grid(
          columns: (1fr, 1fr),
          align(left)[#smallcaps(classification)],
          align(right)[DxSkills Cognitive Standard]
        )
        #line(length: 100%, stroke: 0.5pt + rgb("#e4e4e7"))
      ]
    }),
    footer: locate(loc => {
      text(8pt, fill: rgb("#a1a1aa"), font: "Liberation Sans")[
        #line(length: 100%, stroke: 0.5pt + rgb("#e4e4e7"))
        #v(1mm)
        #grid(
          columns: (1fr, 1fr),
          align(left)[Single-Page Spatial Briefing],
          align(right)[Page #counter(page).display("1")]
        )
      ]
    })
  )

  // Typography Settings
  set text(
    font: ("Liberation Sans", "Helvetica Neue", "Arial"),
    size: 10pt,
    fill: rgb("#18181b"),
    spacing: 120%
  )
  set par(justify: false, leading: 0.65em)

  // Document Header
  v(2mm)
  text(20pt, weight: 800, fill: rgb("#09090b"))[#title]
  v(-2mm)
  text(11pt, weight: 400, fill: rgb("#52525b"))[#subtitle]
  v(1mm)

  grid(
    columns: (auto, 1fr, auto),
    text(9pt, fill: rgb("#71717a"))[Prepared by: *#author*],
    [],
    text(9pt, fill: rgb("#71717a"))[Date: #date]
  )

  v(3mm)
  line(length: 100%, stroke: 1.5pt + rgb("#18181b"))
  v(3mm)

  // BLUF Highlight Box
  rect(
    width: 100%,
    fill: rgb("#f4f4f5"),
    stroke: (left: 4pt + rgb("#18181b"), rest: 0.5pt + rgb("#e4e4e7")),
    radius: (right: 4pt),
    inset: 12pt
  )[
    #text(9pt, weight: 700, fill: rgb("#71717a"))[BOTTOM LINE UP FRONT (BLUF)]
    #v(1mm)
    #text(11pt, weight: 600, fill: rgb("#09090b"))[#bluf]
  ]

  v(4mm)

  // Key Strategic Anchors
  if takeaways.len() > 0 [
    #text(12pt, weight: 700, fill: rgb("#09090b"))[Key Thematic Takeaways]
    #v(1mm)
    #for item in takeaways [
      #grid(
        columns: (12pt, 1fr),
        text(weight: 700)[*•*],
        [#item]
      )
      #v(1mm)
    ]
    #v(3mm)
  ]

  // Action & Accountability Matrix
  if action-items.len() > 0 [
    #text(12pt, weight: 700, fill: rgb("#09090b"))[Operational Action Matrix]
    #v(1mm)
    #table(
      columns: (1.5fr, 1fr, 2fr),
      fill: (x, y) => if y == 0 { rgb("#18181b") } else if calc.even(y) { rgb("#fafafa") } else { rgb("#ffffff") },
      stroke: 0.5pt + rgb("#e4e4e7"),
      inset: 7pt,
      align: (left, left, left),
      // Header
      text(fill: white, weight: 700, size: 9pt)[Deliverable / Focus],
      text(fill: white, weight: 700, size: 9pt)[Status],
      text(fill: white, weight: 700, size: 9pt)[Next Action Item],
      // Rows
      ..action-items.map(row => (
        text(weight: 600, size: 9pt)[#row.at(0)],
        text(size: 9pt)[#row.at(1)],
        text(size: 9pt)[#row.at(2)]
      )).flatten()
    )
  ]

  doc
}

// Sample Instantiation
#show: doc => executive-briefing(
  title: "Cloud Infrastructure Migration",
  subtitle: "Cross-Region Redundancy and Cutover Schedule",
  author: "Architecture Taskforce",
  date: "2026-09-10",
  classification: "INTERNAL ARCHITECTURE",
  bluf: "Milestone 2 cutover scheduled for Friday at 5:00 PM with zero production downtime expected across secondary clusters.",
  takeaways: (
    [Secondary failover clusters verified in Frankfurt and Ireland regions.],
    [Database synchronization lag sustained below 24 milliseconds.],
    [Coordinate reference systems (CRS) updated across all geospatial microservices.]
  ),
  action-items: (
    ("Failover Healthcheck", "Passed", "Trigger final chaos monkey simulation"),
    ("DNS Cutover", "Pending", "Lower TTL to 60 seconds on Thursday morning"),
    ("Engineering Sync", "Scheduled", "Wednesday 2:00 PM to 3:30 PM alignment")
  ),
  doc
)
