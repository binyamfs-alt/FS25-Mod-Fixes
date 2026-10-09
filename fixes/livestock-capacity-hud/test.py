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
assert(vehicle:getMaxNumOfAnimals({typeIndex=2})==0)
assert(warnings==1)
assert(not H.getSupportsAnimalType(vehicle,function() return true end,2))
assert(warnings==1) -- no warning flood
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
