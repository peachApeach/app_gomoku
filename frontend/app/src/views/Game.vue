<template>
  <main class=" text-high-contrast-text container mt-10 flex size-full flex-row justify-center">
    <div class=" flex w-full flex-col items-center justify-center">
      <div id="scoreboard" class="hidden-important text-low-contrast-text mb-5 flex flex-nowrap items-center gap-32">
        <div id="player1" class="flex items-center gap-8">
          <div id="player1-timer" class="rounded-lg bg-blue-700 px-4 py-2 text-lg">

          </div>
          <h1 class="text-center text-3xl font-bold">Player 1</h1>
        </div>
        <div id="round-timer" class="text-high-contrast-text px-4 py-2 text-6xl ">

        </div>
        <div id="player2" class="flex gap-8">
          <h1 class="text-center text-3xl font-bold"></h1>
          <div id="player2-timer" class="rounded-lg bg-orange-700 px-4 py-2 text-lg">

          </div>
        </div>
      </div>
      <div id="message" class="text-center text-xl font-bold" :class="isError ? 'text-red-500' : 'text-white'">&nbsp;{{ message }}</div>
      <div v-if="iaDuration != null" id="ia-duration" class="text-high-contrast-text text-center text-xl ">IA took {{ iaDuration }} to make its decision</div>
      <!-- <div id="error_message" class="text-center text-lg font-bold text-red-500">Consequat officia deserunt deserunt officia laboris. Nostrud laborum nisi id aliqua incididunt commodo velit. Cillum anim ad fugiat ex anim consectetur. Reprehenderit sit labore non est reprehenderit adipisicing sunt enim.</div> -->
      <div id="board" class="grid-cols-19 grid-rows-19 grid">
      </div>
    </div>
  </main>


  <Modal :modal-active="endGameModalActive" @close-modal="toggleEndGameModal">
    <h1 class="text-high-contrast-text mb-5 text-center text-3xl font-bold">End Game</h1>
    <p class="mb-5 text-center text-xl font-bold text-white">{{ message }}</p>
    <!-- <div>
      <p class="text-center text-base font-bold text-white">Black has captured 3 white stones.</p>
      <p class="text-center text-base font-bold text-white">White has captured 3 black stones.</p>
    </div> -->
    <div class="mt-6 flex w-full items-center justify-center">
      <button type="button" class="mb-2 me-2 rounded-lg bg-yellow-700 px-5 py-2.5 text-base font-medium text-white hover:bg-yellow-600 focus:outline-none focus:ring-4 focus:ring-yellow-900" @click="replayGame">Replay</button>
    </div>
  </Modal>


  <Modal :modal-active="generatorModalActive" @close-modal="toggleGeneratorModal">
    <h1 class="text-high-contrast-text mb-5 text-center text-3xl font-bold">
      Paramètres</h1>

    <div class="flex w-full flex-col items-start py-5">
      <label id="time-per-turn-label" for="time-per-turn" class="text-low-contrast-text mb-2 block text-sm font-medium">Temps par tour</label>
      <div class="relative w-full">
          <select name="time-p-turn" id="time-per-turn" class="bg-ui-bg block w-1/2 rounded-lg border border-gray-600 p-2.5 text-sm text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500">
            <option value="10">10 secondes</option>
            <option value="20">20 secondes</option>
            <option value="30">30 secondes</option>
            <option value="40">40 secondes</option>
            <option value="-1" selected>Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="min-per-player-label" for="min-per-player" class="text-low-contrast-text mb-2 block text-sm font-medium">Minutes par joueur</label>
      <div class="relative w-full">
          <select name="min-p-player" id="min-per-player" class="bg-ui-bg block w-1/2 rounded-lg border border-gray-600 p-2.5 text-sm text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500">
            <option value="2" selected>2 minutes</option>
            <option value="3">3 minutes</option>
            <option value="4">4 minutes</option>
            <option value="5">5 minutes</option>
            <option value="-1">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="first-player-label" for="first-player" class="text-low-contrast-text mb-2 block text-sm font-medium">Qui commence en premier ?</label>
      <div class="relative w-full">
          <select name="f-player" id="first-player" class="bg-ui-bg block w-1/2 rounded-lg border border-gray-600 p-2.5 text-sm text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500">
            <option value="-1">Aleatoire</option>
            <option value="0">Je commence en premier</option>
            <option value="1">L'opposant commence en premier</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="opposant-label" class="text-low-contrast-text mb-2 block text-sm font-medium">Jouer contre qui ?</label>
      <div class="flex">
        <div class="me-5 flex items-center rounded-lg border border-gray-600 px-4 dark:border-gray-700">
          <input id="opposant-ia" type="radio" name="opposant" value="ia" class="size-4 bg-gray-100 accent-amber-400" checked>
          <label for="opposant-ia" class="text-low-contrast-text ms-2 w-full py-3 text-sm font-medium"> IA</label>
        </div>
        <div class="flex items-center rounded-lg border border-gray-600 px-4 dark:border-gray-700">
          <input id="opposant-hotseat" type="radio" name="opposant" value="hotseat" class="size-4 border-gray-300 bg-gray-100 accent-amber-400">
          <label class="text-low-contrast-text ms-2 w-full py-3 text-sm font-medium" for="opposant-hotseat"> Local</label>
        </div>
      </div>
    </div>

    <div class="mt-6 flex w-full items-center justify-center">
      <button type="button" class="mb-2 me-2 rounded-lg bg-yellow-700 px-5 py-2.5 text-base font-medium text-white hover:bg-yellow-600 focus:outline-none focus:ring-4 focus:ring-yellow-900" @click="initGame">PLAY</button>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '../components/modal/Modal.vue';
