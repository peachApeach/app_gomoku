<template>
  <main class=" text-high-contrast-text container mt-10 flex size-full flex-row justify-center">
    <!-- <div class=" flex flex-col justify-start gap-4 mt-8">
      <h1 class="text-8xl font-bold">GAME</h1>
      <hr class="w-48 h-px bg-gray-200 border-0">
    </div> -->
    <div class=" flex w-full flex-col items-center justify-center">
      <!-- <hr class="w-72 h-px bg-gray-200 border-0"> -->
      <div ref="board" class="grid grid-cols-19 grid-rows-19 z-50">

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
          // gridBtn.classList.add(...['w-9', 'h-9'])
          gridBtn.classList.add(...['relative', 'grid-button', 'border-solid', 'border', 'border-sky-500', 'w-9', 'h-9'])
          gridElement.classList.add(...['flex', 'items-center', 'justify-center', 'w-10', 'h-10'])

          const hrHorizontal = document.createElement('hr')
          hrHorizontal.classList.add(...['absolute', 'h-px', 'w-10', 'bg-red-600', 'border-0'])
          gridElement.appendChild(hrHorizontal)

          const hrVertical = document.createElement('hr')
          if (i != 0)
            hrVertical.classList.add(...['absolute', 'h-10', 'w-px', 'bg-red-600', 'border-0'])
          else
            hrVertical.classList.add(...['absolute', 'h-5', 'w-px', 'bg-red-600', 'border-0', 'top-0'])
          gridElement.appendChild(hrVertical)
          
          gridElement.appendChild(gridBtn)
          gridParentDiv.appendChild(gridElement)
          counter++
        }
      }
    }
  }
};

</script>
