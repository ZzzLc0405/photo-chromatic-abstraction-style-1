---
name: photo-chromatic-abstraction-style-1
description: Translate an uploaded or local photograph into a color-first chromatic-memory abstraction (Style 1) built from adaptive flat fields and 1-5 restrained, source-derived accents. Use for palette-memory composition, color-weight studies, minimalist color-block translation, 色块抽象、照片色彩记忆、色彩构成、照片色卡转译，or explicit Style-1 requests where broad color hierarchy matters more than subject placement. Do not use when the result must preserve source-specific object geometry or spatial structure; that is Style 2. Deliver an editable SVG plus a PNG preview.
---

# Photo Chromatic Abstraction · Style 1

## Core contract

- Use the photograph as the sole color and motif source.
- Preserve dominant color weight, warm/cool relationships, broad layer order, and visual rhythm. Do not reconstruct the scene.
- Treat people, vehicles, signs, wires, trees, and other semantic subjects as disposable unless their color mass materially affects the palette.
- Build the base from adaptive, flat color fields, usually rectangles or bands.
- Add 1-5 accent instances. Base fields do not count toward this limit.
- Use one accent shape family by default and no more than two families.
- Select accents by perceptual salience: area, contrast, repetition, rhythm, and positional influence. Do not privilege a person, vehicle, or conveniently drawable shape.
- Make every accent traceable to a source color mass, repetition, curve, directional event, or memory motif. Never add a shape merely to decorate an empty area.
- Output the abstraction as a standalone SVG and PNG by default.
- When the user requests a diptych, comparison, collage, or publishing layout, additionally create a separate Style-1 presentation composite. Never embed the source photograph into the abstraction SVG.

Style 1 passes this diagnostic:

> The image is perceived first as a color composition and only later as a memory of the photograph.

If changing the source requires redesigning exact object positions, overlaps, or silhouettes, the result has drifted toward Style 2.

## Workflow

1. Inspect the source at its original orientation and aspect ratio.
2. Identify 4-7 chromatic roles by default: dominant field, supporting fields, transition fields, grounding field, and optional accent color. Use at most 8 total colors, including the separator/background color.
3. Build a perceptual-salience map before drawing. Rank candidate events by occupied area, color contrast, repetition/rhythm, and effect on balance. List what to delete; ignore small subjects and details that contribute little chromatic weight.
4. Select a base composition family:
   - **Palette stack:** ordered bands with adaptive thickness.
   - **Color-field landscape:** large fields retaining only broad vertical or directional order.
   - **Memory motif:** color fields plus one source-derived repeated or singular motif.
5. Decide where fields touch and where they breathe. Add narrow neutral gaps only when adjacent colors need separation; do not mechanically separate every field.
6. Choose 1-5 accent instances from the highest-salience retained event. Let the source determine the shape family: curves or clustered masses may become circles; repeated vertical masses may become rectangles; a distinct mound may become a triangle. Use a second family only when the source contains a separate subordinate event and the result remains clearly color-first.
7. Vary accent size, spacing, height, and boundary contact when the source suggests an organic mass or irregular rhythm. Avoid equal spacing and icon-like rows unless the source itself is repetitive.
8. Consolidate sampled colors. Merge near-duplicates, separate muddy neighbors, and delete weak colors. Do not mechanically display eyedropper samples.
9. Construct an edge-to-edge SVG with opaque solid fills. Mark base fields with `data-role="base"` and every counted accent with `data-role="accent"`.
10. Render a PNG preview, run `scripts/validate_style1_svg.py`, inspect the preview at full size, and perform the self-audit.
11. Save non-destructively as `style1-<source-stem>.svg` and `style1-<source-stem>.png`, adding `-v2`, `-v3`, and so on for revisions.
12. If a presentation composite was requested, assemble it only after the standalone SVG and PNG have passed validation.

Before constructing the artwork, briefly tell the user the selected palette logic, accent source, separator logic, and major deletions.

## Accent rules

- Count visible accent instances, not shape categories. Four circles equal four accents.
- Use 1-5 accents; never deliver a zero-accent final Style-1 artwork.
- If no subject deserves retention, derive the accent from a cloud mass, sunlit patch, repeated color node, strong curve, large object color, or a modified boundary of a main color field.
- Do not force a photographed subject into the abstraction merely to satisfy the accent rule.
- Do not choose a motif because it is easy to draw. Prefer the source event with the strongest combined area, contrast, repetition, rhythm, and positional influence.
- When one repeated source event dominates, represent the group rather than an isolated token: for example, a broad cloud bank may become 3-5 unequal circles, while a line of prominent trees may become a restrained repeated rectangular family. Never draw literal silhouettes.
- Keep total accent area normally within about 5-20% of the canvas. A source-dominant motif may exceed this when justified.
- When using multiple accents, establish hierarchy through size or placement. Do not make five equally prominent badges.
- Reuse palette colors when possible. Do not assign every accent a new color.
- Permit accents to float, cross a band boundary, approach an edge, or form an uneven cluster. Require a shared relation such as color, shape, progression, direction, or source.

