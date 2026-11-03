import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Task, TaskFilterType } from '../types/task'
import { taskApi } from '../services/taskApi'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref<Task[]>([])
  const currentFilter = ref<TaskFilterType>('all')
  const isLoading = ref<boolean>(false)
  const isSubmitting = ref<boolean>(false)
  const errorMessage = ref<string | null>(null)

  const taskCounts = computed(() => {
    const all = tasks.value.length
    const completed = tasks.value.filter((t) => t.is_completed).length
    const active = all - completed
    return { all, active, completed }
  })

  const filteredTasks = computed(() => {
    if (currentFilter.value === 'active') {
      return tasks.value.filter((t) => !t.is_completed)
    }
    if (currentFilter.value === 'completed') {
      return tasks.value.filter((t) => t.is_completed)
    }
    return tasks.value
  })

  function clearError() {
    errorMessage.value = null
  }

  async function loadTasks() {
    isLoading.value = true
    errorMessage.value = null
    try {
      tasks.value = await taskApi.fetchTasks()
    } catch (err: any) {
      errorMessage.value = `Erro ao carregar tarefas: ${err.message}`
    } finally {
      isLoading.value = false
    }
  }

  async function addTask(title: string) {
    const trimmed = title.trim()
    if (!trimmed) return

    isSubmitting.value = true
    errorMessage.value = null
    try {
      const created = await taskApi.createTask({ title: trimmed })
      // Insere no topo da lista
      tasks.value.unshift(created)
    } catch (err: any) {
      errorMessage.value = `Erro ao adicionar tarefa: ${err.message}`
      throw err
    } finally {
      isSubmitting.value = false
    }
  }

  async function toggleTask(id: number) {
    const taskIndex = tasks.value.findIndex((t) => t.id === id)
    if (taskIndex === -1) return

    const task = tasks.value[taskIndex]
    const previousState = task.is_completed

    // Atualização otimista imediata na UI
    task.is_completed = !previousState
    errorMessage.value = null

    try {
      const updated = await taskApi.updateTask(id, { is_completed: task.is_completed })
      task.updated_at = updated.updated_at
    } catch (err: any) {
      // Reversão do estado em caso de falha de rede
      task.is_completed = previousState
      errorMessage.value = `Erro ao atualizar tarefa: ${err.message}. Ação revertida.`
    }
  }

  async function removeTask(id: number) {
    const taskIndex = tasks.value.findIndex((t) => t.id === id)
    if (taskIndex === -1) return

    const [removedTask] = tasks.value.splice(taskIndex, 1)
    errorMessage.value = null

    try {
      await taskApi.deleteTask(id)
    } catch (err: any) {
      // Reversão inserindo de volta no índice original
      tasks.value.splice(taskIndex, 0, removedTask)
      errorMessage.value = `Erro ao excluir tarefa: ${err.message}. Ação revertida.`
    }
  }

  return {
    tasks,
    currentFilter,
    isLoading,
    isSubmitting,
    errorMessage,
    taskCounts,
    filteredTasks,
    clearError,
    loadTasks,
    addTask,
    toggleTask,
    removeTask,
  }
})
