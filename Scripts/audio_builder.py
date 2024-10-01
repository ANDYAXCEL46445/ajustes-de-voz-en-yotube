import soundfile
import pyrubberband
import configparser
import pathlib
import os
import io
import math
from platform import system as sysPlatform

from Scripts.shared_imports import *
import Scripts.TTS as TTS

from pydub import AudioSegment
from pydub.silence import detect_leading_silence
import langcodes
import numpy
import subprocess

# Set working folder
workingFolder = "workingFolder"

# If macOS, add current working directory to path for session for rubberband
if sysPlatform() == "Darwin":
    os.environ['PATH'] += os.pathsep + os.getcwd()


def trim_clip(inputSound):
    trim_leading_silence: AudioSegment = lambda x: x[detect_leading_silence(x) :]
    trim_trailing_silence: AudioSegment = lambda x: trim_leading_silence(x.reverse()).reverse()
    strip_silence: AudioSegment = lambda x: trim_trailing_silence(trim_leading_silence(x))
    strippedSound = strip_silence(inputSound)
    return strippedSound

# Function to insert audio into canvas at specific point
def insert_audio(canvas, audioToOverlay, startTimeMs):
    # Create a copy of the canvas
    canvasCopy = canvas
    # Overlay the audio onto the copy
    canvasCopy = canvasCopy.overlay(audioToOverlay, position=int(startTimeMs))
    # Return the copy
    return canvasCopy

# Function to create a canvas of a specific duration in miliseconds
def create_canvas(canvasDuration, frame_rate=48000):
    canvas = AudioSegment.silent(duration=canvasDuration, frame_rate=frame_rate)
    return canvas

def get_speed_factor(subsDict, trimmedAudio, desiredDuration, num):
    virtualTempFile = AudioSegment.from_file(trimmedAudio, format="wav")
    rawDuration = virtualTempFile.duration_seconds
    trimmedAudio.seek(0) # This MUST be done to reset the file pointer to the start of the file, otherwise will get errors next time try to access the virtual files
    # Calculate the speed factor, put into dictionary
    desiredDuration = float(desiredDuration)
    speedFactor = (rawDuration*1000) / desiredDuration
    subsDict[num]['speed_factor'] = speedFactor
    return subsDict

def stretch_with_rubberband(y, sampleRate, speedFactor):
    rubberband_streched_audio = pyrubberband.time_stretch(y, sampleRate, speedFactor, rbargs={'--fine': '--fine'}) # Need to add rbarges in weird way because it demands a dictionary of two values
    return rubberband_streched_audio

def stretch_with_ffmpeg(audioInput, speed_factor):
    min_speed_factor = 0.5
    max_speed_factor = 100.0
    filter_loop_count = 1

    # Validate speed_factor and calculate filter_loop_count
    if speed_factor < min_speed_factor:
        filter_loop_count = math.ceil(math.log(speed_factor) / math.log(min_speed_factor))
        speed_factor = speed_factor ** (1 / filter_loop_count)
        if speed_factor < 0.001:
            raise ValueError(f"ERROR: Speed factor is extremely low, and likely an error. It was: {speed_factor}")
    elif speed_factor > max_speed_factor:
        raise ValueError(f"ERROR: Speed factor cannot be over 100. It was {speed_factor}.")

    # Prepare ffmpeg command
    command = ['ffmpeg', '-i', 'pipe:0', '-filter:a', f'atempo={speed_factor}', '-f', 'wav', 'pipe:1']
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Pass the audio data to ffmpeg and read the processed data
    out, err = process.communicate(input=audioInput.getvalue())

    # Check for errors
    if process.returncode != 0:
        raise Exception(f'ffmpeg error: {err.decode()}')

    # Convert the output bytes to a NumPy array to be compatible with rest of the program
    # audio_data = numpy.frombuffer(out, numpy.int16)
    # Convert to float64 (which is the format used by pyrubberband)
    # audio_data = audio_data.astype(numpy.float64)
    # # Normalize the data to the range of float64 audio
    # audio_data /= numpy.iinfo(numpy.int16).max

    return out # Returns bytes

def stretch_audio_clip(audioFileToStretch, speedFactor, num):
    virtualTempAudioFile = io.BytesIO()
    # Write the raw string to virtualtempaudiofile
    audioObj, sampleRate = soundfile.read(audioFileToStretch) # auddioObj is a numpy array
    
    # Stretch the audio using user specified method
    if config['local_audio_stretch_method'] == 'ffmpeg':
        stretched_audio = stretch_with_ffmpeg(audioFileToStretch, speedFactor)
        virtualTempAudioFile.write(stretched_audio)
        if config['debug_mode']:
            # For debugging, save the stretched audio file using soundfile
            debug_file_path = os.path.join(workingFolder, f'{num}_stretched_ffmpeg.wav')
            with open(debug_file_path, 'wb') as f:
                f.write(stretched_audio)
    elif config['local_audio_stretch_method'] == 'rubberband':
        stretched_audio = stretch_with_rubberband(audioObj, sampleRate, speedFactor)
        #soundfile.write(f'{workingFolder}\\temp_stretched.wav', streched_audio, sampleRate)
        soundfile.write(virtualTempAudioFile, stretched_audio, sampleRate,
