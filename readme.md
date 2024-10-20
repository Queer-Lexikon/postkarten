# Das Postkartenaktionsdingsi

Wir wollen:
- ein paar Fördermitgliedschaften gewinnen,
- den Fortschritt im Auge behalten
- die Stammdaten händisch zu Ninjaforms mitnehmen
- und Adressen raustragen, um da Postkarten hinzuschicken

das passiert so:
- es gibt eine statische Landingpage
- es gibt ein sehr schlankes Backend, das Fördermitgliedschaften entgegen nimmt
- das Backend legt die jeweils als JSON ab
- das Backend ist fastapi, was über Pydantic Types und Safety produziert

## Setup

Das sollte prinzipiell etwa so gehen

- venv generieren (wir wollen Python 3.11 oder neuer)
- `pip install -r requirements.txt`
- schnell im WordPress checken, wie viele Fördermitgliedschaften schon da sind und gegebenenfalls die `+34` in der `get_current()` anpassen
- `uploads`-Ordner anlegen, weil git keine leeren Ordner mag. 
- mit `fastapi run main.py --port ABC` mit einem freien Port für ABC starten und das Reverse-Proxy dran kleben

optional: in der Theorie kann, was im `static/` liegt, auch am ASGI vorbei geserved werden.

**Bonus**: um Designdinge zu machen, reichts auch völlig, sich die Dateien aus dem `static`-Ordner zu schnappen, da ist alles dran, außer die aktuelle Anzahl Postkarten und es passiert halt nix, wenn man auf abschicken klickt.

## Customize

Das leider bisschen murky, aber:

- Wer **Texte** anpassen mag, findet die alle in der `static/index.html`. Alles, was HTML kann, ist prinzipiell möglich, es wird nichts gefiltert oder geprüft.
- Wer **Design** anpassen mag, wird in `static/generic.css` fündig. Das deklariert oben eine Menge Variablen, so dass abtauchen zu spezifischen Klassen oft gar nicht mehr dringend ist.

## was ist noch?

- vor dem abschicken die formData checken, dass alles notwendig da ist (zeile 373)
  - gegebenenfalls nicht stimmige Dinge highlighten und hinscrollen

