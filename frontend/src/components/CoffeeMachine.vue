<script setup>
import { ref, onMounted } from 'vue'

const state = ref({ water_ml: 0, coffee_g: 0, water_capacity_ml: 2000, coffee_capacity_g: 500 })
const message = ref('')
const error = ref('')

// start blank so placeholders are visible
const fillWater = ref('')
const fillCoffee = ref('')
const recipes = ref({})

async function api(path, options={}) {
  try {
    const res = await fetch(`/api${path}`, {
      headers: { 'Content-Type': 'application/json' },
      ...options
    })
    const body = await res.json().catch(() => ({}))
    if (!res.ok) {
      let msg = 'Unexpected error'
      if (typeof body?.detail === 'string') msg = body.detail
      else if (Array.isArray(body?.detail) && body.detail[0]?.msg) msg = body.detail[0].msg
      error.value = msg
      message.value = ''
      return null
    }
    error.value = ''
    return body
  } catch (err) {
    error.value = err.message || 'Network error'
    message.value = ''
    return null
  }
}

async function refresh() {
  const body = await api('/status')
  if (body) state.value = body
}

async function brew(type) {
  const body = await api('/brew', { method:'POST', body: JSON.stringify({ type }) })
  if (body) { message.value = body.message; state.value = body.state }
}

async function doFillWater() {
  const val = String(fillWater.value ?? '').trim()
  const amt = Number(val)
  if (!val) { error.value = 'Please enter a water amount (ml).'; return }
  if (!Number.isFinite(amt) || amt <= 0) { error.value = 'Water amount must be greater than 0 ml.'; return }
  const body = await api('/fill/water', { method:'POST', body: JSON.stringify({ amount_ml: amt }) })
  if (body) { message.value = body.message; state.value = body.state; fillWater.value = '' }
}

async function doFillCoffee() {
  const val = String(fillCoffee.value ?? '').trim()
  const amt = Number(val)
  if (!val) { error.value = 'Please enter a coffee amount (g).'; return }
  if (!Number.isFinite(amt) || amt <= 0) { error.value = 'Coffee amount must be greater than 0 g.'; return }
  const body = await api('/fill/coffee', { method:'POST', body: JSON.stringify({ amount_g: amt }) })
  if (body) { message.value = body.message; state.value = body.state; fillCoffee.value = '' }
}

onMounted(async () => {
  await refresh()
  recipes.value = await api('/recipes') || {}
})
</script>
<template>
  <div class="row" style="margin-top: .5rem; gap: .5rem;">
    <button class="primary" @click="brew('espresso')">Make Espresso</button>
    <button class="primary" @click="brew('double_espresso')">Make Double Espresso</button>
    <button class="primary" @click="brew('americano')">Make Americano</button>
    <button class="primary" @click="brew('ristretto')">Make Ristretto</button>
  </div>

  <div class="row" style="margin-top: 1rem;">
    <input type="number" v-model="fillWater" placeholder="Water (ml)" min="1" inputmode="numeric" />
    <button @click="doFillWater">Fill Water</button>

    <input type="number" v-model="fillCoffee" placeholder="Coffee (g)" min="1" inputmode="numeric" />
    <button @click="doFillCoffee">Fill Coffee</button>
  </div>


  <div class="status">
    <strong>Status</strong>
    <div>Water: {{ state.water_ml }} / {{ state.water_capacity_ml }} ml</div>
    <div>Coffee: {{ state.coffee_g }} / {{ state.coffee_capacity_g }} g</div>
    <details style="margin-top:.75rem;">
  <summary>Show recipes</summary>
    <div class="recipes-grid">
        <div class="recipe-card" v-for="(val, key) in recipes" :key="key">
        <div class="recipe-title">{{ key.replace('_',' ').replace(/\b\w/g, c => c.toUpperCase()) }}</div>
        <div class="recipe-pills">
            <span class="pill">Water: {{ val.water_ml }} ml</span>
            <span class="pill">Coffee: {{ val.coffee_g }} g</span>
        </div>
        </div>
    </div>
    </details>
  </div>

  <div v-if="message" class="msg">{{ message }}</div>
  <div v-if="error" class="msg error">Error: {{ error }}</div>
</template>
