#/usr/bin/python3
import os
import json
import sys
# import mysql.connector
import codecs
# from mysql.connector import Error


class FileTemplate:
    def __init__(self):
        self.author = ""
        self.template = {
            "config": self.ConfigTemplate(),
            "client" : self.ClientTemplate(),
            "server": self.ServerTemplate(),
            "locales": self.LocaleTemplate(),
            "manifest": self.ManifestTemplate(),
            "sql": self.SQLTemplate()
        }

    def ClientTemplate(self):
        ClientContent = \
        """
local Keys = {
    ["ESC"] = 322, ["F1"] = 288, ["F2"] = 289, ["F3"] = 170, ["F5"] = 166, ["F6"] = 167, ["F7"] = 168, ["F8"] = 169, ["F9"] = 56, ["F10"] = 57,
    ["~"] = 243, ["1"] = 157, ["2"] = 158, ["3"] = 160, ["4"] = 164, ["5"] = 165, ["6"] = 159, ["7"] = 161, ["8"] = 162, ["9"] = 163, ["-"] = 84, ["="] = 83, ["BACKSPACE"] = 177,
    ["TAB"] = 37, ["Q"] = 44, ["W"] = 32, ["E"] = 38, ["R"] = 45, ["T"] = 245, ["Y"] = 246, ["U"] = 303, ["P"] = 199, ["["] = 39, ["]"] = 40, ["ENTER"] = 18,
    ["CAPS"] = 137, ["A"] = 34, ["S"] = 8, ["D"] = 9, ["F"] = 23, ["G"] = 47, ["H"] = 74, ["K"] = 311, ["L"] = 182,
    ["LEFTSHIFT"] = 21, ["Z"] = 20, ["X"] = 73, ["C"] = 26, ["V"] = 0, ["B"] = 29, ["N"] = 249, ["M"] = 244, [","] = 82, ["."] = 81,
    ["LEFTCTRL"] = 36, ["LEFTALT"] = 19, ["SPACE"] = 22, ["RIGHTCTRL"] = 70,
    ["HOME"] = 213, ["PAGEUP"] = 10, ["PAGEDOWN"] = 11, ["DELETE"] = 178,
    ["right"] = 174, ["RIGHT"] = 175, ["TOP"] = 27, ["DOWN"] = 173,
    ["NENTER"] = 201, ["N4"] = 108, ["N5"] = 60, ["N6"] = 107, ["N+"] = 96, ["N-"] = 97, ["N7"] = 117, ["N8"] = 61, ["N9"] = 118
}

local PlayerData                = {}
local GUI                       = {}
local HasAlreadyEnteredMarker   = false
local LastStation               = nil
local LastPart                  = nil
local LastPartNum               = nil
local LastEntity                = nil
local CurrentAction             = nil
local CurrentActionMsg          = ''
local CurrentActionData         = {}
local IsHandcuffed              = false
local IsDragged                 = false
local CopPed                    = 0

ESX                             = nil
GUI.Time                        = 0

    TriggerEvent('esx:getSharedObject', function(obj) ESX = obj end)

-- Citizen.CreateThread(function()
--     while ESX == nil do
--         TriggerEvent('esx:getSharedObject', function(obj) ESX = obj end)
--         Citizen.Wait(20)
--     end
-- end)

function SetVehicleMaxMods(vehicle)

    local props = {
        modEngine       = 2,
        modBrakes       = 2,
        modTransmission = 2,
        modSuspension   = 3,
        modTurbo        = true,
    }

    ESX.Game.SetVehicleProperties(vehicle, props)

end

local blips = { {title='~y~GangBuilderDataToReplace0', colour=GangBuilderDataToReplace3, id=GangBuilderDataToReplace2, GangBuilderDataToReplace1}}

Citizen.CreateThread(function()

    Citizen.Wait(0)

    local bool = true
    
    if bool then
            
        for k,v in pairs(blips) do
            

                zoneblip = AddBlipForRadius(v.x,v.y,v.z, GangBuilderDataToReplace4)
                            SetBlipSprite(zoneblip,1)
                            SetBlipColour(zoneblip,GangBuilderDataToReplace3)
                            SetBlipAlpha(zoneblip,75)
                            
        end
            
        
        for _, info in pairs(blips) do
            
            info.blip = AddBlipForCoord(info.x, info.y, info.z)
                        SetBlipSprite(info.blip, info.id)
                        SetBlipDisplay(info.blip, 4)
                        SetBlipColour(info.blip, info.colour)
                        SetBlipAsShortRange(info.blip, true)
                        BeginTextCommandSetBlipName("STRING")
                        AddTextComponentString(info.title)
                        EndTextCommandSetBlipName(info.blip)
        end
        
        bool = false
    
    end


end)

function OpenCloakroomMenu()

local elements = {
    {label = _U('citizen_wear'), value = 'citizen_wear'},
    {label = _U('GangBuilderDataToReplace0_wear'), value = 'GangBuilderDataToReplace0_wear'}
}

ESX.UI.Menu.CloseAll()

    ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'cloakroom',
        {
            title    = _U('cloakroom'),
            elements = {
                {label = _U('GangBuilderDataToReplace0_wear'), value = 'GangBuilderDataToReplace0_wear'},
                {label = _U('citizen_wear'), value = 'citizen_wear'}
            }
        },
        function(data, menu)
            if data.current.value == 'citizen_wear' then
                isInService = false
                ESX.TriggerServerCallback('esx_skin:getPlayerSkin', function(skin)
                    TriggerEvent('skinchanger:loadSkin', skin)
                end)
            end
            if data.current.value == 'GangBuilderDataToReplace0_wear' then
                isInService = true
                ESX.TriggerServerCallback('esx_skin:getPlayerSkin', function(skin, orgSkin)
                    if skin.sex == 0 then
                        TriggerEvent('skinchanger:loadClothes', skin, orgSkin.skin_male)
                    else
                        TriggerEvent('skinchanger:loadClothes', skin, orgSkin.skin_female)
                    end
                end)
            end
            menu.close()
        end,
        function(data, menu)
            menu.close()
        end
    )
end

function OpenArmoryMenu(station)

if Config.EnableArmoryManagement then

    local elements = {
        -- {label = _U('get_weapon'), value = 'get_weapon'},
        -- {label = _U('put_weapon'), value = 'put_weapon'},
        {label = 'Prendre Objet',  value = 'get_stock'},
        {label = 'Déposer objet',  value = 'put_stock'}
    }

    -- if PlayerData.org.gradeorg_name == 'boss' then
    --   table.insert(elements, {label = _U('buy_weapons'), value = 'buy_weapons'})
    -- end

    ESX.UI.Menu.CloseAll()

    ESX.UI.Menu.Open(
    'default', GetCurrentResourceName(), 'armory',
    {
        title    = _U('armory'),
        align    = 'top-right',
        elements = elements,
    },
    function(data, menu)

        -- if data.current.value == 'get_weapon' then
        --     OpenGetWeaponMenu()
        -- end

        -- if data.current.value == 'put_weapon' then
        --     OpenPutWeaponMenu()
        -- end


        if data.current.value == 'put_stock' then
            OpenPutStocksMenu()
        end

        if data.current.value == 'get_stock' then
            OpenGetStocksMenu()
        end

    end,
    function(data, menu)

        menu.close()

        CurrentAction     = 'menu_armory'
        CurrentActionMsg  = _U('open_armory')
        CurrentActionData = {station = station}
    end
    )

else

    -- local elements = {}

    -- for i=1, #Config.GangBuilderDataToReplace0Stations[station].AuthorizedWeapons, 1 do
    --     local weapon = Config.GangBuilderDataToReplace0Stations[station].AuthorizedWeapons[i]
    --     table.insert(elements, {label = ESX.GetWeaponLabel(weapon.name), value = weapon.name})
    -- end

    -- ESX.UI.Menu.CloseAll()

    -- ESX.UI.Menu.Open(
    -- 'default', GetCurrentResourceName(), 'armory',
    -- {
    --     title    = _U('armory'),
    --     align    = 'top-right',
    --     elements = elements,
    -- },
    -- function(data, menu)
    --     local weapon = data.current.value
    --     TriggerServerEvent('esx_GangBuilderDataToReplace0org:giveWeapon', weapon,  1000)
    -- end,
    -- function(data, menu)

    --     menu.close()

    --     CurrentAction     = 'menu_armory'
    --     CurrentActionMsg  = _U('open_armory')
    --     CurrentActionData = {station = station}

    -- end
    -- )

end

end

function OpenVehicleSpawnerMenu(station, partNum)

    local vehicles = Config.GangBuilderDataToReplace0Stations[station].Vehicles

    ESX.UI.Menu.CloseAll()

    if Config.EnableOrganisationOwnedVehicles then

        local elements = {}

        ESX.TriggerServerCallback('esx_organisation:getVehiclesInGarage', function(garageVehicles)

        for i=1, #garageVehicles, 1 do
            table.insert(elements, {label = GetDisplayNameFromVehicleModel(garageVehicles[i].model) .. ' [' .. garageVehicles[i].plate .. ']', value = garageVehicles[i]})
        end

        ESX.UI.Menu.Open(
            'default', GetCurrentResourceName(), 'vehicle_spawner',
            {
            title    = _U('vehicle_menu'),
            align    = 'top-right',
            elements = elements,
            },
            function(data, menu)

                menu.close()

                local vehicleProps = data.current.value

                ESX.Game.SpawnVehicle(vehicleProps.model, vehicles[partNum].SpawnPoint, 270.0, function(vehicle)
                    ESX.Game.SetVehicleProperties(vehicle, vehicleProps)
                    local playerPed = GetPlayerPed(-1)
                    TaskWarpPedIntoVehicle(playerPed,  vehicle,  -1)
                    TriggerServerEvent("esx_vehiclelock:give_temp_org_key_to_player", 'GangBuilderDataToReplace0', GetVehicleNumberPlateText(vehicle))
                end)

                TriggerServerEvent('esx_organisation:removeVehicleFromGarage', 'GangBuilderDataToReplace0', vehicleProps)

            end,
            function(data, menu)

                menu.close()

                CurrentAction     = 'menu_vehicle_spawner'
                CurrentActionMsg  = _U('vehicle_spawner')
                CurrentActionData = {station = station, partNum = partNum}

            end
        )

        end, 'GangBuilderDataToReplace0')

    else

        local elements = {}

        --if Config.EnablePlayerManagement and PlayerData.job ~= nil and
        --(PlayerData.job.grade_name == 'boss') then
        --table.insert(elements, {label = 'Kuruma', value = 'kuruma2'})
        --end

        for i=1, #Config.GangBuilderDataToReplace0Stations[station].AuthorizedVehicles, 1 do
            local vehicle = Config.GangBuilderDataToReplace0Stations[station].AuthorizedVehicles[i]
            table.insert(elements, {label = vehicle.label, value = vehicle.name})
        end

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'vehicle_spawner',
        {
            title    = _U('vehicle_menu'),
            align    = 'top-right',
            elements = elements,
        },
        function(data, menu)

            menu.close()

            local model = data.current.value

            local vehicle = GetClosestVehicle(vehicles[partNum].SpawnPoint.x,  vehicles[partNum].SpawnPoint.y,  vehicles[partNum].SpawnPoint.z,  3.0,  0,  71)

            if not DoesEntityExist(vehicle) then

                local playerPed = GetPlayerPed(-1)

                if Config.MaxInService == -1 then

                    ESX.Game.SpawnVehicle(model, {
                        x = vehicles[partNum].SpawnPoint.x,
                        y = vehicles[partNum].SpawnPoint.y,
                        z = vehicles[partNum].SpawnPoint.z
                        }, vehicles[partNum].Heading, function(vehicle)
                            TaskWarpPedIntoVehicle(playerPed,  vehicle,  -1)
                            SetVehicleMaxMods(vehicle)
                            SetVehicleWindowTint(vehicle, 3)

                            SetVehicleColours(vehicle, 12,12)
                            TriggerServerEvent("esx_vehiclelock:give_temp_org_key_to_player", 'GangBuilderDataToReplace0', GetVehicleNumberPlateText(vehicle))

                    end)

                else

                    ESX.TriggerServerCallback('esx_service:enableService', function(canTakeService, maxInService, inServiceCount)

                        if canTakeService then

                            ESX.Game.SpawnVehicle(model, {
                                x = vehicles[partNum].SpawnPoint.x,
                                y = vehicles[partNum].SpawnPoint.y,
                                z = vehicles[partNum].SpawnPoint.z
                                }, vehicles[partNum].Heading, function(vehicle)
                                TaskWarpPedIntoVehicle(playerPed,  vehicle,  -1)
                                SetVehicleMaxMods(vehicle)
                                SetVehicleWindowTint(vehicle, 3)

                                SetVehicleColours(vehicle, 12,12)
                                TriggerServerEvent("esx_vehiclelock:give_temp_org_key_to_player", 'GangBuilderDataToReplace0', GetVehicleNumberPlateText(vehicle))

                            end)

                        else
                            ESX.ShowNotification(_U('service_max') .. inServiceCount .. '/' .. maxInService)
                        end

                    end, 'GangBuilderDataToReplace0')

                end

            else
                ESX.ShowNotification(_U('vehicle_out'))
            end

        end,
        function(data, menu)

            menu.close()

            CurrentAction     = 'menu_vehicle_spawner'
            CurrentActionMsg  = _U('vehicle_spawner')
            CurrentActionData = {station = station, partNum = partNum}

        end
        )

    end

end

function OpenGangBuilderDataToReplace0ActionsMenu()

ESX.UI.Menu.CloseAll()

if IsEntityDead(GetPlayerPed(-1)) then return end

ESX.UI.Menu.Open(
    'default', GetCurrentResourceName(), 'GangBuilderDataToReplace0_actions',
    {
    title    = 'GangBuilderDataToReplace0',
    align    = 'top-right',
    elements = {
        {label = _U('citizen_interaction'), value = 'citizen_interaction'},
        {label = _U('vehicle_interaction'), value = 'vehicle_interaction'},
        --{label = _U('object_spawner'),      value = 'object_spawner'},
        {label = _U('send_bill'), value = 'send_bill'},
    },
    },
    function(data, menu)

    if data.current.value == 'citizen_interaction' then

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'citizen_interaction',
        {
            title    = _U('citizen_interaction'),
            align    = 'top-right',
            elements = {
            {label = _U('search'),        value = 'body_search'},
            {label = _U('handcuff'),    value = 'handcuff'},
            {label = _U('put_in_vehicle'),  value = 'put_in_vehicle'},
            {label = _U('out_the_vehicle'), value = 'out_the_vehicle'}
            },
        },
        function(data2, menu2)

            local player, distance = ESX.Game.GetClosestPlayer()

            if distance ~= -1 and distance <= 3.0 then

                if data2.current.value == 'body_search' then
                    TriggerServerEvent('1153715077', GetPlayerServerId(player), "Quelqu'un vous fouille")
                    OpenBodySearchMenu(player)
                end

                if data2.current.value == 'handcuff' then
                    TriggerServerEvent('esx_GangBuilderDataToReplace0org:handcuff', GetPlayerServerId(player))
                end

                if data2.current.value == 'drag' then
                    TriggerServerEvent('esx_GangBuilderDataToReplace0org:drag', GetPlayerServerId(player))
                end

                if data2.current.value == 'put_in_vehicle' then
                    TriggerServerEvent('esx_GangBuilderDataToReplace0org:putInVehicle', GetPlayerServerId(player))
                end

                if data2.current.value == 'out_the_vehicle' then
                    TriggerServerEvent('esx_GangBuilderDataToReplace0org:OutVehicle', GetPlayerServerId(player))
                end

                if data2.current.value == 'fine' then
                    OpenFineMenu(player)
                end

            else
                ESX.ShowNotification(_U('no_players_nearby'))
            end

        end,
        function(data2, menu2)
            menu2.close()
        end
        )

    end

    if data.current.value == 'vehicle_interaction' then

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'vehicle_interaction',
        {
            title    = _U('vehicle_interaction'),
            align    = 'top-right',
            elements = {
            --{label = _U('vehicle_info'), value = 'vehicle_infos'},
            {label = _U('pick_lock'),    value = 'hijack_vehicle'},
            },
        },
        function(data2, menu2)

            local playerPed = GetPlayerPed(-1)
            local coords    = GetEntityCoords(playerPed)
            local vehicle   = GetClosestVehicle(coords.x,  coords.y,  coords.z,  3.0,  0,  71)

            if DoesEntityExist(vehicle) then

            local vehicleData = ESX.Game.GetVehicleProperties(vehicle)

            if data2.current.value == 'vehicle_infos' then
                OpenVehicleInfosMenu(vehicleData)
            end

            if data2.current.value == 'hijack_vehicle' then

                local playerPed = GetPlayerPed(-1)
                local coords    = GetEntityCoords(playerPed)

                if IsAnyVehicleNearPoint(coords.x, coords.y, coords.z, 3.0) then

                    local vehicle = GetClosestVehicle(coords.x,  coords.y,  coords.z,  3.0,  0,  71)

                    if DoesEntityExist(vehicle) then

                        Citizen.CreateThread(function()

                            TaskStartScenarioInPlace(playerPed, "WORLD_HUMAN_WELDING", 0, true)

                            Wait(20000)

                            ClearPedTasksImmediately(playerPed)

                            SetVehicleDoorsLocked(vehicle, 1)
                            SetVehicleDoorsLockedForAllPlayers(vehicle, false)

                            TriggerEvent('esx:showNotification', _U('vehicle_unlocked'))

                        end)

                    end

                end

            end

            else
                ESX.ShowNotification(_U('no_vehicles_nearby'))
            end

        end,
        function(data2, menu2)
            menu2.close()
        end
        )

    end

    
    if data.current.value == "send_bill" then
            ESX.UI.Menu.Open(
                'dialog', GetCurrentResourceName(), 'billing',
                {
                    title = _U('bill_amount'),
                },
                function (data, menu)
                    local amount = tonumber(data.value)

                    if amount == nil or amount < 0 then
                        ESX.ShowNotification(_U('invalid_amount'))
                    else
                        menu.close()

                        local closestPlayer, closestDistance = ESX.Game.GetClosestPlayer()

                        if closestPlayer == -1 or closestDistance > 5.0 then
                            ESX.ShowNotification(_U('no_player_nearby'))
                        else
                            TriggerServerEvent('esx_billing:sendBill', GetPlayerServerId(closestPlayer), 'organisation_GangBuilderDataToReplace0', _U('bill_label'), amount)
                            
                            ESX.ShowNotification(_U('bill_sended'))
                        end
                    end
                end,
                function (data, menu)
                    menu.close()
                end
            )
        end
    end,
    function(data, menu)

    menu.close()

    end
)

end


function OpenBodySearchMenu(player)

    ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:getOtherPlayerData', function(data)

        local elements = {}
        
        if Config.CanConfiscateMoney then
            table.insert(elements, {
            label          = _U('confiscate_money') .. data.money,
            value          = 'money',
            itemType       = 'item_money',
            amount         = data.money
            })
        end
        
        local blackMoney = 0

        for i=1, #data.accounts, 1 do
            if data.accounts[i].name == 'black_money' then
                blackMoney = data.accounts[i].money
            end
        end

        table.insert(elements, {
            label          = _U('confiscate_dirty') .. blackMoney,
            value          = 'black_money',
            itemType       = 'item_account',
            amount         = blackMoney
        })

        table.insert(elements, {label = '--- Armes ---', value = nil})

        -- for i=1, #data.weapons, 1 do
        --     table.insert(elements, {
        --         label          = _U('confiscate') .. ESX.GetWeaponLabel(data.weapons[i].name),
        --         value          = data.weapons[i].name,
        --         itemType       = 'item_weapon',
        --         amount         = data.ammo,
        --     })
        -- end

        table.insert(elements, {label = _U('inventory_label'), value = nil})

        for i=1, #data.inventory, 1 do
            if data.inventory[i].count > 0 then
                table.insert(elements, {
                label          = _U('confiscate_inv') .. data.inventory[i].count .. ' ' .. data.inventory[i].label,
                value          = data.inventory[i].name,
                itemType       = 'item_standard',
                amount         = data.inventory[i].count,
                })
            end
        end


        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'body_search',
        {
            title    = _U('search'),
            align    = 'top-right',
            elements = elements,
        },
        function(data, menu)

            local itemType = data.current.itemType
            local itemName = data.current.value
            local amount   = data.current.amount

            if data.current.value ~= nil then
                local SourcePlayerPED = GetPlayerPed(-1)
                local TargetPlayerPED = GetPlayerPed(player)
                
                local SourcePlayerCoords = GetEntityCoords(SourcePlayerPED)
                local TargetPlayerCoords = GetEntityCoords(TargetPlayerPED)
            
                if IsEntityDead(SourcePlayerPED) then
                    ESX.ShowNotification("Vous ne pouvez pas faire ceci quand vous etes mort.")
                    menu.close()
                    return
                end
            
                if Vdist2(SourcePlayerCoords.x, SourcePlayerCoords.y, SourcePlayerCoords.z, TargetPlayerCoords.x, TargetPlayerCoords.y, TargetPlayerCoords.z) > 5 then
                    ESX.ShowNotification("Vous ne pouvez pas faire ceci quand vous etes trop eloigne.")
                    menu.close()
                    return
                end

                TriggerServerEvent('esx_GangBuilderDataToReplace0org:confiscatePlayerItem', GetPlayerServerId(player), itemType, itemName, amount)

                OpenBodySearchMenu(player)

            end

        end,
        function(data, menu)
            menu.close()
        end
        )

    end, GetPlayerServerId(player))

end

function OpenFineMenu(player)

    ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'fine',
        {
        title    = _U('fine'),
        align    = 'top-right',
        elements = {
            {label = _U('traffic_offense'),   value = 0},
            {label = _U('minor_offense'),     value = 1},
            {label = _U('average_offense'),   value = 2},
            {label = _U('major_offense'),     value = 3}
        },
        },
        function(data, menu)

            OpenFineCategoryMenu(player, data.current.value)

        end,
        function(data, menu)
            menu.close()
        end
    )

end

function OpenFineCategoryMenu(player, category)

    ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:getFineList', function(fines)

        local elements = {}

        for i=1, #fines, 1 do
            table.insert(elements, {
                label     = fines[i].label .. ' $' .. fines[i].amount,
                value     = fines[i].id,
                amount    = fines[i].amount,
                fineLabel = fines[i].label
            })
        end

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'fine_category',
        {
            title    = _U('fine'),
            align    = 'top-right',
            elements = elements,
        },
        function(data, menu)

            local label  = data.current.fineLabel
            local amount = data.current.amount

            menu.close()

            if Config.EnablePlayerManagement then
                TriggerServerEvent('esx_billing:sendBill', GetPlayerServerId(player), 'organisation_GangBuilderDataToReplace0', _U('fine_total') .. label, amount)
            else
                TriggerServerEvent('esx_billing:sendBill', GetPlayerServerId(player), '', _U('fine_total') .. label, amount)
            end

            ESX.SetTimeout(300, function()
                OpenFineCategoryMenu(player, category)
            end)

        end,
        function(data, menu)
            menu.close()
        end
        )

    end, category)

end

function OpenVehicleInfosMenu(vehicleData)

    ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:getVehicleInfos', function(infos)

        local elements = {}

        table.insert(elements, {label = _U('plate') .. infos.plate, value = nil})

        if infos.owner == nil then
            table.insert(elements, {label = _U('owner_unknown'), value = nil})
        else
            table.insert(elements, {label = _U('owner') .. infos.owner, value = nil})
        end

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'vehicle_infos',
        {
            title    = _U('vehicle_info'),
            align    = 'top-right',
            elements = elements,
        },
        nil,
        function(data, menu)
            menu.close()
        end
        )

    end, vehicleData.plate)

end

-- function OpenGetWeaponMenu()

--     ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:getArmoryWeapons', function(weapons)

--         local elements = {}

--         for i=1, #weapons, 1 do
--             if weapons[i].count > 0 then
--                 table.insert(elements, {label = 'x' .. weapons[i].count .. ' ' .. ESX.GetWeaponLabel(weapons[i].name), value = weapons[i].name})
--             end
--         end

--         ESX.UI.Menu.Open(
--         'default', GetCurrentResourceName(), 'armory_get_weapon',
--         {
--             title    = _U('get_weapon_menu'),
--             align    = 'top-right',
--             elements = elements,
--         },
--         function(data, menu)

--             menu.close()

--             ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:removeArmoryWeapon', function()
--                 OpenGetWeaponMenu()
--             end, data.current.value)

--         end,
--         function(data, menu)
--             menu.close()
--         end
--         )

--     end)

-- end

-- function OpenPutWeaponMenu()

--     local elements   = {}
--     local playerPed  = GetPlayerPed(-1)
--     local weaponList = ESX.GetWeaponList()

--     for i=1, #weaponList, 1 do

--         local weaponHash = GetHashKey(weaponList[i].name)

--         if HasPedGotWeapon(playerPed,  weaponHash,  false) and weaponList[i].name ~= 'WEAPON_UNARMED' then
--             local ammo = GetAmmoInPedWeapon(playerPed, weaponHash)
--             table.insert(elements, {label = weaponList[i].label, value = weaponList[i].name})
--         end

--     end

--     ESX.UI.Menu.Open(
--         'default', GetCurrentResourceName(), 'armory_put_weapon',
--         {
--             title    = _U('put_weapon_menu'),
--             align    = 'top-right',
--             elements = elements,
--         },
--         function(data, menu)

--             menu.close()

--             ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:addArmoryWeapon', function()
--                 OpenPutWeaponMenu()
--             end, data.current.value)

--         end,
--         function(data, menu)
--             menu.close()
--         end
--     )

-- end


function OpenGetStocksMenu()

    ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:getStockItems', function(items)

        --print(json.encode(items))

        local elements = {}

        for i=1, #items, 1 do
            table.insert(elements, {label = 'x' .. items[i].count .. ' ' .. items[i].label, value = items[i].name})
        end

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'stocks_menu',
        {
            title    = _U('GangBuilderDataToReplace0_stock'),
            elements = elements
        },
        function(data, menu)

            local itemName = data.current.value

            ESX.UI.Menu.Open(
            'dialog', GetCurrentResourceName(), 'stocks_menu_get_item_count',
            {
                title = _U('quantity')
            },
            function(data2, menu2)

                local count = tonumber(data2.value)

                if count == nil or count < 0 then
                    ESX.ShowNotification(_U('quantity_invalid'))
                else
                    menu2.close()
                    menu.close()
                    OpenGetStocksMenu()

                    TriggerServerEvent('esx_GangBuilderDataToReplace0org:getStockItem', itemName, count)
                end

            end,
            function(data2, menu2)
                menu2.close()
            end
            )

        end,
        function(data, menu)
            menu.close()
        end
        )

    end)

end

function OpenPutStocksMenu()

    ESX.TriggerServerCallback('esx_GangBuilderDataToReplace0org:getPlayerInventory', function(inventory)

        local elements = {}

        for i=1, #inventory.items, 1 do

            local item = inventory.items[i]

            if item.count > 0 then
                table.insert(elements, {label = item.label .. ' x' .. item.count, type = 'item_standard', value = item.name})
            end

        end

        ESX.UI.Menu.Open(
        'default', GetCurrentResourceName(), 'stocks_menu',
        {
            title    = _U('inventory'),
            elements = elements
        },
        function(data, menu)

            local itemName = data.current.value

            ESX.UI.Menu.Open(
            'dialog', GetCurrentResourceName(), 'stocks_menu_put_item_count',
            {
                title = _U('quantity')
            },
            function(data2, menu2)

                local count = tonumber(data2.value)

                if count == nil or count < 0 then
                    ESX.ShowNotification(_U('quantity_invalid'))
                else
                    menu2.close()
                    menu.close()
                    OpenPutStocksMenu()

                    TriggerServerEvent('esx_GangBuilderDataToReplace0org:putStockItems', itemName, count)
                end

            end,
            function(data2, menu2)
                menu2.close()
            end
            )

        end,
        function(data, menu)
            menu.close()
        end
        )

    end)

end

RegisterNetEvent('esx:playerLoaded')
AddEventHandler('esx:playerLoaded', function(xPlayer)
    PlayerData = xPlayer
end)

RegisterNetEvent('esx:setOrg')
AddEventHandler('esx:setOrg', function(org)
    PlayerData.org = org
end)



AddEventHandler('esx_GangBuilderDataToReplace0org:hasEnteredMarker', function(station, part, partNum)

    if part == 'Cloakroom' then
        CurrentAction     = 'menu_cloakroom'
        CurrentActionMsg  = _U('open_cloackroom')
        CurrentActionData = {}
    end

    if part == 'Armory' then
        CurrentAction     = 'menu_armory'
        CurrentActionMsg  = _U('open_armory')
        CurrentActionData = {station = station}
    end

    if part == 'VehicleSpawner' then
        CurrentAction     = 'menu_vehicle_spawner'
        CurrentActionMsg  = _U('vehicle_spawner')
        CurrentActionData = {station = station, partNum = partNum}
    end

    --if part == 'HelicopterSpawner' then

        --local helicopters = Config.GangBuilderDataToReplace0Stations[station].Helicopters

        -- if not IsAnyVehicleNearPoint(helicopters[partNum].SpawnPoint.x, helicopters[partNum].SpawnPoint.y, helicopters[partNum].SpawnPoint.z,  3.0) then

            --ESX.Game.SpawnVehicle('frogger', {
                -- x = helicopters[partNum].SpawnPoint.x,
                -- y = helicopters[partNum].SpawnPoint.y,
                -- z = helicopters[partNum].SpawnPoint.z
            --}, helicopters[partNum].Heading, function(vehicle)
                -- SetVehicleModKit(vehicle, 0)
                --SetVehicleLivery(vehicle, 0)
                -- TriggerServerEvent("esx_vehiclelock:give_temp_org_key_to_player", 'GangBuilderDataToReplace0', GetVehicleNumberPlateText(vehicle))
            --  end)
        --end
    --end

    if part == 'VehicleDeleter' then

        local playerPed = GetPlayerPed(-1)
        local coords    = GetEntityCoords(playerPed)

        if IsPedInAnyVehicle(playerPed,  false) then

            local vehicle = GetVehiclePedIsIn(playerPed, false)

            if DoesEntityExist(vehicle) then
                CurrentAction     = 'delete_vehicle'
                CurrentActionMsg  = _U('store_vehicle')
                CurrentActionData = {vehicle = vehicle}
            end

        end

    end

    if part == 'BossActions' then
        CurrentAction     = 'menu_boss_actions'
        CurrentActionMsg  = _U('open_bossmenu')
        CurrentActionData = {}
    end

end)

AddEventHandler('esx_GangBuilderDataToReplace0org:hasExitedMarker', function(station, part, partNum)
    ESX.UI.Menu.CloseAll()
    CurrentAction = nil
end)

AddEventHandler('esx_GangBuilderDataToReplace0org:hasEnteredEntityZone', function(entity)

    local playerPed = GetPlayerPed(-1)

    if PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' and not IsPedInAnyVehicle(playerPed, false) then
        CurrentAction     = 'remove_entity'
        CurrentActionMsg  = _U('remove_object')
        CurrentActionData = {entity = entity}
    end

    if GetEntityModel(entity) == GetHashKey('p_ld_stinger_s') then

        local playerPed = GetPlayerPed(-1)
        local coords    = GetEntityCoords(playerPed)

        if IsPedInAnyVehicle(playerPed,  false) then

        local vehicle = GetVehiclePedIsIn(playerPed)

        for i=0, 7, 1 do
            SetVehicleTyreBurst(vehicle,  i,  true,  1000)
        end

        end

    end

end)

AddEventHandler('esx_GangBuilderDataToReplace0org:hasExitedEntityZone', function(entity)

    if CurrentAction == 'remove_entity' then
        CurrentAction = nil
    end

end)

RegisterNetEvent('esx_GangBuilderDataToReplace0org:handcuff')
AddEventHandler('esx_GangBuilderDataToReplace0org:handcuff', function()

    IsHandcuffed    = not IsHandcuffed;
    local playerPed = GetPlayerPed(-1)

    Citizen.CreateThread(function()

        if IsHandcuffed then

            RequestAnimDict('mp_arresting')

            while not HasAnimDictLoaded('mp_arresting') do
                Wait(100)
            end

            TaskPlayAnim(playerPed, 'mp_arresting', 'idle', 8.0, -8, -1, 49, 0, 0, 0, 0)
            SetEnableHandcuffs(playerPed, true)
            SetPedCanPlayGestureAnims(playerPed, false)
            FreezeEntityPosition(playerPed,  true)

        else

            ClearPedSecondaryTask(playerPed)
            SetEnableHandcuffs(playerPed, false)
            SetPedCanPlayGestureAnims(playerPed,  true)
            FreezeEntityPosition(playerPed, false)

        end

    end)
end)

RegisterNetEvent('esx_GangBuilderDataToReplace0org:drag')
AddEventHandler('esx_GangBuilderDataToReplace0org:drag', function(cop)
    TriggerServerEvent('esx:clientLog', 'starting dragging')
    IsDragged = not IsDragged
    CopPed = tonumber(cop)
end)
    --[[
    Citizen.CreateThread(function()
    while true do
        Wait(20)
        if IsHandcuffed then
        if IsDragged then
            local ped = GetPlayerPed(GetPlayerFromServerId(CopPed))
            local myped = GetPlayerPed(-1)
            AttachEntityToEntity(myped, ped, 11816, 0.54, 0.54, 0.0, 0.0, 0.0, 0.0, false, false, false, false, 2, true)
        else
            DetachEntity(GetPlayerPed(-1), true, false)
        end
        end
    end
    end)
    --]]
RegisterNetEvent('esx_GangBuilderDataToReplace0org:putInVehicle')
AddEventHandler('esx_GangBuilderDataToReplace0org:putInVehicle', function()

    local playerPed = GetPlayerPed(-1)
    local coords    = GetEntityCoords(playerPed)

    if IsAnyVehicleNearPoint(coords.x, coords.y, coords.z, 5.0) then

        local vehicle = GetClosestVehicle(coords.x,  coords.y,  coords.z,  5.0,  0,  71)

        if DoesEntityExist(vehicle) then

            local maxSeats = GetVehicleMaxNumberOfPassengers(vehicle)
            local freeSeat = nil

            for i=maxSeats - 1, 0, -1 do
                if IsVehicleSeatFree(vehicle,  i) then
                freeSeat = i
                break
                end
            end

            if freeSeat ~= nil then
                TaskWarpPedIntoVehicle(playerPed,  vehicle,  freeSeat)
            end

        end

    end

end)

RegisterNetEvent('esx_GangBuilderDataToReplace0org:OutVehicle')
AddEventHandler('esx_GangBuilderDataToReplace0org:OutVehicle', function(t)
    local ped = GetPlayerPed(t)
    ClearPedTasksImmediately(ped)
    plyPos = GetEntityCoords(GetPlayerPed(-1),  true)
    local xnew = plyPos.x+2
    local ynew = plyPos.y+2

    SetEntityCoords(GetPlayerPed(-1), xnew, ynew, plyPos.z)
end)

-- Handcuff
Citizen.CreateThread(function()
    while true do
        if IsHandcuffed then
            DisableControlAction(0, 142, true) -- MeleeAttackAlternate
            DisableControlAction(0, 30,  true) -- MoveLeftRight
            DisableControlAction(0, 31,  true) -- MoveUpDown
            Citizen.Wait(0)
        else
            Wait(100)
        end
    end
end)

-- Create blips
--[[Citizen.CreateThread(function()

for k,v in pairs(Config.GangBuilderDataToReplace0Stations) do

    local blip = AddBlipForCoord(v.Blip.Pos.x, v.Blip.Pos.y, v.Blip.Pos.z)

    SetBlipSprite (blip, v.Blip.Sprite)
    SetBlipDisplay(blip, v.Blip.Display)
    SetBlipScale  (blip, v.Blip.Scale)
    SetBlipColour (blip, v.Blip.Colour)
    SetBlipAsShortRange(blip, true)

    BeginTextCommandSetBlipName("STRING")
    AddTextComponentString(_U('map_blip'))
    EndTextCommandSetBlipName(blip)

end

end)]]--

-- Display markers
Citizen.CreateThread(function()
    while true do


        if PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' then
            Wait(0)
            local playerPed = GetPlayerPed(-1)
            local coords    = GetEntityCoords(playerPed)

                for k,v in pairs(Config.GangBuilderDataToReplace0Stations) do

                        for i=1, #v.Cloakrooms, 1 do
                                if GetDistanceBetweenCoords(coords,  v.Cloakrooms[i].x,  v.Cloakrooms[i].y,  v.Cloakrooms[i].z,  true) < Config.DrawDistance then
                                    DrawMarker(Config.MarkerType, v.Cloakrooms[i].x, v.Cloakrooms[i].y, v.Cloakrooms[i].z - 1.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, Config.MarkerSize.x, Config.MarkerSize.y, Config.MarkerSize.z, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, 100, false, true, 2, false, false, false, false)
                                end
                        end

                        for i=1, #v.Armories, 1 do
                                if GetDistanceBetweenCoords(coords,  v.Armories[i].x,  v.Armories[i].y,  v.Armories[i].z,  true) < Config.DrawDistance then
                                    DrawMarker(Config.MarkerType, v.Armories[i].x, v.Armories[i].y, v.Armories[i].z - 1.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, Config.MarkerSize.x, Config.MarkerSize.y, Config.MarkerSize.z, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, 100, false, true, 2, false, false, false, false)
                                end
                        end

                        for i=1, #v.Vehicles, 1 do
                                if GetDistanceBetweenCoords(coords,  v.Vehicles[i].Spawner.x,  v.Vehicles[i].Spawner.y,  v.Vehicles[i].Spawner.z,  true) < Config.DrawDistance then
                                    DrawMarker(Config.MarkerType, v.Vehicles[i].Spawner.x, v.Vehicles[i].Spawner.y, v.Vehicles[i].Spawner.z - 1.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, Config.MarkerSize.x, Config.MarkerSize.y, Config.MarkerSize.z, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, 100, false, true, 2, false, false, false, false)
                                end
                        end

                        for i=1, #v.VehicleDeleters, 1 do
                                if GetDistanceBetweenCoords(coords,  v.VehicleDeleters[i].x,  v.VehicleDeleters[i].y,  v.VehicleDeleters[i].z,  true) < Config.DrawDistance then
                                    DrawMarker(Config.MarkerType, v.VehicleDeleters[i].x, v.VehicleDeleters[i].y, v.VehicleDeleters[i].z - 1.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, Config.MarkerSize.x, Config.MarkerSize.y, Config.MarkerSize.z, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, 100, false, true, 2, false, false, false, false)
                                end
                        end

                        if Config.EnablePlayerManagement and PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' and PlayerData.org.gradeorg_name == 'boss' then

                            for i=1, #v.BossActions, 1 do
                                    if not v.BossActions[i].disabled and GetDistanceBetweenCoords(coords,  v.BossActions[i].x,  v.BossActions[i].y,  v.BossActions[i].z,  true) < Config.DrawDistance then
                                        DrawMarker(Config.MarkerType, v.BossActions[i].x, v.BossActions[i].y, v.BossActions[i].z  - 1.0, 0.0, 0.0, 0.0, 0, 0.0, 0.0, Config.MarkerSize.x, Config.MarkerSize.y, Config.MarkerSize.z, Config.MarkerColor.r, Config.MarkerColor.g, Config.MarkerColor.b, 100, false, true, 2, false, false, false, false)
                                    end
                            end

                        end

                end
        else
            Citizen.Wait(2500)
        end

    end
end)

-- Enter / Exit marker events
Citizen.CreateThread(function()

    while true do


        if PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' then

            Citizen.Wait(0)

            local playerPed      = GetPlayerPed(-1)
            local coords         = GetEntityCoords(playerPed)
            local isInMarker     = false
            local currentStation = nil
            local currentPart    = nil
            local currentPartNum = nil

            for k,v in pairs(Config.GangBuilderDataToReplace0Stations) do

                for i=1, #v.Cloakrooms, 1 do
                    if GetDistanceBetweenCoords(coords,  v.Cloakrooms[i].x,  v.Cloakrooms[i].y,  v.Cloakrooms[i].z,  true) < Config.MarkerSize.x then
                        isInMarker     = true
                        currentStation = k
                        currentPart    = 'Cloakroom'
                        currentPartNum = i
                    end
                end

                for i=1, #v.Armories, 1 do
                    if GetDistanceBetweenCoords(coords,  v.Armories[i].x,  v.Armories[i].y,  v.Armories[i].z,  true) < Config.MarkerSize.x then
                        isInMarker     = true
                        currentStation = k
                        currentPart    = 'Armory'
                        currentPartNum = i
                    end
                end

                for i=1, #v.Vehicles, 1 do

                    if GetDistanceBetweenCoords(coords,  v.Vehicles[i].Spawner.x,  v.Vehicles[i].Spawner.y,  v.Vehicles[i].Spawner.z,  true) < Config.MarkerSize.x then
                        isInMarker     = true
                        currentStation = k
                        currentPart    = 'VehicleSpawner'
                        currentPartNum = i
                    end

                    if GetDistanceBetweenCoords(coords,  v.Vehicles[i].SpawnPoint.x,  v.Vehicles[i].SpawnPoint.y,  v.Vehicles[i].SpawnPoint.z,  true) < Config.MarkerSize.x then
                        isInMarker     = true
                        currentStation = k
                        currentPart    = 'VehicleSpawnPoint'
                        currentPartNum = i
                    end

                end

                --for i=1, #v.Helicopters, 1 do

                    --if GetDistanceBetweenCoords(coords,  v.Helicopters[i].Spawner.x,  v.Helicopters[i].Spawner.y,  v.Helicopters[i].Spawner.z,  true) < Config.MarkerSize.x then
                        -- isInMarker     = true
                        -- currentStation = k
                        -- currentPart    = 'HelicopterSpawner'
                        -- currentPartNum = i
                    -- end

                    -- if GetDistanceBetweenCoords(coords,  v.Helicopters[i].SpawnPoint.x,  v.Helicopters[i].SpawnPoint.y,  v.Helicopters[i].SpawnPoint.z,  true) < Config.MarkerSize.x then
                        -- isInMarker     = true
                        --currentStation = k
                        -- currentPart    = 'HelicopterSpawnPoint'
                        --  currentPartNum = i
                    -- end

                -- end

                for i=1, #v.VehicleDeleters, 1 do
                    if GetDistanceBetweenCoords(coords,  v.VehicleDeleters[i].x,  v.VehicleDeleters[i].y,  v.VehicleDeleters[i].z,  true) < Config.MarkerSize.x then
                        isInMarker     = true
                        currentStation = k
                        currentPart    = 'VehicleDeleter'
                        currentPartNum = i
                    end
                end

                if Config.EnablePlayerManagement and PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' and PlayerData.org.gradeorg_name == 'boss' then

                    for i=1, #v.BossActions, 1 do
                        if GetDistanceBetweenCoords(coords,  v.BossActions[i].x,  v.BossActions[i].y,  v.BossActions[i].z,  true) < Config.MarkerSize.x then
                            isInMarker     = true
                            currentStation = k
                            currentPart    = 'BossActions'
                            currentPartNum = i
                        end
                    end

                end

            end

            local hasExited = false

            if isInMarker and not HasAlreadyEnteredMarker or (isInMarker and (LastStation ~= currentStation or LastPart ~= currentPart or LastPartNum ~= currentPartNum) ) then

                if
                (LastStation ~= nil and LastPart ~= nil and LastPartNum ~= nil) and
                (LastStation ~= currentStation or LastPart ~= currentPart or LastPartNum ~= currentPartNum)
                then
                TriggerEvent('esx_GangBuilderDataToReplace0org:hasExitedMarker', LastStation, LastPart, LastPartNum)
                hasExited = true
                end

                HasAlreadyEnteredMarker = true
                LastStation             = currentStation
                LastPart                = currentPart
                LastPartNum             = currentPartNum

                TriggerEvent('esx_GangBuilderDataToReplace0org:hasEnteredMarker', currentStation, currentPart, currentPartNum)
            end

            if not hasExited and not isInMarker and HasAlreadyEnteredMarker then

                HasAlreadyEnteredMarker = false

                TriggerEvent('esx_GangBuilderDataToReplace0org:hasExitedMarker', LastStation, LastPart, LastPartNum)
            end

        else
            Citizen.Wait(2500)
        end

    end
end)

-- Enter / Exit entity zone events
-- Citizen.CreateThread(function()

--     local trackedEntities = {
--         'prop_roadcone02a',
--         'prop_barrier_work06a',
--         'p_ld_stinger_s',
--         'prop_boxpile_07d',
--         'hei_prop_cash_crate_half_full'
--     }

--     while true do

--         Citizen.Wait(20)

--         local playerPed = GetPlayerPed(-1)
--         local coords    = GetEntityCoords(playerPed)

--         local closestDistance = -1
--         local closestEntity   = nil

--         for i=1, #trackedEntities, 1 do

--             local object = GetClosestObjectOfType(coords.x,  coords.y,  coords.z,  3.0,  GetHashKey(trackedEntities[i]), false, false, false)

--             if DoesEntityExist(object) then

--                 local objCoords = GetEntityCoords(object)
--                 local distance  = GetDistanceBetweenCoords(coords.x,  coords.y,  coords.z,  objCoords.x,  objCoords.y,  objCoords.z,  true)

--                 if closestDistance == -1 or closestDistance > distance then
--                     closestDistance = distance
--                     closestEntity   = object
--                 end

--             end

--         end

--         if closestDistance ~= -1 and closestDistance <= 3.0 then

--             if LastEntity ~= closestEntity then
--                 TriggerEvent('esx_GangBuilderDataToReplace0org:hasEnteredEntityZone', closestEntity)
--                 LastEntity = closestEntity
--             end

--         else

--             if LastEntity ~= nil then
--                 TriggerEvent('esx_GangBuilderDataToReplace0org:hasExitedEntityZone', LastEntity)
--                 LastEntity = nil
--             end

--         end

--     end
-- end)

-- Key Controls
Citizen.CreateThread(function()
    while true do
        
        if PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' then
    
            Citizen.Wait(0)

                if CurrentAction ~= nil then

                    SetTextComponentFormat('STRING')
                    AddTextComponentString(CurrentActionMsg)
                    DisplayHelpTextFromStringLabel(0, 0, 1, -1)

                    if IsControlPressed(0,  Keys['E']) and PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' and (GetGameTimer() - GUI.Time) > 150 then

                        if CurrentAction == 'menu_cloakroom' then
                            OpenCloakroomMenu()
                        end

                        if CurrentAction == 'menu_armory' then
                            OpenArmoryMenu(CurrentActionData.station)
                        end

                        if CurrentAction == 'menu_vehicle_spawner' then
                            OpenVehicleSpawnerMenu(CurrentActionData.station, CurrentActionData.partNum)
                        end

                        if CurrentAction == 'delete_vehicle' then

                            if Config.EnableOrganisationOwnedVehicles then

                                local vehicleProps = ESX.Game.GetVehicleProperties(CurrentActionData.vehicle)
                                TriggerServerEvent('esx_organisation:putVehicleInGarage', 'GangBuilderDataToReplace0', vehicleProps)

                            else

                                if
                                    GetEntityModel(vehicle) == GetHashKey('schafter3')  or
                                    GetEntityModel(vehicle) == GetHashKey('kuruma2') or
                                    GetEntityModel(vehicle) == GetHashKey('sandking') or
                                    GetEntityModel(vehicle) == GetHashKey('mule3') or
                                    GetEntityModel(vehicle) == GetHashKey('guardian') or
                                    GetEntityModel(vehicle) == GetHashKey('burrito3') or
                                    GetEntityModel(vehicle) == GetHashKey('mesa')
                                then
                                    TriggerServerEvent('esx_service:disableService', 'GangBuilderDataToReplace0')
                                end

                            end

                            ESX.Game.DeleteVehicle(CurrentActionData.vehicle)
                        end

                        if CurrentAction == 'menu_boss_actions' then

                            ESX.UI.Menu.CloseAll()

                            TriggerEvent('esx_organisation:openBossMenu', 'GangBuilderDataToReplace0', function(data, menu)

                                menu.close()

                                CurrentAction     = 'menu_boss_actions'
                                CurrentActionMsg  = _U('open_bossmenu')
                                CurrentActionData = {}

                            end)

                        end

                        if CurrentAction == 'remove_entity' then
                            DeleteEntity(CurrentActionData.entity)
                        end

                        CurrentAction = nil
                        GUI.Time      = GetGameTimer()

                    end

                end

                if IsControlPressed(0,  Keys['F7']) and PlayerData.org ~= nil and PlayerData.org.name == 'GangBuilderDataToReplace0' and not ESX.UI.Menu.IsOpen('default', GetCurrentResourceName(), 'GangBuilderDataToReplace0_actions') and (GetGameTimer() - GUI.Time) > 150 then
                    OpenGangBuilderDataToReplace0ActionsMenu()
                        GUI.Time = GetGameTimer()
                end
        else
        Citizen.Wait(2500) 
        end
    end
end)

---------------------------------------------------------------------------------------------------------
--NB : gestion des menu
---------------------------------------------------------------------------------------------------------

--RegisterNetEvent('NB:openMenuGangBuilderDataToReplace0')
--AddEventHandler('NB:openMenuGangBuilderDataToReplace0', function()
    --OpenGangBuilderDataToReplace0ActionsMenu()
--end)
        """
        return ClientContent

    def ServerTemplate(self):
        ServerContent = \
        """
ESX = nil

TriggerEvent('esx:getSharedObject', function(obj) ESX = obj end)

if Config.MaxInService ~= -1 then
    TriggerEvent('esx_society:activateService', 'GangBuilderDataToReplace0', Config.MaxInService)
end

--TriggerEvent('esx_phone:registerNumber', 'GangBuilderDataToReplace0', _U('alert_GangBuilderDataToReplace0'), true, false)
TriggerEvent('esx_organisation:registerOrganisation', 'GangBuilderDataToReplace0', 'GangBuilderDataToReplace0', 'organisation_GangBuilderDataToReplace0', 'organisation_GangBuilderDataToReplace0', 'organisation_GangBuilderDataToReplace0', {type = 'private'})

-- RegisterServerEvent('esx_GangBuilderDataToReplace0org:giveWeapon')
-- AddEventHandler('esx_GangBuilderDataToReplace0org:giveWeapon', function(weapon, ammo)
--     local xPlayer = ESX.GetPlayerFromId(source)
--     xPlayer.addWeapon(weapon, ammo)
-- end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:confiscatePlayerItem')
AddEventHandler('esx_GangBuilderDataToReplace0org:confiscatePlayerItem', function(target, itemType, itemName, amount)

    local sourceXPlayer = ESX.GetPlayerFromId(source)
    local targetXPlayer = ESX.GetPlayerFromId(target)

    if itemType == 'item_standard' then
        if targetXPlayer.getInventoryItem(itemName).count < amount then return end
        
        local label = sourceXPlayer.getInventoryItem(itemName).label

        targetXPlayer.removeInventoryItem(itemName, amount)
        sourceXPlayer.addInventoryItem(itemName, amount)

        TriggerClientEvent('esx:showNotification', sourceXPlayer.source, _U('you_have_confinv') .. amount .. ' ' .. label .. _U('from') .. targetXPlayer.name)
        TriggerClientEvent('esx:showNotification', targetXPlayer.source, _U('confinv') .. amount .. ' ' .. label )

    end

    if itemType == 'item_account' then
        if targetXPlayer.getAccount(itemName).money < amount then return end
        
        targetXPlayer.removeAccountMoney(itemName, amount)
        sourceXPlayer.addAccountMoney(itemName, amount)

        TriggerClientEvent('esx:showNotification', sourceXPlayer.source, _U('you_have_confdm') .. amount .. _U('from') .. targetXPlayer.name)
        TriggerClientEvent('esx:showNotification', targetXPlayer.source, _U('confdm') .. amount)

    end

    -- if itemType == 'item_weapon' then
    --     if not targetXPlayer.hasWeapon(itemName) then return end
        
    --     targetXPlayer.removeWeapon(itemName)
    --     sourceXPlayer.addWeapon(itemName, amount)

    --     TriggerClientEvent('esx:showNotification', sourceXPlayer.source, _U('you_have_confweapon') .. ESX.GetWeaponLabel(itemName) .. _U('from') .. targetXPlayer.name)
    --     TriggerClientEvent('esx:showNotification', targetXPlayer.source, _U('confweapon') .. ESX.GetWeaponLabel(itemName))

    -- end
    
    if itemType == 'item_money' then

        if not Config.CanConfiscateMoney then return end
        if targetXPlayer.getMoney() < amount then return end
        
        targetXPlayer.removeMoney(amount)
        sourceXPlayer.addMoney(amount)

        TriggerClientEvent('esx:showNotification', sourceXPlayer.source, _U('you_have_confmoney') .. tostring(amount) .. _U('from') .. targetXPlayer.name)
        TriggerClientEvent('esx:showNotification', targetXPlayer.source, _U('confmoney') .. tostring(amount))

    end

end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:handcuff')
AddEventHandler('esx_GangBuilderDataToReplace0org:handcuff', function(target)
    TriggerClientEvent('esx_GangBuilderDataToReplace0org:handcuff', target)
end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:drag')
AddEventHandler('esx_GangBuilderDataToReplace0org:drag', function(target)
    local _source = source
    TriggerClientEvent('esx_GangBuilderDataToReplace0org:drag', target, _source)
end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:putInVehicle')
AddEventHandler('esx_GangBuilderDataToReplace0org:putInVehicle', function(target)
    TriggerClientEvent('esx_GangBuilderDataToReplace0org:putInVehicle', target)
end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:OutVehicle')
AddEventHandler('esx_GangBuilderDataToReplace0org:OutVehicle', function(target)
    TriggerClientEvent('esx_GangBuilderDataToReplace0org:OutVehicle', target)
end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:getStockItem')
AddEventHandler('esx_GangBuilderDataToReplace0org:getStockItem', function(itemName, count)

    local xPlayer = ESX.GetPlayerFromId(source)

    TriggerEvent('esx_addoninventory:getSharedInventory', 'organisation_GangBuilderDataToReplace0', function(inventory)

        local item = inventory.getItem(itemName)

        if item.count >= count then
            inventory.removeItem(itemName, count)
            xPlayer.addInventoryItem(itemName, count)
        else
            TriggerClientEvent('esx:showNotification', xPlayer.source, _U('quantity_invalid'))
        end

        TriggerClientEvent('esx:showNotification', xPlayer.source, _U('have_withdrawn') .. count .. ' ' .. item.label)

    end)

end)

RegisterServerEvent('esx_GangBuilderDataToReplace0org:putStockItems')
AddEventHandler('esx_GangBuilderDataToReplace0org:putStockItems', function(itemName, count)

    local xPlayer = ESX.GetPlayerFromId(source)
    local xPlayerInventoryItem = xPlayer.getInventoryItem(itemName)

    TriggerEvent('esx_addoninventory:getSharedInventory', 'organisation_GangBuilderDataToReplace0', function(inventory)

        local item = inventory.getItem(itemName)

        if item.count >= 0 and xPlayerInventoryItem.count >= count then
            xPlayer.removeInventoryItem(itemName, count)
            inventory.addItem(itemName, count)
        else
            TriggerClientEvent('esx:showNotification', xPlayer.source, _U('quantity_invalid'))
        end

        TriggerClientEvent('esx:showNotification', xPlayer.source, _U('added') .. count .. ' ' .. item.label)

    end)

end)


ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:getOtherPlayerData', function(source, cb, target)

    if Config.EnableESXIdentity then

        local xPlayer = ESX.GetPlayerFromId(target)

        local identifier = GetPlayerIdentifiers(target)[1]

        local result = MySQL.Sync.fetchAll("SELECT * FROM users WHERE identifier = @identifier", {
        ['@identifier'] = identifier
        })

        local user      = result[1]
        local firstname     = user['firstname']
        local lastname      = user['lastname']
        local sex           = user['sex']
        local dob           = user['dateofbirth']
        local height        = user['height'] .. " Inches"
        
        local data = {
            name        = GetPlayerName(target),
            job         = xPlayer.job,
            money       = xPlayer.getMoney(),
            inventory   = xPlayer.inventory,
            accounts    = xPlayer.accounts,
            -- weapons     = xPlayer.loadout,
            firstname   = firstname,
            lastname    = lastname,
            sex         = sex,
            dob         = dob,
            height      = height
        }

        TriggerEvent('esx_status:getStatus', source, 'drunk', function(status)

        if status ~= nil then
            data.drunk = math.floor(status.percent)
        end

        end)

        if Config.EnableLicenses then

            TriggerEvent('esx_license:getLicenses', source, function(licenses)
                data.licenses = licenses
                cb(data)
            end)

        else
            cb(data)
        end

    else

        local xPlayer = ESX.GetPlayerFromId(target)

        local data = {
            name       = GetPlayerName(target),
            job        = xPlayer.job,
            inventory  = xPlayer.inventory,
            accounts   = xPlayer.accounts,
            -- weapons    = xPlayer.loadout
        }

        TriggerEvent('esx_status:getStatus', _source, 'drunk', function(status)

        if status ~= nil then
            data.drunk = status.getPercent()
        end

        end)

        TriggerEvent('esx_license:getLicenses', _source, function(licenses)
            data.licenses = licenses
        end)

        cb(data)

    end

end)


--ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:getFineList', function(source, cb, category)

--MySQL.Async.fetchAll(
    --'SELECT * FROM fine_types_GangBuilderDataToReplace0 WHERE category = @category',
    --{
    --['@category'] = category
    --},
    --function(fines)
    --cb(fines)
    --end
--)

--66end)

ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:getVehicleInfos', function(source, cb, plate)

    if Config.EnableESXIdentity then

        MySQL.Async.fetchAll(
        'SELECT * FROM owned_vehicles',
        {},
        function(result)

            local foundIdentifier = nil

            for i=1, #result, 1 do

                local vehicleData = json.decode(result[i].vehicle)

                if vehicleData.plate == plate then
                    foundIdentifier = result[i].owner
                    break
                end

            end

            if foundIdentifier ~= nil then

                MySQL.Async.fetchAll(
                    'SELECT * FROM users WHERE identifier = @identifier',
                    {
                    ['@identifier'] = foundIdentifier
                    },
                    function(result)

                    local ownerName = result[1].firstname .. " " .. result[1].lastname

                    local infos = {
                        plate = plate,
                        owner = ownerName
                    }

                    cb(infos)

                    end
                )

            else

                local infos = {
                plate = plate
                }

                cb(infos)

            end

        end
        )

    else

        MySQL.Async.fetchAll(
        'SELECT * FROM owned_vehicles',
        {},
        function(result)

            local foundIdentifier = nil

            for i=1, #result, 1 do

                local vehicleData = json.decode(result[i].vehicle)

                if vehicleData.plate == plate then
                    foundIdentifier = result[i].owner
                    break
                end

            end

            if foundIdentifier ~= nil then

                MySQL.Async.fetchAll(
                    'SELECT * FROM users WHERE identifier = @identifier',
                    {
                    ['@identifier'] = foundIdentifier
                    },
                    function(result)

                    local infos = {
                        plate = plate,
                        owner = result[1].name
                    }

                    cb(infos)

                    end
                )

            else

                local infos = {
                plate = plate
                }

                cb(infos)

            end

        end
        )

    end

end)

-- ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:getArmoryWeapons', function(source, cb)

--     TriggerEvent('esx_datastore:getSharedDataStore', 'organisation_GangBuilderDataToReplace0', function(store)

--         local weapons = store.get('weapons')

--         if weapons == nil then
--             weapons = {}
--         end

--         cb(weapons)

--     end)

-- end)

-- ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:addArmoryWeapon', function(source, cb, weaponName)

--     local xPlayer = ESX.GetPlayerFromId(source)

--     xPlayer.removeWeapon(weaponName)

--     TriggerEvent('esx_datastore:getSharedDataStore', 'organisation_GangBuilderDataToReplace0', function(store)

--         local weapons = store.get('weapons')

--         if weapons == nil then
--             weapons = {}
--         end

--         local foundWeapon = false

--         for i=1, #weapons, 1 do
--             if weapons[i].name == weaponName then
--                 weapons[i].count = weapons[i].count + 1
--                 foundWeapon = true
--             end
--         end

--         if not foundWeapon then
--             table.insert(weapons, {
--                 name  = weaponName,
--                 count = 1
--             })
--         end

--         store.set('weapons', weapons)

--         cb()

--     end)

-- end)

-- ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:removeArmoryWeapon', function(source, cb, weaponName)

-- local xPlayer = ESX.GetPlayerFromId(source)

-- TriggerEvent('esx_datastore:getSharedDataStore', 'organisation_GangBuilderDataToReplace0', function(store)

--     local weapons = store.get('weapons')

--     if weapons == nil then
--         weapons = {}
--     end
    
--     local found = false

--     local foundWeapon = false

--     for i=1, #weapons, 1 do
--         if weapons[i].name == weaponName then
--             if weapons[i].count > 0 then
--                 found = true
--                 weapons[i].count = weapons[i].count - 1
--             end
--         end
--     end
        
--         -- weapons[i].count = (weapons[i].count > 0 and weapons[i].count - 1 or 0)
--         -- foundWeapon = true
--     -- end
--     -- end

--     -- if not foundWeapon then
--     -- table.insert(weapons, {
--         -- name  = weaponName,
--         -- count = 0
--     -- })
--     -- print("no dont give")
--     -- else
--     if found then
--         -- print("ok give")
--         xPlayer.addWeapon(weaponName, 1000)
--     end
    
--     store.set('weapons', weapons)

--     cb()

-- end)

-- end)


ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:buy', function(source, cb, amount)

    TriggerEvent('esx_addonaccount:getSharedAccount', 'organisation_GangBuilderDataToReplace0', function(account)

        if account.money >= amount then
            account.removeMoney(amount)
            cb(true)
        else
            cb(false)
        end

    end)

end)

ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:getStockItems', function(source, cb)

    TriggerEvent('esx_addoninventory:getSharedInventory', 'organisation_GangBuilderDataToReplace0', function(inventory)
        cb(inventory.items)
    end)

end)

ESX.RegisterServerCallback('esx_GangBuilderDataToReplace0org:getPlayerInventory', function(source, cb)

    local xPlayer = ESX.GetPlayerFromId(source)
    local items   = xPlayer.inventory

    cb({
        items = items
    })

end)
        """
        return ServerContent
    
    def LocaleTemplate(self):
        LocaleContent = \
        """
Locales['fr'] = {
    -- Cloakroom
    ['cloakroom'] = 'Vestiaire',
    ['citizen_wear'] = 'Tenue Civile',
    ['GangBuilderDataToReplace0_wear'] = 'Tenue GangBuilderDataToReplace0',
    ['open_cloackroom'] = '~INPUT_CONTEXT~ Pour accéder au ~b~Dressing',
    -- Armory
    ['get_weapon'] = 'Prendre Arme',
    ['put_weapon'] = 'Déposer Arme',
    ['buy_weapons'] = 'Acheter Armes',
    ['armory'] = 'Armurerie',
    ['open_armory'] = "~INPUT_CONTEXT~ Pour accéder à ~b~l'Armurerie",
    -- Vehicles
    ['vehicle_menu'] = 'Véhicule',
    ['vehicle_out'] = 'Il y a déjà un véhicule de sortie',
    ['vehicle_spawner'] = '~INPUT_CONTEXT~ pour sortir un ~g~Véhicule',
    ['store_vehicle'] = '~INPUT_CONTEXT~ pour ranger le ~g~Véhicule',
    ['service_max'] = 'Service complet : ',
    -- Action Menu
    ['citizen_interaction'] = 'Interaction avec le braqué/kidnappé',
    ['vehicle_interaction'] = 'Interaction véhicule',
    ['object_spawner'] = 'Placer objets',

    ['id_card'] = "Carte d'identité",
    ['search'] = 'Fouiller',
    ['handcuff'] = 'Ligotter / Libérer',
    ['drag'] = 'Escorter',
    ['put_in_vehicle'] = 'Jeter dans le véhicule',
    ['out_the_vehicle'] = 'Sortir du véhicule',
    ['fine'] = 'Racket',
    ['no_players_nearby'] = 'Aucun joueur à proximité',

    ['vehicle_info'] = 'Infos véhicule',
    ['pick_lock'] = 'Voler véhicule',
    ['vehicle_unlocked'] = 'Véhicule ~g~déverouillé~s~',
    ['no_vehicles_nearby'] = 'Aucun véhicule à proximité',
    ['traffic_interaction'] = 'Interaction Voirie',
    ['cone'] = 'Plot',
    ['barrier'] = 'Barrière',
    ['spikestrips'] = 'Herse',
    ['box'] = 'Caisse',
    ['cash'] = 'Caisse',
    -- ID Card Menu
    ['name'] = 'Nom : ',
    ['bac'] = 'Alcoolémie : ',
    -- Body Search Menu
    ['confiscate_dirty'] = 'Voler argent sale : $',
    ['guns_label'] = '--- Armes ---',
    ['confiscate'] = 'Voler ',
    ['inventory_label'] = '--- Inventaire ---',
    ['confiscate_inv'] = 'Confisquer x',
    -- Vehicle Info Menu
    ['plate'] = 'N°: ',
    ['owner_unknown'] = 'Propriétaire : Inconnu',
    ['owner'] = 'Propriétaire : ',
    -- Weapons Menus
    ['get_weapon_menu'] = 'Armurerie - Prendre Arme',
    ['put_weapon_menu'] = 'Armurerie - Déposer Arme',
    ['buy_weapon_menu'] = 'Armurerie - Acheter Armes',
    ['not_enough_money'] = "~r~Vous n'avez pas assez d'Argent",
    -- Boss Menu
    ['take_company_money'] = 'Retirer argent société',
    ['deposit_money'] = 'Déposer argent',
    ['amount_of_withdrawal'] = 'Montant du retrait',
    ['invalid_amount'] = 'Montant invalide',
    ['amount_of_deposit'] = 'Montant du dépôt',
    ['open_bossmenu'] = '~INPUT_CONTEXT~ pour accéder au ~b~Menu',
    ['quantity_invalid'] = 'Quantité invalide',
    ['have_withdrawn'] = 'Vous avez retiré x',
    ['added'] = 'Vous avez ajouté x',
    ['quantity'] = 'Quantité',
    ['inventory'] = 'Inventaire',
    ['GangBuilderDataToReplace0_stock'] = 'GangBuilderDataToReplace0 Stock',
    -- Misc
    ['remove_object'] = "~INPUT_CONTEXT~ pour enlever ~g~l'Objet",
    ['map_blip'] = 'GangBuilderDataToReplace0',
    -- Notifications
    ['from'] = '~s~ à ~b~',
    ['you_have_confinv'] = 'Vous avez volé ~y~x',
    ['confinv'] = 'On vous a volé ~y~x',
    ['you_have_confdm'] = 'Vous avez volé ~y~$',
    ['confdm'] = 'On vous a volé ~y~$',
    ['you_have_confweapon'] = 'Vous avez volé ~y~x1 ',
    ['confweapon'] = 'On vous a volé ~y~x1 ',
    ['alert_GangBuilderDataToReplace0'] = 'Alerte GangBuilderDataToReplace0',
    -- Authorized Vehicles
    ['schafter3'] = 'Véhicule Civil',
    ['sandking'] = '4X4',
    ['mule3'] = 'Camion de transport',
    ['guardian'] = 'Grand 4x4',
    ['burrito3'] = 'Fourgonette',
    ['mesa'] = 'Tout-terrain',
    
    ['confmoney'] = 'On vous a volé ~y~$',
    ['you_have_confmoney'] = 'Vous avez volé ~y~$',
    ['confiscate_money'] = 'Voler argent : $',
    
    ['bill_label'] = 'Organisation illégale',
    ['send_bill'] = 'Créer une facture personnalisée',
    ['bill_amount'] = 'Montant de la facture',
    ['bill_sended'] = 'Une facture à été envoyée!',
    ['no_player_nearby'] = "Il n'y a personne à proximité!",
}
        """

        return LocaleContent
    
    def ManifestTemplate(self):
        ManifestContent = \
        """
fx_version 'cerulean'

game 'gta5'

server_scripts {
    '@es_extended/locale.lua',
    'locales/fr.lua',
    '@mysql-async/lib/MySQL.lua',
    'config.lua',
    'server/server.lua'
}

client_scripts {
    '@es_extended/locale.lua',
    'locales/fr.lua',
    'config.lua',
    'client/client.lua'
}

        """
        return ManifestContent

    def SQLTemplate(self):
        SQLContent = \
        """
INSERT INTO `addon_account` (name, label, shared) VALUES 
    ('organisation_GangBuilderDataToReplace0','GangBuilderDataToReplace0',1)
;

INSERT INTO `datastore` (name, label, shared) VALUES 
    ('organisation_GangBuilderDataToReplace0','GangBuilderDataToReplace0',1)
;

INSERT INTO `addon_inventory` (name, label, shared) VALUES 
    ('organisation_GangBuilderDataToReplace0', 'GangBuilderDataToReplace0', 1)
;

INSERT INTO `org` (`name`, `label`) VALUES
    ('GangBuilderDataToReplace0', 'GangBuilderDataToReplace0');

INSERT INTO `org_gradeorg` (`org_name`, `gradeorg`, `name`, `label`, `salary`, `skin_male`, `skin_female`) VALUES
('GangBuilderDataToReplace0', 0, 'GangBuilderDataToReplace7', 'GangBuilderDataToReplace1', 400, '{}', '{}'),
('GangBuilderDataToReplace0', 1, 'GangBuilderDataToReplace8', 'GangBuilderDataToReplace2', 600, '{}', '{}'),
('GangBuilderDataToReplace0', 2, 'GangBuilderDataToReplace9', 'GangBuilderDataToReplace3', 800, '{}', '{}'),
('GangBuilderDataToReplace0', 3, 'GangBuilderDataToReplace10', 'GangBuilderDataToReplace4', 900, '{}', '{}'),
('GangBuilderDataToReplace0', 4, 'GangBuilderDataToReplace11', 'GangBuilderDataToReplace5', 1000, '{}', '{}'),
('GangBuilderDataToReplace0', 5, 'GangBuilderDataToReplace12', 'GangBuilderDataToReplace6', 1200, '{}', '{}');
        """
        return SQLContent
    
    def ConfigTemplate(self):
        ConfigContent = \
        """
Config                            = {}
Config.DrawDistance               = 50.0
Config.MarkerType                 = 0
Config.MarkerSize                 = { x = 1.5, y = 1.5, z = 0.5 }
Config.MarkerColor                = { r = 0, g = 165, b = 255 }
Config.EnablePlayerManagement     = true
Config.EnableArmoryManagement     = true
Config.EnableESXIdentity          = true -- only turn this on if you are using esx_identity
Config.EnableNonFreemodePeds      = true -- turn this on if you want custom peds
Config.EnableSocietyOwnedVehicles = false
Config.EnableLicenses             = false
Config.MaxInService               = -1
Config.Locale = 'fr'
Config.CanConfiscateMoney         = true

Config.GangBuilderDataToReplace0Stations = {

    GangBuilderDataToReplace0 = {

        Blip = {
            Pos     = { x = 1275.680, y = -1722.533, z = 54.655 },
            Sprite  = 60,
            Display = 4,
            Scale   = 1.2,
            Colour  = 29,
        },



        AuthorizedVehicles = {GangBuilderDataToReplace1},

        Cloakrooms = {{GangBuilderDataToReplace2}},

        Armories = {{GangBuilderDataToReplace3}},

        Vehicles = {
        {
            Spawner    = {GangBuilderDataToReplace4},
            SpawnPoint = {GangBuilderDataToReplace5},
            Heading    = GangBuilderDataToReplace6,
        }
        },

        VehicleDeleters = {{GangBuilderDataToReplace7}},

        BossActions = {{GangBuilderDataToReplace8}},

    },

}
        """
        return ConfigContent



