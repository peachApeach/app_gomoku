<template>
  <main class=" text-high-contrast-text container mt-10 flex size-full flex-row justify-center">
    <div class=" flex w-full flex-col items-center justify-center">
      <div id="scoreboard" class="flex flex-nowrap items-center gap-32 mb-5 text-low-contrast-text hidden-important">
        <div id="player1" class="flex items-center gap-8">
          <div id="player1-timer" class="text-lg px-4 py-2 bg-blue-700 rounded-lg">
            
          </div>
          <h1 class="text-center text-3xl font-bold">Player 1</h1>
        </div>
        <div id="round-timer" class="text-6xl text-high-contrast-text px-4 py-2 ">
            
        </div>
        <div id="player2" class="flex gap-8">
          <h1 class="text-center text-3xl font-bold"></h1>
          <div id="player2-timer" class="text-lg px-4 py-2 bg-orange-700 rounded-lg">
            
          </div>
        </div>
      </div>
      <div id="board" class="grid grid-cols-19 grid-rows-19">
      </div>
    </div>
  </main>
  <Modal :modal-active="generatorModalActive" @close-modal="toggleGeneratorModal">
    <h1 class="text-center text-3xl font-bold text-high-contrast-text mb-5">
      Paramètres</h1>

    <div class="flex w-full flex-col items-start py-5">
      <label id="time-per-turn-label" for="time-per-turn" class="block mb-2 text-sm font-medium text-low-contrast-text">Temps par tour</label>
      <div class="relative w-full">
          <select name="time-p-turn" id="time-per-turn" class="bg-ui-bg border border-gray-600 placeholder-gray-400 text-white text-sm rounded-lg focus:border-blue-500 focus:ring-blue-500 block w-1/2 p-2.5">
            <option value="10">10 secondes</option>
            <option value="20">20 secondes</option>
            <option value="30">30 secondes</option>
            <option value="40" selected>40 secondes</option>
            <option value="-1">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="min-per-player-label" for="min-per-player" class="block mb-2 text-sm font-medium text-low-contrast-text">Minutes par joueur</label>
      <div class="relative w-full">
          <select name="min-p-player" id="min-per-player" class="bg-ui-bg border border-gray-600 placeholder-gray-400 text-white text-sm rounded-lg focus:border-blue-500 focus:ring-blue-500 block w-1/2 p-2.5">
            <option value="2">2 minutes</option>
            <option value="3">3 minutes</option>
            <option value="4">4 minutes</option>
            <option value="5" selected>5 minutes</option>
            <option value="-1">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="first-player-label" for="first-player" class="block mb-2 text-sm font-medium text-low-contrast-text">Qui commence en premier ?</label>
      <div class="relative w-full">
          <select name="f-player" id="first-player" class="bg-ui-bg border border-gray-600 placeholder-gray-400 text-white text-sm rounded-lg focus:border-blue-500 focus:ring-blue-500 block w-1/2 p-2.5">
            <option value="-1">Aleatoire</option>
            <option value="0">Je commence en premier</option>
            <option value="1">L'opposant commence en premier</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="opposant-label" class="block mb-2 text-sm font-medium text-low-contrast-text">Jouer contre qui ?</label>
      <div class="flex">
        <div class="flex items-center me-5 px-4 border border-gray-600 rounded-lg dark:border-gray-700">
          <input id="opposant-ia" type="radio" name="opposant" value="ia" class="w-4 h-4 bg-gray-100 accent-amber-400" checked>
          <label for="opposant-ia" class="w-full py-3 ms-2 text-sm font-medium text-low-contrast-text"> IA</label>
        </div>
        <div class="flex items-center px-4 border border-gray-600 rounded-lg dark:border-gray-700">
          <input id="opposant-hotseat" type="radio" name="opposant" value="hotseat" class="w-4 h-4 bg-gray-100 border-gray-300 accent-amber-400">
          <label class="w-full py-3 ms-2 text-sm font-medium text-low-contrast-text" for="opposant-hotseat"> Local</label>
        </div>
      </div>
    </div>

    <div class="mt-6 flex w-full items-center justify-center">
      <button type="button" class="focus:outline-none text-base text-white bg-yellow-700 hover:bg-yellow-600 focus:ring-4 focus:ring-yellow-900 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2" @click="initGame">PLAY</button>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '../components/modal/Modal.vue';
import { onMounted, onUnmounted, ref } from 'vue';

const generatorModalActive = ref(false)
let gameId: Number

let timerPlayer1: Number
let timerPlayer2: Number

let timePerTurn: Number
let currentRoundTimer: Number
let currentRoundTurn: String

let isPausedPlayer1 = true
let isPausedPlayer2 = true

let whoStartFirst = 0; // 0 -> white   1 -> black


const toggleGeneratorModal = () => {
  generatorModalActive.value = !generatorModalActive.value;
}

const initGame = () => {
  toggleGeneratorModal()
  createGrid()
  fillGridWithList(['W'])
  startGame()
}

