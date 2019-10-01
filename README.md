# semaphore

Un sémaphore dans le Blender Game Engine pour créer une IA !

### Contexte

Réalisé avec:

* Debian 10 Buster

### 70 000 images pour créer le réseau de neuronnes

Les images sorties de Blender 320x320:

<img src="/doc/some_shot_320/shot_0_a.png" width="100" height="100"/><img src="/doc/some_shot_320/shot_1_space.png" width="100" height="100"/><img src="/doc/some_shot_320/shot_2_b.png" width="100" height="100"/>

Les images retaillées à 40x40, floutées:

<img src="/doc/some_shot_gray/shot_0_a.png" width="100" height="100"/><img src="/doc/some_shot_gray/shot_1_space.png" width="100" height="100"/><img src="/doc/some_shot_gray/shot_2_b.png" width="100" height="100"/>

Les images en noir et blanc, utilisées pour l'apprentissage:

<img src="/doc/some_shot_nb/shot_0_a.png" width="100" height="100"/><img src="/doc/some_shot_nb//shot_1_space.png" width="100" height="100"/><img src="/doc/some_shot_nb//shot_2_b.png" width="100" height="100"/>

### Utilisation

Ouvrir un teminal dans le dossier semaphore
~~~text
./semaphore.sh
~~~

Il n'est pas necessaire de créer les images avec Blender: cetteétape dure 3 heures !

Les images au format 40x40 en gris sont dans le fichier training_shot.tar.gz

Le décompresser. Vous obtenez un dossier training_shot dans le dossier semaphore.

Et passer directement à l'étape 2.

### La documentation sur ressources.labomedia.org

* [Jeu du sémaphore dans le Blender Game Engine](https://ressources.labomedia.org/jeu_du_semaphore_dans_le_blender_game_engine)
* [L'intelligence du sémaphore](https://ressources.labomedia.org/l_intelligence_du_semaphore)


### Dossiers images

Les images ne sont pas dans ce dépôt

### Installation
### pip3
~~~text
sudo apt install python3-pip
~~~

#### pymultilame
~~~text
sudo pip3 install -e git+https://github.com/sergeLabo/pymultilame.git#egg=pymultilame
~~~

Mise à jour:
~~~text
sudo pip3 install --upgrade git+https://github.com/sergeLabo/pymultilame.git#egg=pymultilame
~~~

#### Opencv et numpy
~~~text
sudo pip3 install numpy
sudo pip3 install opencv-python
~~~

#### Blender 2.79b mais pas 2.80 qui n'a plus de BGE
~~~text
sudo apt install blender
~~~

Important: Ne pas déplacer ou aggrandir la fenêtre de Blender pendant que les
images défilent.

### Merci à:

* [La Labomedia](https://ressources.labomedia.org)
