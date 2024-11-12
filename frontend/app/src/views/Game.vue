<template>
  <main class=" text-high-contrast-text container mt-10 flex size-full flex-row justify-center">
    <!-- <div class=" flex flex-col justify-start gap-4 mt-8">
      <h1 class="text-8xl font-bold">GAME</h1>
      <hr class="w-48 h-px bg-gray-200 border-0">
    </div> -->
    <div class=" flex w-full flex-col items-center justify-center">
      <!-- <hr class="w-72 h-px bg-gray-200 border-0"> -->
      <div ref="board" class="grid grid-cols-19 grid-rows-19">

      </div>
      <!-- <div class="absolute top-[9.6rem] size-17 overflow-hidden">
				<img src="../assets/images/gomoku_board.png" alt="Gomoku Board" class=" size-full object-cover">
			</div> -->
    </div>

    <!-- <div class=" flex w-full flex-col items-center justify-end gap-6">
      <div class=" size-17 overflow-hidden">
        <img src="../assets/images/GomokuBoard.png" alt="Gomoku Board" class=" size-full object-cover opacity-25">
      </div>
    </div> -->
  </main>
</template>

<script lang="ts">

export default {
  mounted() {
    this.createGrid();
  },
  methods: {
    createGrid() {
      let counter = 0
      const gridParentDiv = this.$refs.board
      for (let i = 0; i < 19; i++) {
        for (let j = 0; j < 19; j++) {
          const gridElement = document.createElement('div')
          const gridBtn = document.createElement('button')
          gridBtn.classList.add(...['relative', 'grid-button', 'w-10', 'h-10'])
          gridBtn.addEventListener("click", this.addBlackPown)
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
    },

    addBlackPown() {
      console.log("black")
    }
  }
};

</script>
