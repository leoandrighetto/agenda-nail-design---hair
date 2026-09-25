<template>
  <div class="calendar-wrapper elevation-2">
    <div class="calendar-header bg-primary text-white py-3">
      <v-row no-gutters>
        <v-col v-for="day in daysOfWeek" :key="day" class="text-center font-weight-bold text-subtitle-1">
          {{ day }}
        </v-col>
      </v-row>
    </div>
    <div class="calendar-grid">
      <div 
        v-for="(dayObj, index) in calendarDays" 
        :key="index"
        class="calendar-cell"
        :class="{ 'other-month': !dayObj.isCurrentMonth, 'today': dayObj.isToday }"
      >
        <div class="date-number mb-2 text-right">
          <span class="date-circle" :class="{ 'bg-primary text-white': dayObj.isToday }">{{ dayObj.date }}</span>
        </div>
        
        <div class="events-container">
          <v-card 
            v-for="event in dayObj.events" 
            :key="event.id"
            :color="event.color"
            class="event-card mb-1 pa-2"
            elevation="0"
            rounded="md"
          >
            <div class="d-flex justify-space-between align-center mb-1">
              <span class="text-caption font-weight-bold text-white">{{ event.hora }}</span>
              <v-chip size="x-small" color="white" variant="outlined" class="text-white">{{ event.servico }}</v-chip>
            </div>
            <div class="text-caption text-white text-truncate">{{ event.cliente }}</div>
            <v-tooltip activator="parent" location="top" v-if="event.descricao">
              {{ event.descricao }}
            </v-tooltip>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  year: { type: Number, required: true },
  month: { type: Number, required: true },
  events: { type: Array, default: () => [] }
})

const daysOfWeek = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

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
      events: []
    })
  }
  
  for (let i = 1; i <= daysInMonth; i++) {
    const dateString = `${props.year}-${String(props.month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`
    
    days.push({
      date: i,
      fullDate: dateString,
      isCurrentMonth: true,
      isToday: today.getDate() === i && today.getMonth() === props.month && today.getFullYear() === props.year,
      events: props.events.filter(e => e.data === dateString).sort((a,b) => a.hora.localeCompare(b.hora))
    })
  }
  
  const remainingCells = 42 - days.length
  for (let i = 1; i <= remainingCells; i++) {
    days.push({
      date: i,
      isCurrentMonth: false,
      isToday: false,
      events: []
    })
  }
  
  return days
})
</script>

<style scoped>
.calendar-wrapper {
  border-radius: 12px;
  overflow: hidden;
  background-color: white;
}
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  grid-auto-rows: 130px;
}
.calendar-cell {
  border-right: 1px solid #F0F0F0;
  border-bottom: 1px solid #F0F0F0;
  padding: 8px;
  background-color: #FFFFFF;
  overflow-y: auto;
}
.calendar-cell:nth-child(7n) {
  border-right: none;
}
.other-month {
  background-color: #F9F9F9;
  color: #BDBDBD;
}
.today {
  background-color: #FCF9F8;
}
.date-circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 0.9rem;
}
.events-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.event-card {
  cursor: pointer;
  transition: transform 0.2s;
}
.event-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}
/* Scrollbar customizada para células com muitos eventos */
.calendar-cell::-webkit-scrollbar {
  width: 4px;
}
.calendar-cell::-webkit-scrollbar-thumb {
  background: #E0E0E0;
  border-radius: 4px;
}
</style>
