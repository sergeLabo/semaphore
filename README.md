# semaphore

Un sémaphore dans le Blender Game Engine pour créer une IA !

Un shot:
<img src="/doc/shot_15_y.png" width="300" height="300">

### Contexte

Réalisé avec:

* Debian 10 Buster

### 60 000 images pour créer le réseau de neuronnes

Quelques images pour apprendre, en gris 40x40 floues, différentes tailles et rotations

<img src="/doc/some_training_shot/shot_24000_i.png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24001_ .png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24002_f.png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24003_a.png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24004_c.png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24005_i.png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24006_e.png" width="100" height="100"/>
<img src="/doc/some_training_shot/shot_24007_m.png" width="100" height="100"/>


### La documentation sur ressources.labomedia.org

[Sémaphore](https://ressources.labomedia.org/jeu_du_semaphore_dans_le_blender_game_engine)

### Dossiers images

Les images ne sont pas dans ce dépot

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

### Utilisation

Ouvrir un teminal dans le dossier semaphore
~~~text
./semaphore.sh
~~~

Important: Ne pas déplacer ou aggrandir la fenêtre de Blender pendant que les
images défilent.

### Merci à:

* [La Labomedia](https://ressources.labomedia.org)
