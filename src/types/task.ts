export type TaskFilterType = 'all' | 'active' | 'completed'

export interface Task {
  id: number
  title: string
  is_completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskCreateDTO {
  title: string
}

export interface TaskUpdateDTO {
  title?: string
  is_completed?: boolean
}
