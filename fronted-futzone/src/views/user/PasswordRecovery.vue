<template>
  <div class="max-w-md mx-auto p-6 space-y-4">
    <h2 class="text-2xl font-bold text-center">Recuperar contraseña</h2>

    <BaseInput
      v-model="email"
      type="email"
      label="Correo electrónico"
      placeholder="tu@correo.com"
      icon="fa-envelope"
      @input="clearMessage"
    />

    <button
      @click="handleRecovery"
      class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
    >
      Enviar enlace de recuperación
    </button>

    <p v-if="message" :class="messageClass">{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../stores/authStore'
import BaseInput from '../../components/ui/BaseInput.vue'

const email = ref('')
const message = ref('')
const isError = ref(false)
const auth = useAuthStore()

const clearMessage = () => {
  message.value = ''
  isError.value = false
}

const handleRecovery = async () => {
  clearMessage()
  const ok = await auth.sendRecoveryEmail(email.value)
  if (ok) {
    message.value = 'Revisa tu correo para restablecer tu contraseña.'
    isError.value = false
  } else {
    message.value = auth.error || 'Error al enviar el correo.'
    isError.value = true
  }
}

const messageClass = computed(() =>
  isError.value ? 'text-red-500 text-sm text-center' : 'text-green-500 text-sm text-center'
)
</script>