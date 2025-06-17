<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import BaseInput from '../../components/ui/BaseInput.vue'

const email = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

const errorMessage = computed(() => auth.error)

const handleLogin = async () => {
  auth.error = null
  const success = await auth.login(email.value, password.value)
  if (success) {
    router.push('/canchas')
  }
}
</script>

<template>
  <div class="w-full max-w-md p-8 space-y-5">
    <div class="text-center">
      <img src="/logo.png" alt="Logo" class="w-24 mx-auto mb-4" />
      <h1 class="text-xl md:text-2xl xl:text-3xl font-bold text-[#19296D]">
        Inicia sesión en tu cuenta
      </h1>
    </div>

    <BaseInput
      v-model="email"
      type="email"
      label="Correo"
      placeholder="mail@example.com"
      icon="fa-envelope"
      @input="auth.error = null"
    />

    <BaseInput
      v-model="password"
      type="password"
      label="Contraseña"
      placeholder="********"
      icon="fa-lock"
      @input="auth.error = null"
    />

    <button
      @click="handleLogin"
      class="w-full bg-[#19296D] text-white py-2 rounded hover:bg-blue-900 transition"
    >
      Login
    </button>

    <p v-if="errorMessage" class="text-red-500 text-sm text-center">
      {{ errorMessage }}
    </p>

    <p class="text-center text-sm mt-4">
      ¿No tienes cuenta?
      <router-link to="/register" class="text-[#19296D] font-medium hover:underline">
        Regístrate aquí
      </router-link>
    </p>
  </div>
</template>