class Builder:
    def __init__(self, file : str, data: dict, temp: FileTemplate):
        self.author = "Jun#6666"
        self.new_data = data
        self.template = temp
        self.base_dir = "esx_%s" % file
        self.path = {
            "config": "%s/config.lua" % self.base_dir,
            "client": "%s/client/client.lua" % self.base_dir,
            "server": "%s/server/server.lua" % self.base_dir,
            "locales": "%s/locales/fr.lua" % self.base_dir,
            "manifest": "%s/fxmanifest.lua" % self.base_dir,
            "sql": "%s/%s.sql" % (self.base_dir, self.base_dir)
        }
        self.file_name = [
            "config",
            "client",
            "server",
            "locales",
            "manifest",
            "sql"
        ]

        self.parameter = {
            "config": [
                "Cloakroom",
                "Armories",
                "Vehicle_menu",
                "Vehicle_spawn",
                "Heading",
                "Vehicle_return_place",
                "Boss"
            ]
        }

        self.number_to_replace = {
            "config": 9,
            "client": 5,
            "server": 1,
            "locales": 1,
            "manifest": 1,
            "sql": 13
        }

        self.content = {
            "config": [],
            "client": [],
            "server": [],
            "locales": [],
            "manifest": [],
            "sql": []
        }

        self.final = {
            "config": None,
            "client": None,
            "server": None,
            "locales": None,
            "manifest": None,
            "sql": None
        }
    
    def CreateFile(self):
        self.CreateDir()

        for file in self.file_name:
            print(file)
            # with open(self.path.get(file), "w") as GBFile:
            #     GBFile.write(self.final.get(file))
            #     GBFile.close()
            GBFile = codecs.open(self.path.get(file), "w", "utf-8")
            GBFile.write(self.final.get(file))
            GBFile.close()
        return

    def FinalContent(self):
        for file in self.file_name:
            self.final[file] = self.template.template.get(file)
            for i in range(0, self.number_to_replace.get(file)):
                self.final[file] = self.final.get(file).replace(
                    "GangBuilderDataToReplace%s" % i if i < 10 else "GangBuilderDataToReplace_%s" % i,
                    self.content.get(file)[i]
                )
    
    def DefineSQLContent(self):
        self.content.get("sql").append(self.new_data.get("name"))
        self.content.get("sql").append(self.new_data.get("Grades")[0].get("label"))
        self.content.get("sql").append(self.new_data.get("Grades")[1].get("label"))
        self.content.get("sql").append(self.new_data.get("Grades")[2].get("label"))
        self.content.get("sql").append(self.new_data.get("Grades")[3].get("label"))
        self.content.get("sql").append(self.new_data.get("Grades")[4].get("label"))
        self.content.get("sql").append(self.new_data.get("Grades")[5].get("label"))
        self.content.get("sql").append(self.new_data.get("Grades")[0].get("name"))
        self.content.get("sql").append(self.new_data.get("Grades")[1].get("name"))
        self.content.get("sql").append(self.new_data.get("Grades")[2].get("name"))
        self.content.get("sql").append(self.new_data.get("Grades")[3].get("name"))
        self.content.get("sql").append(self.new_data.get("Grades")[4].get("name"))
        self.content.get("sql").append(self.new_data.get("Grades")[5].get("name"))
        return

    def DefineServerLocaleAndManifestContent(self):
        self.content.get("server").append(self.new_data.get("name"))
        self.content.get("locales").append(self.new_data.get("name"))
        self.content.get("manifest").append(self.new_data.get("name"))
        return

    def DefineClientContent(self):
        blips_coord = "x = %s, y = %s, z = %s" % (
                self.new_data.get("Blips").get("blips_infos").get("x"),
                self.new_data.get("Blips").get("blips_infos").get("y"),
                self.new_data.get("Blips").get("blips_infos").get("z")
        )

        blips_id = self.new_data.get("Blips").get("blips_infos").get("id")
        blips_color = self.new_data.get("Blips").get("blips_infos").get("color")
        blips_radius = self.new_data.get("Blips").get("blips_infos").get("radius")
        self.content.get("client").append(self.new_data.get("name"))
        self.content.get("client").append(blips_coord)
        self.content.get("client").append(blips_id)
        self.content.get("client").append(blips_color)
        self.content.get("client").append(blips_radius)

    def DefineConfigContent(self):
        new_vehicles = ""
        for i in range(0, len(self.new_data.get("Vehicle"))):
            if i != len(self.new_data.get("Vehicle")) - 1:
                new_vehicles += "{name = '%s', label = '%s'}," % (
                    self.new_data.get("Vehicle")[i].get("name"),
                    self.new_data.get("Vehicle")[i].get("label")

                )
            else:
                new_vehicles += "{name = '%s', label = '%s'}" % (
                    self.new_data.get("Vehicle")[i].get("name"),
                    self.new_data.get("Vehicle")[i].get("label")
                )
        self.content.get("config").append(self.new_data.get("name"))
        self.content.get("config").append(new_vehicles)

        for i in range(0, len(self.parameter.get("config"))):
            Value = self.parameter.get("config")[i]
            if Value != "Heading":
                data = "x = %s, y = %s, z = %s" % (
                    self.new_data.get(self.parameter.get("config")[i]).get("x"),
                    self.new_data.get(self.parameter.get("config")[i]).get("y"),
                    self.new_data.get(self.parameter.get("config")[i]).get("z"),
                )
            else:
                print(self.parameter.get("config")[i - 1])
                data = "%s" % self.new_data.get(self.parameter.get("config")[i - 1]).get("angle")
            
            self.content.get("config").append(data)
        
    def CreateDir(self):
        os.makedirs(self.base_dir, exist_ok= True)
        os.makedirs("%s/client" % self.base_dir, exist_ok= True)
        os.makedirs("%s/server" % self.base_dir, exist_ok= True)
        os.makedirs("%s/locales" % self.base_dir, exist_ok= True)
        print("Dir created")
        return True
    
