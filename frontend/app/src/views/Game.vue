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
            <option value="0">10 secondes</option>
            <option value="1">20 secondes</option>
            <option value="2">30 secondes</option>
            <option value="3">40 secondes</option>
            <option value="4">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start gap-4 py-5">
      <label id="min-per-player-label" for="min-per-player" class="text-low-contrast-text">Minutes par joueur</label>
      <div class="relative w-full">
          <select name="min-p-player" id="min-per-player">
            <option value="0">2 minutes</option>
            <option value="1">3 minutes</option>
            <option value="2">4 minutes</option>
            <option value="3">5 minutes</option>
            <option value="4">Illimite</option>
          </select>
      </div>
    </div>

    <div class="flex w-full flex-col items-start gap-4 py-5">
      <label id="first-player-label" for="first-player" class="text-low-contrast-text">Qui commence en premier ?</label>
      <div class="relative w-full">
          <select name="f-player" id="first-player">
            <option value="0">Aleatoire</option>
            <option value="1">Je commence en premier</option>
            <option value="2">L'opposant commence en premier</option>
          </select>
      </div>
    </div>

    <div class="mb-4 mt-6 flex w-full items-center justify-center">
      <button class="text-button px-4 py-2 text-high-contrast-text dark:text-d-high-contrast-text" @click="">PLAY</button>
    </div>
  </Modal>
</template>

<script setup lang="ts">
import Modal from '../components/modal/Modal.vue';
import { onMounted, onUnmounted, ref } from 'vue';

const generatorModalActive = ref(false);

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
      gridBtn.addEventListener("click", addBlackPown)
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

}

const addBlackPown = () => {
  console.log("black")
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
