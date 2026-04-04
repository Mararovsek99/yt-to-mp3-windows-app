import os
import re
import sys
import json
import queue
import threading
import subprocess
import webbrowser
import unicodedata
import time
from pathlib import Path
from collections import deque
import tkinter as tk
from tkinter import filedialog, messagebox


APP_TITLE = "YT to MP3"
CONFIG_FILE = "config.json"
WINDOW_SIZE = "700x560"
MIN_WIDTH = 560
MIN_HEIGHT = 430
LINKEDIN_URL = "https://www.linkedin.com/in/andrej-marov%C5%A1ek-78b040206/"

CONTENT_MAX_WIDTH = 520


def make_lang(
    window_title,
    title,
    subtitle,
    download_button,
    stop_button,
    folder_label,
    browse_button,
    open_button,
    language_label,
    playlist_label,
    status_ready,
    status_preparing,
    status_downloading,
    status_done,
    status_failed,
    status_stopped,
    tip,
    credit,
    warn_clipboard_empty,
    warn_invalid_url,
    warn_no_folder,
    err_missing_ytdlp,
    err_missing_ffmpeg,
    err_open_folder,
    current_item_label,
    playlist_progress_label,
    eta_label,
    last_downloads_label,
    nothing_yet,
    unknown_item,
    partial_done,
    all_failed,
    eta_waiting,
    eta_calculating,
):
    return {
        "window_title": window_title,
        "title": title,
        "subtitle": subtitle,
        "download_button": download_button,
        "stop_button": stop_button,
        "folder_label": folder_label,
        "browse_button": browse_button,
        "open_button": open_button,
        "language_label": language_label,
        "playlist_label": playlist_label,
        "status_ready": status_ready,
        "status_preparing": status_preparing,
        "status_downloading": status_downloading,
        "status_done": status_done,
        "status_failed": status_failed,
        "status_stopped": status_stopped,
        "tip": tip,
        "credit": credit,
        "warn_clipboard_empty": warn_clipboard_empty,
        "warn_invalid_url": warn_invalid_url,
        "warn_no_folder": warn_no_folder,
        "err_missing_ytdlp": err_missing_ytdlp,
        "err_missing_ffmpeg": err_missing_ffmpeg,
        "err_open_folder": err_open_folder,
        "current_item_label": current_item_label,
        "playlist_progress_label": playlist_progress_label,
        "eta_label": eta_label,
        "last_downloads_label": last_downloads_label,
        "nothing_yet": nothing_yet,
        "unknown_item": unknown_item,
        "partial_done": partial_done,
        "all_failed": all_failed,
        "eta_waiting": eta_waiting,
        "eta_calculating": eta_calculating,
    }


