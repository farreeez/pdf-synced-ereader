import whisper, json, vlc, time 
from pynput import keyboard

# model = whisper.load_model("base")

book = "../books/Sam Walton, made in America my story - Sam Walton/audio/Sam Walton Made in America (Unabridged) - 01.m4b"

# result = model.transcribe(book)
# with open("transcript.txt", "w", encoding="utf-8") as f:
#     f.write(result["text"])

# with open("jsonDump.txt", "w", encoding="utf-8") as f:
#     f.write(json.dumps(result, indent=4))

# print("successfully saved to file")
# print(json.dumps(result, indent=4))

with open("jsonDump.txt", "r", encoding="utf-8") as f:
    audioJson = json.load(f)

currAudioSpeed = 1.0
player = vlc.MediaPlayer(book)

def on_press(key):
    global currAudioSpeed
    try:
        if key.char == "d":
            currAudioSpeed += 0.5
            player.set_rate(currAudioSpeed)
        elif key.char == "s":
            currAudioSpeed -= 0.5
            player.set_rate(currAudioSpeed)
        elif key.char == "q":
            print("stopping.")
            if player.is_playing():
                player.stop()
            return False
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press) 
listener.start()

segments = audioJson["segments"]
currSeg = 0

player.play()
time.sleep(0.5)

print(segments[currSeg]["text"])
while player.is_playing():
    ms = player.get_time()

    if ms/1000.0 >= segments[currSeg]["end"]:
        currSeg += 1
        print(segments[currSeg]["text"])

    time.sleep(0.1)


