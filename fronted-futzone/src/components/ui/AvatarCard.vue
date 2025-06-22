<template>
  <div
    class="w-[300px] group bg-white p-6 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 text-center"
    data-aos="zoom-in"
  >
    <div class="relative mb-4">
      <div
        class="w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-[#19296D] to-[#3B82F6] flex items-center justify-center text-white text-xl font-bold shadow-lg"
      >
        {{ initials }}
      </div>
      <div
        v-if="verified"
        class="absolute -bottom-2 -right-2 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center"
      >
        <span class="text-white text-xs">✓</span>
      </div>
    </div>

    <h3 class="font-bold text-md mb-1 text-gray-900">{{ name }}</h3>
    <p class="text-blue-600 font-medium mb-2">{{ role }}</p>
    <p class="text-gray-600 text-sm leading-relaxed">{{ description }}</p>

    <div class="flex flex-wrap justify-center gap-2 mt-3">
      <span
        v-for="skill in skills"
        :key="skill"
        class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium"
      >
        {{ skill }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
defineProps({
  name: String,
  role: String,
  description: String,
  skills: {
    type: Array,
    default: () => [],
  },
  verified: {
    type: Boolean,
    default: false,
  },
});

const initials = computed(() => {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .substring(0, 2)
    .toUpperCase();
});
</script>
