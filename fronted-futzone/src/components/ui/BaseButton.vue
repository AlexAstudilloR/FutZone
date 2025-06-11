<template>
  <button
    :class="[
      'inline-flex items-center justify-center rounded transition focus:outline-none',
      sizeClass,
      bgClass,
      textClass,
      extraClass
    ]"
    @click="$emit('click', $event)"
    :disabled="disabled"
  >
    <font-awesome-icon
      v-if="icon"
      :icon="icon"
      class="mr-2"
    />
    <span><slot>{{ label }}</slot></span>
  </button>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const sizeClasses = {
  sm: 'px-3 py-1 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg'
}

const bgClasses = {
  primary: 'bg-blue-600 hover:bg-blue-700',
  secondary: 'bg-gray-600 hover:bg-gray-700',
  success: 'bg-green-600 hover:bg-green-700',
  danger: 'bg-red-600 hover:bg-red-700',
  warning: 'bg-yellow-500 hover:bg-yellow-600',
  light: 'bg-white hover:bg-gray-100',
  outline: 'bg-transparent border border-current hover:bg-current hover:text-white'
}

const textClasses = {
  white: 'text-white',
  black: 'text-black',
  blue: 'text-blue-600',
  gray: 'text-gray-800',
  inherit: ''
}

export default {
  name: 'BaseButton',
  components: { FontAwesomeIcon },
  props: {
    label: {
      type: String,
      default: ''
    },
    size: {
      type: String,
      default: 'md',
      validator: v => ['sm', 'md', 'lg'].includes(v)
    },
    variant: {
      type: String,
      default: 'primary',
      validator: v => Object.keys(bgClasses).includes(v)
    },
    textColor: {
      type: String,
      default: 'white',
      validator: v => Object.keys(textClasses).includes(v)
    },
    icon: {
      type: Array,
      default: null
    },
    extraClass: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    sizeClass() {
      return sizeClasses[this.size] || ''
    },
    bgClass() {
      return bgClasses[this.variant] || ''
    },
    textClass() {
      return textClasses[this.textColor] || ''
    }
  }
}
</script>
