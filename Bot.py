import telepot
import moviepy.editor as mp

# Replace TOKEN with your bot's token
bot = telepot.Bot(TOKEN)

# Create a dictionary to store the video and subtitle files that have been uploaded
files = {}

def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'document':
        # Extract the file ID of the document from the message
        file_id = msg['document']['file_id']

        # Download the document from Telegram
        file = bot.download_file(file_id)

        # Save the downloaded file to a local directory
        with open('downloaded_file.mkv', 'wb') as f:
            f.write(file)

        # Check the file extension of the downloaded file
        if file_id.endswith('.mkv') or file_id.endswith('.mp4'):
            # Store the video file in the files dictionary
            files[chat_id] = {'video': 'downloaded_file.mkv'}
        elif file_id.endswith('.srt'):
            # Store the subtitle file in the files dictionary
            files[chat_id] = {'subtitle': 'downloaded_file.srt'}

        # Check if both the video and subtitle files have been uploaded
        if 'video' in files[chat_id] and 'subtitle' in files[chat_id]:
            # Create a keyboard with two buttons
            keyboard = telepot.InlineKeyboardMarkup(inline_keyboard=[
                [telepot.InlineKeyboardButton(text='Rename', callback_data='rename')],
                [telepot.InlineKeyboardButton(text='Set Thumbnail', callback_data='set_thumbnail')],
                [telepot.InlineKeyboardButton(text='Approve', callback_data='approve')]
            ])

            # Send a message with the keyboard to the user
            bot.send_message(chat_id, 'Press a button to perform an action:', reply_markup=keyboard)

def handle_callback_query(query):
    # Extract the callback data from the query object
    callback_data = query['data']

    # Check the callback data value
    if callback_data == 'rename':
        # Extract the chat ID from the query object
        chat_id = query['message']['chat']['id']

        # Load the video file using moviepy
        video = mp.VideoFileClip(files[chat_id]['video'])

        # Extract the default subtitle file name for the video
        default_subtitle_name = video.subtitle

        # Rename the subtitle file
        new_subtitle_name = default_subtitle_name.replace('Persian', 'English')
        os.rename(default_subtitle_name, new_subtitle_name)

        # Update the subtitle file in the files dictionary
        files[chat_id]['subtitle'] = new_sub
