<template>
  <div class="flex flex-col items-center text-center">
    <div class="w-20 h-20 rounded-full overflow-hidden shadow-md">
      <img
        :src="avatar"
        :alt="name"
        class="w-full h-full object-cover"
      />
    </div>
    <p class="mt-2 text-sm font-semibold text-gray-700">{{ name }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  avatar: {
    type: String,
    required: true,
  },
})
</script>
