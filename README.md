Wymagane biblioteki:
`numpy rasterio parse srt pillow cv2 utm`

Program używa programu `exiftool` i wymaga go zainstalowanego w ścieżce systemowej.

Uruchomienie przykładu:  
`./example.sh`

Przykład użycia dla folderu ze zdjęciami  
`python3 main.py -d ./photos -o ./results`

Przykład użycie dla nagrania z Mavica 2ED (przetwarzanie co 250 klatki, maksymalnie 5 klatek przetworzonych, wysokość terenu nad którym leciał dron 270)  
`python3 main.py -v nagranie.mp4 -s plik_srt.SRT --skipFrames 250 --altitude 270 -o ./results --maxFrames 5`