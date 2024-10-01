<iframe width="560" height="315" src="https://www.youtube.com/embed/uaHmtJrZRdM" frameborder="0" allowfullscreen></iframe>



# Error de Permisos en Google Cloud Translation API

## Descripción del Problema   raise HttpError(resp, content, uri=self.uri)
googleapiclient.errors.HttpError: <HttpError 403 when requesting https://translation.googleapis.com/v3beta1/projects/sasa:translateText?alt=json returned "Cloud IAM permission 'cloudtranslate.generalModels.predict' denied.". Details: "Cloud IAM permission 'cloudtranslate.generalModels.predict' denied. "


Al intentar utilizar la API de Google Cloud Translation, se presenta el siguiente error:

![Error de Permisos](https://user-images.githubusercontent.com/69730626/212182082-af7fe8e8-d697-4e31-8288-9b8e42ed269f.png)

**Mensaje de error:** 1
00:00:07,000 --> 00:02:06,000
Martin Luther King Jr.

2
00:02:08,000 --> 00:05:07,000
Day is a federal holiday in the United States,

3
00:05:07,000 --> 00:11:01,000
observed on the third Monday of January each year, in
honor of Martin Luther King Jr.


factos y errores :

![Problem with Azure](https://private-user-images.githubusercontent.com/133063174/364478836-f6a2dab4-2efd-43f0-80fb-f6d8cee6329e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3Mjc4MDQ3MzMsIm5iZiI6MTcyNzgwNDQzMywicGF0aCI6Ii8xMzMwNjMxNzQvMzY0NDc4ODM2LWY2YTJkYWI0LTJlZmQtNDNmMC04MGZiLWY2ZDhjZWU2MzI5ZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMDAxJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTAwMVQxNzQwMzNaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05ZDdlMzdlZmQxNDY1ZDY4ZTY4NWE4NDNkYjE3MjhiZDBlMmQ4NWIyZTFkYzk0OTlkMjdlMzhlMDcwZjJkODE2JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.cbYKaiEL0Wk3ZmS9WPne-Dk4OZo0kIEjel4OwIfc7uc)





**Video demonstration** (click the picture):

[![Video explicativo](https://img.youtube.com/vi/uaHmtJrZRdM/0.jpg)](https://www.youtube.com/watch?v=uaHmtJrZRdM&t=5s)

 
🐱‍👤🐱‍🏍de varios idiomas en el ajuste
### AÑADE -Sentí curiosidad por esas traducciones y experimenté comparándolas con las de algunos modelos disponibles en Hugging Face:

Modelo	Descargas del mes pasado	Traducción
Helsinki-PNL/opus-mt-es-en	270.778	Que un juego para niños tenga como objetivo estafar a un pobre aldeano es bastante curioso.
salesken/traduccion-espanol-y-portugues-a-ingles	11,447	Es bastante curioso que el juego de un niño tenga el efecto de apuñalar a un pobre aldeano.
Helsinki-NLP/opus-mt-tc-big-cat_oci_spa-en	55	Que un juego para niños tenga como objetivo estafar a un pobre aldeano es bastante curioso.
Curiosamente, parece que el modelo con menos descargas obtuvo la mejor traducción. Tal vez sea porque es un modelo grande y, por lo tanto, utiliza más recursos a cambio de obtener mejores traducciones, creo.

Me pregunto si es el orden de las palabras ( Wikipedia en inglés , Wikipedia en español ) de la fase original lo que dificulta la traducción automática. No hablo español, lo estudié un poco pero no lo hablo, sin embargo este orden me parece un poco extraño. Tal vez los datos de entrenamiento de esos modelos tenían relativamente pocas fases en este orden. Si lo reescribes como "Es bastante curioso que un juego para niños tenga como logro estafar a un pobre aldeano" - que es un orden que por alguna razón me parece más natural - entonces obtienes las siguientes traducciones:

Modelo	Traducción
Google Translate	Es bastante curioso que un juego para niños tenga como objetivo estafar a un pobre aldeano.
L profundo	Es bastante curioso que un juego infantil tenga como objetivo estafar a un pobre aldeano.
Helsinki-PNL/opus-mt-es-en	Es bastante curioso que un juego para niños tenga como objetivo estafar a un pobre aldeano.
salesken/traduccion-espanol-y-portugues-a-ingles	Es bastante curioso que un juego infantil tenga el efecto de apuñalar a un pobre aldeano.
Helsinki-NLP/opus-mt-tc-big-cat_oci_spa-en	Es bastante curioso que un juego para niños tenga como logro defraudar a un pobre aldeano.
Ahora parece que DeepL funciona mucho mejor (mientras que Helsinki-NLP/opus-mt-es-en todavía funciona mal). Probablemente DeepL necesite mejorar su conjunto de entrenamiento para evitar este tipo de problemas.

# Auto Synced & Translated Dubs
Traduce automáticamente el texto de un video a los idiomas elegidos basándose en un archivo de subtítulos y también utiliza voz de IA para doblar el video, mientras lo mantiene sincronizado correctamente con el video original utilizando los tiempos de los subtítulos.
 
### How It Works
Si ya tiene un archivo de subtítulos SRT creado por humanos para un video, esto hará lo siguiente:
1. Utilizará Google Cloud/DeepL para traducir automáticamente el texto y crear nuevos archivos SRT traducidos
2. Utilizará los tiempos de las líneas de subtítulos para calcular la duración correcta de cada clip de audio hablado
3. Creará clips de audio de texto a voz del texto traducido (usando voces neuronales más realistas)
4. Estirará o encogerá el clip de audio traducido para que tenga exactamente la misma duración que el discurso original.
- Opcional (activado de manera predeterminada): en lugar de estirar los clips de audio, puede realizar una segunda pasada para sintetizar cada clip a través de la API usando la velocidad de habla adecuada calculada durante la primera pasada. Esto mejora levemente la calidad del audio.
- Si usa Azure TTS, todo este paso no es necesario porque permite especificar la duración deseada del discurso antes de la síntesis
5. Construye la pista de audio insertando los nuevos clips de audio en sus puntos de tiempo correctos. Por lo tanto, el discurso traducido permanecerá perfectamente sincronizado con el video original.
### Más funciones clave
- Crea versiones traducidas del archivo de subtítulos SRT
- Procesamiento por lotes de varios idiomas en secuencia
- Archivos de configuración para guardar la traducción, la síntesis y la configuración del idioma para su reutilización
- Permite un control detallado sobre cómo se traduce y sintetiza el texto
- Incluye: una lista de frases "No traducir", una lista de traducción manual, una lista de pronunciación de fonemas y más

### Herramientas adicionales incluidas
- `TrackAdder.py`: agrega pistas de audio de todos los idiomas a un archivo de video
- Con la capacidad de fusionar una pista de efectos de sonido en cada pista de idioma
- `TitleTranslator.py`: traduce el título y la descripción de un video de YouTube a varios idiomas
- `TitleDescriptionUpdater.py`: usa la API de YouTube para actualizar los títulos y las descripciones localizados de un video de YouTube usando la salida de TitleTranslator.py
- `SubtitleTrackRemover.py`: usa la API de YouTube para eliminar una pista de audio específica de un video de YouTube
- `TranscriptTranslator.py`: traduce una transcripción completa de texto
- `TranscriptAutoSyncUploader.py`: usando la API de YouTube, le permite cargar una transcripción para un video y luego hacer que YouTube sincronice el texto con el video
- También puede cargar múltiples transcripciones pretraducidas y hacer que YouTube las sincronice, suponiendo que el idioma sea compatible
- `YouTube_Synced_Translations_Downloader.py`: usando la API de YouTube, traduzca la transcripción de un video y luego haga que YouTube sincronice el texto con el video
subtítulos de un video en los idiomas especificados y luego descargue el archivo de subtítulos sincronizado automáticamente creado por YouTube
----

# Instrucciones

### Requisitos externos:
- ffmpeg debe estar instalado (https://ffmpeg.org/download.html)

### Herramientas externas opcionales:
- Opcional: en lugar de ffmpeg para estirar el audio, puedes usar el programa 'rubberband'
- De hecho, descubrí que ffmpeg funciona mejor, pero dejaré la opción de rubberband si lo deseas.
- Si usas Rubberband, necesitarás los binarios de Rubberband. Específicamente en [esta página]((https://breakfastquay.com/rubberband/), busca el enlace de descarga para "Utilidad de línea de comandos de la biblioteca Rubber Band v3.3.0" (elige la versión de Windows o MacOS según corresponda). Luego, extrae el archivo para encontrar:
- En Windows: rubberband.exe, rubberband-r3.exe y sndfile.dll
- En MacOS: rubberband, rubberband-r3
- No necesita instalarse, solo coloca los archivos mencionados anteriormente en el mismo directorio que main.py

## Configuración y configuración
1. Descargue o clone el repositorio e instale los requisitos usando `pip install -r requirements.txt`
- Escribí esto usando Python 3.9 pero probablemente también funcione con versiones anteriores
2. Instale los programas mencionados en los 'Requisitos externos' anteriores.
3. Configure su Google Cloud (consulte la Wiki), el acceso a la API de Microsoft Azure y/o el token de API de DeepL, y configure las variables en `cloud_service_settings.ini`.
- Recomiendo Azure para la síntesis de voz TTS porque, en mi opinión, tienen voces más nuevas y mejores, y de mayor calidad (Azure admite una frecuencia de muestreo de hasta 48 KHz frente a los 24 KHz de Google).
- Google Cloud es más rápido, más económico y admite más idiomas para la traducción de texto, pero también puede usar DeepL.
4. Configure sus ajustes de configuración en `config.ini`. Los ajustes predeterminados deberían funcionar en la mayoría de los casos, pero léalos, especialmente si está usando Azure para TTS, porque hay más opciones aplicables que puede personalizar.
- Esta configuración incluye opciones como la capacidad de omitir la traducción de texto, configurar formatos y frecuencia de muestreo, y usar la síntesis de voz de dos pasadas
5. Finalmente, abre `batch.ini` para configurar el idioma y la configuración de voz que se usarán para cada ejecución.
- En la sección superior `[SETTINGS]`, ingresarás la ruta al archivo de video original (usado para obtener la duración de audio correcta) y la ruta del archivo de subtítulos original
- También puedes usar la variable `enabled_languages` para enumerar todos los idiomas que se traducirán y sintetizarán a la vez. Los números corresponderán a las secciones `[LANGUAGE-#]` en el mismo archivo de configuración. El programa procesará solo los idiomas enumerados en esta variable.
- Esto te permite agregar tantos ajustes preestablecidos de idioma como quieras (como la voz preferida por idioma) y puedes elegir qué idiomas quieres usar (o no usar) para cualquier ejecución determinada.
- Asegúrate de verificar los idiomas y voces compatibles para cada servicio en su respectiva documentación.

## Instrucciones de uso
- **Cómo ejecutar:** Después de configurar los archivos de configuración, simplemente ejecute el script main.py usando `python main.py` y déjelo ejecutar hasta que se complete
- Los archivos de subtítulos traducidos y las pistas de audio dobladas resultantes se colocarán en una carpeta llamada 'output'
- **Opcional:** Puede usar el script `TrackAdder.py` independiente para agregar automáticamente las pistas de idioma resultantes a un archivo de video mp4. Requiere que ffmpeg esté instalado.
- Abra el archivo de script con un editor de texto y cambie los valores en la sección "Configuración de usuario" en la parte superior.
- Esto etiquetará las pistas para que el archivo de video esté listo para ser cargado a YouTube. SIN EMBARGO, la función de pistas de audio múltiples solo está disponible para una cantidad limitada de canales. Lo más probable es que deba comunicarse con el soporte para creadores de YouTube para solicitar acceso, pero no hay garantía de que lo otorguen.
- **Opcional:** Puedes usar el script `TitleTranslator.py` independiente si subes el video a YouTube, que te permite ingresar el título y la descripción de un video, y el texto se traducirá a todos los idiomas habilitados en `batch.ini`. Se colocarán juntos en un solo archivo de texto en la carpeta "output".

----

## Notas adicionales:
- Esto funciona mejor con subtítulos que no eliminan los espacios entre oraciones y líneas.
- Por ahora, el proceso solo supone que hay un hablante. Sin embargo, si puede crear archivos SRT separados para cada hablante, podría generar cada pista TTS por separado usando diferentes voces y luego combinarlas después.
- Admite tanto la API de Google Translate como DeepL para traducción de texto, y Google, Azure y Eleven Labs para conversión de texto a voz con voces neuronales.
- Este script se escribió teniendo en cuenta mi propio flujo de trabajo personal. Es decir:
- Uso [**OpenAI Whisper**](https://github.com/openai/whisper) para transcribir los videos localmente, luego uso [**Descript**](https://www.descript.com/) para sincronizar esa transcripción y retocarla con correcciones.
- Luego, exporto el archivo SRT con Descript, que es ideal porque no solo junta los tiempos de inicio y fin de cada línea de subtítulo. Esto significa que el doblaje resultante conservará las pausas entre las oraciones del discurso original. Si usa subtítulos de otro programa, es posible que las pausas entre las líneas sean demasiado breves.
- Las configuraciones de exportación SRT en Descript que parecen funcionar decentemente para el doblaje son *150 caracteres como máximo por línea* y *1 línea como máximo por tarjeta*.
- La función de síntesis "Two Pass" (se puede habilitar en la configuración) mejorará drásticamente la calidad del resultado final, pero requerirá sintetizar cada clip dos veces, por lo que duplicará los costos de API.
### Servicios de conversión de texto a voz compatibles actualmente:
- Microsoft Azure
- Google Cloud
- Eleven Labs

### Servicios de traducción compatibles actualmente:
- Google Translate
- DeepL

## Para obtener más información sobre los idiomas compatibles por servicio:
- [Idiomas compatibles con Google Cloud Translation](https://cloud.google.com/translate/docs/languages)
- [Idiomas compatibles con la conversión de texto a voz de Google Cloud](https://cloud.google.com/text-to-speech/docs/voices)
- [Idiomas compatibles con la conversión de texto a voz de Azure](https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech)
- [Idiomas compatibles con DeepL](https://www.deepl.com/docs-api/translating-text/request/)

----

### Para ver ejemplos de resultados, consulte: [Página wiki de ejemplos](https://github.com/ThioJoe/Auto-Synced-Translated-Dubs/wiki/Examples)
### Para ver las funciones planificadas, consulte: [Página wiki de funciones planificadas](https://github.com/ThioJoe/Auto-Synced-Translated-Dubs/wiki/Planned-Features)
### Para ver las instrucciones de configuración del proyecto de Google Cloud, consulte: [Página wiki de instrucciones](https://github.com/ThioJoe/Auto-Synced-Translated-Dubs/wiki/Instructions:-Obtaining-an-API-Key)
### Para ver las instrucciones de configuración de Microsoft Azure, consulte: [Página wiki de instrucciones de Azure](https://github.com/ThioJoe/Auto-Synced-Translated-Dubs/wiki/Instructions:-Microsoft-Azure-Setup)
