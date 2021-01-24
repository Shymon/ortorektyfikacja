### Użycie poprzez Dockera (wymaga pobrania obrazu o rozmiarze około 1.6 GB)

Uruchomienie przykładu (wyniki pojawią się w katalogu results):  
`./example_docker.sh`

Przykład użycia dla folderu ze zdjęciami  
`docker run --name ortorektyfikacja --rm -i -v $(pwd):/app/program -t shymonr/ortorektyfikacja python3 main.py -d ./photos -o ./results`

Przykład użycia dla nagrania z Mavica 2ED (przetwarzanie co 250 klatki, maksymalnie 5 klatek przetworzonych, wysokość terenu nad którym leciał dron 270)  
`docker run --name ortorektyfikacja --rm -i -v $(pwd):/app/program -t shymonr/ortorektyfikacja python3 main.py -v nagranie.mp4 -s plik_srt.SRT --skipFrames 250 --altitude 270 -o ./results --maxFrames 5`

---
Wymagane biblioteki:
`numpy rasterio parse srt pillow opencv-python utm`  
Przed instalacją biblioteki rasterio, jest wymagane zainstalowanie wymaganych zależności. Instrukcje można znaleźć na: https://rasterio.readthedocs.io/en/latest/installation.html

Program używa programu `exiftool` i wymaga go zainstalowanego w ścieżce systemowej.

Uruchomienie przykładu (wyniki pojawią się w katalogu results):  
`./example.sh`

Przykład użycia dla folderu ze zdjęciami  
`python3 main.py -d ./photos -o ./results`

Przykład użycie dla nagrania z Mavica 2ED (przetwarzanie co 250 klatki, maksymalnie 5 klatek przetworzonych, wysokość terenu nad którym leciał dron 270)  
`python3 main.py -v nagranie.mp4 -s plik_srt.SRT --skipFrames 250 --altitude 270 -o ./results --maxFrames 5`