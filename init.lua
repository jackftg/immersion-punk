
------- TODO Accept voice as input -------


-- Text field variables
local inputText = ""
local responseText = ""

-- File paths
local trigger_file_path = "vs_message.txt"
local response_file_path = "response.txt"


-- TODO Function to recognize the person in front of V



-- Function to write text to the python trigger file
local function write_text_to_trigger_file(text)
    local file = io.open(trigger_file_path, "w")
    if file then
        file:write(text)
        file:close()
    end
end


-- Function to handle sending text
local function handleSend()
    if inputText ~= "" then
        print(inputText)
        write_text_to_trigger_file(inputText)
        inputText = "" -- Clear the input box after sending
    end
end


-- Function to read text from the response file
local function read_response_file()
    local file = io.open(response_file_path, "r")
    if file then
        local content = file:read("*all")
        file:close()
--         os.remove(response_file_path) -- Remove the file after reading
        return content
    end
    return nil
end

-- Function to monitor the response file
local function monitorResponseFile()
    local newResponse = read_response_file()
    if newResponse then
        responseText = newResponse -- responseText is bound below
    end
end


-- Register the onDraw event to create the ImGui window
registerForEvent('onDraw', function()

    -- Widget for your text input
    ImGui.SetNextWindowSize(688, 109)
    if not ImGui.Begin("Say Something..") then
        ImGui.End()
        return
    end
    inputText = ImGui.InputTextMultiline("##InputTextMultiline", inputText, 256, -1, 3 * ImGui.GetTextLineHeight())
    if ImGui.Button("Send") then
        handleSend()
    end
    ImGui.End()

     -- Monitor the response file for updates
     monitorResponseFile()

    -- Widget for Panam's response
    ImGui.SetNextWindowSize(688, 109)
    if ImGui.Begin("Panam's response") then
        ImGui.Text("Panam: " .. responseText)
    end
    ImGui.End()

end)




