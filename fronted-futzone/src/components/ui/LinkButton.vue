<template>
  <router-link
    :to="to"
    :class="[
      'inline-flex items-center rounded transition',
      sizeClasses[size]   ,
      bgClasses[variant]  ,
      textClasses[color]  ,
      extraClass
    ]"
  >
    <font-awesome-icon
      v-if="icon"
      :icon="icon"
      class="mr-2"
    />
    <span><slot>{{ label }}</slot></span>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

defineProps({

  to: {
    type: [String, Object],
    required: true
  },

  label: {
    type: String,
    default: ''
  },

  size: {
    type: String,
    default: 'md'
  },

  variant: {
    type: String,
    default: 'primary'
  },

  color: {
    type: String,
    default: 'white'
  },

  icon: {
    type: Array,
    default: null
  },

  extraClass: {
    type: String,
    default: ''
  }
})


const sizeClasses = {
  sm: 'px-2 py-1 text-xs',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base'
}

const bgClasses = {
  primary: 'bg-blue-600 hover:bg-blue-700',
  secondary: 'bg-gray-600 hover:bg-gray-700',
  light: 'bg-white hover:bg-gray-100',
  none: 'bg-transparent'
}

const textClasses = {
  white: 'text-white',
  blue: 'text-blue-600',
  gray: 'text-gray-800',
  inherit: ''
}
</script>
