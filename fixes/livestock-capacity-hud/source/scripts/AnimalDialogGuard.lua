-- Copyright (C) 2026 BinyamFS. SPDX-License-Identifier: GPL-3.0-or-later
LivestockAnimalDialogGuard = {}
local G = LivestockAnimalDialogGuard
local specializationName = g_currentModName .. ".livestockCapacityHUD"

function G.installController(screen)
    local c = screen.controller
    if c == nil or c.trailer == nil or c.husbandry == nil or c.bfsGuardInstalled then return end
    c.bfsGuardInstalled = true
    for _, method in ipairs({"applySource", "applyTarget"}) do
        local original = c[method]
        if type(original) == "function" then
            c[method] = function(controller, ...)
                local spec = g_specializationManager:getSpecializationObjectByName(specializationName)
                local animalType = controller.husbandry:getAnimalTypeIndex()
                if spec ~= nil and not spec.isTypeAllowed(controller.trailer, animalType) then
                    spec.warn(controller.trailer)
                    print("[Livestock HUD] Rejected incompatible husbandry/trailer transfer")
                    return false
                end
                return original(controller, ...)
            end
        end
    end
    -- Viewing clusters must not filter them by the receiving pen's species.
    -- A read-only proxy limits the acceptance override to list construction;
    -- the actual pen and controller are never temporarily modified.
    local original = c.initSourceItems
    if type(original) == "function" then
        c.initSourceItems = function(controller, ...)
            local h = controller.husbandry
            local penView = setmetatable({getSupportsAnimalSubType=function() return true end}, {__index=h})
            local controllerView = setmetatable({husbandry=penView}, {__index=controller, __newindex=controller})
            return original(controllerView, ...)
        end
    end
    print("[Livestock HUD] Installed controller transfer protection")
end

function G.preflight(screen, loading)
    local controller = screen.controller
    local trailer = controller and controller.trailer
    if trailer == nil or trailer.spec_livestockTrailer == nil then return true end
    local spec = g_specializationManager:getSpecializationObjectByName(specializationName)
    if spec == nil then return true end
    -- A rejected/full transfer must not reach native callbacks with an empty
    -- list or a stale selection; those callbacks dereference the selected cluster.
    local list = screen.sourceList
    if list ~= nil and list.getItemCount ~= nil then
        local count = list:getItemCount()
        local index = list.getSelectedIndex ~= nil and list:getSelectedIndex() or list.selectedIndex
        if count == 0 or (index ~= nil and (index < 1 or index > count)) then
            return false
        end
    end
    if loading then
        local selector = screen.sourceSelector
        local animalType = selector ~= nil and selector.getState ~= nil
            and (screen.sourceSelectorStateToAnimalType or {})[selector:getState()] or nil
        local typeIndex = type(animalType) == "table" and animalType.typeIndex or animalType
        if typeIndex ~= nil and not spec.isTypeAllowed(trailer, typeIndex) then
            spec.warn(trailer)
            return false
        end
        local count = spec.getLoad(trailer)
        local capacity = trailer:getMaxNumOfAnimals(trailer:getCurrentAnimalType())
        if count > 0 and count >= capacity then
            g_currentMission:showBlinkingWarning(g_i18n:getText("bfs_trailerFull"), 3000)
            return false
        end
    end
    return true
end

if AnimalScreen ~= nil then
    for _, method in ipairs({"onClickBuyMode", "onClickSellMode"}) do
        if type(AnimalScreen[method]) == "function" then
            AnimalScreen[method] = Utils.prependedFunction(AnimalScreen[method], G.installController)
        end
    end
    for _, method in ipairs({"onClickBuy", "onClickSell"}) do
        if type(AnimalScreen[method]) == "function" then
            local loading = method == "onClickBuy"
            AnimalScreen[method] = Utils.overwrittenFunction(AnimalScreen[method], function(screen, superFunc, ...)
                if not G.preflight(screen, loading) then return false end
                return superFunc(screen, ...)
            end)
        end
    end
end
