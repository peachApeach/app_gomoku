<template>
  <main class=" text-high-contrast-text container my-auto flex size-full flex-row items-center justify-center gap-24">

      <div class=" flex w-full flex-col justify-center gap-7">
        <h1 class="text-8xl text-amber-400">GOMOKU<span class="text-high-contrast-text font-bold"> GAME</span></h1>
        <hr class=" h-px border-0 bg-gray-200">
        <p class=" text-low-contrast-text text-start text-2xl font-medium">
          Challenge yourself with our Gomoku game!<br>
          Take on our smart AI or settle friendly rivalries with your friends.<br>
          Are you ready to prove your strategy skills and claim victory?</p>
        <button @click="routerTo('/game')" type="button" class=" action-button w-40">Get started!</button>
      </div>

      <div class=" flex w-full flex-col items-center justify-end gap-6">
        <div class=" size-17 overflow-hidden">
					<img src="../assets/images/GomokuBoard.png" alt="Gomoku Board" class=" size-full object-cover">
				</div>
      </div>

    <!-- <div class="flex w-full flex-col items-center justify-center gap-6">
      <h1 class="text-2xl font-bold">Test Overview</h1>
      <p class=" text-low-contrast-text text-center">Excepteur fugiat excepteur occaecat sint id reprehenderit excepteur nulla non ipsum. Pariatur aute sunt laboris tempor proident proident exercitation ad nisi deserunt sit dolor labore. Enim consectetur est est non id veniam aliquip elit exercitation. Ex aliqua duis enim incididunt incididunt.</p>
    </div> -->

    <!-- <div class="flex w-full flex-col items-center justify-center gap-6">
      <h1 class="text-2xl font-bold">Test Execution</h1>
      <div class="flex w-full flex-col items-center justify-center gap-3">
        <label for="test-input">Lorem ipsum :</label>
        <input type="text" id="test-input" required class="form-input form-input-border w-5/6">
        <button @click="makeRequests"
							class="border-accent-color text-high-contrast-text hover:bg-accent-color dark:text-d-high-contrast-text group flex flex-row items-center gap-1.5 rounded-full border-2 px-6 py-2 transition-colors">
							<span class=" font-semibold transition-colors group-hover:text-white">Submit</span>
					</button>
      </div>
      <div>
        <h1 class=" text-xl font-semibold">API Result</h1>

        <p id="api_result"></p>
      </div>
    </div> -->
    <!-- <TheWelcome /> -->
  </main>
</template>

<script setup lang="ts">

// const makeRequests = async () => {
//   console.log("Yo !");
//   const input: HTMLElement | null = document.getElementById("test-input");

//   let text: String = '';
//   if (input) {
//     text = input.value;
//   }
//   const url = "http://127.0.0.1:8000/test";

//   try {
//         const response = await fetch(url, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({name: text}),
//         });

//         const result = await response.json();
//         console.log("Response from FastAPI:", result);
//         const api_result = document.getElementById("api_result");
//         if (api_result) {
//           api_result.innerHTML = result.message;
//         }
//     } catch (error) {
//         console.error("Error:", error);
//     }
// };

import { useRouter } from 'vue-router';

const router = useRouter();

const routerTo = (link: String) => {
	router.push(`${link}`);
}

</script>
