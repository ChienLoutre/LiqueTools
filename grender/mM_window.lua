--Instancer Guerilla need a selected element to work.
local	guerillaAssetOpen = command.create ("Menus|Liquefacteur|Load Asset")
local	guerillaSeqOpen = command.create ("Menus|Liquefacteur|Load Sequence")

function guerillaAssetOpen:action()
	local err = pcall(function () win:destroy() end)
	print(err)
	-- create a title window
    win = ui.titlewindow ("Asset Name")
	
	-- the control function builds a named parent window and a control inside, so there is no name clash
	   local	function control (title, name, parent, plug)
		  local frame = ui.window (name, parent)
		  local text = ui.text ("text", frame)
		  text:settext (title)
		  text:setpos { x= 0, y = 0, w=50, h=ui.full }
		  local control = ui.control (frame, plug)
		  control:setpos { x=50, y=0, w=ui.full-50, h=ui.full }
		  return frame, control
	   end
	
	local    myString1 = Plug (win, "TypeString", Plug.NoSerial, types.string, "Ex: chars,props,sets")
    local    stringframe1, stringcontrol1 = control ("Type", "myStringCtrl1", win, myString1)
    stringframe1:setpos { y=ui.top,w=200, h=25 }

    local    myString2 = Plug (win, "AssetString", Plug.NoSerial, types.string, "Ex: photocopieuse")
    local    stringframe2, stringcontrol2 = control ("Name", "myStringCtrl2", win, myString2)
    stringframe2:setpos { y=26,w=200, h=25 }
	
    local    myString3 = Plug (win, "VersionString", Plug.NoSerial, types.string, "Ex: master,V003")
    local    stringframe3, stringcontrol3 = control ("Version", "myStringCtrl3", win, myString3)
    stringframe3:setpos { y=42,w=200, h=25 }

	local    button = ui.textbutton ("button", win, "Click")
	button:setpos { w=50, h=15, y=ui.bottom }

	function button:buttonclicked ()
		if myString1:get()=="Ex: chars,Props,set" or  myString2:get()=="Ex: photocopieuse" or myString3:get()=="Ex: master,V003"  then
				print("Type has not changed")
		else
			local assetPAth = "Y:/Liquefacteur/pipeline/prod/assets/"..myString1:get().."/"..myString2:get().."/lookdev/guerilla/"..myString3:get().."/lookdev.gproject"
			if fs.access(assetPAth,"r")==true then
				loaddocument (assetPAth)
			else
				print("file does not exist")
			end
		end
	end
	
	
	win:setpos { w=225, h=100 }
    win:show ()
	
end


function guerillaSeqOpen:action()
	local err = pcall(function () seqwin:destroy() end)
	print(err)
	-- create a title window
    seqwin = ui.titlewindow ("Seq Number")
	
	-- the control function builds a named parent window and a control inside, so there is no name clash
	   local	function control (title, name, parent, plug)
		  local frame = ui.window (name, parent)
		  local text = ui.text ("text", frame)
		  text:settext (title)
		  text:setpos { x= 0, y = 0, w=50, h=ui.full }
		  local control = ui.control (frame, plug)
		  control:setpos { x=50, y=0, w=ui.full-50, h=ui.full }
		  return frame, control
	   end
	
    local    elString = Plug (seqwin, "SeqString", Plug.NoSerial, types.string, "Ex: 00100")
    local    stringframeOne, stringcontrolOne = control ("SeqNumber", "elStringCtrl", seqwin, elString)
    stringframeOne:setpos { y=ui.top,w=200, h=25 }
	
    local    myString = Plug (seqwin, "VersionString", Plug.NoSerial, types.string, "Ex: master,V003")
    local    stringframe, stringcontrol = control ("Version", "myStringCtrl", seqwin, myString)
    stringframe:setpos { y=26,w=200, h=25 }

	local    elButton = ui.textbutton ("button", seqwin, "Click")
	elButton:setpos { w=50, h=15, y=ui.bottom }

	function elButton:buttonclicked ()
		local assetPath = "Y:/Liquefacteur/pipeline/prod/seq/"..elString:get().."/lookdev/guerilla/"..myString:get().."/lookdev.gproject"
		if fs.access(assetPath,"r")==true then
			loaddocument (assetPath)
		else
			print("file does not exist")
		end
	end
	
	
	seqwin:setpos { w=225, h=100 }
    seqwin:show ()
	
end

if MainMenu then
	MainMenu:addcommand (guerillaAssetOpen, "Liquefacteur")
	MainMenu:addcommand (guerillaSeqOpen, "Liquefacteur")
end