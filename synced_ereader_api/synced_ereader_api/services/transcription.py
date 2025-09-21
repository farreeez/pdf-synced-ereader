import whisper, json, vlc, time, os, sqlite3 
from pydub import AudioSegment
from pynput import keyboard
from pathlib import Path

def _validate_transcription_data(request_data):
    # validate correct input fields were provided.
    if not request_data:
        raise ValueError("No data was provided in the request body.")

    required_fields = ["path", "is_single_audio_file"]

    missing = [field for field in required_fields if field not in request_data]

    if len(missing) > 0:
        raise ValueError("The following required fields are not in request body: " + ",".join(missing))

def _validate_audio_path(path, is_single_file):
    # if is single audio is true check that URI is for a file otherwise check that it is for a directory.
    if type(is_single_file) is not bool:
        raise ValueError("The field is_single_audio_file must be a boolean.")

    audioPath = Path(path)

    if not (audioPath.is_absolute() and audioPath.exists()):
        raise ValueError("path provided is invalid.")

    if is_single_file and audioPath.is_dir():
        raise ValueError("is_single_file is set to true, but the path provided is for a folder.")

    if (not is_single_file)  and audioPath.is_file():
        raise ValueError("is_single_file is set to false, but the path provided is for a file.")

def transcribe_audio(request_data):
    try:
        _validate_transcription_data(request_data)
    except ValueError as e:
        raise ValueError(str(e))

    is_single_file = request_data["is_single_audio_file"]
    rawAudioPath = request_data["path"]

    try:
        _validate_audio_path(rawAudioPath, is_single_file)
    except ValueError as e:
        raise ValueError(str(e))
    
# audioDirectory = "../books/Sam Walton, made in America my story - Sam Walton/audio/"

# files = sorted(f for f in os.listdir(audioDirectory)
#                if os.path.isfile(os.path.join(audioDirectory, f)))
# print(files)

# chunkFolder = Path(audioDirectory + "chunks")
# chunkFolder.mkdir(parents=True, exist_ok=True)

# for file in files:
#     bookDir = audioDirectory + file
#     audio = AudioSegment.from_file(bookDir)

#     durSecs = len(audio) 

#     segLength = 60 * 5 * 1000

#     for i in range(0, len(audio), segLength):
#         chunk = audio[i:i+segLength]

#         chunkFolder = Path(audioDirectory + "chunks")
#         chunkFolder.mkdir(parents=True, exist_ok=True)

#         chunkNumber = int(i / segLength) + 1

#         print(f"{chunkFolder}/{file} Chunk {chunkNumber:02}.mp3 CREATED")
#         chunk.export(f"{chunkFolder}/{file} Chunk {chunkNumber:02}.mp3",format="mp3")

# chunkFiles = sorted(os.listdir(chunkFolder))

# print(chunkFiles)

# model = whisper.load_model("base")
# currTime = 0.0
# currChunk = 0

# for chunk in chunkFiles:
#     print(f"RUNNING MODEL {chunkFolder}/{chunk}")
#     result = model.transcribe(f"{chunkFolder}/{chunk}")
#     currChunk += 1
    
#     if(currTime != 0.0):
#         for segment in result["segments"]:
#             segment["start"] += currTime
#             segment["end"] += currTime
    
#     currTime = result["segments"][-1]["end"]
#     with open(f"{audioDirectory}/transcriptJson/jsonDump{currChunk:02}.txt", "w", encoding="utf-8") as f:
#         f.write(json.dumps(result["segments"], indent=4))

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

