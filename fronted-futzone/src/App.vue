<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/authStore'

import DefaultLayout from './layouts/DefaultLayout.vue'
import AuthLayout from './layouts/AuthLayout.vue'

const route = useRoute()
const router = useRouter()
const isReady = ref(false)

const auth = useAuthStore()

onMounted(async () => {
  const auth = useAuthStore()
  await auth.init() 
  isReady.value = true
})
const layoutComponent = computed(() => {
  switch (route.meta.layout) {
    case 'auth':
      return AuthLayout
    case 'default':
      return DefaultLayout
    default:
      return null
  }
})
</script>

<template>
  <component v-if="isReady && layoutComponent" :is="layoutComponent">
    <router-view />
  </component>

  <router-view v-if="isReady && !layoutComponent" />
</template>
