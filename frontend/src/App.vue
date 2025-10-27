<template>
  <div class="card">
    <h1>☕ Coffee Machine <span class="badge">FastAPI + Vue</span></h1>
    <CoffeeMachine/>
    <footer style="margin-top:1rem;opacity:.7">Recipes from machine requirements. State persists per backend config.</footer>
  </div>
</template>

<script setup>
import CoffeeMachine from './components/CoffeeMachine.vue'
</script>
