# Bees Revamp: optional vanilla honey

This FS25_z_BeesRevamp.zip (version 1.0.1.4) retains the working General Settings toggle and adds regular elapsed-time honey collection while On. It retains the menu fixes from 1.0.1.2/1.0.1.3.

While On, the server asks the existing hive output path for accrued honey once per second. The vanilla calculation uses elapsed game time and advances its timestamp, so additional calls do not multiply the configured hourly rate or duplicate the hourly collection. Honey is added to the existing pallet spawner; its pallet scheduling, fill callbacks, and the Lazy Distribution unload trigger are unchanged. No honey is added directly to LD. Off leaves the original Bees Revamp output scheduling unchanged.

This addresses the previous toggle's lack of between-hour collection. It is not a claim that a live production trace has confirmed every cause of the empty LD inventory. To make remaining problems visible, the log now records On/Off changes and a production summary once per minute while On: registered/active hives, missing spawners, honey getter calls and litres generated since the previous report, pending spawner litres, and spawn/pallet-limit flags.

Version 1.0.1.1 incorrectly passed true to MultiTextOptionElement:setState's forceEvent argument when refreshing the setting. That forced another change callback, which refreshed again until the stack overflowed. The supplied log reported TextElement.lua:591: stack overflow while opening the menu. Version 1.0.1.2 refreshes without forcing callbacks and explicitly makes the cloned row visible/enabled. A regression test using GIANTS' published setState implementation reproduces the callback loop in 1.0.1.1 and passes with this fix, including execution of a later menu hook representing another mod.

Fully exit FS25 before replacing 1.0.1.1, then restart it so the old menu objects and hooks are discarded. There is no need to reset other mods' settings to apply this fix.

In the in-game **General Settings** page, scroll to the **Bees Revamp** heading near the bottom and find **Bees Revamp: vanilla honey production**. Successful creation now records “Honey toggle added to General Settings under Bees Revamp.” in the game log.

- **Off (default):** original Bees Revamp honey behavior, including the young-colony and nectar requirements.
- **On:** vanilla honey calculation, independent of colony maturity and nectar. Ordinary production-active restrictions and the existing zero-population shutoff still apply.

Nectar collection, bees eating nectar, colony development, swarming, hive displays, pollination and the previous compatibility changes remain as they were. When On, honey generation does not consume nectar; stored nectar continues to be collected and eaten. Turning Off resumes the original conversion using whatever nectar is then stored. Young colonies still do not collect nectar under the original collection rules.

The setting applies to all hives in the current savegame. Save the game to persist it. It is stored in beesRevampHoneySettings.xml inside that savegame directory; a save without that file starts with Off. Switching modes resets vanilla honey's elapsed-time marker, so the first vanilla production interval starts when you enable it.

In multiplayer, the host controls this save-wide setting; clients see a read-only value synchronized from the host. A dedicated server can use the same save-local XML setting (with the server stopped):

```xml
<?xml version="1.0" encoding="utf-8"?>
<beesRevampHoneySettings vanillaHoney="true" />
```

To install, back up the installed mod and save, then replace the installed FS25_z_BeesRevamp.zip with this ZIP. Keep the filename unchanged and do not load two copies. No installed files or savegames were modified while preparing it.

Validation: every Lua file compiles in a Lua runtime. Tests with simulated game objects passed for original behavior with Off, vanilla delegation with On, unchanged nectar collection/feeding, timestamp reset, per-save persistence of both states, menu callback/reopening, client read-only enforcement and event serialization. A further integration test runs the installed game's SDK BeehiveSystem, PlaceableBeehive and PlaceableBeehivePalletSpawner code together with the mod, substituting a test pallet for the physical game world. At 312 hives, 7,500 L/day each, one day per period and 2x time scale, ten real minutes accrues 32,500 L and delivers it through the stock fill callback before the next hour. Repeating collection at the same time adds zero; nectar remains unchanged; Off/loading stop regular collection. This does not execute the actual LD trigger or test physical spawn clearance. Archive integrity and the exact changed-file list were checked. In-game confirmation remains necessary.

Changed files: src/main.lua (settings setup/load); src/placeablebeehiveextended.lua (conditional vanilla delegation); new src/honeysettings.lua (menu, persistence and synchronization); modDesc.xml (version only). The rest of the archive is byte-identical to the uploaded mod's entry contents.