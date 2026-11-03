<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BrutalButton from './BrutalButton.vue'

const props = defineProps<{
  isSubmitting?: boolean
}>()

const emit = defineEmits<{
  (e: 'add-task', title: string): void
}>()

const inputRef = ref<HTMLInputElement | null>(null)
const taskTitle = ref('')

function handleSubmit() {
  const trimmed = taskTitle.value.trim()
  if (!trimmed || props.isSubmitting) return

  emit('add-task', trimmed)
  taskTitle.value = ''
  
  // Re-foca no campo de digitação
  inputRef.value?.focus()
}

onMounted(() => {
  inputRef.value?.focus()
})
</script>

<template>
  <form @submit.prevent="handleSubmit" class="flex flex-col sm:flex-row gap-3 w-full">
    <div class="relative flex-1">
      <input
        ref="inputRef"
        v-model="taskTitle"
        type="text"
        maxlength="255"
        :disabled="isSubmitting"
        placeholder="O que precisa ser feito hoje?..."
        class="w-full px-4 py-3 bg-brutal-surface text-brutal-dark font-medium border-3 border-brutal-dark shadow-brutal placeholder:text-neutral-500 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-brutal-yellow focus-visible:ring-offset-2 disabled:opacity-60 disabled:cursor-not-allowed transition-all"
      />
    </div>

    <BrutalButton
      type="submit"
      variant="yellow"
      size="md"
      :disabled="!taskTitle.trim() || isSubmitting"
      aria-label="Adicionar nova atividade à lista"
      class="sm:w-auto w-full py-3"
    >
      <span v-if="isSubmitting" class="flex items-center gap-1">
        <svg class="animate-spin h-4 w-4 mr-1 text-brutal-dark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
        </svg>
        ADICIONANDO...
      </span>
      <span v-else class="flex items-center gap-1.5">
        <span class="text-lg leading-none font-black">+</span> ADICIONAR
      </span>
    </BrutalButton>
  </form>
</template>
