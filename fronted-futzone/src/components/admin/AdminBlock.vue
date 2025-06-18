<template>
  <div class="bg-white rounded-xl shadow-md p-4 space-y-4">
    <h3 v-if="title" class="text-lg font-semibold text-center">{{ title }}</h3>

    <div
      :class="[
        'grid gap-4',
        items.length === 3
          ? 'grid-cols-1 md:grid-cols-2'
          : 'grid-cols-1 sm:grid-cols-2'
      ]"
    >
      <template v-for="(item, index) in items" :key="index">
        <div
          :class="[

            items.length === 3 && index === 0 ? 'md:col-span-2' : '',
            'w-full h-full'
          ]"
        >
          <slot :item="item" :index="index" />
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  items: {
    type: Array,
    required: true,
  },
});
</script>