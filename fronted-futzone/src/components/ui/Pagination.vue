<template>
  <div class="flex items-center justify-center gap-2 mt-4">
    <button
      :disabled="currentPage === 1"
      @click="changePage(currentPage - 1)"
      class="text-xl px-2 disabled:text-gray-400"
    >
      ‹
    </button>

    <button
      v-for="page in totalPages"
      :key="page"
      @click="changePage(page)"
      :class="[
        'w-8 h-8 flex items-center justify-center border rounded',
        page === currentPage ? 'bg-blue-800 text-white' : 'text-blue-800 border-blue-800'
      ]"
    >
      {{ page }}
    </button>

    <button
      :disabled="currentPage === totalPages"
      @click="changePage(currentPage + 1)"
      class="text-xl px-2 disabled:text-gray-400"
    >
      ›
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalItems: {
    type: Number,
    required: true,
  },
  itemsPerPage: {
    type: Number,
    default: 10,
  },
})

const emit = defineEmits(['update:page'])

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(props.totalItems / props.itemsPerPage))
})

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value && page !== props.currentPage) {
    emit('update:page', page)
  }
}
</script>