const createGrid = () => {
  let counter = 0
  document.getElementById('nav-bar').hidden = true
  const gridParentDiv = document.getElementById('board')
  for (let i = 0; i < 19; i++) {
    for (let j = 0; j < 19; j++) {
      const gridElement = document.createElement('div')
      const gridBtn = document.createElement('button')
      gridBtn.classList.add(...['relative', 'grid-button', 'w-10', 'h-10'])
      gridBtn.id = i.toString() + '-' + j.toString()
      gridBtn.addEventListener("click", addPown)
      // gridBtn.classList.add(...['relative', 'grid-button', 'border-solid', 'border', 'border-sky-500', 'w-10', 'h-10'])
      gridElement.classList.add(...['relative', 'flex', 'items-center', 'justify-center', 'w-10', 'h-10', 'grid-div'])

      const hrHorizontal = document.createElement('hr')
        
      const hrVertical = document.createElement('hr')
      if (i == 0)
        hrVertical.classList.add(...['vl-first-line'])
      else if (i == 18)
        hrVertical.classList.add(...['vl-last-line'])
      else
        hrVertical.classList.add(...['vl'])
      if (j == 0)
        hrHorizontal.classList.add(...['hl-first-col'])
      else if (j == 18)
        hrHorizontal.classList.add(...['hl-last-col'])
      else
        hrHorizontal.classList.add(...['hl'])
      const hoverCircle = document.createElement('div')
      hoverCircle.classList.add(...['circle', 'absolute', 'group-hover:block'])
      hoverCircle.id = i.toString() + '-' + j.toString() + '-circle'
      gridBtn.appendChild(hoverCircle)

      gridElement.appendChild(hrVertical)
      gridElement.appendChild(hrHorizontal)
      
      gridElement.appendChild(gridBtn)
      gridParentDiv.appendChild(gridElement)
      counter++
    }
  }
}

const fillGridWithList = (list: any) => {
  const board = document.getElementById('board')
  var childrens = board.children;
  list = list.flat()
  for (let i = 0; i < childrens.length; i++) {
    var tableChild = childrens[i];
    var circleElement = tableChild.querySelector('.circle');
    if (list[i] == 'W') {
      circleElement.style.backgroundColor = '#FFFFFF'
      circleElement.style.opacity = "1"
    }
    else if (list[i] == 'B'){
      circleElement.style.backgroundColor = '#000000'
      circleElement.style.opacity = "1"
    }
  }
}

