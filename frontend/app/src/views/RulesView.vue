<template>
  <main class=" container my-auto flex size-full flex-col items-center justify-center gap-24 text-high-contrast-text lg:flex-row">
    <div class=" h-24 w-full lg:hidden">&nbsp;</div>
    <div class=" flex w-full flex-col justify-center gap-7 ">
      <h1 class="text-8xl font-bold">Rules</h1>
      <hr class="h-px w-48 border-0 bg-gray-200">
      <ul class=" list-disc text-start text-lg text-low-contrast-text">

        Objective:
        <li>
          Align five stones in a row (vertically, horizontally, or diagonally) without being captured, or
          Capture five pairs of your opponent’s stones.
        </li><br>

        Capturing:
        <li>
          You can only capture pairs of opponent’s stones.
          A pair consists of exactly two stones placed in a row, and they must be flanked by your stones on both sides.
          Single stones or more than two stones in a row cannot be captured.
        </li><br>

        Free-Three Rule:
        <li>
          A free-three is a sequence of three stones that, if not blocked immediately, creates an indefendable four-stone alignment (i.e., four stones with open ends on both sides).
          To maintain fairness, forming a double-three (two free-threes at the same time) is considered a forbidden move.
          Winning Conditions:
        </li><br>

        Align five stones in a row while respecting the rules above, or
        Capture five pairs of your opponent’s stones to secure victory.

      </ul>
    </div>

    <div class=" flex w-full flex-col items-center justify-end gap-6">
      <div class=" size-17 overflow-hidden">
        <img src="../assets/images/GomokuBoard.png" alt="Gomoku Board" class=" size-full object-cover opacity-25">
      </div>
    </div>
  </main>
</template>
