<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { computed } from 'vue'
const props = defineProps({
  title: String,
  subtitle: String,
  description: String,
  icon: String, // nombre del icono, ej. 'users'
  gradient: String,
  index: Number,
  selectedId: Number,
  total: Number,
  radius: Number,
  isRotating: Boolean,
})

const emit = defineEmits(['select'])

const isSelected = computed(() => props.index === props.selectedId)
</script>

<template>
  <div
    class="absolute w-64 h-96 cursor-pointer transition-all duration-500 ease-out"
    :class="[
      isSelected ? 'scale-110 shadow-2xl shadow-blue-500/40 z-30' : 'hover:scale-105 z-20',
      isRotating ? 'pointer-events-none' : ''
    ]"
    :style="{
      left: '50%',
      top: '50%',
      marginLeft: '-128px', // w/2
      marginTop: '-192px',  // h/2
      transform: `rotateY(${index * (360 / total)}deg) translateZ(${radius}px)`,
      transformStyle: 'preserve-3d'
    }"
    @click="emit('select', index)"
  >
    <div class="p-0 h-full relative overflow-hidden rounded-lg">
      <!-- Fondo con gradiente -->
      <div :class="`absolute inset-0 bg-gradient-to-br ${gradient} opacity-90`" />

      <!-- Patrón de fondo -->
      <div class="absolute inset-0 opacity-10">
        <div
          class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(255,255,255,0.1)_1px,transparent_1px)]
                   bg-[length:20px_20px]"
        />
      </div>

      <!-- Indicador selección -->
      <div v-if="isSelected" class="absolute top-2 right-2 w-8 h-8 bg-white/30 rounded-full flex items-center justify-center backdrop-blur-sm border-2 border-white/50">
        <div class="w-3 h-3 bg-white rounded-full animate-pulse" />
      </div>

      <!-- Contenido -->
      <div class="relative h-full flex flex-col p-6 text-white">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-semibold tracking-wide">{{ subtitle }}</span>
          <FontAwesomeIcon :icon="['fas', icon]" class="w-6 h-6" />
        </div>

        <div class="mb-4">
          <h3 class="text-xl font-bold mb-1">{{ title }}</h3>
        </div>

        <div class="flex-1 flex items-center justify-center">
          <div class="w-20 h-20 rounded-full bg-white/20 flex items-center justify-center backdrop-blur-sm">
            <FontAwesomeIcon :icon="['fas', icon]" class="w-10 h-10" />
          </div>
        </div>

        <!-- Información expandida solo si está al frente -->
        <transition name="fade">
          <div
            v-if="isSelected"
            class="mt-4 p-4 bg-black/30 rounded-lg backdrop-blur-sm text-sm"
          >
            <p class="mb-2">{{ description }}</p>
          </div>
        </transition>
      </div>

      <!-- Brillo -->
      <div
        :class="[
          'absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent transition-all duration-700 ease-out',
          isSelected ? 'translate-x-full' : '-translate-x-full'
        ]"
      />

      <!-- Borde -->
      <div v-if="isSelected" class="absolute inset-0 border-2 border-white/30 rounded-lg pointer-events-none" />
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  max-height: 0;
}
</style>
