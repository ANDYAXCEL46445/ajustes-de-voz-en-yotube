importar archivo de sonido
importar pyrubberband
importar configparser
importar pathlib
importar os
importar io
importar math
desde plataforma importar sistema como sysPlatform

desde Scripts.shared_imports importar *
importar Scripts.TTS como TTS

desde pydub importar AudioSegment
desde pydub.silence importar detect_leading_silence
importar langcodes
importar numpy
importar subproceso

# Establecer carpeta de trabajo
workingFolder = "workingFolder"

# Si es macOS, agregar el directorio de trabajo actual a la ruta de la sesión para rubberband
si sysPlatform() == "Darwin":
os.environ['PATH'] += os.pathsep + os.getcwd()

def trim_clip(inputSound):
trim_leading_silence: AudioSegment = lambda x: x[detect_leading_silence(x) :]
trim_trailing_silence: AudioSegment = lambda x: trim_leading_silence(x.reverse()).reverse()
strip_silence: AudioSegment = lambda x: trim_trailing_silence(trim_leading_silence(x))
strippedSound = strip_silence(inputSound)
return strippedSound

# Función para insertar audio en el lienzo en un punto específico
def insert_audio(canvas, audioToOverlay, startTimeMs):
# Crear una copia del lienzo
canvasCopy = canvas
# Superponer el audio sobre la copia
canvasCopy = canvasCopy.overlay(audioToOverlay, position=int(startTimeMs))
# Devolver la copia
return canvasCopy

# Función para crear un lienzo de una duración específica en milisegundos
def create_canvas(canvasDuration, frame_rate=48000):
canvas = AudioSegment.silent(duration=canvasDuration, frame_rate=frame_rate)
return canvas

def get_speed_factor(subsDict, trimmedAudio, desireDuration, num):
virtualTempFile = AudioSegment.from_file(trimmedAudio, format="wav")
rawDuration = virtualTempFile.duration_seconds
trimmedAudio.seek(0) # Esto DEBE hacerse para restablecer el puntero del archivo al inicio del archivo, de lo contrario obtendrá errores la próxima vez que intente acceder a los archivos virtuales
# Calcular el factor de velocidad, poner en el diccionario
desireDuration = float(desiredDuration)
speedFactor = (rawDuration*1000) / desireDuration
subsDict[num]['speed_factor'] = speedFactor
return subsDict

def stretch_with_rubberband(y, sampleRate, speedFactor):
rubberband_streched_audio = pyrubberband.time_stretch(y, sampleRate, speedFactor, rbargs={'--fine': '--fine'}) # Es necesario agregar rbarges de una manera extraña porque exige un diccionario de dos valores
return rubberband_streched_audio

def stretch_with_ffmpeg(audioInput, speed_factor):
min_speed_factor = 0.5
max_speed_factor = 100.0
filter_loop_count = 1

# Validar speed_factor y calcular filter_loop_count
if speed_factor < min_speed_factor:
filter_loop_count = math.ceil(math.log(speed_factor) / math.log(min_speed_factor))
speed_factor = speed_factor ** (1 / filter_loop_count)
if speed_factor < 0.001:
raise ValueError(f"ERROR: El factor de velocidad es extremadamente bajo y probablemente sea un error. Era: {speed_factor}")
elif speed_factor > max_speed_factor:
raise ValueError(f"ERROR: El factor de velocidad no puede ser mayor que 100. Era {speed_factor}.")

# Preparar comando ffmpeg
command = ['ffmpeg', '-i', 'pipe:0', '-filter:a', f'atempo={speed_factor}', '-f', 'wav', 'pipe:1']
process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Pasar los datos de audio a ffmpeg y leer los datos procesados
out, err = process.communicate(input=audioInput.getvalue())

# Verificar errores
if process.returncode != 0:
raise Exception(f'ffmpeg error: {err.decode()}')

# Convertir los bytes de salida a una matriz NumPy para que sea compatible con el resto del programa
# audio_data = numpy.frombuffer(out, numpy.int16)
# Convertir a float64 (que es el formato utilizado por pyrubberband)
# audio_data = audio_data.astype(numpy.float64)
# # Normalizar los datos al rango de audio float64
# audio_data /= numpy.iinfo(numpy.int16).max

return out # Devuelve bytes

def stretch_audio_clip(audioFileToStretch, speedFactor, num):
virtualTempAudioFile = io.BytesIO()
# Escribir la cadena sin formato en virtualtempaudiofile
audioObj, sampleRate = soundfile.read(audioFileToStretch) # auddioObj es una matriz numpy

# Estirar el audio utilizando el método especificado por el usuario
if config['local_audio_stretch_method'] == 'ffmpeg':
stretched_audio = stretch_with_ffmpeg(audioFileToStretch, speedFactor)
virtualTempAudioFile.write(stretched_audio)
if config['debug_mode']:
# Para la depuración, guarde el archivo de audio estirado utilizando soundfile
debug_file_path = os.path.join(workingFolder, f'{num}_stretched_ffmpeg.wav')
with open(debug_file_path, 'wb') as f:
f.write(stretched_audio)
elif config['local_audio_stretch_method'] == 'rubberband':
stretched_audio = stretch_with_rubberband(audioObj, sampleRate, speedFactor)
#archivo_de_sonido.write(f'{carpeta_de_trabajo}\\temp_stretched.wav', audio_estirado, frecuencia_de_muestreo)
archivo_de_sonido.write(archivo_de_audio_tempular_virtual, audio_estirado, frecuencia_de_muestreo,
