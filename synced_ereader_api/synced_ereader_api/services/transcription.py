import whisper, json, vlc, time, os, sqlite3 
from pydub import AudioSegment
from pynput import keyboard
from pathlib import Path

audioDirectory = "../books/Sam Walton, made in America my story - Sam Walton/audio/"

files = sorted(f for f in os.listdir(audioDirectory)
               if os.path.isfile(os.path.join(audioDirectory, f)))
print(files)

chunkFolder = Path(audioDirectory + "chunks")
chunkFolder.mkdir(parents=True, exist_ok=True)

for file in files:
    bookDir = audioDirectory + file
    audio = AudioSegment.from_file(bookDir)

    durSecs = len(audio) 

    segLength = 60 * 5 * 1000

    for i in range(0, len(audio), segLength):
        chunk = audio[i:i+segLength]

        chunkFolder = Path(audioDirectory + "chunks")
        chunkFolder.mkdir(parents=True, exist_ok=True)

        chunkNumber = int(i / segLength) + 1

        print(f"{chunkFolder}/{file} Chunk {chunkNumber:02}.mp3 CREATED")
        chunk.export(f"{chunkFolder}/{file} Chunk {chunkNumber:02}.mp3",format="mp3")

chunkFiles = sorted(os.listdir(chunkFolder))

print(chunkFiles)

model = whisper.load_model("base")
currTime = 0.0
currChunk = 0

for chunk in chunkFiles:
    print(f"RUNNING MODEL {chunkFolder}/{chunk}")
    result = model.transcribe(f"{chunkFolder}/{chunk}")
    currChunk += 1
    
    if(currTime != 0.0):
        for segment in result["segments"]:
            segment["start"] += currTime
            segment["end"] += currTime
    
    currTime = result["segments"][-1]["end"]
    with open(f"{audioDirectory}/transcriptJson/jsonDump{currChunk:02}.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result["segments"], indent=4))

# with open("jsonDump.txt", "r", encoding="utf-8") as f:
#     audioJson = json.load(f)

# currAudioSpeed = 1.0
# player = vlc.MediaPlayer(book)

# def on_press(key):
#     global currAudioSpeed
#     try:
#         if key.char == "d":
#             currAudioSpeed += 0.5
#             player.set_rate(currAudioSpeed)
#         elif key.char == "s":
#             currAudioSpeed -= 0.5
#             player.set_rate(currAudioSpeed)
#         elif key.char == "q":
#             print("stopping.")
#             if player.is_playing():
#                 player.stop()
#             return False
#     except AttributeError:
#         pass

# listener = keyboard.Listener(on_press=on_press) 
# listener.start()

# segments = audioJson["segments"]
# currSeg = 0

# player.play()
# time.sleep(0.5)

# print(segments[currSeg]["text"])
# while player.is_playing():
#     ms = player.get_time()

#     if ms/1000.0 >= segments[currSeg]["end"]:
#         currSeg += 1
#         print(segments[currSeg]["text"])

#     time.sleep(0.1)

