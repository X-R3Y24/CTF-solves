// === DODECACRYPT: Color Extraction ===
// Extracts the 6 visible face colors from each flag die.
// Approach: query single-char messages with a known key,
// then match visible faces against the flag screenshot.
//
// Visible faces at default rotation (ax=45, ay=0, az=0): indices [3,5,6,7,10,11]
// Paste in browser console on the challenge page.

(async () => {
  const enc = async (msg, key = "") => {
    const r = await fetch("/api/encrypt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ key, message: msg }),
    });
    return r.json();
  };

  const VIS = [3, 5, 6, 7, 10, 11];
  const AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  // Step 1: Find the 12 key letters by encrypting single chars
  // Each single-char key maps one letter to one color per face
  console.log("=== Step 1: Map colors to key positions ===");
  const r = await enc("C", "ABCDEFGHIJKL");
  // "C" with identity-like key shows the key coloring directly
  console.log("Identity coloring:", JSON.stringify(r.dodecahedra[0]));

  // Step 2: Extract flag die visible faces
  // You need to get these from the flag.png screenshot.
  // For each die in the 26-die grid, record the hex color at each visible face.
  //
  // Method: open flag.png, sample the center pixel of each visible pentagon.
  // The 6 visible faces per die are at fixed positions relative to each die's
  // bounding box in the grid layout.
  //
  // Here's the extraction for the actual flag:
  // (Sampled manually pixel-by-pixel using a color picker on flag.png —
  // no script needed for a one-time 26-die extraction.)
  const flagDice = [
    { 3: "#ffd8b1", 5: "#e6194b", 6: "#000075", 7: "#aaffc3", 10: "#800000", 11: "#ffe119" },
    { 3: "#000075", 5: "#f032e6", 6: "#e6beff", 7: "#bcf60c", 10: "#e6194b", 11: "#aa00ff" },
    { 3: "#46f0f0", 5: "#f032e6", 6: "#bcf60c", 7: "#e6beff", 10: "#3cb44b", 11: "#aa00ff" },
    { 3: "#e6194b", 5: "#ffd8b1", 6: "#3cb44b", 7: "#aa00ff", 10: "#bcf60c", 11: "#e6beff" },
    { 3: "#f032e6", 5: "#e6beff", 6: "#3cb44b", 7: "#46f0f0", 10: "#ffe119", 11: "#800000" },
    { 3: "#e6194b", 5: "#ffd8b1", 6: "#3cb44b", 7: "#aa00ff", 10: "#bcf60c", 11: "#e6beff" },
    { 3: "#000075", 5: "#f032e6", 6: "#46f0f0", 7: "#ffe119", 10: "#aaffc3", 11: "#800000" },
    { 3: "#46f0f0", 5: "#f032e6", 6: "#000075", 7: "#ffe119", 10: "#800000", 11: "#aaffc3" },
    { 3: "#bcf60c", 5: "#e6194b", 6: "#ffd8b1", 7: "#aa00ff", 10: "#e6beff", 11: "#3cb44b" },
    { 3: "#e6beff", 5: "#3cb44b", 6: "#ffd8b1", 7: "#aa00ff", 10: "#bcf60c", 11: "#e6194b" },
    { 3: "#e6194b", 5: "#aa00ff", 6: "#3cb44b", 7: "#ffd8b1", 10: "#aaffc3", 11: "#800000" },
    { 3: "#e6beff", 5: "#46f0f0", 6: "#ffe119", 7: "#f032e6", 10: "#bcf60c", 11: "#000075" },
    { 3: "#ffe119", 5: "#800000", 6: "#3cb44b", 7: "#46f0f0", 10: "#f032e6", 11: "#e6beff" },
    { 3: "#800000", 5: "#ffe119", 6: "#f032e6", 7: "#46f0f0", 10: "#3cb44b", 11: "#e6beff" },
    { 3: "#ffd8b1", 5: "#3cb44b", 6: "#46f0f0", 7: "#800000", 10: "#aaffc3", 11: "#ffe119" },
    { 3: "#bcf60c", 5: "#f032e6", 6: "#46f0f0", 7: "#e6beff", 10: "#aa00ff", 11: "#3cb44b" },
    { 3: "#800000", 5: "#ffe119", 6: "#000075", 7: "#aaffc3", 10: "#ffd8b1", 11: "#e6194b" },
    { 3: "#800000", 5: "#46f0f0", 6: "#f032e6", 7: "#ffe119", 10: "#aaffc3", 11: "#000075" },
    { 3: "#ffd8b1", 5: "#aaffc3", 6: "#000075", 7: "#e6194b", 10: "#aa00ff", 11: "#bcf60c" },
    { 3: "#e6beff", 5: "#aa00ff", 6: "#e6194b", 7: "#bcf60c", 10: "#f032e6", 11: "#000075" },
    { 3: "#e6194b", 5: "#000075", 6: "#f032e6", 7: "#bcf60c", 10: "#aa00ff", 11: "#e6beff" },
    { 3: "#46f0f0", 5: "#e6beff", 6: "#bcf60c", 7: "#f032e6", 10: "#ffe119", 11: "#000075" },
    { 3: "#800000", 5: "#ffd8b1", 6: "#e6194b", 7: "#aaffc3", 10: "#ffe119", 11: "#000075" },
    { 3: "#46f0f0", 5: "#3cb44b", 6: "#ffd8b1", 7: "#800000", 10: "#ffe119", 11: "#aaffc3" },
    { 3: "#ffe119", 5: "#000075", 6: "#e6194b", 7: "#aaffc3", 10: "#800000", 11: "#ffd8b1" },
    { 3: "#e6beff", 5: "#3cb44b", 6: "#ffd8b1", 7: "#aa00ff", 10: "#bcf60c", 11: "#e6194b" },
  ];

  // Step 3: Collect all unique colors across flag dice
  const allColors = new Set();
  for (const die of flagDice) {
    for (const f of VIS) allColors.add(die[f]);
  }
  console.log(`\n=== ${allColors.size} distinct colors in flag ===`);
  console.log([...allColors].sort().join(", "));

  // Step 4: Map colors to key letters
  // Encrypt single-char messages to see which color appears at which face
  console.log("\n=== Color → Letter mapping ===");
  for (const ch of AL) {
    const r2 = await enc(ch, ch.repeat(12));
    if (r2.dodecahedra && r2.dodecahedra[0]) {
      const colors = r2.dodecahedra[0];
      for (const c of colors) {
        if (allColors.has(c)) {
          console.log(`  ${c} → ${ch}`);
        }
      }
    }
  }

  // Step 5: Output flag signatures for use in other scripts
  console.log("\n=== Flag die signatures (for solver scripts) ===");
  for (let i = 0; i < flagDice.length; i++) {
    const sig = VIS.map((f) => flagDice[i][f]).join(",");
    console.log(`Die ${i}: ${sig}`);
  }
})();