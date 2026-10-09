from pathlib import Path
from lupa.lua51 import LuaRuntime
r=LuaRuntime()
r.execute('''
g_currentModName='FS25_z_LivestockCapacityHUD'
AnimalScreen=nil; warnings=0; moves=0; allowed=false
g_specializationManager={getSpecializationObjectByName=function() return {
isTypeAllowed=function(_,t) return allowed end,warn=function() warnings=warnings+1 end} end}
h={getAnimalTypeIndex=function() return 2 end,getSupportsAnimalSubType=function() return false end}
c={trailer={},husbandry=h,applySource=function() moves=moves+1 end,applyTarget=function() moves=moves+1 end,
initSourceItems=function(self) assert(self.husbandry:getSupportsAnimalSubType(1)); return 'clusters',nil,3 end}
''')
r.execute(Path('work/FS25-Mod-Fixes/fixes/livestock-capacity-hud/source/scripts/AnimalDialogGuard.lua').read_text())
r.execute('''
LivestockAnimalDialogGuard.installController({controller=c})
c:applySource(1); c:applyTarget(1)
assert(moves==0 and warnings==2)
allowed=true; c:applySource(1); c:applyTarget(1)
assert(moves==2)
local a,b,d=c:initSourceItems()
assert(a=='clusters' and b==nil and d==3)
assert(not h:getSupportsAnimalSubType(1))
''')
print('PASS controller rejection, same-type transfers, list-only filter override and restoration')