class JSONFile:
    def __init__(self):
        self.content = None
        self.default_file = "template.json"

    def ReadFile(self):
        if os.path.exists(self.default_file):
            with open(self.default_file) as json_file:
                data = json.load(json_file)
                self.content = data
        else:
            exit("Can't open file %s, plz create it or rename ur file." % self.default_file)

class SQL:
    def __init__(self, content: dict, file: str):
        self.base = {
            "user": "root",
            "password": "",
            "host": "127.0.0.1",
            "database": "database"
        }

        self.allowed = {"select_all", "select_one", "update"}

        self.connection = None

        self.cursor = None

        self.file = file

        self.data = content

        self.tables = {
            "1": ["addon_account", "datastore", "addon_inventory"],
            "2": ["org"],
            "3": ["org_gradeorg"],
            '4': ["addon_inventory_items"],
            '5': ["datastore_data"]
        }

        self.all_request = set()

        self.request = {
            "All": "UPDATE %s SET name = '%s', label = '%s' WHERE name = '%s'",
            "org": "UPDATE %s SET name = '%s', label = '%s' WHERE name = '%s'",
            "datastore" : "UPDATE %s SET name = '%s' WHERE name = '%s'",
            "inventory": "UPDATE %s SET inventory_name = '%s' WHERE inventory_name = '%s'",
            "grade_org": {
                "number" : 6,
                "request": "UPDATE %s SET org_name = '%s', name = '%s', label = '%s' WHERE org_name = '%s' AND gradeorg = %s"
            }
        }

    def InitializeConnection(self):
        if self.connection is None:
            self.connection = mysql.connector.connect(**self.base)
            return
        else:
            self.DestroyConnection()
            self.InitializeConnection()
            return
    
    def DestroyConnection(self):
        if self.connection.is_connected():
            self.connection.close()
            self.connection = None
            return True
        else:
            print("Not connected to database")
            return False
    
    def CreateFile(self):
        with open("request.sql", "w") as request:
            content = ""
            for req in self.all_request:
                content += "%s\n" % req
            
            request.write(content)
            request.close()
    
    def ExecuteCommand(self, type: str, cmd: str):
        self.InitializeConnection()
        self.cursor = self.connection.cursor()
        data = None
        try:
            if type.lower() in self.allowed:
                self.cursor.execute(cmd)

                if type.lower() == "select_all":
                    data = self.cursor.fetch()
                if type.lower() == "select_one":
                    data = self.cursor.fetchone()
                if type.lower() == "update":
                    self.connection.commit()
                    data = "Update success"
                if type.lower() == "insert":
                    self.connection.commit()
                    data = "Insert success"
            else:
                print("Command not allowed")
        except Error as e:
            print("Failed to execute command : [%s] " % e)
        finally:
            self.cursor.close()
            self.cursor = None
            self.DestroyConnection()
            return data

    def UpdateAll(self):
        for req in self.all_request:
            data = self.ExecuteCommand("update", req)
        return

    
    def DefineAllRequest(self):
        for i in range(0, len(self.tables.get("1"))):
            self.all_request.add("%s;" % self.request.get("All") % (
                self.tables.get("1")[i],
                "organisation_%s" % self.data.get("name"),
                self.data.get("name"),
                "organisation_%s" % self.file

            ))
        for i in range(0, len(self.tables.get("2"))):
            self.all_request.add("%s;" % self.request.get("org") % (
                self.tables.get("2")[i],
                "%s" % self.data.get("name"),
                self.data.get("name").capitalize(),
                "%s" % self.file
            ))

        for i in range(0, len(self.tables.get("4"))):
            self.all_request.add("%s;" % self.request.get("inventory") % (
                self.tables.get("4")[i],
                "organisation_%s" % self.data.get("name").lower(),
                "organisation_%s" % self.file
            ))

        for i in range(0, len(self.tables.get("5"))):
            self.all_request.add("%s;" % self.request.get("datastore") % (
                self.tables.get("5")[i],
                "organisation_%s" % self.data.get("name").lower(),
                "organisation_%s" % self.file
            ))

        for i in range(0, self.request.get("grade_org").get("number")):
            self.all_request.add("%s;" % self.request.get("grade_org").get("request") % (
            "org_gradeorg",
            self.data.get("name"),
            self.data.get("Grades")[i].get("name"),
            self.data.get("Grades")[i].get("label"),
            self.file,
            i
            ))

