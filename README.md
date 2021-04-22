# Hunting-Horn-Player

Very simple Discord music player bot made with discord.py, with Munster Hunter quirks. Do not recommend adding additional functionalities to this bot without organizing the existing music bot functionality into a cog, as this was made with just the music bot in mind, and uses some messy global variables to accomplish certain tasks.

Python 3; youtube_dl and discord.py with audio extension libraries required. FFmpeg also needs to be downloaded and added to path: https://www.ffmpeg.org/

  - clear :      clears queue
  - current :    dispalys current song
  - disconnect : disconnects bot from voice channel
  - help :       Shows this message
  - pause :      pauses current song
  - play :      Joins the vc of the person issuing the command, plays and queues songs. Takes in arguments to be searched on youtube
  - queued :     displays currently queued up songs if there are any
  - remove :     removes a song from queue, takes in number
  - resume :     resumes paused song
  - shuffle :    shuffles the current queue of songs
  - skip :       skips the current song
  - stop :       stops playing songs, but does not disconnect from voice channel
