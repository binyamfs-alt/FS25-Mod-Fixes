# Equipment and other mod repairs — separate from Zielonka

Prepared 5 September 2026. These changes are **not** inside the Zielonka map archive. This report records the available work history, distinguishes confirmed results from unresolved compatibility issues, and omits personal working-width and production-rate tuning as release recommendations.

## Hemp harvesting equipment

**Diamant 8 header:** the tested 12×8 corn-style CUTTER arrangement continued to fail after map-side auxiliary effects were added, including a nil `speedScale` failure. The successful equipment change used one 32×42 grain CUTTER on the existing plant effect node, with `$data/vehicles/macDon/fd250/beltXArrayCenter.dds`, texture real width 16, minimum fade 0.06, and speed scale 0.18. Smoke was retained. This resolved the remaining tested cutter failure; it must not be attributed solely to the map patch.

Removed four `chopperArea index="2"` references addressing a nonexistent second area. Added a top-level AI `agentAttachment` with `useSize="true"`; a declaration only in the nested configuration did not satisfy the relevant loading requirement.

The Diamant and Colossus 9000 crop lists also contained crops from another multifruit setup: TRITICALE, SPELT, SOYBEAN2, SAFFLOWER, GREENRYE, TARO, OKRA, MINT, and EDAMAME. Unsupported entries were removed for this Zielonka setup. These are compatibility edits, not evidence that those crop names are universally invalid.

**Hirschfeld AW2217:** BULK handling was used, with the actual HEMP/FLAX classification repaired in the map. Hemp unloading was confirmed. See the map report for the source-side change.

## NS3030 AI node references

The model had eight relevant children, while configuration paths addressed nonexistent children 8 and 9. Corrected the marker references to the existing nodes: the 60 configuration uses children 4/5 and the 10 configuration uses 6/7, retaining the shared original rear marker. Removed nonexistent dedicated rear-marker references. Added the top-level AI agent sizing (width 3.2, height 1.5, length 2.65, offset −0.22). Follow-up loading was clean. Personal selectable working widths are not proposed as general fixes.

## MUL1000 specialization mismatch

The mulcher included three roller work-area blocks requesting `processRollerArea` although its active type did not provide that processing function. Removed those roller blocks and their sound section, retained the mulcher work areas, and added the top-level AI agent declaration. Follow-up errors cleared.

## Sell Everything XL

`RABBIT_MALE` entered through an animal category but had no usable sale price in this setup. Added it to `fillTypesExclude` instead of inventing a price. The associated log error cleared.

## MultiFarmStorage production conversion and loading

The storage was converted to a production-point arrangement while retaining the required object-storage functionality. Physical object-storage rows and production pallet output rows were separated to prevent conflicting use of the same space. Four parallel production lines were inset into the intended area: two lines accommodating seven IBCs on the left and two accommodating five on the right. The previous diagonal corner arrangement did not describe the intended production spawning rectangles.

Restored the oversized pipe's `loadTrigger_01` and `liquid_01` connections to the shared storage. Both pipes were tested. Stored contents were migrated from the old Farma400 arrangement to the replacement; persistence was checked before the old storage was removed by the user. These savegame migration steps are specific to that farm, not a map distribution change.

A duplicate production ID `LIME` was renamed to `limeProduction` during XML cleanup. Personal capacities, recipes, and yield choices are excluded from the recommended repair list.

## Shared Ritter logging conflicts

AdjustStorageCapacity, TransactionLog, ManureForAll, and LimitHusbandryAnimals reused `RmLogging`. Per-mod registration guards did not prevent the shared conflict. AdjustStorageCapacity was retained as the registration owner; the complete registration/unregistration functions in the other three were replaced with no-ops while preserving logging calls. MoreVisualAnimals was inspected but was not the logging-module source.

This is a coordinated compatibility workaround for that combination of mods. Authors should review ownership/lifecycle behavior before adopting it independently.

## TransactionLog input registration

The input-registration call returned a false boolean alongside a valid action-event ID. Treating the boolean alone as failure produced the `RM_SHOW...` error. Updated the check to validate whether the returned event ID is nil, following the working AdjustStorageCapacity pattern, and retained validation before changing visibility. Subsequent logs no longer showed the false registration error.

## Localization repairs

- **Case Magnum:** removed duplicate `configuration_color` and `configuration_warningSigns` definitions from modDesc, preserving the vehicle references. A later file overwrite reintroduced the original content, so the repair was reapplied and the corrected version distinguished from the source. The final checked version was clean.
- **SellMultiplier:** its missing localization-folder reference was replaced with an inline localization entry for `input_SM_TOGGLE_HUD`, including “Toggle Sell Multiplier HUD.” Follow-up missing-localization errors cleared.

## Dashboard compatibility

OXBO dashboard-related errors disappeared after DashboardLive and its companion were removed from the user's setup. There is no evidence here of a repaired OXBO model-node file; the result was obtained by changing the mod combination. FarmOperationDashboard was unrelated and retained.

## Distribution compatibility investigation

DistributionRedux encountered a nil comparison in `SmartDistribution.lua` around line 7460 at an hourly update. Treat-as-storage/pass-through changes alone did not clear the issue. ImprovedProductionDistribution and ObjectStorageExtension/Visuals were later removed, after which a longer session did not reproduce it. Because several components changed, responsibility cannot be assigned conclusively to one removed mod. No verified DistributionRedux source patch was produced.

Pallets appearing while distribution was active and being removed at the hourly update were observed alongside inventory changes. That observation did not establish lost production. AdjustStorageCapacity was retained.

## Vibro sprayer assets

Copying a base-game model into a local mod left relative asset references that no longer resolved correctly. Repairing the asset locations/references restored the model, and digestate operation was tested. The decision to use it as a pure sprayer rather than a cultivator, plus enlarged working widths, was a personal configuration choice.

## Unresolved or unproven items

- BetterContracts and the official Vredo feeding-station placing mission encountered a missing vehicle-group failure around missionVehicles lines 634–635. No conclusive repair was established; absence from a later short log is not proof of resolution.
- Core LOD tile-capacity, GUI fallback, and NPClient64/OpenTrack warnings were not repaired by this work.
- Large working widths, variable-width tools, crop-rate tuning, feeding-robot choices, and other personal equipment balancing are outside this repair report.
- Older Lone Star Plains farmland/ownership investigations are not Zielonka repairs and are not included in its map report.

## Evidence limits

This report reconstructs equipment work from the available conversations, including Continue Equipment Setup, Sort XML Fill Types, Edit Forage Wagon XML, Find HUD Reference, and the earlier log-error analysis. It is not a fresh binary audit of every installed equipment archive. Confirmed outcomes above refer to the recorded tests; independent redistribution packages for those mods were not created in this session.
