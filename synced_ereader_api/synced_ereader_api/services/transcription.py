import whisper, json
from pydub import AudioSegment
from pynput import keyboard
from pathlib import Path
from .shared import validate_request_data

def _validate_audio_path(path, is_single_file):
    # if is single audio is true check that URI is for a file otherwise check that it is for a directory.
    if type(is_single_file) is not bool:
        raise ValueError("The field is_single_audio_file must be a boolean.")

    if not (path.is_absolute() and path.exists()):
        raise ValueError("path provided is invalid.")

    if is_single_file and path.is_dir():
        raise ValueError("is_single_file is set to true, but the path provided is for a folder.")

    if (not is_single_file)  and path.is_file():
        raise ValueError("is_single_file is set to false, but the path provided is for a file.")

def transcribe_audio(request_data: json, project_path:Path):
    try:
        validate_request_data(request_data, ["path","is_single_audio_file"])
    except ValueError as e:
        raise e

    is_single_file = request_data["is_single_audio_file"]
    raw_audio_path = request_data["path"]
    audio_path = Path(raw_audio_path)

    try:
        _validate_audio_path(audio_path, is_single_file)
    except ValueError as e:
        raise e
    
    if is_single_file:
        files = [audio_path]
    else:
        files = sorted(f for f in audio_path.iterdir() if f.is_file())
    
    # TODO: Create a metadata json file along with the json dumps that can then be used to validate the status of the json dumps.
    try:
        chunkFolder = project_path / "chunks"
        chunkFolder.mkdir(parents=True, exist_ok=True)

        for file in files:
            bookDir = file.absolute().__str__()
            print("getting audio from file")
            print(bookDir)
            audio = AudioSegment.from_file(bookDir)

            segLength = 60 * 5 * 1000

            for i in range(0, len(audio), segLength):
                chunk = audio[i:i+segLength]

                chunkNumber = int(i / segLength) + 1

                chunk.export(f"{chunkFolder}/{file.name} Chunk {chunkNumber:02}.mp3",format="mp3")

                if(i > 2):
                    break

        chunkFiles = sorted(f for f in Path(chunkFolder).iterdir() if f.is_file())

        model = whisper.load_model("base")
        currTime = 0.0
        currChunk = 0

        transcript_folder = project_path / "transcriptJson"
        transcript_folder.mkdir(parents=True, exist_ok=True)

        for chunk in chunkFiles:
            print(f"{chunkFolder}/{chunk.name}")
            result = model.transcribe(f"{chunkFolder}/{chunk.name}")
            currChunk += 1
            
            if(currTime != 0.0):
                for segment in result["segments"]:
                    segment["start"] += currTime
                    segment["end"] += currTime
            
            currTime = result["segments"][-1]["end"]
            print("created jsonDump" + str(currChunk))
            with open(f"{transcript_folder}/jsonDump{currChunk:02}.txt", "w", encoding="utf-8") as f:
                f.write(json.dumps(result["segments"], indent=4))
    except Exception as e:
        raise e