const postRequest = async (url: string, payload: any) => {
  try {
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const response = await fetch(url, {
      method: "POST",
      body: payload,
      headers: myHeaders,
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const json = await response.json();
    return json
  } catch (error: any) {
    console.error(error.message);
  }
}

const createScoreboard = () => {
  const scoreboard = document.getElementById('scoreboard')
  const minPerPlayer = document.getElementById('min-per-player')?.value
  timePerTurn = document.getElementById('time-per-turn')?.value
  const gamemode = document.querySelector('input[name="opposant"]:checked')?.value;

  document.getElementById('player1-timer').textContent = minPerPlayer != -1 ? '0' + minPerPlayer + ':00' : 'XX:XX'
  document.getElementById('player2-timer').textContent = minPerPlayer != -1 ? '0' + minPerPlayer + ':00' : 'XX:XX'
  document.getElementById('round-timer').textContent = timePerTurn != -1 ? '00:' + timePerTurn : ''
  document.getElementById('player2').children[0].textContent = gamemode == 'ia' ? 'Robot' : 'Player 2'
  if (minPerPlayer != -1) {
    createCountdownPlayer1(minPerPlayer * 60, 'player1-timer')
    createCountdownPlayer2(minPerPlayer * 60, 'player2-timer')
  }
  if (timePerTurn != -1) {
    createCountdownForRound(timePerTurn, 'round-timer')
  }
  scoreboard.classList.remove('hidden-important')
}

const startGame = () => {
  whoStartFirst = document.getElementById('first-player')?.value
  const gamemode = document.querySelector('input[name="opposant"]:checked')?.value;
  if (whoStartFirst == -1) { whoStartFirst = Math.floor(Math.random() * 2) }
  const payload = {
    "mode": gamemode,
    "who_start": whoStartFirst == 0 ? "W" : "B",
    "IA_suggestion": true,
    "options": {
      "allowed_capture": true,
      "allowed_win_by_capture": true,
      "allowed_double_three": false
    },
    "opening": "standard",
    "difficulty": "medium"
    }

  // if (whoStartFirst == 2) { currentRoundTurn = 1 }
  // else if (whoStartFirst == 0) { currentRoundTurn = Math.floor(Math.random() * 2) }
  // console.log(Math.floor(Math.random() * 2))
  // const data = postRequest("http://127.0.0.1:8000/game/new", payload)
  const data = {
   "game_id": 1,
   "player_turn": "B",
   "IA": true,
   "IA_suggestion": false,
   "board": [
      [' ', ' ', ' '],
      [' ', ' ', ' '],
   ]
  }
  fillGridWithList(data.board)
  createScoreboard()
  gameId = data.game_id
  currentRoundTurn = data.player_turn
  console.log(currentRoundTurn)
  if (data.player_turn == 'B') {
    // hover == black
    isPausedPlayer2 = false
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
      circleClass[i].style.backgroundColor = '#000000'
    // click add permanent black pawn
     // inverse round turn

  }
  else {
    // hover == white
    isPausedPlayer1 = false
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
      circleClass[i].style.backgroundColor = '#FFFFFF'
    // click add permanent black pawn

  }
    // anyway get position of pawn, using i and j, have to add it to id value, separate by '-'
    // send api call
}

const addPown = (event) => {
  let pawnId = event.target.id
  if (event.target.localName == 'button')
    pawnId += '-circle'
  console.log(pawnId)
  const pawnCircle = document.getElementById(pawnId)
  if (pawnCircle.style.opacity == "1") {
    console.log('already clicked')
    return
  }
  const coordinates = [pawnId.split('-')[0], pawnId.split('-')[1]]
  const payload = {
    "player_move": {"x": coordinates[0], "y": coordinates[1]}
  }
  // const data = postRequest("http://127.0.0.1:8000/game//move", payload)
  const data = {
   "player_turn": "W",
   "IA_suggestion": false,
   "IA_move": {"x": 8, "y": 7},
   "IA_duration": 99,//xp streamez Jolagreen23
   "board": [
      ["W", "B", " "],
      [" ", " ", " "]
   ],
   "black_capture": 2,
   "white_capture": 1,
   "error": null, // si c'est pas nul c'est que y'a une erreur de placement.
   "status": "finished"
  }
  // Handle response
  if (data.status != 'playing')
    return handleEndGame()
  if (data.error != null)
    console.log('Placement error')
  if (data.status != "playing")
    console.log('Fin')
  isPausedPlayer1 = !isPausedPlayer1
  isPausedPlayer2 = !isPausedPlayer2
  if (timePerTurn != -1) {
    clearInterval(currentRoundTimer)
    createCountdownForRound(parseInt(timePerTurn) + 1, 'round-timer')
  }
  currentRoundTurn = data.player_turn
  fillGridWithList(data.board)
  if (currentRoundTurn == 'B') {
    // hover == black
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
    if (circleClass[i].style.opacity != "1") { circleClass[i].style.backgroundColor = '#000' }
  }
  else {
    // hover == white
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
    if (circleClass[i].style.opacity != "1") { circleClass[i].style.backgroundColor = '#FFF' }
  }
}

const handleEndGame = () => {
  clearInterval(timerPlayer1)
  clearInterval(timerPlayer2)
  clearInterval(currentRoundTimer)
  document.removeEventListener('click', addPown)

  // scoreboard.classList.add('hidden-important')
  // document.getElementById('nav-bar').hidden = false
}

const secondsToMinSeconds = (count) => {
  let minutes = Math.floor(count / 60);
  let seconds = count - minutes * 60;
  return [minutes, seconds]
}

const createCountdownPlayer1 = (count, timerDivId) => {
  timerPlayer1 = setInterval(function() {
    if (!isPausedPlayer1) {
      count--;
      const [minutes, seconds] = secondsToMinSeconds(count)
      if (seconds < 10)
        document.getElementById(timerDivId).textContent = minutes + ':0' + seconds
      else
        document.getElementById(timerDivId).textContent = minutes + ':' + seconds
      if (count === 0) {
        clearInterval(timerPlayer1);
        console.log("Time's up!");
      }
    }
  }, 1000);
}

const createCountdownPlayer2 = (count, timerDivId) => {
  timerPlayer2 = setInterval(function() {
    if (!isPausedPlayer2) {
      count--;
      const [minutes, seconds] = secondsToMinSeconds(count)
      if (seconds < 10)
        document.getElementById(timerDivId).textContent = minutes + ':0' + seconds
      else
        document.getElementById(timerDivId).textContent = minutes + ':' + seconds
      if (count === 0) {
        clearInterval(timerPlayer2);
        console.log("Time's up!");
      }
    }
  }, 1000);
}

const swapCurrentRound = () => {
  // send ajax request with isTimeout = True
  if (currentRoundTurn == 'B') {
    currentRoundTurn = 'W'
  }
  else
    currentRoundTurn = 'B'
}

const createCountdownForRound = (count, timerDivId) => {
  currentRoundTimer = setInterval(function() {
      count--;
      if (count < 10)
        document.getElementById(timerDivId).textContent = '00:0' + count
      else
        document.getElementById(timerDivId).textContent = '00:' + count
      if (count === 0) {
        clearInterval(currentRoundTimer);
        swapCurrentRound()
      }
  }, 1000);
}

onMounted(() => {
  toggleGeneratorModal()
});

</script>
