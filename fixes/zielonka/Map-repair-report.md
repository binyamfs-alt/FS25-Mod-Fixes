# Zielonka Real Orchards Edition Multifruit — repair and enhancement report

Prepared 5 September 2026 for the map author, from Ben Burdette's testing session and the available earlier work records.

## Scope and evidence

This report covers changes inside the Zielonka map archive. Equipment and unrelated mod work is documented separately. It distinguishes working repairs, optional greenhouse enhancements, retained experiments, and personal settings that should not automatically become release defaults.

The supplied archive is an exact snapshot of Ben's active version 1.3.0.1, not a newly cleaned upstream release. Comparison against the inactive local copy of the same version found 13 changed files and two added files. That comparison copy is not claimed to be a pristine author release. Findings were cross-checked against the repair conversations, current archive contents, and final game log.

**Final test:** the greenhouse looked correct in game; watering had been observed across repeated activations. The final log contains two loads, at approximately 13:47 and 13:50 on 5 September. There are no `Error:` entries, no donor-bed non-binary warning, and no reported hops format/mipmap or greenhouse loading errors. This is evidence for the tested configuration, not exhaustive testing of all map features or multiplayer.

## 1. Hemp and flax bulk handling

**File:** `multifruit/fillTypes.xml`

Hemp could not transfer correctly through equipment relying on the BULK classification. Both HEMP and FLAX lacked the bulk declaration used by that equipment.

Changes:

- Added `isBulkType="true"` to HEMP and FLAX.
- Added HEMP and FLAX to the explicit BULK fill-type category.
- Added a filling sound for each: coarse `grainLargeFill` for hemp and `grainSmallFill` for flax.

**Verification:** hemp transfer from the combine to the Hirschfeld AW2217 was confirmed. Flax received the equivalent classification repair, but a separate flax harvesting test was not recorded. The sound choices are presentation preferences rather than transfer fixes.

Raw CLOVER, ALFALFA, and SILPHIE were not added to BULK. Earlier discussion of doing so was corrected; their windrow forms are the relevant materials. A proposed strawberry BULK change is not installed.

## 2. Missing fill-type HUD images

**File:** `multifruit/fillTypes.xml`

Corrected two paths to existing assets:

| Fill type | Previous reference | Replacement |
|---|---|---|
| GRASS_BUNKER | `multifruit/huds/hud_fill_grass.png` | `multifruit/huds/hud_fill_grass_windrow.dds` |
| DUCK | `multifruit/huds/fillTypes/hud_fill_duck.png` | `multifruit/huds/hud_fill_duck.dds` |

Follow-up logs no longer reported those missing images. This was a filename/directory repair. A `.png` reference is not inherently wrong: the engine can resolve a corresponding DDS asset.

## 3. Hemp harvesting effects

**Files:** `multifruit/effects/cutterFruitEffects.xml`, `cutterThreshingEffects.xml`, `chopperEffects.xml`, and `cutterEffects.xml`.

Missing HEMP effect registrations produced missing mesh warnings for harvesting and combine discharge effects. The installed changes supply these auxiliary effects:

- **CUTTER_FRUITS:** HEMP stage 5, maize fruit geometry, mesh sizes 6×18, 12×28, and 20×38, with the corn-header fruit array and speed scale 0.3.
- **CUTTER_THRESHING:** HEMP stage 5, maize threshing geometry, sizes 6×10, 12×10, and 20×10, with the threshing array and speed scale 1.
- **STRAW_CHOPPER / CHOPPER / CHAFFER / DROP:** added HEMP to the appropriate existing definitions and material groups. The CHOPPER group uses density scale 0.75 and speed scale 1.

Follow-up work confirmed that the missing 12×28 fruit, 12×10 threshing, 29×31 and 16×18 chaffer, and 16×12 drop requests were resolved.

**Important retained experiment:** `cutterEffects.xml` also contains an appended maize-derived HEMP CUTTER stage-5 block with 6×8, 12×8, and 20×8 meshes and speed scale 0.6. This did **not** resolve the tested header's 12×8 CUTTER problem. The existing 32×42 HEMP foliage block was retained. The final solution for that header was an equipment-side conversion to the 32×42 grain cutter architecture, described in the separate report. The appended map block should be reviewed as an experiment, not promoted as a proven fix.

Hops uses a different effect arrangement; hops effects were not the successful hemp donor. No installed repair to `hopsEffects.xml` was identified.

## 4. Belt material holder references

**File:** `multifruit/effects/belt/beltMeshes_materialHolder.i3d`

