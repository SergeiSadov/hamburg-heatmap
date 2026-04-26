# Hamburg Crime Heatmap

This is an interactive heatmap of crime cases across Hamburg neighborhoods, generated from official PDF report and visualized using Folium.

Live map: https://sergeisadov.github.io/hamburg-heatmap

Official criminal statistic report: https://www.polizei.hamburg/resource/blob/1153262/317efafe8864b9ad0f182577ba409c54/pks-stadtteilatlas2025-do-data.pdf

---

### Overview

#### EN

This project generates a map based on a Hamburg police report pdf file. I used square-root transformation for the heatmap itself so the coloring is even and corresponds with the numbers.

The map itself may be useful, when you are searching for a place to move in, but please also explore the neighborhoods by yourselves as each of them has it's nice corners.

#### DE


Dieses Projekt erstellt eine Karte auf Basis eines PDF-Berichts der Hamburger Polizei. Für die Heatmap wurde eine Quadratwurzel-Transformation verwendet, damit die Farbverteilung gleichmäßiger ist und besser zu den tatsächlichen Werten passt.

Die Karte kann hilfreich sein, wenn man nach einem neuen Wohnort sucht. Dennoch lohnt es sich, die Stadtteile auch selbst zu erkunden jeder von ihnen hat seine eigenen schönen Ecken.

---

### Tools

- Python
- Pandas
- GeoPandas
- Folium
- Camelot (PDF table extraction)
- NumPy

### How to run it

```bash
pip install -r requirements.txt
python main.py
```