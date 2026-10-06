# Bees Revamp honey inspection

**Update:** The ZIP now contains the optional General Settings toggle described in [Honey-toggle-README.md](Honey-toggle-README.md). The unconditional compatibility repair described later in this original inspection has been superseded; the source findings below still describe the original uploaded mod.

Inspected the actual uploaded FS25_z_BeesRevamp.zip, version 1.0.1.0, including its previous compatibility changes. Line references below refer to the unmodified source, copied into original-source/src alongside this report.

## Main finding: honey is deliberately gated by colony maturity

The most direct explanation for zero production is the YOUNG_HIVE state. This is proven behavior in the source, but the supplied material does not include placeables.xml or a live state capture establishing the state of your particular hives. The earlier conversation's claim that honey production was necessarily broken was too strong.

- src/beecare.lua, BeeCare:onLoad, lines 293–325: initializes every colony as YOUNG_HIVE (line 310).
- BeeCare:loadFromXMLFile, lines 91–104: reads saved #state, retaining that young default if absent. There is no migration preserving productivity for existing vanilla hives when this mod is first enabled. Changing the mod ZIP basename can also change the save-data namespace.
- BeeCare:onFinalizePlacement, lines 273–294: assigns YOUNG_HIVE when placedDay is empty. New hives are deliberately young.
- BeeCare:onYearChanged, lines 355–390: promotes colonies to ECONOMIC_HIVE on YEAR_CHANGED if treatment succeeds; treatment is currently automatically supplied because OXUSIM_FEATURE_DISABLE is true. It does not actually measure one year since placement.
- src/placeablebeehiveextended.lua, onHourChanged, lines 246–281: collects nectar only when FX are active AND colony state is ECONOMIC_HIVE (line 255).
- getHoneyAmountToSpawn, lines 303–337: replaces the original function and never calls superFunc. Returns zero unless production is active, the colony is ECONOMIC_HIVE, and nectar is positive (line 312 onward).

Thus a healthy, animated hive with a displayed bee population can produce exactly zero honey. Removing the mod restores the original calculation without these maturity/nectar gates, explaining the observed A/B result without requiring a pallet failure. If the infobox already says economic colony, this explanation alone is insufficient; check nectar, production state, and owner/spawner matching next.

## Hook and output trace

1. src/main.lua, init (line 153): prepends load and appends postLoad to Mission00.load. postLoad (line 104) upgrades the existing engine system in place, retaining its registered objects and callbacks.
2. src/beehivesystemextended.lua, upgradeExisting (line 43): copies extended methods, including updateBeehivesOutput, onto that instance. Explicitly excludes updateState and delete. Consequently the custom winter/temperature updateState at line 66 is NOT used on the normal upgrade path; stock state handling survives. It is used only on the fallback new-system path.
3. SpecializationPatcher adds beehiveextended and beecare to hive types. The extended specialization subscribes to HOUR_CHANGED and WEATHER_CHANGED. Its per-frame onUpdate only refreshes displayed nectar; it does not generate honey.
4. BeeCare:updateBeehiveState (line 581) first calls the original state update, then disables production and FX when calculated population is nonpositive. Young colonies with positive populations can still display flying bees.
5. BeehiveSystemExtended:updateBeehivesOutput (line 99) iterates beehivesSortedRadius, optionally filters farmId, obtains the owner's registered pallet spawner, calls hive:getHoneyAmountToSpawn(), and passes the result to addFillLevel. Missing spawners skip the honey call entirely. Zero honey is passed through rather than rejected; adding zero does not create honey.
6. This ZIP contains no replacement for the engine's periodic system update, pallet updatePallets, getPalletCallback, spawn-area logic, or pallet limits. It preserves the original system object on the normal path. No direct pallet-spawn suppression was found.

GIANTS' published FS25 PlaceableBeehive code calculates output using the configured honey rate, elapsed time capped at one hour, and timeAdjustment. Its state update copies the system production flag. See [GIANTS PlaceableBeehive documentation](https://gdn.giants-software.com/documentation_scripting_fs25.php?category=78&class=709&version=engine).

