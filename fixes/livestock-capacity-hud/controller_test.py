from pathlib import Path
from lupa.lua51 import LuaRuntime
r=LuaRuntime()
r.execute('''
g_currentModName='FS25_z_LivestockCapacityHUD'
AnimalScreen=nil; warnings=0; moves=0; allowed=false
g_specializationManager={getSpecializationObjectByName=function() return {
isTypeAllowed=function(_,t) return allowed end,warn=function() warnings=warnings+1 end,
getLoad=function() return 4000,{[3]=true} end} end}
g_currentMission={animalSystem={getTypeByIndex=function(_,i) return {typeIndex=i} end}}
h={getAnimalTypeIndex=function() return 2 end,getSupportsAnimalSubType=function() return false end}
c={trailer={},husbandry=h,applySource=function() moves=moves+1 end,applyTarget=function() moves=moves+1 end,
getSourceAnimalTypes=function(self,mode) return {{typeIndex=2}} end}
''')
r.execute((Path(__file__).parent/'source/scripts/AnimalDialogGuard.lua').read_text())
r.execute('''
LivestockAnimalDialogGuard.installController({controller=c})
c:applySource(1); c:applyTarget(1)
assert(moves==0 and warnings==2)
allowed=true; c:applySource(1); c:applyTarget(1)
assert(moves==2)
assert(c:getSourceAnimalTypes(true)[1].typeIndex==3) -- goats/sheep trailer at cow pen
assert(c:getSourceAnimalTypes(false)[1].typeIndex==2) -- pen view stays cows
assert(not h:getSupportsAnimalSubType(1))
''')
print('PASS controller rejection, same-type transfers, trailer types and unchanged pen view')
