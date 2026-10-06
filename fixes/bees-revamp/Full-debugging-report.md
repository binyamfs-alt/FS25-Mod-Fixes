# Bees Revamp full debugging report

This is a readable summary of the supplied [original Word report](BeesRevamp_Full_Debugging_Report.docx), which is preserved unchanged. The report covers the earlier compatibility repair, not the later optional honey toggle. The latter remains documented in [Repair-notes.md](Repair-notes.md) and [Inspection.md](Inspection.md).

## Scope and confirmed outcome

Historical final build: `FS25_BeesRevamp_fixed.zip`, mod version 1.0.1.0. Test environment: Glenleathann multifruit with 209 registered hive installations and Yurg custom 33 Langstroth hives. Evidence: ten runtime logs from 17 September 2026, inspected mod source, Yurg hive XML and user gameplay verification.

The report records successful map loading, active production flags, restored visible/audible bees, correct nearest-hive information boxes, five-metre exit behavior and 33-colony population scaling. Active production flags alone are not proof of generated honey volume; the later honey investigation and toggle work address that separately.

## All nine documented items

| ID | Defect or compatibility issue | Implemented correction |
| --- | --- | --- |
| B01 | Multifruit field-info lookup dereferenced a missing fruit or bee bonus | Guard both the resolved fruit and `beeYieldBonusPercentage` in `fieldAddField`; omit the bee field line when unavailable |
| B02 | Replacing the engine-created hive system broke object identity and retained references | Upgrade the existing `mission.beehiveSystem` after stock mission loading; create a replacement only if no stock system exists |
| B03 | A derived metatable did not expose extension methods | Attach extension members directly to the stock instance; fixes missing `getGrowthFactor` and repeated initialization exceptions |
| B04 | Function-only copying omitted class tables/constants | Copy required data as well as methods, including the monthly growth lookup; prevents nil indexing and repeated loading failures |
| B05 | Legacy `updateState` disabled sound/visual FX; replacing `delete` risked lifecycle breakage | Exclude `new`, `upgradeExisting`, `updateState` and `delete` from the graft; preserve current FS25 state/lifecycle and refresh each hive once |
| B06 | Idle placeable updates did not reliably activate, close or switch infoboxes | Mission listener selects the nearest eligible registered hive every 250 ms within five metres, removes the old drawable and activates the selected stock info trigger |
| B07 | Custom 33 Langstroth hive inherited a fallback count of 12 | Add explicit `placeable.beehive#hiveCount` = 33 in the separate Yurg custom hive XML |
| B08 | HEMP/CLOVER lacked local multifruit density metadata | Add 0.10 bee-yield bonus and one hive per hectare for each in the local patch list |
| B09 | Test naming and duplicate builds caused rejection/confusion | Use valid FS25 archive names, remove old active test copies, package the final historical repair and remove temporary diagnostic logging |

## Files and ownership

- `src/main.lua`: post-load system upgrade, late third-party specialization pass, mission-level proximity listener and HEMP/CLOVER entries.
- `src/beehivesystemextended.lua`: selective complete graft and defensive multifruit field-info validation.
- `src/beecare.lua`: one-time live-state refresh, nearest-hive selection and fallback state cleanup.
- `modDesc.xml`: historical release version 1.0.1.0.
- Yurg `beehiveGeneric02.xml`: explicit colony count; this belongs to the custom hive pack, not Bees Revamp.

The Yurg edit is an attribute override: add a `set` entry with path `placeable.beehive#hiveCount` and value `33` alongside the existing radius and honey-rate overrides. Do not change the declared honey rate or radius merely to correct colony count.

## Recorded debugging and validation

Tests progressed from broken object replacement, through missing methods (test4) and missing class data (test5), to legacy FX suppression (test6/test7). Repeated initialization exceptions exhausted interval timers and produced the apparent 75% hang. Preserving stock state handling restored effects in test8. Tests9-11 isolated UI regressions; test12 confirmed switching across ten hives spaced about two metres apart and closing out of range. Final logs showed `hives=33`, and the user confirmed proportional population increase.

The report records passing map load, Lua stability, interval-timer behavior, registration, production state, visible/audible bees, information entry/exit, nearest-hive switching, custom count, population scaling and HEMP/CLOVER patching. These are recorded historical results, not newly rerun gameplay tests.

Proximity scanning at 209 hives and four passes per second performs approximately 836 squared-distance checks per second. The report assesses this as a small workload, not a measured universal benchmark. Very large hive counts warrant profiling.

## Installation and rollback today

The final filename in the historical report describes that handoff. The current Alma installation is the later `FS25_z_BeesRevamp.zip` version 1.0.1.4; preserve its current basename and use only one Bees Revamp build. Back up mods and saves before applying edits. Keep the hive-count change in the Yurg pack. Restore backed-up ZIPs to undo changes, and restore the save backup when test gameplay changed save data. Revalidate against future FS25 or mod updates, particularly hive registry and info-trigger internals.

## Later honey work

The optional vanilla-honey toggle, menu recursion repair, regular elapsed-time output, mode persistence and network synchronization were added later. [Compatibility history](Compatibility-history.md) records the later On -> Off -> On gameplay confirmation. Faster Honey Pallet Cadence is a separate utility that changes pallet spawning cadence.