Read [references/visual-grammar.md](references/visual-grammar.md) when selecting fields, gaps, colors, or accents. Read [references/validated-examples.md](references/validated-examples.md) when diagnosing a result that feels generic, too literal, too empty, or overdecorated.

## Style-1 presentation composite

Apply these rules only when the user requests a collage, comparison image, diptych, or publishing layout. Always complete and validate the standalone abstraction first.

### Landscape source

- Use a square raster canvas, 2048 × 2048 px by default.
- Use a neutral off-white background such as `#F2F2F2`.
- Place the unchanged source photograph at the top, spanning the full canvas width.
- Preserve the source aspect ratio. Do not crop, stretch, redraw, or stylize it.
- Place the abstraction below the photograph, horizontally centered at approximately 50–55% of the canvas width.
- Preserve the abstraction’s original aspect ratio.
- Leave a clear middle interval of approximately 6–8% of the canvas height.
- Keep the lower whitespace larger than the middle interval so that the abstraction reads as a restrained visual footnote.

### Portrait source

- Use a square raster canvas, 2048 × 2048 px by default.
- Use the same neutral off-white background.
- Place the completed abstraction on the left and the unchanged source photograph on the right.
- Preserve both aspect ratios. Do not crop or stretch either panel.
- Keep the source photograph visually primary; the abstraction must not appear larger or heavier than the source.
- Vertically center both panels by default.
- Leave a clear neutral gap of approximately 6–8% of the canvas width.
- Maintain generous, balanced outer margins.
- Do not force a portrait source into the landscape top-and-bottom arrangement.

### Shared presentation rules

- Source orientation determines the composite arrangement.
- The external layout may remain consistent across a series, while the internal abstraction must remain source-adaptive.
- Do not add text, borders, shadows, frames, rounded corners, or decorative graphics.
- When the user asks only for the abstraction, do not generate the composite.
- Export the composite as `style1-<source-stem>-composite.png`.
- Run the SVG validator only on the standalone abstraction, not on the raster composite.

## SVG construction and validation

- Use native primitives (`rect`, `circle`, `ellipse`, `polygon`) whenever possible.
- Use `path` only for a straight-edged triangle, trapezoid, or simple diagonal field. Do not use Bézier commands.
- Use opaque hex fills. Do not use gradients, filters, masks, patterns, transparency, strokes, raster images, photographic texture, or visible text.
- Keep base fields visually dominant. Accents must punctuate rather than replace the palette structure.
- Preserve source orientation and aspect ratio unless the user requests another format.

Run:

```powershell
python scripts/validate_style1_svg.py <output.svg>
```

The validator enforces flat construction, 1-5 labeled accents, no more than two accent families, and at most 8 colors. Fix every error before delivery.

## Example-guided calibration

After independently analyzing the source photograph, inspect relevant curated examples in `assets/examples/` before constructing the final artwork.

- If the folder contains four or fewer examples, inspect all of them. Otherwise, select 2-4 examples that address a similar chromatic or compositional problem.
- Use examples to calibrate abstraction depth, color weight, spacing, accent hierarchy, restraint, and presentation quality.
- Treat examples as demonstrations of reasoning, not reusable templates.
- Never copy an example’s palette, band count, accent count, shape family, spacing, or placement unless independently justified by the current source.
- Let the source photograph and the Core contract override the examples whenever they conflict.
- During the final audit, compare the result with the examples for clarity and restraint while ensuring that it does not visibly imitate any single example.

## Self-audit

1. Is the dominant color field clearly larger than the supporting fields?
2. Does the palette preserve the photograph's chromatic weight rather than its object inventory?
3. Were weak details and small narrative subjects removed?
4. Are there 1-5 accent instances, each with a traceable source reason?
5. Was the accent selected because it is perceptually dominant rather than semantically important or geometrically convenient?
6. Is there one accent family by default and no more than two?
7. Would removing an accent improve the composition? If yes, remove it, while retaining at least one.
8. Are gaps used selectively rather than as a mandatory white grid?
9. Are multiple accents varied enough to avoid an icon row yet related enough to avoid random decoration?
10. Is the first impression a color composition rather than a simplified illustration?
11. Are all fills flat, opaque, hard-edged, editable, and texture-free?

Deliver the preview, editable SVG, and PNG. Briefly explain the palette hierarchy, accent source, and major deletions.
