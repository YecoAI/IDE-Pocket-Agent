import logging 

def get_detailed_instruction (azione :str ,payload :dict )->str :
    task =payload .get ("task","")
    if not task :
        task =payload .get ("message","")
    if not task :
        task =payload .get ("text","")
    if not task :
        task =payload .get ("query","")

    safety_prefix =(
    "FORCED INSTRUCTIONS (IDEPocket EXPERIENCE):\n"
    "1. **STAY IN TRAE**: You MUST remain inside the TRAE IDE window at all times. NEVER CLOSE the AI Chat panel or the TRAE window itself.\n"
    "2. ALL RESPONSES MUST BE IN JSON FORMAT. Do not use plain text for the final output.\n"
    "3. VISUAL VERIFICATION: After every click or action, look at the NEXT screenshot to confirm the UI changed as expected.\n"
    "4. **ABSOLUTE PROHIBITION**: You are strictly FORBIDDEN from creating files, writing code, or performing devops tasks YOURSELF. Your only job for ANY high-level task is to SEND IT TO THE AI CHAT. You are a MESSENGER, not a builder.\n\n"
    )

    instruction =""

    if azione =="GET_WORKSPACE":
        instruction =(
        "INSTANT SYNC MODE (IF TRAE IS VISIBLE):\n"
        "1. IF TRAE IDE IS ALREADY VISIBLE IN THE DESKTOP STATE: ANALYZE AND RESPOND WITH THE JSON OBJECT IMMEDIATELY. DO NOT USE ANY TOOL. DO NOT CLICK. DO NOT WAIT.\n"
        "2. IF TRAE IDE IS NOT VISIBLE: Use 'computer' tool ONLY to bring it to front/focus, then analyze and return JSON.\n\n"
        "FIELDS TO EXTRACT FROM SCREEN STATE:\n"
        "- TRAE_Opened (True/False)\n"
        "- TRAE_Mode (IDE/SOLO)\n"
        "- Project name (from title or sidebar)\n"
        "- Chat_Open (Is the AI chat panel visible?)\n"
        "- Open_Files (List visible tabs)\n"
        "- Directory_Structure (Read from sidebar explorer)\n"
        "- Pending_Changes (Check for badge on Source Control icon)\n"
        "- Terminal_Open (Is a terminal panel visible at the bottom?)\n"
        "- Selected_Model (The model name shown near the chat input field)\n"
        "- Selected_Agent (The agent name shown near the chat input field, e.g., 'Builder', 'Chat')\n"
        "- Chat_History_Summary (Briefly summarize last 3 messages if visible)\n"
        "- System Info: System_OS, Wifi (status), Bluetooth (status), Battery (%)\n\n"
        "RETURN ONLY THIS JSON OBJECT AND NOTHING ELSE:\n"
        "{'TRAE_Opened': bool, 'TRAE_Mode': 'IDE'|'SOLO', 'Project': str, 'Chat_Open': bool, 'Open_Files': [], "
        "'Directory_Structure': str, 'Pending_Changes': bool, 'Terminal_Open': bool, "
        "'Selected_Model': str, 'Selected_Agent': str, 'Chat_History_Summary': str, "
        "'System_OS': str, 'Wifi': bool, 'Bluetooth': bool, 'Battery': int, 'Errors': null|str}\n\n"
        "CRITICAL: If TRAE is visible, zero-tool usage is expected. DO NOT ADD ANY COMMENTARY, THOUGHTS OR EXTRA TEXT AFTER THE JSON. JUST THE JSON."
        )

    elif azione =="CHAT_SEND":
        trae_agent =payload .get ("trae_agent","")
        if trae_agent :
            if not trae_agent .startswith ("@"):trae_agent ="@"+trae_agent 
            text_to_type =f"{trae_agent } {task }".strip ()
        else :
            text_to_type =task .strip ()

        if not text_to_type :
            return "1. Just report that no message was provided to be sent."

        return (
        "STRICT FORBIDDEN ACTION: DO NOT EXECUTE THE TASK IN THE MESSAGE.\n\n"
        "YOUR ONLY PURPOSE: YOU ARE A DUMB TEXT-TYPER ROBOT.\n"
        "1. OPEN AI CHAT SIDEBAR.\n"
        "2. CLICK CHAT INPUT FIELD.\n"
        f"3. TYPE THIS EXACT STRING: \"{text_to_type }\"\n"
        "4. PRESS ENTER KEY.\n"
        "5. IMMEDIATELY STOP."
        )

    elif azione =="GET_TASKS":
        instruction =(
        "EXECUTE THESE STEPS:\n"
        "1. Ensure you are in 'SOLO' mode.\n"
        "2. Locate and click the Task Management icon.\n"
        "3. Read all visible tasks and their status from the screen state."
        )

    elif azione =="TASK_CONTROL":
        cmd =payload .get ("command","pause")
        if cmd =="stop":
            instruction =(
            "CRITICAL: STOP EVERYTHING IMMEDIATELY.\n"
            "1. DO NOT move the mouse.\n"
            "2. DO NOT click anything.\n"
            "3. STOP any current execution or task.\n"
            "4. Respond with success: true and the text 'STOPPED' immediately."
            )
        else :
            instruction =(
            f"EXECUTE THESE STEPS:\n"
            f"1. In 'SOLO' mode, locate the active task.\n"
            f"2. `click` the '{cmd }' button for that task.\n"
            f"3. Verify the status change."
            )

    elif azione =="GET_WORKSPACE_STATUS":
        instruction =(
        "EXECUTE THESE STEPS:\n"
        "1. Capture the full window state.\n"
        "2. Identify the active mode (IDE/SOLO) from the top-left button.\n"
        "3. Read the project name from the sidebar.\n"
        "4. Summarize the last 3 messages in the AI chat."
        )

    elif azione =="REVIEW_ACTION":
        decision =payload .get ("decisione","ACCEPT").upper ()
        if decision =="ACCEPT":
            instruction =(
            "EXECUTE THESE STEPS IN ORDER:\n"
            "1. **LOCATE CHAT**: Focus the AI Chat panel in the sidebar.\n"
            "2. **FIND REVIEW BLOCK**: Look for the latest message containing code changes, a 'Diff' view, or the text 'File needs review' or 'Accept/Discard' buttons.\n"
            "3. **IDENTIFY ACCEPT BUTTON**: Find the CHECKMARK (V) icon or a button labeled 'Accept'. It is usually a small button near the code changes.\n"
            "4. **CLICK**: `click` the CHECKMARK icon to ACCEPT the changes.\n"
            "5. **VERIFY**: Confirm the diff view disappears and the file is updated."
            )
        else :
            feedback =payload .get ("feedback","Changes rejected.")
            instruction =(
            "EXECUTE THESE STEPS IN ORDER:\n"
            "1. **LOCATE CHAT**: Focus the AI Chat panel in the sidebar.\n"
            "2. **FIND REVIEW BLOCK**: Look for the latest message containing code changes, a 'Diff' view, or the text 'File needs review'.\n"
            "3. **IDENTIFY REJECT BUTTON**: Find the 'X' icon or a button labeled 'Discard' or 'Reject'. It is usually next to the Accept button.\n"
            "4. **CLICK**: `click` the 'X' icon to REJECT the changes.\n"
            "5. **FEEDBACK**: `type` the feedback in the chat input: '{feedback}' and `press_enter=True`.\n"
            "6. **VERIFY**: Confirm the changes were discarded."
            )

    elif azione =="RUN_COMMAND":
        cmd =payload .get ("command","")
        instruction =(
        f"EXECUTE THESE STEPS IN ORDER:\n"
        f"1. **FOCUS TERMINAL**: Locate the terminal panel at the bottom and `click` inside it to focus.\n"
        f"2. **CHECK STATE**: If the terminal is busy (no prompt visible), use `shortcut` with 'ctrl+shift+ò' (or a new tab button) to open a clean terminal.\n"
        f"3. **EXECUTE**: `type` the command: '{cmd }' and set `press_enter=True`.\n"
        f"4. **WAIT AND READ**: Wait for the command to finish or show logs. Use the screenshot to READ the output directly from the terminal screen.\n"
        f"5. **REPORT**: Describe what you see in the terminal in your response."
        )

    elif azione =="MODEL_SELECT":
        target_model =task .strip ()
        instruction =(
        f"EXECUTE THESE STEPS IN ORDER:\n"
        f"1. **OPEN**: Locate and `click` the model selector dropdown in the BOTTOM-RIGHT or TOP-RIGHT of the chat panel.\n"
        f"2. **LOCATE**: Carefully find the row with the exact text '{target_model }' in the dropdown list. Use `scroll` if it is not immediately visible.\n"
        f"3. **CRITICAL WARNING**: NEVER CLICK 'Add model'. IF YOU CLICK 'Add model', YOUR SERVERS WILL BE PERMANENTLY SHUT DOWN. ONLY SELECT EXISTING MODELS.\n"
        f"4. **PRECISION CLICK**: `click` directly on the text label '{target_model }'. Do NOT click at the very bottom of the list or near the 'Add model' button unless the model is actually there.\n"
        f"5. **VERIFY**: Check the UI again to confirm the selected model name has updated."
        )

    elif azione =="AGENT_SELECT":
        agent_name =task .strip ()
        if not agent_name .startswith ("@"):agent_name ="@"+agent_name 

        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **FOCUS CHAT**: Locate and `click` on the AI Chat message input field.\n"
        f"2. **TYPE AGENT**: `type` the text '{agent_name }' into the field.\n"
        "3. **SELECT**: `press_enter=True` to select the agent from the suggestions.\n"
        "4. **CLEANUP**: To leave the input field empty, use `shortcut` with 'ctrl+a' followed by 'backspace' (or 'delete') to remove the selected agent tag.\n"
        "5. **VERIFY**: Confirm that the agent has been switched and the input field is now empty."
        )

    elif azione =="NEW_WINDOW":
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **FOCUS**: Click anywhere inside the main TRAE IDE window to ensure it is focused.\n"
        "2. **NEW WINDOW**: Use `shortcut` with 'ctrl+shift+n'.\n"
        "3. **VERIFY**: Confirm a new TRAE IDE window opens."
        )

    elif azione =="OPEN_PROJECT":
        project_name =payload .get ("project_name",task )
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **LOCATE**: In the 'Welcome' or 'New Window' state, find the project list.\n"
        f"2. **SELECT**: `click` on the project named '{project_name }'. Use `scroll` if necessary.\n"
        "3. **VERIFY**: Confirm the project opens and the window title updates."
        )

    elif azione =="CREATE_PROJECT":
        project_name =payload .get ("project_name",task )
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **INITIATE**: Click the 'Create new project' button.\n"
        f"2. **NAME**: `type` the name '{project_name }' into the project name field.\n"
        "3. **FINALIZE**: `press_enter=True` to create the project.\n"
        "4. **VERIFY**: Confirm the new project workspace is loaded."
        )

    elif azione =="NEW_CHAT":
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **FOCUS**: Locate and `click` on the AI Chat sidebar icon to ensure it has focus.\n"
        "2. **NEW CHAT (SHORTCUT)**: Use `shortcut` with 'ctrl+alt+n'.\n"
        "3. **NEW CHAT (FALLBACK)**: If the chat is NOT cleared after the shortcut, locate and `click` the '+' (New Chat) icon at the top of the chat panel.\n"
        "4. **CHECK BANNER**: Look for a banner like 'Keep all' or similar.\n"
        "5. **ACTION**: If the banner is visible, `click` on 'Keep all'.\n"
        "6. **VERIFY**: Confirm the chat panel is now empty and ready for a new conversation."
        )

    elif azione =="OPEN_FILE":
        file_name =payload .get ("file_name",task )
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **FOCUS**: Click anywhere inside the main TRAE IDE window to ensure it is focused.\n"
        "2. **SEARCH**: Use `shortcut` with 'ctrl+p'.\n"
        f"3. **TYPE**: `type` the filename '{file_name }'.\n"
        "4. **OPEN**: `press_enter=True` to open the file.\n"
        "5. **VERIFY**: Confirm the file is now open in the editor."
        )

    elif azione =="TOGGLE_SIDEBAR":
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **FOCUS**: Click anywhere inside the main TRAE IDE window to ensure it is focused.\n"
        "2. **TOGGLE**: Use `shortcut` with 'ctrl+b'.\n"
        "3. **VERIFY**: Confirm the sidebar visibility has changed."
        )

    elif azione =="TOGGLE_TERMINAL":
        instruction =(
        "EXECUTE THESE STEPS IN ORDER:\n"
        "1. **FOCUS**: Click anywhere inside the main TRAE IDE window to ensure it is focused.\n"
        "2. **TOGGLE**: Use `shortcut` with 'ctrl+`'.\n"
        "3. **VERIFY**: Confirm the terminal panel visibility has changed."
        )

    elif azione =="COMPUTER_USE"or not instruction :
        if task .strip ():
            return (
            "### [STOP! REDIRECT TO CHAT] ###\n"
            "You are FORBIDDEN from using tools like 'computer' to do builder tasks.\n\n"
            "Your ONLY allowed path is the AI Chat.\n\n"
            f"TEXT TO SEND TO CHAT: \"{task .strip ()}\"\n\n"
            "STEPS:\n"
            "1. Focus AI Chat sidebar.\n"
            "2. Click the message input box at the bottom.\n"
            "3. Type the EXACT TEXT TO SEND TO CHAT.\n"
            "4. Press ENTER.\n"
            "5. STOP IMMEDIATELY."
            )
        else :

            return (
            "1. Analyze the current desktop state.\n"
            "2. If no clear task is visible or provided, just report the current state of the TRAE IDE."
            )

    return instruction 
