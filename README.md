# Biblia

## Opis
Skrypt umożliwia pobieranie tekstu z różnych tłumaczeń Biblii na podstawie nazwy księgi, numeru rozdziału i wersetu oraz wybranego języka tekstu. Możliwe jest pobranie tekstu w języku polskim, greckim lub hebrajskim.

## Wymagania
Aby skrypt działał poprawnie, wymagane jest posiadanie zainstalowanych następujących bibliotek Pythona:
- `requests`
- `beautifulsoup4`

## Uruchomienie
Skrypt uruchamia się z linii poleceń. Przykładowe użycie:
```
python bible_text_retrieval.py Rdz 1-1 pl
```
Gdzie:
- `Rdz` - nazwa księgi (np. "Rdz" dla Księgi Rodzaju) nazwę trzeba zapisać w języku angielskim dla opcji greek i hebrew,
- `1-1` - numer rozdziału i wersetu (np. "1-1" dla pierwszego wersetu pierwszego rozdziału),
- `pl` - język tekstu (dostępne opcje to: "pl" dla polskiego, "greek" dla greckiego, "hebrew" dla hebrajskiego).

## Zapisywanie danych
Dane pobrane z internetu są zapisywane do plików tekstowych w celu ich ponownego użycia bez konieczności ponownego pobierania z internetu. Nazwa pliku generowana jest na podstawie podanych danych (nazwa księgi, numer rozdziału i wersetu oraz język tekstu).

---

W README zalecam uzupełnienie sekcji "Autor" i "Licencja" zgodnie z Twoimi preferencjami. Dodatkowo, należy upewnić się, że istnieje plik `LICENSE` zawierający odpowiednią licencję, np. MIT.
