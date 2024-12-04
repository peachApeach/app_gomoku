# Gomoku

<img src="/gitimages/miniature.png" alt="Project Overview" width="100%">

## 📄 Overview

Gomoku is a classic strategy board game played on a grid, where the goal is to outsmart your opponent by aligning five stones in a row. This web-based version brings Gomoku to life with sleek design, challenging AI, and dynamic gameplay.

Available on this link : **[Gomoku](http://164.90.229.9:4001/)**

## 📋 Rules

Le but du jeu de Gomoku est d'aligné five stones in a row. Pour rendre le jeu plus intéressant, nous avons intégré la possibilité de capturer les paires de l'adversaire. Vous pouvez gagner en capturant 5 paires de l'adversaire.

### Captures
Si vous placez two of your stones aux extrémités de two stones (not single stone and not more than two stones) of the opponent, that will remove them from the game. Vous pouvez donc réutiliser ces emplacements.

#### Examples:
<img src="/gitimages/capture.png" width="45%">
White stones can capture the black stones by placing at the highlight emplacement.


### Double free three
Un free three est un alignement that can introduce a free four, qui est un mouvement impossible a defendre car les deux extremites permettent d'obtenir un alignement de cinq. Pour eviter de creer des opportunites trop avantageuses, les placements qui introduisent deux free three are forbidden.

#### Free three:
<img src="/gitimages/free_three.png" width="45%">

#### Free four:
<img src="/gitimages/free_four.png" width="45%">

#### Double free three:
<img src="/gitimages/double_free_three.png" width="45%">

## 🤖 How AI works?

Used algorithm : Mini-max

Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. 

### Implement Optimization

- ✅ Alpha-Beta Pruning Lorem Ipsum is simply dummy text of the printing and typesetting industry.
- ✅ Depth Lorem Ipsum is simply dummy text of the printing and typesetting industry.
- ✅ Action Range Lorem Ipsum is simply dummy text of the printing and typesetting industry.

<!--
## 🎮 Game Design & User Experience

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent quis neque quis tortor scelerisque ultricies. Nunc nec feugiat eros. Sed viverra est vel sem volutpat, in faucibus mauris pharetra. Pellentesque ac massa et orci aliquam volutpat at ac metus. Duis laoreet pulvinar lectus ut viverra. Ut volutpat aliquam justo et aliquam.

https://github.com/user-attachments/assets/92e7767a-42fb-428e-b834-2a56093c6635
-->

## Try the Project - WebApp

### 1. Install Docker

To run this project, the first step is to install [Docker](https://docs.docker.com/engine/install/) on your machine. Docker simplifies deployment by providing an isolated environment for your application.

### 2. Install Make (Optional)

This project includes a Makefile, which allows you to execute Docker commands more easily, without having to type them manually. While using `make` is optional, it is highly recommended to simplify operations. You can install `make` by following [this link](https://www.gnu.org/software/make/#download) or by searching for installation instructions specific to your system.

### 3. Run the WebApp

#### With Make

Run this command in your terminal:

```bash
make
```
This will display:

<img src="/gitimages/make_output.png" width="75%">
Next, run this to start the web application:

```bash
make run
```
#### Without Make

If you prefer not to use `make`, you can start the web application by running the following command:

```bash
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d
```
## Try the Project - Script Only

**Navigate to the Project Folder**

You can access the project folder by using [this link](https://github.com/DevJ2K/app_gomoku/tree/main/backend/gomoku).

<!-- ## Todo-list
- [ ] Update current and project README.md.
- [x] Change colors Host link in display_project
- [x] Download project link?
- [x] Computorv1 -> Project_name in frontend/app/.../HomeView.vue
- [x] Use Args in Dockerfile
- [x] Add colors to Makefile -->
