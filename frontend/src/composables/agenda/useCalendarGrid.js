/**
 * Composable para cálculo reativo das 42 células da grade mensal do calendário.
 */
import { computed } from 'vue'

export function useCalendarGrid(props) {
  const daysOfWeek = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

  // constrói a matriz de 42 dias do mês (incluindo preenchimento anterior e posterior) e associa os eventos
  const calendarDays = computed(() => {
    const days = []
    const firstDayOfMonth = new Date(props.year, props.month, 1)
    const lastDayOfMonth = new Date(props.year, props.month + 1, 0)

    const startingDayOfWeek = firstDayOfMonth.getDay()
    const daysInMonth = lastDayOfMonth.getDate()

    const today = new Date()

    const prevMonthLastDay = new Date(props.year, props.month, 0).getDate()
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      days.push({
        date: prevMonthLastDay - i,
        isCurrentMonth: false,
        isToday: false,
        events: [],
      })
    }

    for (let i = 1; i <= daysInMonth; i++) {
      const dateString = `${props.year}-${String(props.month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`

      days.push({
        date: i,
        fullDate: dateString,
        isCurrentMonth: true,
        isToday:
          today.getDate() === i &&
          today.getMonth() === props.month &&
          today.getFullYear() === props.year,
        events: (props.events || [])
          .filter((e) => e.data === dateString)
          .sort((a, b) => a.hora.localeCompare(b.hora)),
      })
    }

    const remainingCells = 42 - days.length
    for (let i = 1; i <= remainingCells; i++) {
      days.push({
        date: i,
        isCurrentMonth: false,
        isToday: false,
        events: [],
      })
    }

    return days
  })

  return {
    daysOfWeek,
    calendarDays,
  }
}

