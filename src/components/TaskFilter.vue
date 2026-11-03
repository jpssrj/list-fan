<script setup lang="ts">
import type { TaskFilterType } from '../types/task'

defineProps<{
  currentFilter: TaskFilterType
  counts: {
    all: number
    active: number
    completed: number
  }
}>()

const emit = defineEmits<{
  (e: 'filter-change', filter: TaskFilterType): void
}>()

const filters: { key: TaskFilterType; label: string }[] = [
  { key: 'all', label: 'TODAS' },
  { key: 'active', label: 'PENDENTES' },
  { key: 'completed', label: 'CONCLUÍDAS' },
]
</script>

<template>
  <div class="flex flex-wrap gap-2 items-center" role="tablist" aria-label="Filtro de tarefas">
    <button
      v-for="item in filters"
      :key="item.key"
      role="tab"
      :aria-selected="currentFilter === item.key"
      :class="[
        'px-3.5 py-1.5 text-xs font-bold uppercase tracking-wider border-3 border-brutal-dark flex items-center gap-2 select-none brutal-interactive cursor-pointer',
        'focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-brutal-yellow focus-visible:ring-offset-2',
        currentFilter === item.key
          ? 'bg-brutal-dark text-white shadow-brutal-sm'
          : 'bg-white text-brutal-dark shadow-brutal-sm hover:bg-neutral-100'
      ]"
      @click="emit('filter-change', item.key)"
    >
      <span>{{ item.label }}</span>
      <span
        :class="[
          'px-1.5 py-0.2 rounded-none text-[11px] font-black border border-brutal-dark',
          currentFilter === item.key
            ? 'bg-brutal-yellow text-brutal-dark'
            : 'bg-neutral-100 text-brutal-dark'
        ]"
      >
        {{ item.key === 'all' ? counts.all : item.key === 'active' ? counts.active : counts.completed }}
      </span>
    </button>
  </div>
</template>
