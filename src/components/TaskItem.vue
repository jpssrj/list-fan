<script setup lang="ts">
import type { Task } from '../types/task'
import BrutalButton from './BrutalButton.vue'

const props = defineProps<{
  task: Task
}>()

const emit = defineEmits<{
  (e: 'toggle', id: number): void
  (e: 'delete', id: number): void
}>()
</script>

<template>
  <div
    :class="[
      'group flex items-center justify-between p-4 border-3 border-brutal-dark shadow-brutal transition-all',
      task.is_completed ? 'bg-neutral-50/80' : 'bg-brutal-surface'
    ]"
  >
    <!-- Área da Checkbox e Título com Acessibilidade WAI-ARIA Nativa -->
    <label class="flex items-center gap-3.5 flex-1 min-w-0 cursor-pointer select-none">
      <input
        type="checkbox"
        :checked="task.is_completed"
        class="sr-only peer"
        @change="emit('toggle', task.id)"
      />
      
      <!-- Caixa Brutalista Customizada estilizada via Peer -->
      <span
        :class="[
          'flex-shrink-0 w-6 h-6 border-3 border-brutal-dark flex items-center justify-center font-black text-sm transition-colors',
          'peer-focus-visible:ring-4 peer-focus-visible:ring-brutal-yellow peer-focus-visible:ring-offset-2',
          task.is_completed ? 'bg-brutal-mint text-brutal-dark' : 'bg-white hover:bg-neutral-100'
        ]"
      >
        <span v-if="task.is_completed">✓</span>
      </span>

      <!-- Texto da Atividade -->
      <span
        :class="[
          'text-base font-semibold break-words overflow-hidden leading-snug transition-all',
          task.is_completed ? 'line-through text-neutral-500' : 'text-brutal-dark'
        ]"
      >
        {{ task.title }}
      </span>
    </label>

    <!-- Botão de Remover com rótulo acessível -->
    <div class="flex-shrink-0 ml-2">
      <BrutalButton
        variant="coral"
        size="sm"
        :aria-label="`Excluir tarefa: ${task.title}`"
        title="Remover tarefa"
        class="!p-2 w-8 h-8 !text-xs font-black"
        @click="emit('delete', task.id)"
      >
        ✕
      </BrutalButton>
    </div>
  </div>
</template>
