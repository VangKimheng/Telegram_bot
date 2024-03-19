from telethon import TelegramClient, events

api_id = 26657451
api_hash = 'c176ac32cf3673e7b4090b18ede626d9'

phone_number = '+85515615565'

# Target chat IDs where you want to forward messages
target_chat_ids = [-4088529963, -4136244753, -4180487147, -4131909225, -4101705190]

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Define a dictionary to store the last forwarded message ID for each chat
last_forwarded_message = {chat_id: None for chat_id in target_chat_ids}

# Define an event handler for incoming messages
@client.on(events.NewMessage)
async def forward_message(event):
    # Forward the message to the target chats
    for chat_id in target_chat_ids:
        if event.message.text:  # Forward text messages
            forwarded_message = await client.send_message(chat_id, event.message.text)
        elif event.message.photo:  # Forward photos
            forwarded_message = await client.send_file(chat_id, event.message.photo)
        elif event.message.voice:  # Forward voice messages
            forwarded_message = await client.send_file(chat_id, event.message.voice)
        
        # Save the ID of the last forwarded message for this chat
        last_forwarded_message[chat_id] = forwarded_message.id

# Define a command handler for unsending the last forwarded message
@client.on(events.NewMessage(pattern='D_elete'))
async def delete_last_forwarded(event):
    # Get the chat ID of the incoming message
    chat_id = event.chat_id
    # Get the ID of the last forwarded message for this chat
    last_message_id = last_forwarded_message.get(chat_id)
    if last_message_id:
        # Unsend the last forwarded message
        await client.edit_message(chat_id, last_message_id, message='')
        # Remove the unsent message ID from the dictionary
        last_forwarded_message[chat_id] = None
    else:
        await event.respond("No forwarded messages to delete.")

# Start the client
async def main():
    await client.start()
    await client.run_until_disconnected()

# Run the client forever
while True:
    try:
        client.loop.run_until_complete(main())
    except Exception as e:
        print(f"An error occurred: {e}")