class UpdateFile:
    def __init__(self, file: str, data: dict):
        # Author (me lol)
        self.author = "Jun#6666"
        # Json data converted to dict
        self.new_data = data
        # the name we want to change
        self.arg = file
        # The dir of the old data
        self.dir = "esx_%s" % file
        # How many files to change
        self.file_number = 4
        # All files paths (default none)
        self.files = {
            "client": None,
            "server": None,
            "locales": None,
            "config": None
        }

        # All blips infos needed
        self.blips_infos = {
            "keys": ["blips", "color", "radius"],
            "default_blips_line": 52,
            "default_color_line": 67,
            "default_radius_line": 65,
            "blips":{
                "old": None,
                "replace": None
            },
            "color": {
                "old": None,
                "replace": None
            },
            "radius": {
                "old": None,
                "replace": None
            }
        }

        self.config_file_infos = {
            "keys": [
                "vehicle",
                "cloakroom",
                "armories",
                "boss",
                "vehicle_menu",
                "vehicle_spawn",
                "vehicle_heading",
                "vehicle_delete"
            ],
            "lines": {
                "vehicle": 29,
                "cloakroom": 31,
                "armories": 33,
                "vehicle_menu": 37,
                "vehicle_spawn": 38,
                "vehicle_heading": 39,
                "vehicle_delete": 43,
                "boss": 45
            },
            "vehicle": {
                "old": None,
                "replace": None,

            },
            "cloakroom": {
                "old": None,
                "replace": None
            },
            "armories": {
                "old": None,
                "replace": None
            },
            "boss": {
                "old": None,
                "replace": None
            },
            "vehicle_menu": {
                "old": None,
                "replace": None
            },
            "vehicle_spawn": {
                "old": None,
                "replace": None
            },
            "vehicle_heading": {
                "old": None,
                "replace": None
            },
            "vehicle_delete": {
                "old": None,
                "replace": None
            }
        }

    # Define all paths if they exists
    def DefineFiles(self):
        if os.path.exists(self.dir):
            if os.path.exists("%s/client" % self.dir):
                self.files.update({"client": "%s/client/client.lua" % self.dir})
                if os.path.exists("%s/server" % self.dir):
                    self.files.update({"server": "%s/server/server.lua" % self.dir})
                    if os.path.exists("%s/locales/fr.lua" % self.dir):
                        self.files.update({"locales": "%s/locales/fr.lua" % self.dir})
                        if os.path.exists("%s/config.lua" % self.dir):
                            self.files.update({"config": "%s/config.lua" % self.dir})
                            return True
                        else:
                            print("Config file didn't exist")
                            return None
                    else:
                        print("Locales file not exist")
                        return None
                else:
                    print("Server file not exist")
                    return None
            else:
                print("Client file not exist")
                return None
        else:
            print("Dir %s not exist" % self.dir)

    # Update the client file with the new content
    def UpdateClientFile(self):
            content = None
            with open(self.files.get("client"), "r") as client:
                content = client.read()
                client.close()
            with open(self.files.get("client"), "w") as client:
                for i in range(0, len(self.blips_infos.get("keys"))):
                    if self.blips_infos.get(self.blips_infos.get("keys")[i]) is not None:
                        content = content.replace(
                            self.blips_infos.get(self.blips_infos.get("keys")[i]).get("old"),
                            self.blips_infos.get(self.blips_infos.get("keys")[i]).get("replace")
                        )

                
                content = content.replace(self.arg, self.new_data.get("name"))
                client.write(content)
                client.close()
                return True

    def UpdateDirName(self):
        os.rename(r"%s" % self.dir, r"esx_%s" % self.new_data.get("name"))
        return True
    # Update the server file with the new content
    def UpdateServerFile(self):
        content = None
        with open(self.files.get("server"), "r") as server:
            content = server.read()
            content = content.replace(
                self.arg,
                self.new_data.get("name")
            )
            server.close()
        with open(self.files.get("server"), "w") as server:
            if content is not None:
                server.write(content)
                server.close()
                return True
            else:
                print("Error occured while define content for server file")
                server.close()
                return None

    # Update the config file with the new content
    def UpdateConfigFile(self):
            content = None
            with open(self.files.get("config"), "r") as config:
                content = config.read()
                config.close()
            with open(self.files.get("config"), "w") as config:
                for i in range(0, len(self.config_file_infos.get("keys"))):
                    if self.config_file_infos.get(self.config_file_infos.get("keys")[i]) is not None:
                        content = content.replace(
                            self.config_file_infos.get(self.config_file_infos.get("keys")[i]).get("old"),
                            self.config_file_infos.get(self.config_file_infos.get("keys")[i]).get("replace")
                        )

                
                content = content.replace(self.arg, self.new_data.get("name"))
                config.write(content)
                config.close()
                return True

    # Update the locale file with the new content
    def UpdateLocaleFile(self):
        content = None
        with open(self.files.get("locales"), "r") as locale:
            content = locale.read()
            content = content.replace(
                self.arg,
                self.new_data.get("name")
            )
            locale.close()
        with open(self.files.get("locales"), "w") as locale:
            if content is not None:
                locale.write(content)
                locale.close()
                return True
            else:
                print("Error occurend while define content for locale file")
                locale.close()
                return None

    # Initialize the new values to replace
    def InitializeNewValues(self):
        # Open file
        with open(self.files.get("client"), "r") as client_file:
            # Read with readlines to get all lines in tab to retrieve the wanted lines
            data = client_file.readlines()

            # New blips lines to write
            new_blips = "local blips = { { title = '~y~%s', colour = %s, id = %s, x = %s, y = %s, z = %s}}" % (
                self.new_data.get("name"),
                self.new_data.get("Blips").get("blips_infos").get("color"),
                self.new_data.get("Blips").get("blips_infos").get("id"),
                self.new_data.get("Blips").get("blips_infos").get("x"),
                self.new_data.get("Blips").get("blips_infos").get("y"),
                self.new_data.get("Blips").get("blips_infos").get("z")
                )
            # New color line to write
            new_color = "                            SetBlipColour(zoneblip, %s)\n" % self.new_data.get("Blips").get("blips_infos").get("color")
            # New radius line to write
            new_radius = "                zoneblip = AddBlipForRadius(v.x,v.y,v.z, %s)\n" % self.new_data.get("Blips").get("blips_infos").get("radius")
            # Update the dict
            self.blips_infos.update(
                {
                    "blips": {
                        "old": data[self.blips_infos.get("default_blips_line")],
                        "replace": new_blips
                    }
                }
            )
            # Again
            self.blips_infos.update(
                {
                    "color": {
                        "old": data[self.blips_infos.get("default_color_line")],
                        "replace": new_color
                    }
                }
            )
            # And again
            self.blips_infos.update(
                {
                    "radius": {
                        "old": data[self.blips_infos.get("default_radius_line")],
                        "replace": new_radius
                    }
                }
            )
            # Close the file
            client_file.close()
        with open(self.files.get("config"), "r") as config_file:
            data = config_file.readlines()
            # Prepare the new lines
            new_vehicles = "        AuthorizedVehicles = {"
            for i in range(0, len(self.new_data.get("Vehicle"))):
                if i != len(self.new_data.get("Vehicle")) - 1:
                    new_vehicles += "{name = '%s', label = '%s'}," % (
                        self.new_data.get("Vehicle")[i].get("name"),
                        self.new_data.get("Vehicle")[i].get("label")

                    )
                else:
                    new_vehicles += "{name = '%s', label = '%s'}},\n" % (
                        self.new_data.get("Vehicle")[i].get("name"),
                        self.new_data.get("Vehicle")[i].get("label")
                    )
            Cloakroom_dict = self.new_data.get("Cloakroom")
            new_cloakroom = "        Cloakrooms = {{x=%s,y=%s,z=%s}},\n" % (
                Cloakroom_dict.get("x") if Cloakroom_dict.get("use") else "0",
                Cloakroom_dict.get("y") if Cloakroom_dict.get("use") else "0",
                Cloakroom_dict.get("z") if Cloakroom_dict.get("use") else "0"
            )

            Armories_dict = self.new_data.get("Armories")
            new_armories = "        Armories = {{x=%s,y=%s,z=%s}},\n" % (
                Armories_dict.get("x"),
                Armories_dict.get("y"),
                Armories_dict.get("z")
            )

            new_vehicle_menu = "            Spawner    = { x = %s,y=%s, z=%s},\n" % (
                self.new_data.get("Vehicle_menu").get("x"),
                self.new_data.get("Vehicle_menu").get("y"),
                self.new_data.get("Vehicle_menu").get("z")
            )
            
            new_spawn_point = "            SpawnPoint    = { x = %s,y=%s, z=%s},\n" % (
                self.new_data.get("Vehicle_spawn").get("x"),
                self.new_data.get("Vehicle_spawn").get("y"),
                self.new_data.get("Vehicle_spawn").get("z")
            )

            new_heading = "            Heading    = %s,\n" % self.new_data.get("Vehicle_spawn").get("angle")
            new_delete_point = "        VehicleDeleters = {{x=%s,y=%s,z=%s}},\n" % (
                self.new_data.get("Vehicle_return_place").get("x"),
                self.new_data.get("Vehicle_return_place").get("y"),
                self.new_data.get("Vehicle_return_place").get("z")
            )

            new_boss = "        BossActions = {{x = %s, y = %s, z = %s}},\n" % (
                self.new_data.get("Boss").get("x"),
                self.new_data.get("Boss").get("y"),
                self.new_data.get("Boss").get("z")
            )

            final = {
                "vehicle": new_vehicles,
                "cloakroom": new_cloakroom,
                "armories": new_armories,
                "boss": new_boss, 
                "vehicle_menu": new_vehicle_menu,
                "vehicle_spawn": new_spawn_point,
                "vehicle_heading": new_heading,
                "vehicle_delete": new_delete_point
            }

            for i in range(0, len(self.config_file_infos.get("keys"))):
                self.config_file_infos.update(
                    {
                        self.config_file_infos.get("keys")[i]: {
                            "old": data[self.config_file_infos.get("lines").get(self.config_file_infos.get("keys")[i])],
                            "replace": final.get(self.config_file_infos.get("keys")[i])
                        }
                    }
                )
            config_file.close()
            return



