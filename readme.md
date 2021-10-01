# Extracteur de textes et de métadonnées des fichiers XML des décisions de justice

## Introduction

Les fichiers *xml* des décisions adminsitratives ne sont pas facilement exploitables. 
Ce répertoire permet d'extraire le texte et les métadonnées de ces fichiers: 
1. [get_meta_data_from_xml_folder.py](src/get_meta_data_from_xml_folder.py "get_meta_data_from_xml_folder.py") :  extrait les métadonnées des fichiers et les enregistre dans un fichier json
2. [get_text_from_xml_folder.py](src/get_text_from_xml_folder.py "get_txt_files_from_xml.py") : extrait le texte des fichiers xml et les enregistre dans des fichiers txt 


## Faire tourner les scripts 

Il suffit de spécifier **dossier d'input** contenant les fichiers xml, le **dossier d'output** pour enregistrer les fichiers textes et la base de données (DatabaseName) (ici Ariane mais cela fonctionne également pour CAPP et JuriCa) . 

<br>

**1\. Meta data.** Exécuter la commande suivante :
```
python3 get_meta_data_from_xml_folder.py input_directory output_directory Database_Name -info
```

Si tout s'est bien passé, un fichier json devrait etre enregistré avec les métadonnées ainsi qu'un fichier log `meta_data_extraction.log` si l'option `-info` est activée

<br>

**2\. Extraire le texte.** Exéuter la commande suivante: 
```
python3 get_txt_files_from_xml.py input_directory output_dir DATABASE_NAME -info
```
Cela enregistrera des fichiers au format .txt dans le dossier d'output. Un fichier log `text_extraction.log` sera créé si l'option `-info` est activée
