<template>
  <main class=" container mt-10 flex size-full flex-row justify-center text-high-contrast-text">

    <div v-show="!gridIsCreated" class="flex h-[90vh] w-5/6 flex-col items-center justify-center gap-8 ">
      <h1 class="text-3xl font-bold text-white">Are You Ready?</h1>
      <p class="text-center">
        Challenge your mind and strategy skills in our Gomoku game! Take on the AI or a friend, and see who comes out on top. Will you align five stones or capture five pairs first? The game awaits you!
      </p>
      <button type="button" class="action-button replay-button-shadow z-30 mb-4" @click="toggleGeneratorModal">Play Now!</button>

    </div>

    <div v-show="gridIsCreated" class=" flex w-full flex-col items-center justify-center">
      <div id="scoreboard" class="hidden-important mb-3 flex flex-nowrap items-center gap-32 text-low-contrast-text">

        <div id="player1" class="flex items-center gap-8">
          <div id="player1-timer" class="rounded-lg px-4 py-2 text-lg" :class="player1Color == 'B' ? 'bg-black text-white' : 'bg-white text-black'"></div>
          <div class="flex flex-col gap-0">
            <h1 class="text-nowrap text-center text-2xl font-bold">Player 1</h1>
            <p class="text-nowrap font-medium text-white/60">Captured - {{ player1Color == 'B' ? blackCapture : whiteCapture }}</p>
          </div>
        </div>

        <div id="round-timer" class="px-4 py-2 text-5xl text-high-contrast-text "></div>

        <div id="player2" class="flex items-center gap-8">
          <div class="flex flex-col gap-0">
            <h1 id="player2pseudo" class="text-nowrap text-center text-2xl font-bold"></h1>
            <p class="text-nowrap font-medium text-white/60">Captured - {{ player2Color == 'B' ? blackCapture : whiteCapture }}</p>
          </div>

          <div id="player2-timer" class="rounded-lg px-4 py-2 text-lg" :class="player2Color == 'B' ? 'bg-black text-white' : 'bg-white text-black'"></div>
        </div>
      </div>
      <div class="mb-2 flex w-full flex-col items-center justify-center gap-0">
        <div id="message" class="text-center text-xl font-bold" :class="isError ? 'text-red-500' : 'text-white'">&nbsp;{{ message }}</div>
        <div id="ia-duration" :class="iaDuration != null ? 'opacity-100' : 'opacity-0'" class="text-center text-lg text-high-contrast-text ">IA took {{ iaDuration }} to make its decision</div>
      </div>
      <!-- <div id="error_message" class="text-center text-lg font-bold text-red-500">Consequat officia deserunt deserunt officia laboris. Nostrud laborum nisi id aliqua incididunt commodo velit. Cillum anim ad fugiat ex anim consectetur. Reprehenderit sit labore non est reprehenderit adipisicing sunt enim.</div> -->
       <div class="relative flex w-full flex-col items-center justify-center">
         <div id="board" class="board-shadow grid grid-cols-19 grid-rows-19 rounded-xl bg-board-background">
        </div>
           <button v-show="gameIsEnd" type="button" class=" action-button replay-button-shadow absolute bottom-0 z-30 mb-4" @click="toggleGeneratorModal">Replay</button>

       </div>
    </div>
  </main>


  <Modal :modal-active="endGameModalActive" @close-modal="toggleEndGameModal" :close-button="true">
    <h1 class="mb-5 text-center text-3xl font-bold text-high-contrast-text">End Game</h1>
    <p class="mb-5 text-center text-xl font-bold text-white">{{ message }}</p>
    <!-- <div>
      <p class="text-center text-base font-bold text-white">Black has captured 3 white stones.</p>
      <p class="text-center text-base font-bold text-white">White has captured 3 black stones.</p>
    </div> -->
    <div class="mt-6 flex w-full items-center justify-center">
      <button type="button" class="action-button" @click="replayGame">Replay</button>
    </div>
  </Modal>


  <Modal :modal-active="generatorModalActive" @close-modal="toggleGeneratorModal" :close-button="true">
    <h1 class="mb-2 text-center text-3xl font-bold text-high-contrast-text">Settings</h1>

    <div class="flex w-full flex-col items-start py-3">
      <label id="time-per-turn-label" for="time-per-turn" class="mb-2 block text-sm font-bold text-low-contrast-text">Time per turn</label>
      <div class="relative w-full">
          <select name="time-p-turn" id="time-per-turn" class="block w-full rounded-lg border-2 border-gray-600 bg-ui-bg p-2.5 text-sm font-bold text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500">
            <option value="10">10 seconds</option>
            <option value="20">20 seconds</option>
            <option value="30">30 seconds</option>
            <option value="40" selected>40 seconds</option>
            <option value="-1">Unlimited</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-3">
      <label id="min-per-player-label" for="min-per-player" class="mb-2 block text-sm font-bold text-low-contrast-text">Minutes per player</label>
      <div class="relative w-full">
          <select name="min-p-player" id="min-per-player" class="block w-full rounded-lg border-2 border-gray-600 bg-ui-bg p-2.5 text-sm font-bold text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500">
            <option value="2">2 minutes</option>
            <option value="3">3 minutes</option>
            <option value="4">4 minutes</option>
            <option value="5" selected>5 minutes</option>
            <option value="-1">Unlimited</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-5">
      <label id="opposant-label" class="mb-2 block text-sm font-bold text-low-contrast-text">Rules</label>
      <div class="flex w-full">
        <button @click="rules_capturing = !rules_capturing" class="input-radio-opponent me-5" :class="rules_capturing ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="rules_capturing ? 'highlight-text-opponent' : 'text-white'">Capturing stones</p>
        </button>
        <button @click="rules_win_by_capture = !rules_win_by_capture" class="input-radio-opponent me-5" :class="rules_win_by_capture ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="rules_win_by_capture ? 'highlight-text-opponent' : 'text-white'">Winning by capture</p>
        </button>
        <button @click="rules_double_three = !rules_double_three" class="input-radio-opponent" :class="rules_double_three ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="rules_double_three ? 'highlight-text-opponent' : 'text-white'">Creating double threes</p>
        </button>
      </div>
    </div>


    <div class="flex w-full flex-col items-start py-3">
      <label id="opposant-label" class="mb-2 block text-sm font-bold text-low-contrast-text">IA suggestion?</label>
      <div class="flex w-full">
        <div @click="eventSwitchIaSuggestion('no')" class="input-radio-opponent me-5" :class="!iaSuggestion ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="!iaSuggestion ? 'highlight-text-opponent' : 'text-white'">No</p>
        </div>
        <div @click="eventSwitchIaSuggestion('yes')" class="input-radio-opponent" :class="iaSuggestion ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="iaSuggestion ? 'highlight-text-opponent' : 'text-white'">Yes</p>
        </div>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-3">
      <label id="opposant-label" class="mb-2 block text-sm font-bold text-low-contrast-text">Mode</label>
      <div class="flex w-full">
        <div @click="eventSwitchMode('IA')" class="input-radio-opponent me-5" :class="displayModalWhoStart ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="displayModalWhoStart ? 'highlight-text-opponent' : 'text-white'">IA</p>
          <!-- <input id="opposant-ia" type="radio" name="opposant" value="ia" class="size-4" checked>
          <label for="opposant-ia" >IA</label> -->
        </div>
        <div @click="eventSwitchMode('hotseat')" class="input-radio-opponent" :class="!displayModalWhoStart ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="!displayModalWhoStart ? 'highlight-text-opponent' : 'text-white'">Local</p>
          <!-- <input id="opposant-hotseat" type="radio" name="opposant" value="hotseat" class="size-4">
          <label class="  py-3 text-sm font-bold" for="opposant-hotseat" :class="!displayModalWhoStart ? 'highlight-text-opponent' : 'text-white'">Local</label> -->
        </div>
      </div>
    </div>

    <div class="flex w-full flex-col items-start py-3" :class="displayModalWhoStart ? 'opacity-100' : 'opacity-0'">
      <label id="first-player-label" for="first-player" class="mb-2 block text-sm font-bold text-low-contrast-text">Who plays first?</label>
      <div class="relative w-full">
          <select name="f-player" id="first-player" class="block w-full rounded-lg border-2 border-gray-600 bg-ui-bg p-2.5 text-sm font-bold text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500" :disabled="displayModalWhoStart == false">
            <option value="-1">Random</option>
            <option value="0">I start first</option>
            <option value="1">Opponent start first</option>
          </select>
      </div>
    </div>


    <!-- <div class="flex w-full flex-col items-start py-5" :class="displayModalWhoStart ? 'opacity-100' : 'opacity-0'">
      <label id="opposant-label" class="mb-2 block text-sm font-bold text-low-contrast-text">Algorithm Depth <span class=" font-light text-gray-600">(Response time < {{ iaDifficultyResponseTime }})</span> </label>
      <div class="flex w-full">
        <button @click="eventSwitchDifficulty('easy')" :disabled="displayModalWhoStart == false" class="input-radio-opponent me-5" :class="iaDifficulty == 'easy' ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="iaDifficulty == 'easy' ? 'highlight-text-opponent' : 'text-white'">2</p>
        </button>
        <button @click="eventSwitchDifficulty('medium')" :disabled="displayModalWhoStart == false" class="input-radio-opponent me-5" :class="iaDifficulty == 'medium' ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="iaDifficulty == 'medium' ? 'highlight-text-opponent' : 'text-white'">6</p>
        </button>
        <button @click="eventSwitchDifficulty('hard')" :disabled="displayModalWhoStart == false" class="input-radio-opponent" :class="iaDifficulty == 'hard' ? 'highlight-radio-opponent' : ''">
          <p class=" py-3 text-sm font-bold" :class="iaDifficulty == 'hard' ? 'highlight-text-opponent' : 'text-white'">10</p>
        </button>
      </div>
    </div> -->


    <div class="mt-6 flex w-full items-center justify-center">
      <button type="button" class="action-button mb-2 me-2" @click="initGame">Play</button>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '../components/modal/DefaultModal.vue';