Unused sugar-beet material-holder entries referenced missing file IDs and generated texture warnings. The repair removed the two obsolete material blocks (`sugarBeetsClean_mat` and `sugarBeetsDirt_mat`), their two unused holder Shapes, and the now-unused sugar-beet specular file entry. The corresponding missing file IDs included 9, 10, and 12.

The working beetroot, potato, and belt-array material holders were preserved. Subsequent logs did not report the stale-reference warnings. This was cleanup of unused references, not replacement of every belt material with a new texture.

## 5. Hops normal-map compression and mipmaps

**File:** `multifruit/fillPlanes/hops_normal.dds`

The fill-plane normal texture had an unsuitable BC7/four-channel format and needed its mipmaps rebuilt. It was converted to **DXT1 / BC1** and saved with a valid mip chain.

Successful process:

1. Open the image in GIMP and use the full 1024×1024 surface.
2. Export an intermediate BC1 DDS without mipmaps, avoiding reuse of the problematic existing chain.
3. Open it in the NVIDIA texture exporter, turn **Extract from Atlas off**, enable **Generate Mipmaps**, use a 4-pixel minimum mip size and maximum mip count, and export BC1 with production compression.
4. Inspect the final DDS and reload the game to check the warning.

**Verified result:** 1024×1024, DXT1/BC1, 699,176 bytes, nine total DDS levels: the base image plus eight smaller levels, ending at 4×4. The engine's count of eight smaller mipmaps and the DDS header's nine total levels describe the same chain. The format/mipmap warning disappeared.

This is the **fill-plane** image. It is not the separate `multifruit/orchards/hops/hops_normal.dds` orchard texture.

## 6. Duplicate SILPHIE mission setting

**File:** `modDesc.xml`

A duplicate SILPHIE entry in the disabled-crop list was identified and removed. However, Ben also chose to comment out the entire `disableFieldMissions` configuration block while leaving its script loaded.

**Release recommendation:** remove the duplicate while preserving the author's intended mission restrictions. Disabling the whole restriction list is a personal gameplay choice included in the supplied snapshot; it is not required to fix a duplicate entry. Contracts for all formerly excluded crops have not been validated.

## 7. Hemp windrow declaration and mixed personal changes

**File:** `multifruit/foliage/hemp.xml`

The active archive adds `fillType="HEMP_FIBER"` to the windrow declaration, which previously specified only `cutFillType="HEMP_FIBER"`. This structural addition is present in the archive, but its individual runtime effect was not isolated in testing.

The same file also contains personal yield changes. Those should be separated from the structural declaration during author review; see the snapshot exceptions below.

## 8. Industrial greenhouse — functional repair

**Files:** `multifruit/placeables/greenhouses/industrialGreenhouse.xml`, `industrialGreenhouse.i3d`, and `industrialGreenhouse.i3d.shapes`.

The original watering arrangement contained 88 empty effect TransformGroups rather than the renderable spray Shapes needed for the effect. A separate invalid smoke effect reference (`0>4|1`) addressed a missing child under the indoor-area hierarchy and caused loading failures. Additional configuration problems included an unload trigger mapping that was commented out and an incorrect sprayer sound template name.

Repairs:

- Restored `unloadTrigger2` mapping to `0>0|12|0`.
- Replaced `DEFAULT_SPRAYER` with the working `defaultSprayer` sound template.
- Replaced the invalid effect arrangement with actual donor spray Shapes and matching XML mappings.

The abandoned 88-node structure was reported to predate this map adaptation; this report does not attribute its creation to the map author.

### Working spray implementation

A single-nozzle effect from the newer donor greenhouse was first imported and tested. Ben observed it start and stop and heard the sound. Replication across the original 88 positions covered only part of the two center rows. The physical nozzle assembly is merged into the `Details` mesh, so the individual nozzles could not be selected as separate scene nodes. Analysis of its exported OBJ established **264 positions in eight lines of 33**.

The final model contains 264 spray Shapes using shared geometry, with one corresponding mapped XML effect per nozzle. The effects use `materialType="sprayer"`, `defaultFillType="liquidFertilizer"`, and `dynamicFillType="false"`. That fill type selects the visual effect material; it does not introduce a liquid-fertilizer requirement for watering.

The spray height was extended using scale `4.25162 1.8 1`, preserving the nozzle tips. Ben approved the resulting fade above the soil. Repeated watering activations and sound were observed with the final visual upgrades installed.

