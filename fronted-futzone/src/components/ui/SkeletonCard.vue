<template>
  <div :class="['bg-white rounded shadow p-4 space-y-3', extraClass]">
    <div v-if="avatar" class="w-12 h-12 rounded-full overflow-hidden">
      <Skeleton circle width="48px" height="48px" />
    </div>

    <div v-for="n in lines" :key="n">
      <Skeleton :width="getWidth(n)" :height="lineHeight" :borderRadius="radius" />
    </div>
  </div>
</template>

<script setup>
import Skeleton from 'vue-loading-skeleton'
import { computed } from 'vue'

const props = defineProps({
  lines: {
    type: Number,
    default: 3,
  },
  avatar: {
    type: Boolean,
    default: false,
  },
  lineHeight: {
    type: String,
    default: '16px',
  },
  radius: {
    type: String,
    default: '0.375rem', // rounded-md
  },
  extraClass: {
    type: String,
    default: '',
  },
})

// Simula diferentes anchos para que parezca contenido real
const getWidth = (index) => {
  const widths = ['100%', '90%', '75%', '60%']
  return widths[index % widths.length]
}
</script>