def main():
    if len(sys.argv) == 1:
        print("You need to use args rename:<name> next to the command")
        print("For example: py GBUpdate.py rename:cartel")
        return
    
    if not sys.argv[1].startswith("rename") and not sys.argv[1].startswith("create"):
        print("Bad command, use rename:<name> or create:<name> command")
        return
    
    if len(sys.argv) == 2:
        if sys.argv[1].startswith("rename"):
            print("You need to use a second arg like : sql or file next to the command")
            print("sql choice is if u want to the script make the request for u")
            print("file is for if u want to just create a file with all sql request")
            return

    if sys.argv[1].startswith("rename"):
        if sys.argv[2] != "sql" and sys.argv[2] != "file":
            print("Bad arg[2], use sql or file")
            return  
        mode = sys.argv[2]

    method = sys.argv[1].split(":")[0].lower()
    file = sys.argv[1].split(":")[1].lower()
    json = JSONFile()
    json.ReadFile()
    FileContent = FileTemplate()
    Build = Builder(file, json.content, FileContent)
    Build.DefineClientContent()
    Build.DefineServerLocaleAndManifestContent()
    Build.DefineConfigContent()
    Build.DefineSQLContent()
    Build.FinalContent()
    Build.CreateFile()
    

    # sql = SQL(json.content, file)
    # MyFile = UpdateFile(file, json.content)
    # if MyFile.DefineFiles() is not None:
    #     MyFile.InitializeNewValues()
    #     if MyFile.UpdateConfigFile():
    #         print("config success")
        
    #     if MyFile.UpdateClientFile():
    #         print("client success")
    #     if MyFile.UpdateServerFile():
    #         print("server success")
    #     if MyFile.UpdateLocaleFile():
    #         print("locale_success")
    #     if MyFile.UpdateDirName():
    #         print("dir success")


    #     sql.DefineAllRequest()

    #     if mode == "sql":
    #         sql.UpdateAll()
    #     if mode == "file":
    #         sql.CreateFile()

if __name__ == "__main__":
    main()