LANGUAGES = {
    "Slovenian": make_lang(
        "YT v MP3",
        "YT v MP3",
        "Enostavno in hitro prenese MP3 iz YouTube povezave v odložišču.",
        "Prenesi MP3 iz odložišča",
        "Ustavi",
        "Mapa za prenos",
        "Izberi",
        "Odpri mapo",
        "Jezik",
        "Dovoli prenos playliste",
        "Kopiraj YouTube povezavo in pritisni gumb.",
        "Pripravljam prenos...",
        "Prenašam...",
        "Končano.",
        "Prenos ni uspel.",
        "Prenos ustavljen.",
        "Namig: pred klikom kopiraj celoten YouTube link s Ctrl+C.",
        "Made by Andrej Marovšek",
        "Odložišče je prazno.",
        "V odložišču ni veljavne YouTube povezave.",
        "Izberi mapo za prenos.",
        "Manjka datoteka:\n{path}",
        "Manjka datoteka:\n{path}",
        "Mape ni bilo mogoče odpreti.\n\n{error}",
        "Trenutno:",
        "Playlista:",
        "Konec približno:",
        "Zadnjih 5 uspešnih prenosov",
        "Še ni prenesenih komadov.",
        "Prepoznavam naslov ...",
        "Končano. Nekateri komadi so bili preskočeni.",
        "Noben komad ni bil uspešno prenesen.",
        "-",
        "računam ...",
    ),
    "English": make_lang(
        "YT to MP3",
        "YT to MP3",
        "Simple and fast MP3 download from a YouTube link in clipboard.",
        "Download MP3 from Clipboard",
        "Stop",
        "Download folder",
        "Browse",
        "Open Folder",
        "Language",
        "Allow playlist download",
        "Copy a YouTube link and press the button.",
        "Preparing download...",
        "Downloading...",
        "Done.",
        "Download failed.",
        "Download stopped.",
        "Tip: copy the full YouTube link with Ctrl+C before pressing the button.",
        "Made by Andrej Marovšek",
        "Clipboard is empty.",
        "Clipboard does not contain a valid YouTube link.",
        "Please choose a download folder.",
        "Missing file:\n{path}",
        "Missing file:\n{path}",
        "Could not open folder.\n\n{error}",
        "Current:",
        "Playlist:",
        "Approx. finish:",
        "Last 5 successful downloads",
        "No successful downloads yet.",
        "Detecting title ...",
        "Finished. Some items were skipped.",
        "No item was downloaded successfully.",
        "-",
        "calculating ...",
    ),
    "German": make_lang(
        "YT zu MP3", "YT zu MP3",
        "Einfacher und schneller MP3-Download aus einem YouTube-Link in der Zwischenablage.",
        "MP3 aus Zwischenablage laden", "Stoppen", "Download-Ordner", "Wählen", "Ordner öffnen",
        "Sprache", "Playlist-Download erlauben", "Kopiere einen YouTube-Link und drücke die Taste.",
        "Download wird vorbereitet...", "Lade herunter...", "Fertig.", "Download fehlgeschlagen.",
        "Download gestoppt.", "Tipp: Kopiere den vollständigen YouTube-Link mit Ctrl+C vor dem Klick.",
        "Made by Andrej Marovšek", "Zwischenablage ist leer.", "Kein gültiger YouTube-Link in der Zwischenablage.",
        "Bitte Download-Ordner wählen.", "Datei fehlt:\n{path}", "Datei fehlt:\n{path}",
        "Ordner konnte nicht geöffnet werden.\n\n{error}", "Aktuell:", "Playlist:", "Ungefähres Ende:",
        "Letzte 5 erfolgreichen Downloads", "Noch keine erfolgreichen Downloads.", "Titel wird erkannt ...",
        "Fertig. Einige Titel wurden übersprungen.", "Kein Titel wurde erfolgreich heruntergeladen.",
        "-", "wird berechnet ...",
    ),
    "French": make_lang(
        "YT en MP3", "YT en MP3",
        "Téléchargement MP3 simple et rapide depuis un lien YouTube dans le presse-papiers.",
        "Télécharger MP3 du presse-papiers", "Arrêter", "Dossier de téléchargement", "Choisir", "Ouvrir le dossier",
        "Langue", "Autoriser le téléchargement de playlist", "Copiez un lien YouTube et appuyez sur le bouton.",
        "Préparation du téléchargement...", "Téléchargement...", "Terminé.", "Échec du téléchargement.",
        "Téléchargement arrêté.", "Astuce : copiez le lien YouTube complet avec Ctrl+C avant de cliquer.",
        "Made by Andrej Marovšek", "Le presse-papiers est vide.", "Le presse-papiers ne contient pas de lien YouTube valide.",
        "Veuillez choisir un dossier.", "Fichier manquant :\n{path}", "Fichier manquant :\n{path}",
        "Impossible d'ouvrir le dossier.\n\n{error}", "En cours :", "Playlist :", "Fin approximative :",
        "5 derniers téléchargements réussis", "Aucun téléchargement réussi pour le moment.", "Détection du titre ...",
        "Terminé. Certains éléments ont été ignorés.", "Aucun élément n'a été téléchargé avec succès.",
        "-", "calcul ...",
    ),
    "Italian": make_lang(
        "YT in MP3", "YT in MP3",
        "Download MP3 semplice e veloce da un link YouTube negli appunti.",
        "Scarica MP3 dagli appunti", "Ferma", "Cartella download", "Scegli", "Apri cartella",
        "Lingua", "Consenti download playlist", "Copia un link YouTube e premi il pulsante.",
        "Preparazione download...", "Download in corso...", "Fatto.", "Download non riuscito.",
        "Download interrotto.", "Suggerimento: copia il link YouTube completo con Ctrl+C prima di cliccare.",
        "Made by Andrej Marovšek", "Gli appunti sono vuoti.", "Gli appunti non contengono un link YouTube valido.",
        "Scegli una cartella di download.", "File mancante:\n{path}", "File mancante:\n{path}",
        "Impossibile aprire la cartella.\n\n{error}", "Corrente:", "Playlist:", "Fine indicativa:",
        "Ultimi 5 download riusciti", "Nessun download riuscito finora.", "Rilevamento titolo ...",
        "Fatto. Alcuni elementi sono stati saltati.", "Nessun elemento è stato scaricato con successo.",
        "-", "calcolo ...",
    ),
    "Spanish": make_lang(
        "YT a MP3", "YT a MP3",
        "Descarga MP3 simple y rápida desde un enlace de YouTube en el portapapeles.",
        "Descargar MP3 del portapapeles", "Detener", "Carpeta de descarga", "Elegir", "Abrir carpeta",
        "Idioma", "Permitir descarga de playlist", "Copia un enlace de YouTube y pulsa el botón.",
        "Preparando descarga...", "Descargando...", "Hecho.", "La descarga falló.",
        "Descarga detenida.", "Consejo: copia el enlace completo de YouTube con Ctrl+C antes de pulsar.",
        "Made by Andrej Marovšek", "El portapapeles está vacío.", "El portapapeles no contiene un enlace válido de YouTube.",
        "Elige una carpeta de descarga.", "Falta el archivo:\n{path}", "Falta el archivo:\n{path}",
        "No se pudo abrir la carpeta.\n\n{error}", "Actual:", "Playlist:", "Final aproximado:",
        "Últimas 5 descargas exitosas", "Todavía no hay descargas exitosas.", "Detectando título ...",
        "Hecho. Algunos elementos fueron omitidos.", "Ningún elemento se descargó correctamente.",
        "-", "calculando ...",
    ),
    "Portuguese": make_lang(
        "YT para MP3", "YT para MP3",
        "Download MP3 simples e rápido a partir de um link do YouTube na área de transferência.",
        "Baixar MP3 da área de transferência", "Parar", "Pasta de download", "Escolher", "Abrir pasta",
        "Idioma", "Permitir download de playlist", "Copie um link do YouTube e pressione o botão.",
        "Preparando download...", "Baixando...", "Concluído.", "Falha no download.",
        "Download parado.", "Dica: copie o link completo do YouTube com Ctrl+C antes de clicar.",
        "Made by Andrej Marovšek", "A área de transferência está vazia.", "A área de transferência não contém um link válido do YouTube.",
        "Escolha uma pasta de download.", "Arquivo ausente:\n{path}", "Arquivo ausente:\n{path}",
        "Não foi possível abrir a pasta.\n\n{error}", "Atual:", "Playlist:", "Fim aproximado:",
        "Últimos 5 downloads bem-sucedidos", "Ainda não há downloads bem-sucedidos.", "Detectando título ...",
        "Concluído. Alguns itens foram ignorados.", "Nenhum item foi baixado com sucesso.",
        "-", "calculando ...",
    ),
    "Dutch": make_lang(
        "YT naar MP3", "YT naar MP3",
        "Eenvoudige en snelle MP3-download van een YouTube-link uit het klembord.",
        "Download MP3 uit klembord", "Stop", "Downloadmap", "Kiezen", "Map openen",
        "Taal", "Playlist-download toestaan", "Kopieer een YouTube-link en druk op de knop.",
        "Download voorbereiden...", "Downloaden...", "Klaar.", "Download mislukt.",
        "Download gestopt.", "Tip: kopieer de volledige YouTube-link met Ctrl+C voordat je klikt.",
        "Made by Andrej Marovšek", "Klembord is leeg.", "Het klembord bevat geen geldige YouTube-link.",
        "Kies een downloadmap.", "Bestand ontbreekt:\n{path}", "Bestand ontbreekt:\n{path}",
        "Kon map niet openen.\n\n{error}", "Huidig:", "Playlist:", "Geschatte eindtijd:",
        "Laatste 5 succesvolle downloads", "Nog geen succesvolle downloads.", "Titel detecteren ...",
        "Klaar. Sommige items zijn overgeslagen.", "Geen enkel item is succesvol gedownload.",
        "-", "berekenen ...",
    ),
    "Croatian": make_lang(
        "YT u MP3", "YT u MP3",
        "Jednostavno i brzo preuzimanje MP3 iz YouTube linka u međuspremniku.",
        "Preuzmi MP3 iz međuspremnika", "Zaustavi", "Mapa za preuzimanje", "Odaberi", "Otvori mapu",
        "Jezik", "Dopusti preuzimanje playliste", "Kopiraj YouTube link i pritisni gumb.",
        "Priprema preuzimanja...", "Preuzimanje...", "Gotovo.", "Preuzimanje nije uspjelo.",
        "Preuzimanje zaustavljeno.", "Savjet: kopiraj cijeli YouTube link s Ctrl+C prije klika.",
        "Made by Andrej Marovšek", "Međuspremnik je prazan.", "U međuspremniku nije valjan YouTube link.",
        "Odaberi mapu za preuzimanje.", "Nedostaje datoteka:\n{path}", "Nedostaje datoteka:\n{path}",
        "Mapu nije moguće otvoriti.\n\n{error}", "Trenutno:", "Playlista:", "Približan kraj:",
        "Zadnjih 5 uspješnih preuzimanja", "Još nema uspješnih preuzimanja.", "Prepoznavanje naslova ...",
        "Gotovo. Neki elementi su preskočeni.", "Nijedan element nije uspješno preuzet.",
        "-", "računam ...",
    ),
    "Serbian": make_lang(
        "YT u MP3", "YT u MP3",
        "Jednostavno i brzo preuzimanje MP3 iz YouTube linka u klipbordu.",
        "Preuzmi MP3 iz klipborda", "Zaustavi", "Folder za preuzimanje", "Izaberi", "Otvori folder",
        "Jezik", "Dozvoli preuzimanje playliste", "Kopiraj YouTube link i pritisni dugme.",
        "Priprema preuzimanja...", "Preuzimanje...", "Gotovo.", "Preuzimanje nije uspelo.",
        "Preuzimanje zaustavljeno.", "Savet: kopiraj ceo YouTube link sa Ctrl+C pre klika.",
        "Made by Andrej Marovšek", "Klipbord je prazan.", "U klipbordu nije ispravan YouTube link.",
        "Izaberi folder za preuzimanje.", "Nedostaje fajl:\n{path}", "Nedostaje fajl:\n{path}",
        "Folder nije moguće otvoriti.\n\n{error}", "Trenutno:", "Plejliste:", "Približan kraj:",
        "Poslednjih 5 uspešnih preuzimanja", "Još nema uspešnih preuzimanja.", "Prepoznavanje naslova ...",
        "Gotovo. Neki elementi su preskočeni.", "Nijedan element nije uspešno preuzet.",
        "-", "računam ...",
    ),
    "Bosnian": make_lang(
        "YT u MP3", "YT u MP3",
        "Jednostavno i brzo preuzimanje MP3 iz YouTube linka u međuspremniku.",
        "Preuzmi MP3 iz međuspremnika", "Zaustavi", "Mapa za preuzimanje", "Izaberi", "Otvori mapu",
        "Jezik", "Dozvoli preuzimanje playliste", "Kopiraj YouTube link i pritisni dugme.",
        "Priprema preuzimanja...", "Preuzimanje...", "Gotovo.", "Preuzimanje nije uspjelo.",
        "Preuzimanje zaustavljeno.", "Savjet: kopiraj cijeli YouTube link sa Ctrl+C prije klika.",
        "Made by Andrej Marovšek", "Međuspremnik je prazan.", "U međuspremniku nije ispravan YouTube link.",
        "Izaberi mapu za preuzimanje.", "Nedostaje datoteka:\n{path}", "Nedostaje datoteka:\n{path}",
        "Mapu nije moguće otvoriti.\n\n{error}", "Trenutno:", "Playlista:", "Približan kraj:",
        "Zadnjih 5 uspješnih preuzimanja", "Još nema uspješnih preuzimanja.", "Prepoznavanje naslova ...",
        "Gotovo. Neki elementi su preskočeni.", "Nijedan element nije uspješno preuzet.",
        "-", "računam ...",
    ),
    "Czech": make_lang(
        "YT do MP3", "YT do MP3",
        "Jednoduché a rychlé stahování MP3 z YouTube odkazu ve schránce.",
        "Stáhnout MP3 ze schránky", "Zastavit", "Složka pro stažení", "Vybrat", "Otevřít složku",
        "Jazyk", "Povolit stažení playlistu", "Zkopírujte odkaz z YouTube a stiskněte tlačítko.",
        "Připravuji stažení...", "Stahuji...", "Hotovo.", "Stažení se nezdařilo.",
        "Stažení zastaveno.", "Tip: před kliknutím zkopírujte celý odkaz YouTube pomocí Ctrl+C.",
        "Made by Andrej Marovšek", "Schránka je prázdná.", "Ve schránce není platný odkaz YouTube.",
        "Vyberte složku pro stažení.", "Chybí soubor:\n{path}", "Chybí soubor:\n{path}",
        "Složku se nepodařilo otevřít.\n\n{error}", "Aktuálně:", "Playlist:", "Přibližný konec:",
        "Posledních 5 úspěšných stažení", "Zatím žádné úspěšné stažení.", "Zjišťuji název ...",
        "Hotovo. Některé položky byly přeskočeny.", "Žádná položka nebyla úspěšně stažena.",
        "-", "počítám ...",
    ),
    "Slovak": make_lang(
        "YT do MP3", "YT do MP3",
        "Jednoduché a rýchle sťahovanie MP3 z YouTube odkazu v schránke.",
        "Stiahnuť MP3 zo schránky", "Zastaviť", "Priečinok na stiahnutie", "Vybrať", "Otvoriť priečinok",
        "Jazyk", "Povoliť sťahovanie playlistu", "Skopírujte YouTube odkaz a stlačte tlačidlo.",
        "Pripravujem sťahovanie...", "Sťahujem...", "Hotovo.", "Sťahovanie zlyhalo.",
        "Sťahovanie zastavené.", "Tip: pred kliknutím skopírujte celý YouTube odkaz pomocou Ctrl+C.",
        "Made by Andrej Marovšek", "Schránka je prázdna.", "V schránke nie je platný YouTube odkaz.",
        "Vyberte priečinok na sťahovanie.", "Chýba súbor:\n{path}", "Chýba súbor:\n{path}",
        "Priečinok sa nepodarilo otvoriť.\n\n{error}", "Aktuálne:", "Playlist:", "Približný koniec:",
        "Posledných 5 úspešných stiahnutí", "Zatiaľ žiadne úspešné stiahnutia.", "Zisťujem názov ...",
        "Hotovo. Niektoré položky boli preskočené.", "Žiadna položka nebola úspešne stiahnutá.",
        "-", "počítam ...",
    ),
    "Polish": make_lang(
        "YT do MP3", "YT do MP3",
        "Proste i szybkie pobieranie MP3 z linku YouTube w schowku.",
        "Pobierz MP3 ze schowka", "Stop", "Folder pobierania", "Wybierz", "Otwórz folder",
        "Język", "Zezwól na pobieranie playlisty", "Skopiuj link YouTube i naciśnij przycisk.",
        "Przygotowywanie pobierania...", "Pobieranie...", "Gotowe.", "Pobieranie nie powiodło się.",
        "Pobieranie zatrzymane.", "Wskazówka: przed kliknięciem skopiuj pełny link YouTube przez Ctrl+C.",
        "Made by Andrej Marovšek", "Schowek jest pusty.", "Schowek nie zawiera poprawnego linku YouTube.",
        "Wybierz folder pobierania.", "Brak pliku:\n{path}", "Brak pliku:\n{path}",
        "Nie można otworzyć folderu.\n\n{error}", "Aktualnie:", "Playlista:", "Przybliżony koniec:",
        "Ostatnie 5 udanych pobrań", "Brak udanych pobrań.", "Wykrywanie tytułu ...",
        "Gotowe. Niektóre elementy zostały pominięte.", "Żaden element nie został pobrany poprawnie.",
        "-", "obliczam ...",
    ),
    "Romanian": make_lang(
        "YT în MP3", "YT în MP3",
        "Descărcare MP3 simplă și rapidă dintr-un link YouTube din clipboard.",
        "Descarcă MP3 din clipboard", "Oprește", "Folder descărcare", "Alege", "Deschide folderul",
        "Limbă", "Permite descărcarea playlistului", "Copiază un link YouTube și apasă butonul.",
        "Pregătire descărcare...", "Descărcare...", "Gata.", "Descărcarea a eșuat.",
        "Descărcare oprită.", "Sfat: copiază linkul complet YouTube cu Ctrl+C înainte de click.",
        "Made by Andrej Marovšek", "Clipboard-ul este gol.", "Clipboard-ul nu conține un link YouTube valid.",
        "Alege un folder de descărcare.", "Lipsește fișierul:\n{path}", "Lipsește fișierul:\n{path}",
        "Folderul nu a putut fi deschis.\n\n{error}", "Curent:", "Playlist:", "Final aproximativ:",
        "Ultimele 5 descărcări reușite", "Încă nu există descărcări reușite.", "Detectare titlu ...",
        "Gata. Unele elemente au fost omise.", "Niciun element nu a fost descărcat cu succes.",
        "-", "calculez ...",
    ),
    "Hungarian": make_lang(
        "YT MP3-ba", "YT MP3-ba",
        "Egyszerű és gyors MP3 letöltés a vágólapon lévő YouTube-linkből.",
        "MP3 letöltése vágólapról", "Leállít", "Letöltési mappa", "Választ", "Mappa megnyitása",
        "Nyelv", "Lejátszási lista letöltésének engedélyezése", "Másolj be egy YouTube-linket és nyomd meg a gombot.",
        "Letöltés előkészítése...", "Letöltés...", "Kész.", "A letöltés sikertelen.",
        "Letöltés leállítva.", "Tipp: kattintás előtt másold a teljes YouTube-linket Ctrl+C-vel.",
        "Made by Andrej Marovšek", "A vágólap üres.", "A vágólap nem tartalmaz érvényes YouTube-linket.",
        "Válassz letöltési mappát.", "Hiányzik a fájl:\n{path}", "Hiányzik a fájl:\n{path}",
        "A mappát nem lehetett megnyitni.\n\n{error}", "Jelenlegi:", "Playlist:", "Kb. befejezés:",
        "Utolsó 5 sikeres letöltés", "Még nincsenek sikeres letöltések.", "Cím felismerése ...",
        "Kész. Néhány elem ki lett hagyva.", "Egy elem sem lett sikeresen letöltve.",
        "-", "számolom ...",
    ),
    "Danish": make_lang(
        "YT til MP3", "YT til MP3",
        "Enkel og hurtig MP3-download fra et YouTube-link i udklipsholderen.",
        "Download MP3 fra udklipsholder", "Stop", "Downloadmappe", "Vælg", "Åbn mappe",
        "Sprog", "Tillad playlist-download", "Kopier et YouTube-link og tryk på knappen.",
        "Forbereder download...", "Downloader...", "Færdig.", "Download mislykkedes.",
        "Download stoppet.", "Tip: kopier hele YouTube-linket med Ctrl+C, før du klikker.",
        "Made by Andrej Marovšek", "Udklipsholderen er tom.", "Udklipsholderen indeholder ikke et gyldigt YouTube-link.",
        "Vælg en downloadmappe.", "Manglende fil:\n{path}", "Manglende fil:\n{path}",
        "Kunne ikke åbne mappen.\n\n{error}", "Aktuel:", "Playlist:", "Ca. sluttid:",
        "Seneste 5 vellykkede downloads", "Ingen vellykkede downloads endnu.", "Finder titel ...",
        "Færdig. Nogle elementer blev sprunget over.", "Ingen elementer blev downloadet korrekt.",
        "-", "beregner ...",
    ),
    "Swedish": make_lang(
        "YT till MP3", "YT till MP3",
        "Enkel och snabb MP3-nedladdning från en YouTube-länk i urklipp.",
        "Ladda ner MP3 från urklipp", "Stoppa", "Nedladdningsmapp", "Välj", "Öppna mapp",
        "Språk", "Tillåt nedladdning av spellista", "Kopiera en YouTube-länk och tryck på knappen.",
        "Förbereder nedladdning...", "Laddar ner...", "Klart.", "Nedladdningen misslyckades.",
        "Nedladdning stoppad.", "Tips: kopiera hela YouTube-länken med Ctrl+C innan du klickar.",
        "Made by Andrej Marovšek", "Urklippet är tomt.", "Urklippet innehåller ingen giltig YouTube-länk.",
        "Välj en nedladdningsmapp.", "Filen saknas:\n{path}", "Filen saknas:\n{path}",
        "Kunde inte öppna mappen.\n\n{error}", "Aktuell:", "Spellista:", "Ungefärligt slut:",
        "Senaste 5 lyckade nedladdningar", "Inga lyckade nedladdningar ännu.", "Upptäcker titel ...",
        "Klart. Vissa objekt hoppades över.", "Inget objekt laddades ner korrekt.",
        "-", "beräknar ...",
    ),
    "Norwegian": make_lang(
        "YT til MP3", "YT til MP3",
        "Enkel og rask MP3-nedlasting fra en YouTube-lenke i utklippstavlen.",
        "Last ned MP3 fra utklippstavlen", "Stopp", "Nedlastingsmappe", "Velg", "Åpne mappe",
        "Språk", "Tillat nedlasting av spilleliste", "Kopier en YouTube-lenke og trykk på knappen.",
        "Forbereder nedlasting...", "Laster ned...", "Ferdig.", "Nedlasting mislyktes.",
        "Nedlasting stoppet.", "Tips: kopier hele YouTube-lenken med Ctrl+C før du klikker.",
        "Made by Andrej Marovšek", "Utklippstavlen er tom.", "Utklippstavlen inneholder ikke en gyldig YouTube-lenke.",
        "Velg en nedlastingsmappe.", "Fil mangler:\n{path}", "Fil mangler:\n{path}",
        "Kunne ikke åpne mappen.\n\n{error}", "Gjeldende:", "Spilleliste:", "Omtrentlig slutt:",
        "Siste 5 vellykkede nedlastinger", "Ingen vellykkede nedlastinger ennå.", "Finner tittel ...",
        "Ferdig. Noen elementer ble hoppet over.", "Ingen elementer ble lastet ned.",
        "-", "beregner ...",
    ),
    "Finnish": make_lang(
        "YT MP3:ksi", "YT MP3:ksi",
        "Yksinkertainen ja nopea MP3-lataus leikepöydän YouTube-linkistä.",
        "Lataa MP3 leikepöydältä", "Pysäytä", "Latauskansio", "Valitse", "Avaa kansio",
        "Kieli", "Salli soittolistan lataus", "Kopioi YouTube-linkki ja paina painiketta.",
        "Valmistellaan latausta...", "Ladataan...", "Valmis.", "Lataus epäonnistui.",
        "Lataus pysäytetty.", "Vinkki: kopioi koko YouTube-linkki Ctrl+C:lla ennen klikkausta.",
        "Made by Andrej Marovšek", "Leikepöytä on tyhjä.", "Leikepöydässä ei ole kelvollista YouTube-linkkiä.",
        "Valitse latauskansio.", "Tiedosto puuttuu:\n{path}", "Tiedosto puuttuu:\n{path}",
        "Kansiota ei voitu avata.\n\n{error}", "Nykyinen:", "Soittolista:", "Arvioitu loppu:",
        "Viimeiset 5 onnistunutta latausta", "Ei onnistuneita latauksia vielä.", "Tunnistetaan nimeä ...",
        "Valmis. Osa kohteista ohitettiin.", "Mitään kohdetta ei ladattu onnistuneesti.",
        "-", "lasketaan ...",
    ),
    "Estonian": make_lang(
        "YT MP3-ks", "YT MP3-ks",
        "Lihtne ja kiire MP3 allalaadimine lõikelaual olevast YouTube'i lingist.",
        "Laadi MP3 lõikelaualt", "Peata", "Allalaadimiskaust", "Vali", "Ava kaust",
        "Keel", "Luba esitusloendi allalaadimine", "Kopeeri YouTube'i link ja vajuta nuppu.",
        "Allalaadimise ettevalmistus...", "Laadin alla...", "Valmis.", "Allalaadimine ebaõnnestus.",
        "Allalaadimine peatatud.", "Nipp: kopeeri täielik YouTube'i link Ctrl+C-ga enne klõpsamist.",
        "Made by Andrej Marovšek", "Lõikelaud on tühi.", "Lõikelaual pole sobivat YouTube'i linki.",
        "Vali allalaadimiskaust.", "Fail puudub:\n{path}", "Fail puudub:\n{path}",
        "Kausta ei saanud avada.\n\n{error}", "Praegu:", "Esitusloend:", "Ligikaudne lõpp:",
        "Viimased 5 edukat allalaadimist", "Edukad allalaadimised puuduvad.", "Tuvastan pealkirja ...",
        "Valmis. Osa elemente jäeti vahele.", "Ühtegi elementi ei laaditud edukalt alla.",
        "-", "arvutan ...",
    ),
    "Latvian": make_lang(
        "YT uz MP3", "YT uz MP3",
        "Vienkārša un ātra MP3 lejupielāde no YouTube saites starpliktuvē.",
        "Lejupielādēt MP3 no starpliktuves", "Apturēt", "Lejupielādes mape", "Izvēlēties", "Atvērt mapi",
        "Valoda", "Atļaut playlistes lejupielādi", "Nokopē YouTube saiti un nospied pogu.",
        "Sagatavo lejupielādi...", "Lejupielāde...", "Pabeigts.", "Lejupielāde neizdevās.",
        "Lejupielāde apturēta.", "Padoms: pirms klikšķēšanas nokopē pilnu YouTube saiti ar Ctrl+C.",
        "Made by Andrej Marovšek", "Starpliktuve ir tukša.", "Starpliktuve nesatur derīgu YouTube saiti.",
        "Izvēlieties lejupielādes mapi.", "Trūkst faila:\n{path}", "Trūkst faila:\n{path}",
        "Neizdevās atvērt mapi.\n\n{error}", "Pašlaik:", "Playliste:", "Aptuvenās beigas:",
        "Pēdējās 5 veiksmīgās lejupielādes", "Vēl nav veiksmīgu lejupielāžu.", "Nosaukuma noteikšana ...",
        "Pabeigts. Daži elementi tika izlaisti.", "Neviens elements netika veiksmīgi lejupielādēts.",
        "-", "rēķinu ...",
    ),
    "Lithuanian": make_lang(
        "YT į MP3", "YT į MP3",
        "Paprastas ir greitas MP3 atsisiuntimas iš YouTube nuorodos iškarpinėje.",
        "Atsisiųsti MP3 iš iškarpinės", "Stabdyti", "Atsisiuntimų aplankas", "Pasirinkti", "Atidaryti aplanką",
        "Kalba", "Leisti grojaraščio atsisiuntimą", "Nukopijuokite YouTube nuorodą ir paspauskite mygtuką.",
        "Ruošiamas atsisiuntimas...", "Atsisiunčiama...", "Baigta.", "Atsisiuntimas nepavyko.",
        "Atsisiuntimas sustabdytas.", "Patarimas: prieš spausdami nukopijuokite visą YouTube nuorodą su Ctrl+C.",
        "Made by Andrej Marovšek", "Iškarpinė tuščia.", "Iškarpinėje nėra tinkamos YouTube nuorodos.",
        "Pasirinkite atsisiuntimų aplanką.", "Trūksta failo:\n{path}", "Trūksta failo:\n{path}",
        "Nepavyko atidaryti aplanko.\n\n{error}", "Dabar:", "Grojaraštis:", "Apytikslė pabaiga:",
        "Paskutiniai 5 sėkmingi atsisiuntimai", "Dar nėra sėkmingų atsisiuntimų.", "Nustatomas pavadinimas ...",
        "Baigta. Kai kurie elementai buvo praleisti.", "Ne vienas elementas nebuvo sėkmingai atsisiųstas.",
        "-", "skaičiuoju ...",
    ),
    "Greek": make_lang(
        "YT σε MP3", "YT σε MP3",
        "Απλή και γρήγορη λήψη MP3 από σύνδεσμο YouTube στο πρόχειρο.",
        "Λήψη MP3 από πρόχειρο", "Στοπ", "Φάκελος λήψης", "Επιλογή", "Άνοιγμα φακέλου",
        "Γλώσσα", "Να επιτρέπεται λήψη playlist", "Αντέγραψε έναν σύνδεσμο YouTube και πάτησε το κουμπί.",
        "Προετοιμασία λήψης...", "Λήψη...", "Έτοιμο.", "Η λήψη απέτυχε.",
        "Η λήψη σταμάτησε.", "Συμβουλή: αντέγραψε ολόκληρο το link YouTube με Ctrl+C πριν πατήσεις.",
        "Made by Andrej Marovšek", "Το πρόχειρο είναι άδειο.", "Το πρόχειρο δεν έχει έγκυρο link YouTube.",
        "Διάλεξε φάκελο λήψης.", "Λείπει το αρχείο:\n{path}", "Λείπει το αρχείο:\n{path}",
        "Δεν ήταν δυνατό να ανοίξει ο φάκελος.\n\n{error}", "Τρέχον:", "Playlist:", "Περίπου τέλος:",
        "Τα τελευταία 5 επιτυχημένα downloads", "Δεν υπάρχουν ακόμη επιτυχημένα downloads.", "Αναγνώριση τίτλου ...",
        "Ολοκληρώθηκε. Κάποια στοιχεία παραλείφθηκαν.", "Κανένα στοιχείο δεν κατέβηκε επιτυχώς.",
        "-", "υπολογίζω ...",
    ),
    "Bulgarian": make_lang(
        "YT в MP3", "YT в MP3",
        "Лесно и бързо сваляне на MP3 от YouTube връзка в клипборда.",
        "Свали MP3 от клипборда", "Спри", "Папка за сваляне", "Избери", "Отвори папка",
        "Език", "Разреши сваляне на playlist", "Копирай YouTube връзка и натисни бутона.",
        "Подготвям сваляне...", "Сваляне...", "Готово.", "Свалянето е неуспешно.",
        "Свалянето е спряно.", "Съвет: копирай пълната YouTube връзка с Ctrl+C преди клик.",
        "Made by Andrej Marovšek", "Клипбордът е празен.", "В клипборда няма валидна YouTube връзка.",
        "Избери папка за сваляне.", "Липсва файл:\n{path}", "Липсва файл:\n{path}",
        "Папката не може да се отвори.\n\n{error}", "Текущо:", "Playlist:", "Приблизителен край:",
        "Последните 5 успешни сваляния", "Все още няма успешни сваляния.", "Разпознавам заглавие ...",
        "Готово. Някои елементи бяха пропуснати.", "Нито един елемент не е свален успешно.",
        "-", "изчислявам ...",
    ),
    "Ukrainian": make_lang(
        "YT у MP3", "YT у MP3",
        "Просте і швидке завантаження MP3 з YouTube посилання в буфері обміну.",
        "Завантажити MP3 з буфера", "Зупинити", "Тека завантаження", "Обрати", "Відкрити теку",
        "Мова", "Дозволити завантаження плейлиста", "Скопіюйте посилання YouTube і натисніть кнопку.",
        "Підготовка завантаження...", "Завантаження...", "Готово.", "Завантаження не вдалося.",
        "Завантаження зупинено.", "Порада: скопіюйте повне посилання YouTube за допомогою Ctrl+C перед натисканням.",
        "Made by Andrej Marovšek", "Буфер обміну порожній.", "У буфері обміну немає дійсного посилання YouTube.",
        "Оберіть теку завантаження.", "Відсутній файл:\n{path}", "Відсутній файл:\n{path}",
        "Не вдалося відкрити теку.\n\n{error}", "Поточний:", "Плейлист:", "Приблизний кінець:",
        "Останні 5 успішних завантажень", "Ще немає успішних завантажень.", "Визначення назви ...",
        "Готово. Деякі елементи були пропущені.", "Жоден елемент не було успішно завантажено.",
        "-", "обчислюю ...",
    ),
    "Turkish": make_lang(
        "YT'den MP3", "YT'den MP3",
        "Panodaki YouTube bağlantısından basit ve hızlı MP3 indirme.",
        "Panodan MP3 indir", "Durdur", "İndirme klasörü", "Seç", "Klasörü aç",
        "Dil", "Oynatma listesi indirmeye izin ver", "Bir YouTube bağlantısı kopyalayın ve düğmeye basın.",
        "İndirme hazırlanıyor...", "İndiriliyor...", "Tamamlandı.", "İndirme başarısız oldu.",
        "İndirme durduruldu.", "İpucu: tıklamadan önce tam YouTube bağlantısını Ctrl+C ile kopyalayın.",
        "Made by Andrej Marovšek", "Pano boş.", "Panoda geçerli bir YouTube bağlantısı yok.",
        "Lütfen indirme klasörü seçin.", "Dosya eksik:\n{path}", "Dosya eksik:\n{path}",
        "Klasör açılamadı.\n\n{error}", "Güncel:", "Oynatma listesi:", "Yaklaşık bitiş:",
        "Son 5 başarılı indirme", "Henüz başarılı indirme yok.", "Başlık algılanıyor ...",
        "Tamamlandı. Bazı öğeler atlandı.", "Hiçbir öğe başarılı şekilde indirilmedi.",
        "-", "hesaplanıyor ...",
    ),
    "Albanian": make_lang(
        "YT në MP3", "YT në MP3",
        "Shkarkim MP3 i thjeshtë dhe i shpejtë nga linku YouTube në clipboard.",
        "Shkarko MP3 nga clipboard", "Ndalo", "Dosja e shkarkimit", "Zgjidh", "Hap dosjen",
        "Gjuha", "Lejo shkarkimin e playlistes", "Kopjo një link YouTube dhe shtyp butonin.",
        "Po përgatitet shkarkimi...", "Po shkarkohet...", "U krye.", "Shkarkimi dështoi.",
        "Shkarkimi u ndal.", "Këshillë: kopjo linkun e plotë YouTube me Ctrl+C para klikimit.",
        "Made by Andrej Marovšek", "Clipboard është bosh.", "Clipboard nuk përmban një link të vlefshëm YouTube.",
        "Zgjidh dosjen e shkarkimit.", "Mungon skedari:\n{path}", "Mungon skedari:\n{path}",
        "Dosja nuk mund të hapej.\n\n{error}", "Aktualisht:", "Playlist:", "Fund i përafërt:",
        "5 shkarkimet e fundit të suksesshme", "Ende nuk ka shkarkime të suksesshme.", "Po zbulohet titulli ...",
        "U krye. Disa elemente u kaluan.", "Asnjë element nuk u shkarkua me sukses.",
        "-", "po llogaris ...",
    ),
    "Macedonian": make_lang(
        "YT во MP3", "YT во MP3",
        "Едноставно и брзо симнување MP3 од YouTube линк во clipboard.",
        "Симни MP3 од clipboard", "Стоп", "Фолдер за симнување", "Избери", "Отвори фолдер",
        "Јазик", "Дозволи симнување на плејлиста", "Копирај YouTube линк и притисни го копчето.",
        "Се подготвува симнување...", "Се симнува...", "Готово.", "Симнувањето не успеа.",
        "Симнувањето е стопирано.", "Совет: копирај го целиот YouTube линк со Ctrl+C пред клик.",
        "Made by Andrej Marovšek", "Clipboard е празен.", "Во clipboard нема валиден YouTube линк.",
        "Избери фолдер за симнување.", "Недостасува датотека:\n{path}", "Недостасува датотека:\n{path}",
        "Фолдерот не може да се отвори.\n\n{error}", "Тековно:", "Плејлиста:", "Приближен крај:",
        "Последни 5 успешни симнувања", "Сè уште нема успешни симнувања.", "Препознавање наслов ...",
        "Готово. Некои ставки беа прескокнати.", "Ниту една ставка не беше успешно симната.",
        "-", "пресметувам ...",
    ),
    "Icelandic": make_lang(
        "YT í MP3", "YT í MP3",
        "Einfalt og hratt MP3 niðurhal úr YouTube-linki á klemmuspjaldi.",
        "Hlaða niður MP3 af klemmuspjaldi", "Stoppa", "Niðurhalsmappa", "Velja", "Opna möppu",
        "Tungumál", "Leyfa niðurhal á spilunarlista", "Afritaðu YouTube-link og ýttu á hnappinn.",
        "Undirbý niðurhal...", "Hleð niður...", "Lokið.", "Niðurhal mistókst.",
        "Niðurhal stoppað.", "Ábending: afritaðu allan YouTube-linkinn með Ctrl+C áður en þú smellir.",
        "Made by Andrej Marovšek", "Klemmuspjald er tómt.", "Klemmuspjald inniheldur ekki gilt YouTube-link.",
        "Veldu niðurhalsmöppu.", "Skrá vantar:\n{path}", "Skrá vantar:\n{path}",
        "Ekki var hægt að opna möppuna.\n\n{error}", "Núverandi:", "Spilunarlisti:", "Áætluð lok:",
        "Síðustu 5 heppnuðu niðurhöl", "Engin heppnuð niðurhöl enn.", "Finn titil ...",
        "Lokið. Nokkrum atriðum var sleppt.", "Engu atriði var hlaðið niður með árangri.",
        "-", "reikna ...",
    ),
    "Irish": make_lang(
        "YT go MP3", "YT go MP3",
        "Íoslódáil MP3 simplí agus tapa ó nasc YouTube sa ghearrthaisce.",
        "Íoslódáil MP3 ón ghearrthaisce", "Stop", "Fillteán íoslódála", "Roghnaigh", "Oscail fillteán",
        "Teanga", "Ceadaigh íoslódáil playlist", "Déan nasc YouTube a chóipeáil agus brúigh an cnaipe.",
        "Ag ullmhú íoslódála...", "Ag íoslódáil...", "Críochnaithe.", "Theip ar an íoslódáil.",
        "Stopadh an íoslódáil.", "Leid: cóipeáil an nasc iomlán YouTube le Ctrl+C roimh chliceáil.",
        "Made by Andrej Marovšek", "Tá an ghearrthaisce folamh.", "Níl nasc bailí YouTube sa ghearrthaisce.",
        "Roghnaigh fillteán íoslódála.", "Comhad ar iarraidh:\n{path}", "Comhad ar iarraidh:\n{path}",
        "Níorbh fhéidir an fillteán a oscailt.\n\n{error}", "Reatha:", "Playlist:", "Críoch thart ar:",
        "Na 5 íoslódáil rathúla is déanaí", "Níl aon íoslódáil rathúil ann go fóill.", "Teideal á aithint ...",
        "Críochnaithe. Scipeáladh roinnt nithe.", "Ní íoslódáladh aon mhír go rathúil.",
        "-", "ag ríomh ...",
    ),
    "Maltese": make_lang(
        "YT għal MP3", "YT għal MP3",
        "Niżżil MP3 sempliċi u veloċi minn link ta' YouTube fil-clipboard.",
        "Niżżel MP3 mill-clipboard", "Waqqaf", "Folder tat-tniżżil", "Agħżel", "Iftaħ folder",
        "Lingwa", "Ippermetti tniżżil ta' playlist", "Ikkopja link ta' YouTube u agħfas il-buttuna.",
        "Qed nipprepara t-tniżżil...", "Qed inniżżel...", "Lest.", "It-tniżżil falla.",
        "It-tniżżil twaqqaf.", "Parir: ikkopja l-link kollu ta' YouTube b'Ctrl+C qabel tikklikkja.",
        "Made by Andrej Marovšek", "Il-clipboard huwa vojt.", "Il-clipboard ma fihx link validu ta' YouTube.",
        "Agħżel folder tat-tniżżil.", "File nieqes:\n{path}", "File nieqes:\n{path}",
        "Ma setax jinfetaħ il-folder.\n\n{error}", "Kurrenti:", "Playlist:", "Tmiem approssimattiv:",
        "L-aħħar 5 tniżżiliet b'suċċess", "Għad m'hemmx tniżżiliet b'suċċess.", "Qed niskopri t-titlu ...",
        "Lest. Xi elementi ġew maqbuża.", "L-ebda element ma tniżżel b'suċċess.",
        "-", "qed nikkalkula ...",
    ),
}


def resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def transliterate_text(text: str) -> str:
    if not text:
        return ""

    manual_map = {
        "Š": "S", "š": "s",
        "Ž": "Z", "ž": "z",
        "Č": "C", "č": "c",
        "Ć": "C", "ć": "c",
        "Đ": "D", "đ": "d",
        "Å": "A", "å": "a",
        "Ä": "A", "ä": "a",
        "Ö": "O", "ö": "o",
        "Ü": "U", "ü": "u",
        "ẞ": "SS", "ß": "ss",
        "Æ": "AE", "æ": "ae",
        "Ø": "O", "ø": "o",
        "Ł": "L", "ł": "l",
        "Ń": "N", "ń": "n",
        "Ś": "S", "ś": "s",
        "Ź": "Z", "ź": "z",
        "Ż": "Z", "ż": "z",
        "Ň": "N", "ň": "n",
        "Ř": "R", "ř": "r",
        "Ť": "T", "ť": "t",
        "Ď": "D", "ď": "d",
        "Ľ": "L", "ľ": "l",
        "Ĺ": "L", "ĺ": "l",
        "Ŕ": "R", "ŕ": "r",
        "Ě": "E", "ě": "e",
        "Ů": "U", "ů": "u",
        "Ý": "Y", "ý": "y",
        "Á": "A", "á": "a",
        "É": "E", "é": "e",
        "Í": "I", "í": "i",
        "Ó": "O", "ó": "o",
        "Ú": "U", "ú": "u",
        "Â": "A", "â": "a",
        "Ê": "E", "ê": "e",
        "Î": "I", "î": "i",
        "Ô": "O", "ô": "o",
        "Û": "U", "û": "u",
        "À": "A", "à": "a",
        "È": "E", "è": "e",
        "Ì": "I", "ì": "i",
        "Ò": "O", "ò": "o",
        "Ù": "U", "ù": "u",
        "Ã": "A", "ã": "a",
        "Õ": "O", "õ": "o",
        "Ç": "C", "ç": "c",
    }

    for old, new in manual_map.items():
        text = text.replace(old, new)

    normalized = unicodedata.normalize("NFKD", text)
    cleaned = []
    for ch in normalized:
        if unicodedata.category(ch) == "Mn":
            continue
        cleaned.append(ch)

    text = "".join(cleaned)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg):
        super().__init__(parent, bg=bg)

        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg)

        self.inner.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _bind_mousewheel(self):
        def _on_mousewheel(event):
            if sys.platform.startswith("win"):
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif sys.platform == "darwin":
                self.canvas.yview_scroll(int(-1 * event.delta), "units")
            else:
                if event.num == 4:
                    self.canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    self.canvas.yview_scroll(1, "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas.bind_all("<Button-4>", _on_mousewheel)
        self.canvas.bind_all("<Button-5>", _on_mousewheel)


class YTToMP3App:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.current_language = "Slovenian"
        self.texts = LANGUAGES[self.current_language]

        self.download_folder = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.language_var = tk.StringVar(value=self.current_language)
        self.allow_playlist_var = tk.BooleanVar(value=False)

        self.status_text = tk.StringVar()
        self.current_title_text = tk.StringVar()
        self.playlist_counter_text = tk.StringVar()
        self.eta_text = tk.StringVar()
        self.progress_var = tk.DoubleVar(value=0.0)

        self.is_downloading = False
        self.stop_requested = False
        self.current_process = None
        self.ui_queue = queue.Queue()

        self.last_successful_titles = deque(maxlen=5)

        self.total_items = None
        self.current_index = None
        self.success_count = 0
        self.fail_count = 0
        self.download_started_at = None

        self.load_settings()
        self.texts = LANGUAGES[self.current_language]

        self.root.title(self.texts["window_title"])
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.root.configure(bg="#eef2f7")

        self.build_ui()
        self.apply_language()
        self.root.after(100, self.process_ui_queue)

    def save_settings(self):
        data = {
            "language": self.current_language,
            "download_folder": self.download_folder.get(),
            "allow_playlist": self.allow_playlist_var.get(),
            "last_successful_titles": list(self.last_successful_titles),
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_settings(self):
        if not os.path.exists(CONFIG_FILE):
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            lang = data.get("language")
            if lang in LANGUAGES:
                self.current_language = lang
                self.language_var.set(lang)

            folder = data.get("download_folder")
            if folder:
                self.download_folder.set(folder)

            self.allow_playlist_var.set(bool(data.get("allow_playlist", False)))

            saved_titles = data.get("last_successful_titles", [])
            for title in saved_titles[-5:]:
                self.last_successful_titles.append(transliterate_text(title))
        except Exception:
            pass

    def build_ui(self):
        self.scrollable = ScrollableFrame(self.root, bg="#eef2f7")
        self.scrollable.pack(fill="both", expand=True)

        outer = self.scrollable.inner

        card = tk.Frame(
            outer,
            bg="#ffffff",
            bd=0,
            highlightthickness=0,
            padx=16,
            pady=16,
        )
        card.pack(padx=14, pady=14)

        content = tk.Frame(card, bg="#ffffff")
        content.pack()

        top_row = tk.Frame(content, bg="#ffffff", width=CONTENT_MAX_WIDTH)
        top_row.pack(fill="x", pady=(0, 8))

        self.language_label = tk.Label(
            top_row,
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 8, "bold"),
        )
        self.language_label.pack(side="left")

        self.language_combo = tk.OptionMenu(
            top_row,
            self.language_var,
            *sorted(LANGUAGES.keys()),
            command=lambda _=None: self.on_language_change()
        )
        self.language_combo.config(
            font=("Segoe UI", 8),
            bg="#f8fafc",
            fg="#111827",
            activebackground="#e5e7eb",
            activeforeground="#111827",
            relief="solid",
            bd=1,
            highlightthickness=0,
            width=14,
        )
        self.language_combo["menu"].config(font=("Segoe UI", 8))
        self.language_combo.pack(side="right")

        self.title_label = tk.Label(
            content,
            bg="#ffffff",
            fg="#0f172a",
            font=("Segoe UI", 18, "bold"),
        )
        self.title_label.pack(pady=(2, 4))

        self.subtitle_label = tk.Label(
            content,
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 8),
            wraplength=CONTENT_MAX_WIDTH,
            justify="center",
        )
        self.subtitle_label.pack(pady=(0, 10))

        current_box = tk.Frame(content, bg="#f8fafc", bd=1, relief="solid", width=CONTENT_MAX_WIDTH)
        current_box.pack(fill="x", pady=(0, 8))

        self.current_item_caption = tk.Label(
            current_box,
            bg="#f8fafc",
            fg="#475569",
            font=("Segoe UI", 8, "bold"),
            anchor="w",
            padx=8,
            pady=6,
        )
        self.current_item_caption.pack(fill="x")

        self.current_item_value = tk.Label(
            current_box,
            textvariable=self.current_title_text,
            bg="#f8fafc",
            fg="#0f172a",
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            justify="left",
            wraplength=CONTENT_MAX_WIDTH - 20,
            padx=8,
            pady=0,
        )
        self.current_item_value.pack(fill="x", pady=(0, 8))

        info_row = tk.Frame(content, bg="#ffffff", width=CONTENT_MAX_WIDTH)
        info_row.pack(fill="x", pady=(0, 8))

        left_info = tk.Frame(info_row, bg="#ffffff")
        left_info.pack(side="left", anchor="w")

        right_info = tk.Frame(info_row, bg="#ffffff")
        right_info.pack(side="right", anchor="e")

        self.playlist_progress_caption = tk.Label(
            left_info,
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 8, "bold"),
        )
        self.playlist_progress_caption.pack(side="left")

        self.playlist_progress_value = tk.Label(
            left_info,
            textvariable=self.playlist_counter_text,
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 8),
        )
        self.playlist_progress_value.pack(side="left", padx=(5, 0))

        self.eta_caption = tk.Label(
            right_info,
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 8, "bold"),
        )
        self.eta_caption.pack(side="left")

        self.eta_value = tk.Label(
            right_info,
            textvariable=self.eta_text,
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 8),
        )
        self.eta_value.pack(side="left", padx=(5, 0))

        self.download_button = tk.Button(
            content,
            text="",
            command=self.on_download_click,
            bg="#ef4444",
            fg="white",
            activebackground="#dc2626",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=12,
            pady=10,
            width=1,
        )
        self.download_button.pack(fill="x", pady=(0, 8))

        self.stop_button = tk.Button(
            content,
            text="",
            command=self.stop_download,
            bg="#e5e7eb",
            fg="#6b7280",
            activebackground="#d1d5db",
            activeforeground="#374151",
            relief="flat",
            bd=0,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2",
            padx=10,
            pady=7,
            state="disabled",
        )
        self.stop_button.pack(pady=(0, 8))

        self.playlist_check = tk.Checkbutton(
            content,
            text="",
            variable=self.allow_playlist_var,
            bg="#ffffff",
            fg="#111827",
            activebackground="#ffffff",
            activeforeground="#111827",
            font=("Segoe UI", 8),
            selectcolor="#ffffff",
            bd=0,
            highlightthickness=0,
        )
        self.playlist_check.pack(pady=(0, 8))

        self.status_label = tk.Label(
            content,
            textvariable=self.status_text,
            bg="#ffffff",
            fg="#2563eb",
            font=("Segoe UI", 8, "bold"),
            justify="center",
        )
        self.status_label.pack(pady=(0, 6))

        progress_outer = tk.Frame(content, bg="#e5e7eb", height=10, width=CONTENT_MAX_WIDTH)
        progress_outer.pack(fill="x", pady=(0, 4))
        progress_outer.pack_propagate(False)

        self.progress_fill = tk.Frame(progress_outer, bg="#2563eb", width=0)
        self.progress_fill.place(x=0, y=0, relheight=1)

        self.progress_percent_label = tk.Label(
            content,
            text="0%",
            bg="#ffffff",
            fg="#475569",
            font=("Segoe UI", 8),
        )
        self.progress_percent_label.pack(pady=(0, 10))

        self.folder_title_label = tk.Label(
            content,
            bg="#ffffff",
            fg="#111827",
            font=("Segoe UI", 8, "bold"),
            anchor="w",
        )
        self.folder_title_label.pack(fill="x", pady=(0, 4))

        folder_row = tk.Frame(content, bg="#ffffff", width=CONTENT_MAX_WIDTH)
        folder_row.pack(fill="x", pady=(0, 8))

        self.folder_entry = tk.Entry(
            folder_row,
            textvariable=self.download_folder,
            font=("Segoe UI", 8),
            relief="solid",
            bd=1,
            bg="#f8fafc",
            fg="#111827",
            insertbackground="#111827",
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, ipady=5)

        self.browse_button = tk.Button(
            folder_row,
            text="",
            command=self.choose_folder,
            bg="#f1f5f9",
            fg="#111827",
            activebackground="#e2e8f0",
            activeforeground="#111827",
            relief="flat",
            bd=0,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2",
            padx=9,
            pady=7,
        )
        self.browse_button.pack(side="left", padx=(6, 0))

        self.open_button = tk.Button(
            content,
            text="",
            command=self.open_folder,
            bg="#f1f5f9",
            fg="#111827",
            activebackground="#e2e8f0",
            activeforeground="#111827",
            relief="flat",
            bd=0,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2",
            padx=10,
            pady=7,
        )
        self.open_button.pack(anchor="w", pady=(0, 10))

        log_box = tk.Frame(content, bg="#f8fafc", bd=1, relief="solid", width=CONTENT_MAX_WIDTH)
        log_box.pack(fill="x", pady=(0, 10))

        self.log_title_label = tk.Label(
            log_box,
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 8, "bold"),
            anchor="w",
            padx=8,
            pady=6,
        )
        self.log_title_label.pack(fill="x")

        self.log_labels = []
        for _ in range(5):
            lbl = tk.Label(
                log_box,
                bg="#f8fafc",
                fg="#475569",
                font=("Segoe UI", 8),
                anchor="w",
                justify="left",
                wraplength=CONTENT_MAX_WIDTH - 20,
                padx=8,
                pady=2,
            )
            lbl.pack(fill="x")
            self.log_labels.append(lbl)

        self.tip_label = tk.Label(
            content,
            bg="#ffffff",
            fg="#64748b",
            font=("Segoe UI", 7),
            wraplength=CONTENT_MAX_WIDTH,
            justify="center",
        )
        self.tip_label.pack(pady=(0, 8))

        self.credit_label = tk.Label(
            content,
            bg="#ffffff",
            fg="#2563eb",
            font=("Segoe UI", 7),
            cursor="hand2",
        )
        self.credit_label.pack()
        self.credit_label.bind("<Button-1>", lambda e: webbrowser.open(LINKEDIN_URL))

        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, _event=None):
        self.update_progress_bar()

    def update_progress_bar(self):
        self.root.update_idletasks()
        percent = max(0.0, min(100.0, self.progress_var.get()))
        parent = self.progress_fill.master
        total_width = max(parent.winfo_width(), 1)
        fill_width = int(total_width * (percent / 100.0))
        self.progress_fill.place(x=0, y=0, width=fill_width, relheight=1)

    def on_language_change(self):
        self.current_language = self.language_var.get()
        self.texts = LANGUAGES[self.current_language]
        self.apply_language()
        self.save_settings()

    def apply_language(self):
        self.root.title(self.texts["window_title"])
        self.title_label.config(text=self.texts["title"])
        self.subtitle_label.config(text=self.texts["subtitle"])
        self.language_label.config(text=self.texts["language_label"])
        self.download_button.config(text=self.texts["download_button"])
        self.stop_button.config(text=self.texts["stop_button"])
        self.playlist_check.config(text=self.texts["playlist_label"])
        self.folder_title_label.config(text=self.texts["folder_label"])
        self.browse_button.config(text=self.texts["browse_button"])
        self.open_button.config(text=self.texts["open_button"])
        self.tip_label.config(text=self.texts["tip"])
        self.credit_label.config(text=self.texts["credit"])
        self.current_item_caption.config(text=self.texts["current_item_label"])
        self.playlist_progress_caption.config(text=self.texts["playlist_progress_label"])
        self.eta_caption.config(text=self.texts["eta_label"])
        self.log_title_label.config(text=self.texts["last_downloads_label"])

        if not self.current_title_text.get():
            self.current_title_text.set(self.texts["unknown_item"])

        if not self.playlist_counter_text.get():
            self.playlist_counter_text.set("-")

        if not self.eta_text.get():
            self.eta_text.set(self.texts["eta_waiting"])

        if not self.is_downloading:
            if self.progress_var.get() >= 100:
                self.status_text.set(self.texts["status_done"])
            else:
                self.status_text.set(self.texts["status_ready"])

        self.refresh_log_view()
        self.update_progress_bar()

    def refresh_log_view(self):
        titles = list(self.last_successful_titles)[::-1]

        for i, lbl in enumerate(self.log_labels):
            if i < len(titles):
                lbl.config(text=f"• {titles[i]}", fg="#334155")
            elif i == 0:
                lbl.config(text=self.texts["nothing_yet"], fg="#94a3b8")
            else:
                lbl.config(text="", fg="#94a3b8")

    def choose_folder(self):
        selected = filedialog.askdirectory(
            title=self.texts["folder_label"],
            initialdir=self.download_folder.get() or str(Path.home()),
        )
        if selected:
            self.download_folder.set(selected)
            self.save_settings()

    def open_folder(self):
        folder = self.download_folder.get().strip()
        if not folder:
            messagebox.showwarning(APP_TITLE, self.texts["warn_no_folder"])
            return

        os.makedirs(folder, exist_ok=True)

        try:
            if sys.platform.startswith("win"):
                os.startfile(folder)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            else:
                subprocess.Popen(["xdg-open", folder])
        except Exception as exc:
            messagebox.showerror(APP_TITLE, self.texts["err_open_folder"].format(error=exc))

    def reset_download_state(self):
        self.total_items = None
        self.current_index = None
        self.success_count = 0
        self.fail_count = 0
        self.download_started_at = None
        self.progress_var.set(0)
        self.progress_percent_label.config(text="0%")
        self.current_title_text.set(self.texts["unknown_item"])
        self.playlist_counter_text.set("-")
        self.eta_text.set(self.texts["eta_waiting"])
        self.update_progress_bar()

    def on_download_click(self):
        if self.is_downloading:
            return

        try:
            clipboard_text = self.root.clipboard_get().strip()
        except tk.TclError:
            messagebox.showwarning(APP_TITLE, self.texts["warn_clipboard_empty"])
            return

        if not clipboard_text:
            messagebox.showwarning(APP_TITLE, self.texts["warn_clipboard_empty"])
            return

        if "youtube.com/" not in clipboard_text and "youtu.be/" not in clipboard_text:
            messagebox.showwarning(APP_TITLE, self.texts["warn_invalid_url"])
            return

        output_folder = self.download_folder.get().strip()
        if not output_folder:
            messagebox.showwarning(APP_TITLE, self.texts["warn_no_folder"])
            return

        os.makedirs(output_folder, exist_ok=True)

        yt_dlp_path = resource_path(os.path.join("bin", "yt-dlp.exe"))
        ffmpeg_path = resource_path(os.path.join("bin", "ffmpeg.exe"))

        if not os.path.exists(yt_dlp_path):
            messagebox.showerror(APP_TITLE, self.texts["err_missing_ytdlp"].format(path=yt_dlp_path))
            return

        if not os.path.exists(ffmpeg_path):
            messagebox.showerror(APP_TITLE, self.texts["err_missing_ffmpeg"].format(path=ffmpeg_path))
            return

        command = [
            yt_dlp_path,
            "--newline",
            "--progress",
            "--ignore-errors",
            "--no-abort-on-error",
            "--extract-audio",
            "--audio-format", "mp3",
            "--ffmpeg-location", os.path.dirname(ffmpeg_path),
            "-o", os.path.join(output_folder, "%(title)s.%(ext)s"),
            "--print", "after_move:SUCCESS_TITLE=%(title)s",
            "--print", "before_dl:NOW_TITLE=%(title)s",
            "--print", "before_dl:PLAYLIST_POS=%(playlist_index|1)s",
            "--print", "before_dl:PLAYLIST_TOTAL=%(n_entries|1)s",
        ]

        if self.allow_playlist_var.get():
            command.append("--yes-playlist")
        else:
            command.append("--no-playlist")

        command.append(clipboard_text)
        self.start_download(command)

    def start_download(self, command):
        self.is_downloading = True
        self.stop_requested = False
        self.reset_download_state()
        self.download_started_at = time.time()

        self.status_text.set(self.texts["status_preparing"])
        self.download_button.config(state="disabled", bg="#fca5a5", activebackground="#fca5a5")
        self.stop_button.config(state="normal", bg="#e5e7eb", fg="#111827")

        thread = threading.Thread(target=self.run_download, args=(command,), daemon=True)
        thread.start()

    def stop_download(self):
        if not self.is_downloading:
            return

        self.stop_requested = True
        self.status_text.set(self.texts["status_stopped"])

        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
            except Exception:
                pass

    def format_eta(self):
        if not self.download_started_at or self.current_index is None or self.total_items is None:
            return self.texts["eta_waiting"]

        try:
            current = int(self.current_index)
            total = int(self.total_items)
        except (TypeError, ValueError):
            return self.texts["eta_waiting"]

        processed = max(current - 1, 0)
        remaining = max(total - processed, 0)

        if processed < 1:
            return self.texts["eta_calculating"]

        elapsed = time.time() - self.download_started_at
        if elapsed <= 0:
            return self.texts["eta_calculating"]

        avg_per_item = elapsed / processed
        remaining_seconds = int(avg_per_item * remaining)

        finish_ts = time.time() + remaining_seconds
        return time.strftime("%H:%M", time.localtime(finish_ts))

    def refresh_eta(self):
        self.eta_text.set(self.format_eta())

    def process_ui_queue(self):
        while not self.ui_queue.empty():
            action, value = self.ui_queue.get_nowait()

            if action == "progress":
                try:
                    number = float(value)
                except ValueError:
                    number = 0.0

                clamped = max(0.0, min(100.0, number))
                self.progress_var.set(clamped)
                self.progress_percent_label.config(text=f"{int(clamped)}%")
                self.update_progress_bar()

                if self.is_downloading:
                    self.status_text.set(f'{self.texts["status_downloading"]} {int(clamped)}%')

            elif action == "current_title":
                self.current_title_text.set(transliterate_text(value))
                self.refresh_eta()

            elif action == "playlist_pos":
                self.current_index = value
                self.refresh_playlist_counter()
                self.refresh_eta()

            elif action == "playlist_total":
                self.total_items = value
                self.refresh_playlist_counter()
                self.refresh_eta()

            elif action == "success_title":
                self.success_count += 1
                clean_title = transliterate_text(value)
                self.last_successful_titles.append(clean_title)
                self.refresh_log_view()
                self.save_settings()
                self.refresh_eta()

            elif action == "fail_count":
                self.fail_count += 1
                self.refresh_eta()

            elif action == "status":
                self.status_text.set(value)

            elif action == "done":
                self.finish_success()

            elif action == "error":
                self.finish_error(value)

            elif action == "stopped":
                self.finish_stopped()

        self.root.after(100, self.process_ui_queue)

    def refresh_playlist_counter(self):
        if self.current_index is not None and self.total_items is not None:
            self.playlist_counter_text.set(f"{self.current_index} / {self.total_items}")
        elif self.current_index is not None:
            self.playlist_counter_text.set(f"{self.current_index} / ?")
        elif self.total_items is not None:
            self.playlist_counter_text.set(f"? / {self.total_items}")
        else:
            self.playlist_counter_text.set("-")

    def parse_progress(self, line):
        match = re.search(r"\[download\]\s+(\d+(?:\.\d+)?)%", line)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

    def run_download(self, command):
        try:
            creationflags = 0
            if sys.platform.startswith("win"):
                creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

            self.current_process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=creationflags,
            )

            output_lines = []

            if self.current_process.stdout is not None:
                for raw_line in self.current_process.stdout:
                    line = raw_line.strip()
                    if not line:
                        continue

                    output_lines.append(line)

                    if self.stop_requested:
                        break

                    if line.startswith("NOW_TITLE="):
                        title = line.replace("NOW_TITLE=", "", 1).strip()
                        if title:
                            self.ui_queue.put(("current_title", title))
                        continue

                    if line.startswith("PLAYLIST_POS="):
                        pos = line.replace("PLAYLIST_POS=", "", 1).strip()
                        if pos.isdigit():
                            self.ui_queue.put(("playlist_pos", pos))
                        continue

                    if line.startswith("PLAYLIST_TOTAL="):
                        total = line.replace("PLAYLIST_TOTAL=", "", 1).strip()
                        if total.isdigit():
                            self.ui_queue.put(("playlist_total", total))
                        continue

                    if line.startswith("SUCCESS_TITLE="):
                        title = line.replace("SUCCESS_TITLE=", "", 1).strip()
                        if title:
                            self.ui_queue.put(("success_title", title))
                        continue

                    progress_value = self.parse_progress(line)
                    if progress_value is not None:
                        self.ui_queue.put(("progress", str(progress_value)))
                        continue

                    lowered = line.lower()
                    if "error" in lowered and "unsupported url" not in lowered:
                        self.ui_queue.put(("fail_count", "1"))
                        continue

            self.current_process.wait()

            if self.stop_requested:
                self.ui_queue.put(("stopped", ""))
                return

            if self.success_count > 0:
                self.ui_queue.put(("progress", "100"))
                self.ui_queue.put(("done", ""))
                return

            error_text = "\n".join(output_lines[-10:]) if output_lines else "Unknown error."
            self.ui_queue.put(("error", error_text))

        except Exception as exc:
            self.ui_queue.put(("error", str(exc)))
        finally:
            self.current_process = None

    def finish_success(self):
        self.is_downloading = False
        self.download_button.config(state="normal", bg="#ef4444", activebackground="#dc2626")
        self.stop_button.config(state="disabled", bg="#e5e7eb", fg="#6b7280")
        self.progress_var.set(100)
        self.progress_percent_label.config(text="100%")
        self.update_progress_bar()
        self.refresh_eta()

        if self.fail_count > 0:
            self.status_text.set(self.texts["partial_done"])
        else:
            self.status_text.set(self.texts["status_done"])

        self.save_settings()

    def finish_error(self, _error_message):
        self.is_downloading = False
        self.download_button.config(state="normal", bg="#ef4444", activebackground="#dc2626")
        self.stop_button.config(state="disabled", bg="#e5e7eb", fg="#6b7280")
        self.progress_var.set(0)
        self.progress_percent_label.config(text="0%")
        self.update_progress_bar()
        self.eta_text.set(self.texts["eta_waiting"])

        if self.fail_count > 0:
            self.status_text.set(self.texts["all_failed"])
        else:
            self.status_text.set(self.texts["status_failed"])

    def finish_stopped(self):
        self.is_downloading = False
        self.download_button.config(state="normal", bg="#ef4444", activebackground="#dc2626")
        self.stop_button.config(state="disabled", bg="#e5e7eb", fg="#6b7280")
        self.status_text.set(self.texts["status_stopped"])
        self.eta_text.set(self.texts["eta_waiting"])
        self.save_settings()


def main():
    root = tk.Tk()
    app = YTToMP3App(root)
    root.mainloop()


if __name__ == "__main__":
    main()