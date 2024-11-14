<template>
  <main class=" text-high-contrast-text container mt-10 flex size-full flex-row justify-center">
    <div class=" flex w-full flex-col items-center justify-center">
      <div id="board" class="grid grid-cols-19 grid-rows-19">
      </div>
    </div>
    <!-- Bouton pour ouvrir la modal -->
    <button class="icon-button" @click="toggleGeneratorModal">
      <p>OPEN MODAL</p>
    </button>
  </main>
  <Modal :modal-active="generatorModalActive" @close-modal="toggleGeneratorModal">
    <h1 class="text-center text-xl font-extrabold text-high-contrast-text">
      Game Settings</h1>

    <div class="flex w-full flex-col items-start gap-4 py-5">
      <label id="time-per-turn-label" for="time-per-turn" class="text-low-contrast-text">Temps par tour</label>
      <div class="relative w-full">
          <select name="time-p-turn" id="time-per-turn">
            <option value="10">10 secondes</option>
            <option value="20">20 secondes</option>
            <option value="30">30 secondes</option>
            <option value="40" selected>40 secondes</option>
            <option value="-1">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start gap-4 py-5">
      <label id="min-per-player-label" for="min-per-player" class="text-low-contrast-text">Minutes par joueur</label>
      <div class="relative w-full">
          <select name="min-p-player" id="min-per-player">
            <option value="2">2 minutes</option>
            <option value="3">3 minutes</option>
            <option value="4">4 minutes</option>
            <option value="5" selected>5 minutes</option>
            <option value="-1">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start gap-4 py-5">
      <label id="first-player-label" for="first-player" class="text-low-contrast-text">Qui commence en premier ?</label>
      <div class="relative w-full">
          <select name="f-player" id="first-player">
            <option value="-1">Aleatoire</option>
            <option value="0">Je commence en premier</option>
            <option value="1">L'opposant commence en premier</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start gap-4 py-5">
      <label id="opposant-label" class="text-low-contrast-text">Jouer contre qui ?</label>
      <div class="relative w-full">
        <input type="radio" name="opposant" value="ia">
        <label class="text-low-contrast-text" for="opposant">IA</label>
        <br>
        <input type="radio" name="opposant" value="hotseat">
        <label class="text-low-contrast-text" for="opposant">Local</label>
      </div>
    </div>

    <div class="mb-4 mt-6 flex w-full items-center justify-center">
      <button class="text-button px-4 py-2 text-high-contrast-text dark:text-d-high-contrast-text" @click="initGame">PLAY</button>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '../components/modal/Modal.vue';
import { onMounted, onUnmounted, ref } from 'vue';

const generatorModalActive = ref(false);
var currentRoundTurn = 0; // 0 -> white   1 -> black

const toggleGeneratorModal = () => {
  generatorModalActive.value = !generatorModalActive.value;
}

const createGrid = () => {
  let counter = 0
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

const initGame = () => {
  toggleGeneratorModal()
  createGrid()
  startGame()
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

const startGame = () => {
  const timePerTurn = document.getElementById('time-per-turn')?.value
  const minPerPlayer = document.getElementById('min-per-player')?.value
  let whoStartFirst = document.getElementById('first-player')?.value
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
  const data = postRequest("http://127.0.0.1:8000/game/new", payload)
  if (currentRoundTurn) {
    // hover == black 
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
      circleClass[i].style.backgroundColor = '#000000'
    // click add permanent black pawn
     // inverse round turn

  }
  else {
    // hover == white
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
  pawnCircle.style.opacity = "1"
  if (currentRoundTurn) {
    // add black pawn
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
      if (circleClass[i].style.opacity != "1") { circleClass[i].style.backgroundColor = '#FFFFFF' }
  }
  else {
    // add white pawn
    const circleClass = document.getElementsByClassName('circle')
    for (var i = 0; i < circleClass.length; i++ )
      if (circleClass[i].style.opacity != "1") { circleClass[i].style.backgroundColor = '#000000' }
  }
  currentRoundTurn = 1 - currentRoundTurn
}

const addWhitePown = () => {
  console.log("white")
}

const openModal = () => {

}

onMounted(() => {
  // createGrid();
});

</script>
