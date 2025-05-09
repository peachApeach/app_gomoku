# Gomoku

<img src="/gitimages/miniature.png" alt="Project Overview" width="100%">

## 📄 Overview

Gomoku is a timeless strategy board game played on a grid, where players aim to align five stones in a row to outsmart their opponent. This web-based version offers a modern design, a challenging AI, and dynamic gameplay.

<!-- 🎮 **Play now:** **[Gomoku](...)** -->


## 📋 Rules

The objective of Gomoku is to align five stones in a row before your opponent. To add complexity, this version includes the ability to capture your opponent's stones. You can also win by capturing five pairs of your opponent's stones.

### Captures

Captures occur when you place two of your stones at both ends of exactly two of your opponent’s stones (neither one stone nor more than two stones). The captured stones are removed from the board, freeing those positions for reuse.

#### Example:

White stones can capture the black stones by placing a stone at the highlighted position.
<img src="/gitimages/capture.png" width="45%">


### Double Free Three

A "free three" is a line of three stones that can lead to a "free four"—a move that cannot be defended because either endpoint of the line creates a winning row of five stones. To balance gameplay, moves that create two simultaneous free threes (a "double free three") are forbidden.

#### ✅ Free Three:

<img src="/gitimages/free_three.png" width="45%">

#### ✅ Free Four:

<img src="/gitimages/free_four.png" width="45%">

#### ❌ Double Free Three:

<img src="/gitimages/double_free_three.png" width="45%">


## 🤖 How the AI Works

The AI uses the **Mini-Max Algorithm with Alpha-Beta Pruning** to make strategic decisions.

### Algorithm Overview

- **Mini-Max**: A decision-making algorithm that simulates all possible moves to minimize the opponent's advantage while maximizing the AI's chances of winning.
- **Alpha-Beta Pruning**: An optimization technique that skips evaluating branches of the decision tree that won't affect the outcome, significantly reducing computation time.

#### Mini-max Visualization with a Tic-Tac-Toe:

<img src="/backend/gomoku/tree_visual.png" width="45%">

### Optimization Techniques

The AI implements several optimizations for enhanced performance:
- ✅ **Alpha-Beta Pruning**: Reduces unnecessary calculations.
- ✅ **Dynamic Depth Adjustment**: Adjusts the search depth based on the current game state.
- ✅ **Risk-Based Action Evaluation**: Focuses on moves that represent threats or opportunities.
- ✅ **Priority Sorting**: Evaluates actions in order of strategic importance.
- ✅ **Efficient Game State Simulation**: Saves only the move and game status instead of performing a complete deepcopy for simulations.

<!--

## 🚀 Features

- 🎲 **Playable online**: Test your skills against friends or the AI.
- 🤖 **Challenging AI**: Compete with an intelligent AI opponent.
- 📈 **Advanced rules**: Captures and "double free three" mechanics enhance gameplay depth.
- 🎨 **Modern design**: Enjoy a clean and intuitive user interface.


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
