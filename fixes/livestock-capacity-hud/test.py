"""Lua 5.1 regression checks for breed/type rules and capacity rendering."""
from pathlib import Path
from lupa.lua51 import LuaRuntime
r = LuaRuntime()
r.execute('''
g_time=0
g_i18n={getText=function(_, key) return key end, formatNumber=function(_, n) return tostring(n) end}
warnings=0
local subTypes={[1]={typeIndex=1,fillTypeIndex=10},[2]={typeIndex=1,fillTypeIndex=11},[3]={typeIndex=2,fillTypeIndex=12}}
g_currentMission={animalSystem={getSubTypeByIndex=function(_,i) return subTypes[i] end,
getTypeByIndex=function(_,i) return {typeIndex=i} end},showBlinkingWarning=function() warnings=warnings+1 end}
FillType={UNKNOWN=0}; FillLevelsDisplay={TYPE_BAR=1}
function cluster(i,n) return {getSubTypeIndex=function() return i end,getNumAnimals=function() return n end} end
load={cluster(1,1000),cluster(2,460)}
vehicle={spec_livestockTrailer={clusterSystem={getClusters=function() return load end},animalTypeIndexToPlaces={[1]={},[2]={}}},
getCurrentAnimalType=function() return #load>0 and {typeIndex=1} or nil end}
''')
r.execute((Path(__file__).parent/'source/scripts/LivestockCapacityHUD.lua').read_text())
r.execute('''
local H=LivestockCapacityHUD
assert(H.isTypeAllowed(vehicle,1)) -- Different sheep breeds, including goats
assert(not H.isTypeAllowed(vehicle,2))
local capacity=5000
vehicle.getMaxNumOfAnimals=function(self,t) return H.getMaxNumOfAnimals(self,function() return capacity end,t) end
assert(vehicle:getMaxNumOfAnimals({typeIndex=1})==5000)
assert(vehicle:getMaxNumOfAnimals({typeIndex=2})==5000)
assert(warnings==0) -- opening/browsing must never fire a rejection warning
assert(H.getSupportsAnimalType==nil) -- never filter the screen's advertised animal types
assert(warnings==0)
local display={fillLevelData={}}
function display:addFillLevel(ft,n,c,p,m,t,label)
  self.fillLevelData={{isValid=true,fillType=ft,customFillTypeText=label,fillLevel=n,capacity=c}}
end
H.updateDisplay(display,function(d) H.getFillLevelInformation(vehicle,function() end,d) end)
assert(display.fillLevelData[1].fillLevelText=='1460 / 5000 (29%)')
capacity=2000
H.updateDisplay(display,function(d) H.getFillLevelInformation(vehicle,function() end,d) end)
assert(display.fillLevelData[1].fillLevelText=='1460 / 2000 (73%)')
load={}
assert(H.isTypeAllowed(vehicle,2)) -- Empty trailer unlocks
assert(vehicle:getMaxNumOfAnimals({typeIndex=2})==2000)
assert(vehicle:getMaxNumOfAnimals({typeIndex=99})==0) -- modifier must not enable unsupported types
H.updateDisplay(display,function(d) H.getFillLevelInformation(vehicle,function() end,d) end)
assert(display.fillLevelData[1].fillLevelText=='0 / 2000 (0%)')
H.updateDisplay(display,function(d) d.fillLevelData={} end)
assert(next(display.bfsAnimalRows)==nil) -- Switching vehicles clears metadata
''')
print('PASS: mixed breeds, blocked types, live capacity, empty unlock, warning throttle, HUD counts')
r.execute('''
g_currentModName='FS25_z_LivestockCapacityHUD'
g_specializationManager={getSpecializationObjectByName=function() return LivestockCapacityHUD end}
AnimalScreen=nil
''')
r.execute((Path(__file__).parent/'source/scripts/AnimalDialogGuard.lua').read_text())
r.execute('''
local G=LivestockAnimalDialogGuard
local screen={controller={trailer=vehicle},sourceList={getItemCount=function() return 1 end,getSelectedIndex=function() return 1 end},
sourceSelector={getState=function() return 1 end},sourceSelectorStateToAnimalType={[1]=2}}
load={cluster(1,1000),cluster(2,460)}
capacity=5000
assert(not G.preflight(screen,true)) -- actual wrong-type loading action
assert(warnings==1)
assert(not G.preflight(screen,true))
assert(warnings==1)
screen.sourceSelectorStateToAnimalType[1]=1
assert(G.preflight(screen,true)) -- goats/sheep same type
assert(G.preflight(screen,false)) -- unloading must still work
screen.sourceList.getItemCount=function() return 0 end
assert(not G.preflight(screen,true)) -- stale/empty selection never reaches game callback
load={}
screen.sourceList.getItemCount=function() return 1 end
screen.sourceSelectorStateToAnimalType[1]=2
assert(G.preflight(screen,true)) -- emptied trailer permits another type
''')
print('PASS: transfer-only warning, unchanged browsing, stale selection, same-type loading and unloading')