GIANTS' pallet spawner accumulates addFillLevel into pendingLiters. updatePallets requests a pallet when pendingLiters exceeds 10 and no spawn is pending; the callback transfers honey and subtracts the accepted volume. Space and pallet limits can delay this. This mod does not replace those functions. See [GIANTS PlaceableBeehivePalletSpawner documentation](https://gdn.giants-software.com/documentation_scripting_fs25.php?category=78&class=710&version=engine).

## Separate defects in custom honey conversion

These are real accounting defects, but neither proves permanent zero production in your save.

**Missing elapsed-time accounting:** getHoneyAmountToSpawn uses an entire hour's conversion capacity on every call and never reads or updates lastDayTimeHoneySpawned. Two calls at the same game time can both consume nectar and produce honey. The stock function accounts for elapsed time. A simulation-preserving fix must apply elapsed hours and update the timestamp, including appropriate behavior while production is inactive.

**Clamping before time scaling:** lines 322–331 cap raw hourly conversion against stored nectar, then updateNectar (line 350) multiplies the debit by timeAdjustment, and the returned honey is scaled too. When timeAdjustment is below 1, this under-converts nectar near depletion. For example, with 0.1 L stored, 1 L/hour capacity and adjustment 0.5, it consumes 0.05 L instead of the available 0.1 L. When adjustment exceeds 1, it can return honey corresponding to more nectar than was available. The correct sequence is: compute hourly capacity × elapsed hours × timeAdjustment; clamp that actual volume to stored nectar; subtract that exact volume once; return volume / 3. Do not feed that already-scaled debit back into updateNectar unchanged, because updateNectar scales again.

**Migration omission:** an existing vanilla hive has no saved colony state and becomes young. A simulation-preserving repair should distinguish loading a pre-existing hive with no mod state from purchasing a new hive, initialize only the former as economic, and preserve explicit saved states. Already-saved young states require a deliberate migration or state edit; changing only the missing-state default will not convert them.

## Included compatibility repair

FS25_z_BeesRevamp.zip replaces only the body of PlaceableBeehiveExtended:getHoneyAmountToSpawn with:

```lua
function PlaceableBeehiveExtended:getHoneyAmountToSpawn(superFunc)
    -- Compatibility mode: use the original honey rate and elapsed-time accounting.
    -- BeeCare and nectar remain simulated, but no longer gate honey output.
    return superFunc(self)
end
```

This delegates through the existing overwrite chain, restoring the original rate and timing when no other mod replaces it. Colony maturity and nectar no longer gate honey. It retains the prior infobox fixes, bee population simulation, crop changes, and honey price adjustment. Nectar remains displayed and simulated but is no longer consumed to make honey; this is a vanilla-honey compatibility option, not a full repair of the realism model. The existing nonpositive-population production shutoff still applies, as do stock production conditions and spawner requirements.

Keep the exact ZIP filename FS25_z_BeesRevamp.zip. Back up the currently installed ZIP and save, then replace the installed ZIP with this one; do not load both versions. No installed mod or save was changed during this inspection.

Validation: ZIP integrity passed; entry names match the original; exactly one source file changed and all other archive entry contents are byte-identical. The patch and replaced function were inspected. FS25 and a Lua runtime were not available for an execution test, so this is not yet verified in-game.

In-game verification: load a copy of the save with a living hive and an owned, unobstructed honey spawner during a production-active season. Allow two full game-hour changes. Check honey volume, not just the appearance of a new full pallet. Compare with the original mod on the same save/time. If no honey arrives, capture the current hive state, nectar, production flag, registered hive count, spawner owner/pendingLiters, and a fresh log.

The attached older log records successful system upgrade and hive/spawner assets loading, but contains no per-hive honey/state diagnostics establishing which gate was closed. It cannot prove that all current runtime registrations are correct.