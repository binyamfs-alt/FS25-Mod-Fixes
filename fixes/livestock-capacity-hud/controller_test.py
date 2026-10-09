from pathlib import Path
from lupa.lua51 import LuaRuntime
r=LuaRuntime()
r.execute('''
g_currentModName='FS25_z_LivestockCapacityHUD'
AnimalScreen={onYesNoSource=function(_,yes) if yes then moves=moves+1; successes=successes+1 end end,
onYesNoTarget=function(_,yes) if yes then moves=moves+1; successes=successes+1 end end}
successes=0; notices=0
Utils={overwrittenFunction=function(base,hook) return function(self,...) return hook(self,base,...) end end}
InfoDialog={show=function(text) notices=notices+1; assert(text=='Trailer already loaded!') end}
g_i18n={getText=function() return 'Trailer already loaded!' end}
warnings=0; moves=0; allowed=false
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

r.execute("""
allowed=false
local screen=setmetatable({controller=c},{__index=AnimalScreen})
local before=moves
screen:onYesNoTarget(true)
assert(moves==before and successes==0 and notices==1)
screen:onYesNoSource(true)
assert(moves==before and successes==0 and notices==2)
screen:onYesNoTarget(false)
assert(notices==2 and successes==0)
allowed=true; screen:onYesNoTarget(true)
assert(moves==before+1 and successes==1 and notices==2)
""")
print('PASS dialog rejection suppresses success, cancel and compatible confirmation remain native')
