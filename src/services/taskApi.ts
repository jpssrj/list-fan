import type { Task, TaskCreateDTO, TaskUpdateDTO } from '../types/task'

const BASE_URL = '/api/tasks'

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Falha na requisição (Status ${res.status})`
    try {
      const data = await res.json()
      if (typeof data.detail === 'string') {
        errorDetail = data.detail
      } else if (Array.isArray(data.detail)) {
        errorDetail = data.detail.map((err: any) => err.msg || JSON.stringify(err)).join(', ')
      }
    } catch {
      errorDetail = res.statusText || errorDetail
    }
    throw new Error(errorDetail)
  }

  if (res.status === 204) {
    return null as T
  }

  return res.json()
}

export const taskApi = {
  async fetchTasks(): Promise<Task[]> {
    const res = await fetch(BASE_URL, {
      headers: { 'Accept': 'application/json' }
    })
    return handleResponse<Task[]>(res)
  },

  async createTask(dto: TaskCreateDTO): Promise<Task> {
    const res = await fetch(BASE_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(dto),
    })
    return handleResponse<Task>(res)
  },

  async updateTask(id: number, dto: TaskUpdateDTO): Promise<Task> {
    const res = await fetch(`${BASE_URL}/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(dto),
    })
    return handleResponse<Task>(res)
  },

  async deleteTask(id: number): Promise<void> {
    const res = await fetch(`${BASE_URL}/${id}`, {
      method: 'DELETE',
      headers: { 'Accept': 'application/json' },
    })
    return handleResponse<void>(res)
  },
}