import { onMounted, onUnmounted, ref } from 'vue';

const generatorModalActive = ref(false)
const endGameModalActive = ref(false)

const baseUrl = import.meta.env.VITE_API_URL;;

const gridIsCreated = ref(false)

const displayModalWhoStart = ref(true);
const iaSuggestion = ref(false);

const iaDifficulty = ref<string>("easy");
const iaDifficultyResponseTime = ref<string>("500ms");

const rules_capturing = ref<boolean>(true);
const rules_win_by_capture = ref<boolean>(true);
const rules_double_three = ref<boolean>(false);

const gameIsEnd = ref(false);

const message = ref<string | null>(null);
const iaDuration = ref<string | null>(null)

const blackCapture = ref<number | null>(null);
const whiteCapture = ref<number | null>(null);

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

let isTimeout = false
let isCountdown = false

const player1Color = ref<string | null>("B");
const player2Color = ref<string | null>("W");

let isPownHandling = false

let whoStartFirst = 0; // 0 -> white   1 -> black


const toggleGeneratorModal = () => {
  generatorModalActive.value = !generatorModalActive.value;
}
const toggleEndGameModal = () => {
  endGameModalActive.value = !endGameModalActive.value;
}

const initGame = () => {
  gameIsEnd.value = false;
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
  gridIsCreated.value = true
  document.getElementById('nav-bar').hidden = true
  const gridParentDiv = document.getElementById('board')
  gridParentDiv.innerHTML = ""
  for (let i = 0; i < 19; i++) {
    for (let j = 0; j < 19; j++) {
      const gridElement = document.createElement('div')
      const gridBtn = document.createElement('button')
      gridBtn.classList.add(...['relative', 'grid-button', 'w-9', 'h-9'])
      gridBtn.id = i.toString() + '-' + j.toString()
      gridBtn.addEventListener("click", addPown)
      // gridBtn.classList.add(...['relative', 'grid-button', 'border-solid', 'border', 'border-sky-500', 'w-10', 'h-10'])
      gridElement.classList.add(...['relative', 'flex', 'items-center', 'justify-center', 'w-9', 'h-9', 'grid-div'])

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

      hrHorizontal.classList.add(...['board-line-style'])
      hrVertical.classList.add(...['board-line-style'])

      const hoverCircle = document.createElement('div')
      hoverCircle.classList.add(...['circle', 'absolute', 'group-hover:block'])
      hoverCircle.id = i.toString() + '-' + j.toString() + '-circle'
      gridBtn.appendChild(hoverCircle)

      gridElement.appendChild(hrVertical)
      gridElement.appendChild(hrHorizontal)

      gridElement.appendChild(gridBtn)
      gridParentDiv.appendChild(gridElement)
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
    if (!circleElement) {
      continue ;
    }
    if (list[i] == 'W') {
      circleElement.style.backgroundColor = '#EFEFEF'
      circleElement.style.opacity = "1"
      circleElement.classList.add("white-stone-shadow");
      circleElement.classList.add("animate-stone-placement");
    }
    else if (list[i] == 'B'){
      circleElement.style.backgroundColor = '#232323'
      circleElement.style.opacity = "1"
      circleElement.classList.add("black-stone-shadow");
      circleElement.classList.add("animate-stone-placement");
    }
    else if (list[i] == ' '){
      circleElement.classList.remove("black-stone-shadow");
      circleElement.classList.remove("white-stone-shadow");
      circleElement.classList.remove("animate-stone-placement");
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
    // isError.value = false;
    // message.value = '';
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
  // const gamemode = document.querySelector('input[name="opposant"]:checked')?.value;
  const gamemode = displayModalWhoStart.value == true ? 'ia' : 'hotseat';

  document.getElementById('player1-timer').textContent = minPerPlayer != -1 ? '0' + minPerPlayer + ':00' : 'XX:XX'
  document.getElementById('player2-timer').textContent = minPerPlayer != -1 ? '0' + minPerPlayer + ':00' : 'XX:XX'
  document.getElementById('round-timer').textContent = timePerTurn != -1 ? '00:' + timePerTurn : ''
  document.getElementById('player2pseudo').textContent = gamemode == 'ia' ? 'Robot' : 'Player 2'

  if (minPerPlayer != -1) {
    createCountdownPlayer1(parseInt(minPerPlayer) * 60, 'player1-timer')
    createCountdownPlayer2(parseInt(minPerPlayer) * 60, 'player2-timer')
  }
  if (timePerTurn != -1) {
    createCountdownForRound(parseInt(timePerTurn), 'round-timer')
  }
  scoreboard.classList.remove('hidden-important')
}

const startGame = async () => {
  isTimeout = false
  isCountdown = false
  isPownHandling = false
  whoStartFirst = document.getElementById('first-player')?.value
  // const gamemode = document.querySelector('input[name="opposant"]:checked')?.value;
  const gamemode = displayModalWhoStart.value == true ? 'ia' : 'hotseat';
  if (whoStartFirst == -1) { whoStartFirst = Math.floor(Math.random() * 2) }
  const payload = {
    "mode": gamemode,
    "main_player": whoStartFirst == 0 ? "B" : "W",
    "IA_suggestion": iaSuggestion.value,
    "options": {
      "allowed_capture": rules_capturing.value,
      "allowed_win_by_capture": rules_win_by_capture.value,
      "allowed_double_three": rules_double_three.value
    },
    "opening": "standard",
    "difficulty": iaDifficulty.value
    }
  // if (whoStartFirst == 2) { currentRoundTurn = 1 }
  // else if (whoStartFirst == 0) { currentRoundTurn = Math.floor(Math.random() * 2) }
  // console.log(Math.floor(Math.random() * 2))
  const data = await postRequest(baseUrl + "/game/new", payload);
  // console.log(iaDifficulty.value);
  // console.log(data);
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
  player1Color.value = data.player1_color
  player2Color.value = data.player2_color

  fillGridWithList(data.board, data.IA_suggestion, data.player_turn)
  iaDuration.value = data.IA_duration;
  blackCapture.value = data.black_capture;
  whiteCapture.value = data.white_capture;
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
  if (isPownHandling == true) {
    console.log("Pown is pending...")
    return ;
  }
  isPownHandling = true;
  let pawnId = event.target.id
  if (event.target.localName == 'button')
    pawnId += '-circle'
  // console.log(pawnId)
  const pawnCircle = document.getElementById(pawnId)
  if (pawnCircle.style.opacity == "1") {
    isPownHandling = false;
    return
  }
  const coordinates = [pawnId.split('-')[0], pawnId.split('-')[1]]
  const payload = {
    "player_move": {"x": coordinates[1], "y": coordinates[0]},
    "game_id": gameId
  }
  let data = await postRequest(baseUrl + "/game/move", payload)
  if (!data) {
    isPownHandling = false;
    return ;
  }
  isPausedPlayer1 = !isPausedPlayer1
  isPausedPlayer2 = !isPausedPlayer2
  if (data.status != 'playing')
  {
    fillGridWithList(data.board)
    blackCapture.value = data.black_capture;
    whiteCapture.value = data.white_capture;
    isPownHandling = false;
    return handleEndGame()
  }
  if (data.error != null)
    console.log('Placement error')

  fillGridWithList(data.board);
  // console.log(data)
  if (data.IA_response) {
    if (timePerTurn != -1) {
      clearInterval(currentRoundTimer)
      createCountdownForRound(parseInt(timePerTurn), 'round-timer')
    }
    currentRoundTurn = data.player_turn;
    if (iaDifficulty.value == 'easy') {
      await new Promise(r => setTimeout(r, 300));
    }
    data = await postRequest(baseUrl + "/game/IA_response", {
      "game_id": gameId
    });
    // console.log(data)
    if (isTimeout == true) {
      // console.log('here')
      return ;
    } else if (isCountdown == true) {
      return ;
    }
    // console.log("HER3", data);
    if (!data) {
      isPownHandling = false;
      return ;
    }
    // fillGridWithList(data.before_IA_board)
    if (data.status != 'playing')
    {
      fillGridWithList(data.board)
      blackCapture.value = data.black_capture;
      whiteCapture.value = data.white_capture;
      isPownHandling = false;
      return handleEndGame()
    }
    message.value = data.message;
  }
  // if (data.before_IA_board) {
  //   if (timePerTurn != -1) {
  //     clearInterval(currentRoundTimer)
  //     createCountdownForRound(parseInt(timePerTurn), 'round-timer')
  //   }
  //   fillGridWithList(data.before_IA_board)
  //   await new Promise(r => setTimeout(r, 600));
  //   message.value = data.message_after_IA;
  // }
  isPausedPlayer1 = data.isPausedPlayer1;
  isPausedPlayer2 = data.isPausedPlayer2;
  if (timePerTurn != -1) {
    clearInterval(currentRoundTimer)
    createCountdownForRound(parseInt(timePerTurn), 'round-timer')
  }
  currentRoundTurn = data.player_turn
  fillGridWithList(data.board, data.IA_suggestion, data.player_turn)
  iaDuration.value = data.IA_duration;
  blackCapture.value = data.black_capture;
  whiteCapture.value = data.white_capture;
  isPownHandling = false;
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
  gameIsEnd.value = true;
  clearInterval(timerPlayer1)
  clearInterval(timerPlayer2)
  clearInterval(currentRoundTimer)
  const gridBtn = document.getElementsByClassName('grid-button')
  for (let i = 0; i < gridBtn.length; i++) {
    gridBtn[i].removeEventListener('click', addPown)
  }


  toggleEndGameModal();
  // document.getElementById('nav-bar').hidden = false;

  // scoreboard.classList.add('hidden-important')
  // document.getElementById('nav-bar').hidden = false
}

const secondsToMinSeconds = (count: number) => {
  let minutes = Math.floor(count / 60);
  let seconds = count - minutes * 60;
  return [minutes, seconds]
}

const createCountdownPlayer1 = (count: number, timerDivId: string) => {
  // count += 1
  timerPlayer1 = setInterval(function() {
    if (!isPausedPlayer1) {
      count -= 0.1;
      const [minutes, seconds] = secondsToMinSeconds(Math.floor(count))
      if (seconds < 10)
        document.getElementById(timerDivId).textContent = minutes + ':0' + seconds
      else
        document.getElementById(timerDivId).textContent = minutes + ':' + seconds
      if (minutes <= 0 && seconds <= 0) {
        clearInterval(timerPlayer1);
        // console.log("Time's up!");
        handlePlayerCountdown();
      }
    }
  }, 100);
}

const createCountdownPlayer2 = (count: number, timerDivId: string) => {
  // count += 1
  timerPlayer2 = setInterval(function() {
    if (!isPausedPlayer2) {
      count -= 0.1;
      const [minutes, seconds] = secondsToMinSeconds(Math.floor(count))
      if (seconds < 10)
        document.getElementById(timerDivId).textContent = minutes + ':0' + seconds
      else
        document.getElementById(timerDivId).textContent = minutes + ':' + seconds
      if (minutes <= 0 && seconds <= 0) {
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
    "game_id": gameId
  }
  let data = await postRequest(baseUrl + "/game/timeout", payload);
  // console.log("TIMEOUT DATA:");
  // console.log(data);
  // Handle response
  if (data.status != 'playing')
  {
    fillGridWithList(data.board)
    blackCapture.value = data.black_capture;
    whiteCapture.value = data.white_capture;
    isPownHandling = false;
    return handleEndGame()
  }
  if (data.error != null)
  {
    console.log('Placement error')
  }
  isPausedPlayer1 = !isPausedPlayer1
  isPausedPlayer2 = !isPausedPlayer2
  fillGridWithList(data.board);
  if (data.IA_response) {
    if (timePerTurn != -1) {
      clearInterval(currentRoundTimer)
      createCountdownForRound(parseInt(timePerTurn), 'round-timer')
    }
    currentRoundTurn = data.player_turn
    if (iaDifficulty.value == 'easy') {
      await new Promise(r => setTimeout(r, 200));
    }
    data = await postRequest(baseUrl + "/game/IA_response", {
      "game_id": gameId
    });
    if (isTimeout == true) {
      return ;
    } else if (isCountdown == true) {
      return ;
    }
    isTimeout = false
    if (!data) {
      isPownHandling = false;
      return ;
    }
    // fillGridWithList(data.before_IA_board)
    if (data.status != 'playing')
    {
      fillGridWithList(data.board)
      blackCapture.value = data.black_capture;
      whiteCapture.value = data.white_capture;
      isPownHandling = false;
      return handleEndGame()
    }
    message.value = data.message;
  }
  // if (data.before_IA_board) {
  //   if (timePerTurn != -1) {
  //     clearInterval(currentRoundTimer)
  //     createCountdownForRound(parseInt(timePerTurn), 'round-timer')
  //   }
  //   fillGridWithList(data.before_IA_board)
  //   await new Promise(r => setTimeout(r, 600));
  //   message.value = data.message_after_IA;
  // }
  isPausedPlayer1 = data.isPausedPlayer1;
  isPausedPlayer2 = data.isPausedPlayer2;
  // isPausedPlayer1 = !isPausedPlayer1
  // isPausedPlayer2 = !isPausedPlayer2
  if (timePerTurn != -1) {
    clearInterval(currentRoundTimer)
    createCountdownForRound(parseInt(timePerTurn), 'round-timer')
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
    "game_id": gameId
  }
  isCountdown = true;
  const data = await postRequest(baseUrl + "/game/countdown", payload);
  if (data.status != 'playing')
    return handleEndGame()
  if (data.error != null)
    console.log('Placement error')
}

const createCountdownForRound = (count: number, timerDivId: string) => {
  currentRoundTimer = setInterval(function() {
      count -= 0.1;
      let second = Math.floor(count)
      if (second < 10)
        document.getElementById(timerDivId).textContent = '00:0' + second
      else
        document.getElementById(timerDivId).textContent = '00:' + second
      if (second <= 0) {
        clearInterval(currentRoundTimer);
        handlePlayerTimeout()
      }
  }, 100);
}

const eventSwitchMode = (mode: string) => {
  if (mode == "hotseat") {
    displayModalWhoStart.value = false
  } else {
    displayModalWhoStart.value = true
  }
}

const eventSwitchIaSuggestion = (suggestion: string) => {
  if (suggestion == "yes") {
    iaSuggestion.value = true
  } else {
    iaSuggestion.value = false
  }
}

const eventSwitchDifficulty = (difficulty: string) => {
  iaDifficulty.value = difficulty
  if (difficulty == "easy") {
    iaDifficultyResponseTime.value = "500ms"
  } else if (difficulty == "medium") {
    iaDifficultyResponseTime.value = "6s"
  } else if (difficulty == "hard") {
    iaDifficultyResponseTime.value = "9s"
  }
}

onMounted(() => {
  document.getElementById('board').classList.add('hidden-important')
  document.getElementById('scoreboard').classList.add('hidden-important')
  // toggleGeneratorModal();

  // createGrid()
  // createScoreboard();
  // blackCapture.value = 3;
  // whiteCapture.value = 2;
  // fillGridWithList([
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," ","W","B","B"," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," ","W"," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," ","W"," ","W"," ","W"," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// 	[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	// ])


});

onUnmounted(() => {
  clearInterval(timerPlayer1)
  clearInterval(timerPlayer2)
  clearInterval(currentRoundTimer)
  document.getElementById('nav-bar').hidden = false
});

</script>
