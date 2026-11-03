<script setup lang="ts">
import { onMounted } from 'vue'
import { useTaskStore } from './stores/taskStore'
import TaskInput from './components/TaskInput.vue'
import TaskItem from './components/TaskItem.vue'
import TaskFilter from './components/TaskFilter.vue'

const store = useTaskStore()

onMounted(() => {
  store.loadTasks()
})
</script>

<template>
  <main class="min-h-screen px-4 py-8 sm:py-16 flex flex-col items-center justify-start">
    <!-- Container Principal Neobrutalista -->
    <div class="w-full max-w-xl flex flex-col gap-6">
      
      <!-- Cabeçalho Estilizado -->
      <header class="bg-brutal-yellow p-6 border-3 border-brutal-dark shadow-brutal-card relative overflow-hidden">
        <!-- Sticker decorativo brutalista -->
        <div class="inline-block bg-brutal-lavender text-brutal-dark px-2.5 py-0.5 text-xs font-black uppercase border-2 border-brutal-dark shadow-brutal-sm mb-3">
          List Fan
        </div>

        <div class="flex items-baseline justify-between flex-wrap gap-2">
          <h1 class="text-3xl sm:text-4xl font-black tracking-tight text-brutal-dark uppercase">
            Minha lista de tarefas
          </h1>
          <span class="text-xs font-bold bg-white text-brutal-dark px-2.5 py-1 border-2 border-brutal-dark shadow-brutal-sm">
            {{ store.taskCounts.completed }} DE {{ store.taskCounts.all }} FEITAS
          </span>
        </div>
        <p class="text-sm font-medium text-neutral-800 mt-2">
          Organize suas atividades diárias com velocidade e sem distrações.
        </p>
      </header>

      <!-- Banner de Notificação de Erro (com Rollback UI) -->
      <div
        v-if="store.errorMessage"
        class="bg-brutal-coral text-brutal-dark p-4 border-3 border-brutal-dark shadow-brutal flex items-start justify-between gap-3 animate-pulse"
        role="alert"
      >
        <div class="flex items-center gap-2">
          <span class="font-black text-lg"><i class="fa-solid fa-triangle-exclamation"></i></span>
          <p class="text-sm font-bold">{{ store.errorMessage }}</p>
        </div>
        <button
          @click="store.clearError"
          class="font-black text-sm px-2 py-0.5 border-2 border-brutal-dark bg-white hover:bg-neutral-100 cursor-pointer"
          aria-label="Fechar mensagem de erro"
        >
          ✕
        </button>
      </div>

      <!-- Barra de Entrada de Tarefas -->
      <section class="bg-brutal-surface p-5 border-3 border-brutal-dark shadow-brutal-card">
        <h2 class="text-xs font-bold uppercase tracking-wider text-neutral-600 mb-3">
          Nova Atividade
        </h2>
        <TaskInput
          :is-submitting="store.isSubmitting"
          @add-task="(title) => store.addTask(title)"
        />
      </section>

      <!-- Controles de Filtro e Lista -->
      <section class="flex flex-col gap-4">
        <div class="flex items-center justify-between flex-wrap gap-2 px-1">
          <TaskFilter
            :current-filter="store.currentFilter"
            :counts="store.taskCounts"
            @filter-change="(f) => store.currentFilter = f"
          />

          <span v-if="store.isLoading" class="text-xs font-bold uppercase tracking-wider text-neutral-600 flex items-center gap-1">
            <svg class="animate-spin h-3.5 w-3.5 text-brutal-dark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
            </svg>
            SINCRONIZANDO...
          </span>
        </div>

        <!-- Lista de Tarefas -->
        <div class="flex flex-col gap-3">
          <!-- Estado Vazio -->
          <div
            v-if="!store.isLoading && store.filteredTasks.length === 0"
            class="bg-white p-8 border-3 border-brutal-dark shadow-brutal text-center flex flex-col items-center justify-center gap-2"
          >
            <span class="text-3xl" id="icon-clipboard-pending"><i class="fa-solid fa-clipboard-question fa-2xl" style="margin-bottom: 0.6em;"></i></span>
            <p class="font-bold text-base uppercase text-brutal-dark">
              Nenhuma tarefa encontrada
            </p>
            <p class="text-xs text-neutral-500 font-medium">
              {{ store.currentFilter === 'completed'
                ? 'Você ainda não concluiu nenhuma tarefa nesta visualização.'
                : store.currentFilter === 'active'
                ? 'Todas as atividades foram finalizadas! Bom trabalho.'
                : 'Digite uma atividade acima para começar a sua lista.'
              }}
            </p>
          </div>

          <!-- Cards das Tarefas -->
          <TaskItem
            v-for="task in store.filteredTasks"
            :key="task.id"
            :task="task"
            @toggle="(id) => store.toggleTask(id)"
            @delete="(id) => store.removeTask(id)"
          />
        </div>
      </section>

      <!-- Rodapé Tecnológico Neobrutalista -->
      <footer class="mt-8 text-center text-xs font-bold text-neutral-500 flex flex-wrap items-center justify-center gap-2">
        <span class="border border-brutal-dark px-2 py-0.5 bg-white">Desenvolvido por <a href="https://linkedin.com/in/jpssrj">João Pedro Santos</a> como 3º desafio da Alura + Google</span>
      </footer>

    </div>
  </main>
</template>
