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



## Export von Content-Packages
Content-packages können direkt im CKAN-Katalog erzeugt werden. Der Export setzt vorraus dass Sie als Administrator im CKAN-Katalog eingeloggt sind. Navigieren Sie hierfür zum Datensatz-Tab und führen Sie eine beliebige Suche durch. Sie können auch eigene Such-Erweiterungen wie eine Räumliche Suche verwenden. Oben rechts taucht nun ein Button `Auswahl als Content-Package exportieren` auf.
![Export](images/exp_cont.PNG?raw=true "Export")


## Export eines einzelnen Datensatzes
Diese CKAN-Erweiterung ermöglicht auch den Export eines einzelnen Datensatzes. Loggen Sie sich hierfür als Administrator im Katalog ein Öffnen Sie einen Datensatz. Unten rechts erscheint nun ein Button `Datensatz exportieren`.
![Export](images/exp_data.PNG?raw=true "Export")


## Import eines Content-packages
Für den Import von Content-Packages gibt es einen eigenen Tab im Administrations-Bereich des CKAN-Katalogs. Sollte dieser Tab nicht wie im folgenden Bild aussehen, könnte der Grund dafür sein, dass der katalog nicht mittels SSL-Verschlüsselt ist.
![Export](images/imp_cont.PNG?raw=true "Import")
Sie haben hier die Möglichkeit 


## Import eines einzelnen Datensatzes





## CKAN Dokumentation und Hilfe

Die offizielle CKAN-Dokumentation finden Sie unter: [https://docs.ckan.org/en/2.9](https://docs.ckan.org/en/2.9).  
Informationen zur Benutzung der CKAN-API finden Sie unter: [https://docs.ckan.org/en/2.9/api/index.html](https://docs.ckan.org/en/2.9/api/index.html).


## Lizenz

The content of this repository is released under the terms of the [Apache-2.0 License](https://github.com/tum-gis/3dcitydb-docker-postgis/blob/master/LICENSE). The software components used in this project may be subject to different licensing conditions. Please refer to the website of the individual projects for further information.