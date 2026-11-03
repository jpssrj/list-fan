<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    variant?: 'yellow' | 'coral' | 'mint' | 'cyan' | 'white' | 'dark'
    size?: 'sm' | 'md' | 'lg'
    disabled?: boolean
    ariaLabel?: string
    type?: 'button' | 'submit' | 'reset'
  }>(),
  {
    variant: 'yellow',
    size: 'md',
    disabled: false,
    type: 'button',
  }
)

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'coral':
      return 'bg-brutal-coral text-brutal-dark'
    case 'mint':
      return 'bg-brutal-mint text-brutal-dark'
    case 'cyan':
      return 'bg-brutal-cyan text-brutal-dark'
    case 'white':
      return 'bg-brutal-surface text-brutal-dark'
    case 'dark':
      return 'bg-brutal-dark text-brutal-surface'
    case 'yellow':
    default:
      return 'bg-brutal-yellow text-brutal-dark'
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-2.5 py-1 text-xs'
    case 'lg':
      return 'px-6 py-3.5 text-base'
    case 'md':
    default:
      return 'px-4 py-2 text-sm'
  }
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    :aria-label="ariaLabel"
    :class="[
      'inline-flex items-center justify-center font-bold tracking-wider uppercase border-3 border-brutal-dark shadow-brutal select-none',
      'focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-brutal-yellow focus-visible:ring-offset-2',
      variantClasses,
      sizeClasses,
      disabled ? 'opacity-50 cursor-not-allowed shadow-none' : 'brutal-interactive cursor-pointer',
    ]"
    @click="(e) => !disabled && emit('click', e)"
  >
    <slot />
  </button>
</template>
