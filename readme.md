# CKAN Plugin für den Export und Import von Content-Packages

Die Themenplattform Smarte Städte und Regionen setzt unter anderem die [Smart District Data Infrastructure (SDDI)](https://www.lrg.tum.de/gis/projekte/sddi/) Strategie für den Aufbau einer Dateninfrastruktur in smarten Städten und Regionen. SDDI wurde im Ramen des [Smart Sustainable Districts (SSD)](https://www.lrg.tum.de/gis/projekte/smart-sustainable-districts-ssd/) Projekts entwickelt und enthält als zentralen Inhalt eine Katalogplattform, in der alle relevanten Daten, Projekte und Dienste registriert sind.

Dieses Repository enthält ein Plugin um eine neue Instanz einer [CKAN-Katalogplattform](https://ckan.org) mit einem Grundbestand an Datensätzen zu befüllen. Dies wird durch sogenannte "Content-Packages" ermöglicht, welche eine Sammlung an Datensätzen sind.


## Features

* Content-Packages exportieren über einem Button
* Content-Packages importieren über Datei-Upload oder Link
* Einzelnen Datensatz exportieren über einem Button
* Einzelnen Datensatz importieren über Datei-Upload oder Link


## Inhalt

* [Features](#features)
* [Inhalt](#inhalt)
* [Installation](#installation)
* [Aufbau eines Content-Packages](#aufbau-eines-content-packages)
* [Export von Content-Packages](#export-von-content-packages)
* [Export eines einzelnen Datensatzes](#export-eines-einzelnen-Datensatzes)
* [Import von Content-Packages](#import-von-content-packages)
* [Import eines einzelnen Datensatzes](#import-eines-einzelnen-Datensatzes)
* [FAQ](#FAQ)
* [CKAN Dokumentation und Hilfe](#ckan-dokumentation-und-hilfe)
* [Lizenz](#lizenz)


## Installation

Dieses Kapitel beschreibt die Installation des Plugins. Es wird empfohlen das Plugin nur zu verwenden, wenn der Katalogidenst über ein SSL-Zertifikat verfügt und verschlüsselt ist. Andernfalls kann es zu Problemen beim Datei-Uplaod kommen, da der Browser Mixed-Content blockiert.

```
. /usr/lib/ckan/default/bin/activate
cd /usr/lib/ckan/default/src
pip install -e "git+https://github.com/tum-gis/ckanext-importerexporter-sddi#egg=ckanext-importerexporter-sddi"
```

Um die Erweiterung im Administratoren-bereich zu registrieren, muss die Datei  
`/usr/lib/ckan/default/src/ckan/ckan/views/admin.py`
unten um folgende zeile ergänzt werden:
```
admin.add_url_rule(u'/', view_func=index, strict_slashes=False)
admin.add_url_rule(u'/reset_config', view_func=ResetConfigView.as_view(str(u'reset_config')))
admin.add_url_rule(u'/config', view_func=ConfigView.as_view(str(u'config')))
admin.add_url_rule(u'/trash', view_func=TrashView.as_view(str(u'trash')))

...

admin.add_url_rule(u'/contentpackages', view_func=TrashView.as_view(str(u'contentpackages')))
```

Um das Plugin zu aktivieren muss in der Datei `/etc/ckan/default/production.ini` bei den Plugins `importerexporter` hinzugefügt werden. Das Plugin sollte als letztes in der Liste setehen, zumindest hinter allen Erweiterungen die die Suche nach Datensätzen modifizieren.


## Aufbau eines Content-Packages
Ein Content-Package ist eine Sammlung von einzelnen Datensätzen im ZIP-Format. Jeder Datensatz ist wiederum eine eigene ZIP-Datei, die jeweils den Datensatz im JSON-Format sowie zusätzliche Ressourcen wie Bilder enthält.  
Content Packages müssen in der Form `CKAN_CONTENTPACKAGE_[Name].zip` gespeichert sein.  
Datensätze innerhalb eines Content-Packages müssen in der Form `CKAN_DATASET_[Name].zip` gespeichert sein.
Folgende Grafik zeigt Beispielhaft den Aufbau eines Content-Packages:

```
CKAN_CONTENTPACKAGE_Basispaket.zip  
├───CKAN_DATASET_Datensatz-1.zip  
│   └───CKAN_DATASET_Datensatz-1  
│       ├───dataset.json
│       ├───bild-1.jpg
│       └───bild-2.png
└───CKAN_DATASET_Datensatz-2.zip  
    └───CKAN_DATASET_Datensatz-2  
        ├───dataset.json
        ├───grafik-1.jpg
		├───grafik-2.gif
        └───tabelle.svc 
```

## Export von Content-Packages
Content-packages können direkt im CKAN-Katalog erzeugt werden. Der Export setzt vorraus dass Sie als Administrator im CKAN-Katalog eingeloggt sind. Navigieren Sie hierfür zum Datensatz-Tab und führen Sie eine beliebige Suche durch. Sie können auch eigene Such-Erweiterungen wie eine Räumliche Suche verwenden. Oben rechts taucht nun ein Button `Auswahl als Content-Package exportieren` auf.
![Export](images/exp_cont.PNG?raw=true "Export")


## Export eines einzelnen Datensatzes
Diese CKAN-Erweiterung ermöglicht auch den Export eines einzelnen Datensatzes. Loggen Sie sich hierfür als Administrator im Katalog ein Öffnen Sie einen Datensatz. Unten rechts erscheint nun ein Button `Datensatz exportieren`.
![Export](images/exp_data.PNG?raw=true "Export")


## Import eines Content-packages
Für den Import von Content-Packages gibt es einen eigenen Tab im Administrations-Bereich des CKAN-Katalogs. Sollte dieser Tab nicht wie im folgenden Bild aussehen, könnte der Grund dafür sein, dass der katalog nicht mittels SSL-Verschlüsselt ist.
![Import](images/imp_cont.PNG?raw=true "Import")
Sie haben hier die Möglichkeit ein Content-Package entweder über einen Datei-Upload oder über einen Link zu importieren. Falls Sie die Link-Option verwenden, muss die URL direkt zur Datei weisen. Über den Button `Import` wird das Content-Package importiert. Ist einer der Datensätze im Content-Package bereits im Katalog registriert, wird dieser Datensatz übersprungen und eine Warnung ausgegeben.

### Import Erfolgreich
Ist der Import erfolgreich, sind die Datensätze des Content-Packages nun im Katalog registriert.
![Import](images/imp_cont_success.PNG?raw=true "Import")

### Import mit Warnungen
Wenn während dem Import Warnungen auftreten, werden diese in gelb ausgegeben. Eine häufige Warnung ist, dass einer der Datensätze bereits im Katalog registriert sind. Sie können nun diesen Datensatz direkt anklicken und bei Bedarf löschen. Anschließend können Sie das Content-Package erneut importieren. Tritt eine Warnung auf, werden alle anderen Datensätze im Content-Package trotzdem importiert.
![Import](images/imp_cont_warning.PNG?raw=true "Import")

### Import fehlgeschlagen
Wenn während dem Import ein Fehler auftritt, wird der Fehlercode in rot ausgegeben. Sämtliche Datensätze im Content-Package die fehlerfrei sind, werden dennoch importiert.
![Import](images/imp_cont_error.PNG?raw=true "Import")

## Import eines einzelnen Datensatzes
Analog zum Export kann auch der Import mit einem Einzelnen Datensatz erfolgen. Hierfür können Sie direkt eine Datei im Format `CKAN_DATASET_[Name].zip` importieren.


## FAQ

* Was passiert wenn ein Datensatz importiert wird, der bereits im Katalog vorhanden ist?  
Ist ein Datensatz bereits registriert wird er übersprungen und eine Warnung mit einem Link zum Datensatz ausgegeben.
* Werden Ressourcen wie z.B. Bilder mit exportiert und Importiert?  
Ja, Sämtliche Ressourcen werden exportiert und auch wieder importiert.
* Gehen beim Export und Import Daten verloren?  
Beim Export werden alle Meta-Daten eines Datensatzes exportiert. Beim Import gehen lediglich Informationen verloren, die sich auf den ursprünglichen Datensatz beziehen, also z.B. das Erstellungs-Datum oder der urpsrüngliche Autor

## CKAN Dokumentation und Hilfe

Die offizielle CKAN-Dokumentation finden Sie unter: [https://docs.ckan.org/en/2.9](https://docs.ckan.org/en/2.9).  
Informationen zur Benutzung der CKAN-API finden Sie unter: [https://docs.ckan.org/en/2.9/api/index.html](https://docs.ckan.org/en/2.9/api/index.html).


## Lizenz

The content of this repository is released under the terms of the [Apache-2.0 License](https://github.com/tum-gis/3dcitydb-docker-postgis/blob/master/LICENSE). The software components used in this project may be subject to different licensing conditions. Please refer to the website of the individual projects for further information.