import { onMounted, onUnmounted, ref } from 'vue';

const generatorModalActive = ref(false)
const endGameModalActive = ref(false)

const message = ref<string | null>(null);
const iaDuration = ref<string | null>(null)
const isError = ref<boolean>(true);
// const errorDescription = ref<string | null>(null);

let gameId: number

let timerPlayer1: number
let timerPlayer2: number

let timePerTurn: number
let currentRoundTimer: number
let currentRoundTurn: string

let isPausedPlayer1 = true
let isPausedPlayer2 = true

let whoStartFirst = 0; // 0 -> white   1 -> black


const toggleGeneratorModal = () => {
  generatorModalActive.value = !generatorModalActive.value;
}
const toggleEndGameModal = () => {
  endGameModalActive.value = !endGameModalActive.value;
}

const initGame = () => {
  toggleGeneratorModal();
  createGrid()
  // fillGridWithList(['W'])
  startGame()
}

const replayGame = () => {
  toggleEndGameModal();
  toggleGeneratorModal();
  // startGame();
}

const createGrid = () => {
  let counter = 0
  document.getElementById('nav-bar').hidden = true
  const gridParentDiv = document.getElementById('board')
  gridParentDiv.innerHTML = ""
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
  gridParentDiv.classList.remove('hidden-important')
}

const fillGridWithList = (list: any, iaSuggestion: any = null, player_turn: any = null) => {
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
    else if (list[i] == ' '){
      circleElement.style.opacity = "0"
    }
    if (iaSuggestion != null && (iaSuggestion[1] * 19 + iaSuggestion[0]) == i) {
      if (player_turn != null) {
        if (player_turn == 'B') {
          circleElement.style.backgroundColor = '#000'
          circleElement.style.opacity = "0.5"
        } else if (player_turn == 'W') {
          circleElement.style.backgroundColor = '#fff'
          circleElement.style.opacity = "0.3"
        } else {
          circleElement.style.backgroundColor = '#bdbfc3'
          circleElement.style.opacity = "0.4"
        }
      } else {
        circleElement.style.backgroundColor = '#bdbfc3'
        circleElement.style.opacity = "0.4"
      }
    }
  }
}

