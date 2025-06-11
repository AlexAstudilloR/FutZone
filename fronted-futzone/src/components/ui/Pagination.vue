<template>
  <div class="flex items-center justify-center gap-2 mt-4">
    <!-- Flecha izquierda -->
    <button
      :disabled="currentPage === 1"
      @click="$emit('update:page', currentPage - 1)"
      class="text-xl px-2 disabled:text-gray-400"
    >
      ‹
    </button>

    <button
      v-for="page in totalPages"
      :key="page"
      @click="$emit('update:page', page)"
      :class="[
        'w-8 h-8 flex items-center justify-center border rounded',
        page === currentPage ? 'bg-blue-800 text-white' : 'text-blue-800 border-blue-800'
      ]"
    >
      {{ page }}
    </button>

    <!-- Flecha derecha -->
    <button
      :disabled="currentPage === totalPages"
      @click="$emit('update:page', currentPage + 1)"
      class="text-xl px-2 disabled:text-gray-400"
    >
      ›
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: Number,
  totalItems: Number,
  itemsPerPage: {
    type: Number,
    default: 10
  }
})

const totalPages = computed(() => {
  const items = Number(props.totalItems) || 0
  const perPage = Number(props.itemsPerPage) || 1
  return Math.max(1, Math.ceil(items / perPage))
})
</script>