Activation uses the greenhouse's existing engine behavior, not a new watering script. Different greenhouse instances were observed activating separately. An approximately 3:15 cycle was observed during testing, but no global synchronized schedule or exact random-timer rule is claimed from that observation.

The earlier Razak array donor was not used in the final implementation. Failure to observe its watering during an earlier wait does not establish that the donor itself is broken.

## 9. Industrial greenhouse — optional visual enhancements

These are additions beyond repairing the original watering configuration.

### Lighting

- Automatic blue-violet night lighting using the NIGHT visibility arrangement.
- Independently switched white work lighting.
- Twelve white and twelve violet light positions, with shared fixture assets and suitable real-light groups.
- Increased illumination after the first in-game test was too dim; enabled specular contribution for highlights.
- Physical switch moved inside to the metal post by the manure box: position **−5.9, 1.5, 19.9**, rotation **0, 180, 0**. Its interaction trigger is at **−5.9, 1.5, 19.0**.

Ben approved both lighting modes and the corrected switch position. The grow lights are visual; no growth or yield bonus was added.

### Raised beds

Added `greenhouseUpgrades/donorBed.i3d` and its matching `.i3d.shapes` file, referenced by the main model. Four approximately 3×30-metre beds reproduce the donor style.

Simply stretching the original small planter also stretched the wood and made the end boards excessively thick. Plants then intersected those boards and appeared elevated. The repair adjusted the frame geometry to retain board thickness under the bed scale, repeated the wood texture appropriately, and tiled the soil. All 272 plant positions were aligned to the soil surface. The final soil height is approximately 0.302214, below the frame top of approximately 0.398153 in the relevant bed coordinates.

The first and last plant rows were checked again after the frame repair. Ben's final visual check was good. The new bed frames are visual additions; no new collision geometry was added.

### Binary geometry warning

The repaired donor initially contained inline, non-binary indexed triangles. Saving it as **Binary I3D** in GIANTS Editor produced the correct matched pair: an approximately 1,689-byte I3D and 98,316-byte shapes file. Both were deployed together. The final log loads the donor in approximately 0.69 ms without the previous warning.

Development failures such as an accidentally missing XML closing tag and a mismatched donor geometry export were corrected during construction. They are not presented as defects in the author's original release.

## Snapshot exceptions: do not adopt wholesale

The attached map archive deliberately preserves the tested active setup. It includes these settings that need author review:

| File/setting | Difference from local comparison | Treatment |
|---|---|---|
| Clover harvest litres per square metre | 3 → 4.5 | Personal balance; not a repair |
| Hemp harvest litres per square metre | 0.3 → 1.93 | Personal balance; not a repair |
| Hemp bee bonus | 0.05 → 0.10 | Personal balance; not a repair |
| Hemp windrow litres per square metre | 4 → 6 | Personal balance; not a repair |
| Hemp windrow cut factor | 1 → 1.5 | Personal balance; not a repair |
| Disabled field mission configuration | Entire block commented out | Personal contract policy; retain author restrictions if desired |
| Appended 12×8 HEMP cutter effect family | Experimental block remains | Not a proven solution; review before inclusion |

The map's `door3molette` mapping still uses shorthand `9|0|14`. An earlier proposal to normalize it to `0>9|0|14` was not an installed map repair, and the final log does not prove that shorthand is faulty. The standalone package normalizes the reference for clarity.

## Remaining warnings and testing limits

The final log still reports an `ingameMenuAILimitReached` GUI fallback and a core LOD tile-capacity warning. These were not repaired in this work. The larger mod setup also reports an NPClient64/OpenTrack library-loading issue; no greenhouse cause was established.

Ben noticed no visible lag when the sprayers activated. This is an observation, not a full-farm performance benchmark. Multiplayer, every crop/contract, and every combination of optional production mods remain outside the final verification.

## Archive inventory and provenance

The comparison manifest alongside this report lists all 13 changed and two added files; no files were removed. A companion text diff provides reviewable changes for XML and textual I3D content. Binary assets are included in the full map snapshot.

Snapshot SHA-256: `3d62b9b13b810ddb5ac69aff3ee605aed2d7f2c340e531eaeb51aa26edb81e9d`.

Primary records reviewed: Gameplay Log Check; Fix Hemp Bulk Category; Continue Equipment Setup; the earlier log-error analysis; and the greenhouse development/test conversation. Older work concerning Lone Star Plains and its farmland ownership issues is excluded because it was not Zielonka work.

The greenhouse uses inherited assets as well as new modifications. Credits and any necessary redistribution permission should accompany an author release. This report and archive are prepared for private author review; no publication or message to the author was performed.