const postRequest = async (url: string, payload: any) => {
  try {
    isError.value = false;
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const response = await fetch(url, {
      method: "POST",
      body: JSON.stringify(payload),
      headers: myHeaders,
    });
    const data = await response.json();
    if (!response.ok) {
      if (data.detail) {
        throw new Error(data.detail);
      } else {
        throw new Error;
      }
    }
    isError.value = false;
    message.value = data.message || '';
    return data;
  } catch (e: any) {
    console.error(e.message);
    isError.value = true;
    message.value = e.message || 'An unknown error occurred';
    return null;
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

const startGame = async () => {
  whoStartFirst = document.getElementById('first-player')?.value
  const gamemode = document.querySelector('input[name="opposant"]:checked')?.value;
  if (whoStartFirst == -1) { whoStartFirst = Math.floor(Math.random() * 2) }
  const payload = {
    "mode": gamemode,
    "main_player": whoStartFirst == 0 ? "B" : "W",
    "IA_suggestion": true,
    "options": {
      "allowed_capture": true,
      "allowed_win_by_capture": true,
      "allowed_double_three": false
    },
    "opening": "standard",
    }
  // if (whoStartFirst == 2) { currentRoundTurn = 1 }
  // else if (whoStartFirst == 0) { currentRoundTurn = Math.floor(Math.random() * 2) }
  // console.log(Math.floor(Math.random() * 2))
  const data = await postRequest("http://127.0.0.1:8000/game/new", payload);
  // console.log(data);
  // console.log(data.board);
  // const data = {
  //  "game_id": 1,
  //  "player_turn": "B",
  // //  "IA": true,
  //  "IA_suggestion": false,
  //  "board": [
  //     [' ', ' ', ' '],
  //     [' ', ' ', ' '],
  //  ]
  // }
  // console.log(data.IA_suggestion)
  fillGridWithList(data.board, data.IA_suggestion, data.player_turn)
  iaDuration.value = data.IA_duration;
  createScoreboard()
  gameId = data.game_id
  currentRoundTurn = data.player_turn
  isPausedPlayer1 = data.isPausedPlayer1;
  isPausedPlayer2 = data.isPausedPlayer2;
  // if (data.player_turn == 'W') {
  //   // hover == black
  //   isPausedPlayer2 = false
  //   // const circleClass = document.getElementsByClassName('circle')
  //   // for (var i = 0; i < circleClass.length; i++ )
  //   //   circleClass[i].style.backgroundColor = '#000000'
  //   // click add permanent black pawn
  //    // inverse round turn

  // }
  // else {
  //   // hover == white
  //   isPausedPlayer1 = false
  // //   const circleClass = document.getElementsByClassName('circle')
  // //   for (var i = 0; i < circleClass.length; i++ )
  // //     circleClass[i].style.backgroundColor = '#FFFFFF'
  // //   // click add permanent black pawn

  // }
  //   // anyway get position of pawn, using i and j, have to add it to id value, separate by '-'
  //   // send api call
}

const addPown = async (event) => {
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
    "player_move": {"x": coordinates[1], "y": coordinates[0]}
  }
  isPausedPlayer1 = !isPausedPlayer1
  isPausedPlayer2 = !isPausedPlayer2
  const data = await postRequest("http://127.0.0.1:8000/game/" + gameId + "/move", payload)
  console.log(data)
  // Handle response
  if (data.status != 'playing')
  {
    fillGridWithList(data.board)
    return handleEndGame()
  }
  if (data.error != null)
    console.log('Placement error')
  if (data.status != "playing")
    console.log('Fin')
  // isPausedPlayer1 = !isPausedPlayer1
  // isPausedPlayer2 = !isPausedPlayer2
  isPausedPlayer1 = data.isPausedPlayer1;
  isPausedPlayer2 = data.isPausedPlayer2;
  if (timePerTurn != -1) {
    clearInterval(currentRoundTimer)
    createCountdownForRound(parseInt(timePerTurn) + 1, 'round-timer')
  }
  currentRoundTurn = data.player_turn
  fillGridWithList(data.board, data.IA_suggestion, data.player_turn)
  iaDuration.value = data.IA_duration;
  // if (currentRoundTurn == 'B') {
  //   // hover == black
  //   const circleClass = document.getElementsByClassName('circle')
  //   for (var i = 0; i < circleClass.length; i++ )
  //   if (circleClass[i].style.opacity == "0") { circleClass[i].style.backgroundColor = '#000' }
  // }
  // else {
  //   // hover == white
  //   const circleClass = document.getElementsByClassName('circle')
  //   for (var i = 0; i < circleClass.length; i++ )
  //   if (circleClass[i].style.opacity == "0") { circleClass[i].style.backgroundColor = '#FFF' }
  // }
}

const handleEndGame = () => {
  clearInterval(timerPlayer1)
  clearInterval(timerPlayer2)
  clearInterval(currentRoundTimer)
  const gridBtn = document.getElementsByClassName('grid-button')
  for (let i = 0; i < gridBtn.length; i++) {
    gridBtn[i].removeEventListener('click', addPown)
  }


  toggleEndGameModal();

  // scoreboard.classList.add('hidden-important')
  // document.getElementById('nav-bar').hidden = false
}

const secondsToMinSeconds = (count: number) => {
  let minutes = Math.floor(count / 60);
  let seconds = count - minutes * 60;
  return [minutes, seconds]
}

const createCountdownPlayer1 = (count: number, timerDivId: string) => {
  timerPlayer1 = setInterval(function() {
    if (!isPausedPlayer1) {
      count -= 0.1;
      const [minutes, seconds] = secondsToMinSeconds(Math.floor(count))
      if (seconds < 10)
        document.getElementById(timerDivId).textContent = minutes + ':0' + seconds
      else
        document.getElementById(timerDivId).textContent = minutes + ':' + seconds
      if (count === 0) {
        clearInterval(timerPlayer1);
        // console.log("Time's up!");
        handlePlayerCountdown();
      }
    }
  }, 100);
}

const createCountdownPlayer2 = (count: number, timerDivId: string) => {
  timerPlayer2 = setInterval(function() {
    if (!isPausedPlayer2) {
      count -= 0.1;
      const [minutes, seconds] = secondsToMinSeconds(Math.floor(count))
      if (seconds < 10)
        document.getElementById(timerDivId).textContent = minutes + ':0' + seconds
      else
        document.getElementById(timerDivId).textContent = minutes + ':' + seconds
      if (count === 0) {
        clearInterval(timerPlayer2);
        // console.log("Time's up!");
        handlePlayerCountdown();
      }
    }
  }, 100);
}

const handlePlayerTimeout = async () => {
  const payload = {
    "who_timeout": currentRoundTurn,
  }
  const data = await postRequest("http://127.0.0.1:8000/game/" + gameId + "/timeout", payload);
  // console.log("TIMEOUT DATA:");
  // console.log(data);
  // Handle response
  if (data.status != 'playing')
    return handleEndGame()
  if (data.error != null)
    console.log('Placement error')
  isPausedPlayer1 = data.isPausedPlayer1;
  isPausedPlayer2 = data.isPausedPlayer2;
  // isPausedPlayer1 = !isPausedPlayer1
  // isPausedPlayer2 = !isPausedPlayer2
  if (timePerTurn != -1) {
    clearInterval(currentRoundTimer)
    createCountdownForRound(parseInt(timePerTurn) + 1, 'round-timer')
  }
  currentRoundTurn = data.player_turn
  // fillGridWithList(data.board)
  fillGridWithList(data.board, data.IA_suggestion, data.player_turn)
  // if (currentRoundTurn == 'B') {
  //   // hover == black
  //   const circleClass = document.getElementsByClassName('circle')
  //   for (var i = 0; i < circleClass.length; i++ )
  //   if (circleClass[i].style.opacity != "1") { circleClass[i].style.backgroundColor = '#000' }
  // }
  // else {
  //   // hover == white
  //   const circleClass = document.getElementsByClassName('circle')
  //   for (var i = 0; i < circleClass.length; i++ )
  //   if (circleClass[i].style.opacity != "1") { circleClass[i].style.backgroundColor = '#FFF' }
  // }
}
const handlePlayerCountdown = async () => {
  const payload = {
    "who_timeout": currentRoundTurn,
  }
  const data = await postRequest("http://127.0.0.1:8000/game/" + gameId + "/countdown", payload);
  if (data.status != 'playing')
    return handleEndGame()
  if (data.error != null)
    console.log('Placement error')
}

const createCountdownForRound = (count: number, timerDivId: string) => {
  currentRoundTimer = setInterval(function() {
      // count--;
      count -= 0.1;
      let second = Math.floor(count)
      if (second < 10)
        document.getElementById(timerDivId).textContent = '00:0' + second
      else
        document.getElementById(timerDivId).textContent = '00:' + second
      if (second === 0) {
        clearInterval(currentRoundTimer);
        handlePlayerTimeout()
      }
  }, 100);
}

onMounted(() => {
  document.getElementById('board').classList.add('hidden-important')
  document.getElementById('scoreboard').classList.add('hidden-important')
  toggleGeneratorModal();
  // toggleEndGameModal();
});

onUnmounted(() => {
  clearInterval(timerPlayer1)
  clearInterval(timerPlayer2)
  clearInterval(currentRoundTimer)
  document.getElementById('nav-bar').hidden = false
});

</script>
