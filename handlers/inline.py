from keyboards.inline import main_options, option2_submenu






async def test_options(query):
    if query.data == "opt1":
        await query.edit_message_text("You chose Option 1 ✅")
        # await query.message.reply_text("Please select from menu:", reply_markup=main_menu())

    elif query.data == "opt2":
        await query.edit_message_text("Option 2 selected. Pick a sub-option:", reply_markup=option2_submenu())

    elif query.data == "subA":
        await query.edit_message_text("You selected Sub-Option A 👍")
        # await query.message.reply_text("Please select from menu:", reply_markup=main_menu())

    elif query.data == "subB":
        await query.edit_message_text("You selected Sub-Option B 🎉")
        # await query.message.reply_text("Please select from menu:", reply_markup=main_menu())
        # await query.message.reply_text("Hi")

    elif query.data == "back":
        await query.edit_message_text("Back to main inline menu:", reply_markup=main_options())
