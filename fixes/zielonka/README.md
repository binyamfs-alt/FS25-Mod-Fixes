# Zielonka repair records

These records were supplied from the Zielonka author-review folder. [Map repair report](Map-repair-report.md) documents the tested local version 1.3.0.1 snapshot from 5 September 2026. Its comparison copy was not established as a pristine upstream release. [Equipment and other mod report](Other-mod-repair-report.md) covers separate changes outside the map.

## Reproducible text edits

On a backed-up copy of the matching map version:

1. In `multifruit/fillTypes.xml`, set `isBulkType="true"` on HEMP and FLAX and include both names once in the explicit BULK category. Hemp unloading was confirmed; separate flax gameplay verification was not recorded. Optional grain filling sounds are presentation choices.
2. In the same file, change the GRASS_BUNKER HUD reference to `multifruit/huds/hud_fill_grass_windrow.dds` and DUCK to `multifruit/huds/hud_fill_duck.dds`, after confirming those assets exist.
3. In `multifruit/placeables/greenhouses/industrialGreenhouse.xml`, restore `unloadTrigger2` to `0>0|12|0` only after verifying that node in the paired I3D, and replace `DEFAULT_SPRAYER` with `defaultSprayer`.
4. Remove the duplicate SILPHIE exclusion while preserving the author's intended field-mission restriction block. Disabling the entire block is a separate personal setting.

Repack with `modDesc.xml` at the ZIP root, retain `FS25_Zielonka_Multifruit.zip`, and enable only one copy. Verify hemp unloading, HUD images and greenhouse loading in game, checking the log. Restore the original ZIP to undo the edits.

## Greenhouse and asset work

The watering repair requires renderable spray Shapes, geometry and XML mappings together; text edits alone do not reproduce it. The report records the working 264-nozzle implementation, optional lighting and raised beds, and a matched binary I3D/shapes pair. No donor or original assets are included here. The fill-plane hops normal-map repair is documented in the report, including its BC1 format and validated mip chain.

## Review before reuse

Read the report's snapshot exceptions: crop yield tuning, bee bonuses, mission policy and the unsuccessful 12x8 hemp cutter experiment should not be promoted as general repairs. The successful tested header fix was equipment-side. The historical snapshot fingerprint is recorded in the report; the current installed map has not been freshly audited in this repository setup.
