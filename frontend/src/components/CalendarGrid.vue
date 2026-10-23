<template>
  <div class="calendar-wrapper elevation-2">
    <div class="calendar-header bg-primary text-white py-3">
      <v-row no-gutters>
        <v-col
          v-for="day in daysOfWeek"
          :key="day"
          class="text-center font-weight-bold text-subtitle-1"
        >
          {{ day }}
        </v-col>
      </v-row>
    </div>

    <div class="calendar-grid">
      <div
        v-for="(dayObj, index) in calendarDays"
        :key="index"
        class="calendar-cell"
        :class="{
          'other-month': !dayObj.isCurrentMonth,
          'today': dayObj.isToday,
          'clickable-cell': dayObj.isCurrentMonth,
        }"
        @click="dayObj.isCurrentMonth && emit('select-date', dayObj.fullDate)"
      >
        <div class="date-header d-flex align-center justify-space-between mb-2">
          <v-btn
            v-if="dayObj.isCurrentMonth"
            icon="mdi-plus"
            size="x-small"
            variant="text"
            color="primary"
            class="add-day-btn"
            title="Agendar neste dia"
            @click.stop="emit('select-date', dayObj.fullDate)"
          ></v-btn>
          <span v-else></span>

          <span
            class="date-circle"
            :class="{ 'bg-primary text-white font-weight-bold': dayObj.isToday }"
          >
            {{ dayObj.date }}
          </span>
        </div>

        <div class="events-container">
          <v-card
            v-for="event in dayObj.events"
            :key="event.id"
            :color="event.color"
            class="event-card mb-1 pa-2"
            :class="{ 'event-cancelado': event.status === 'Cancelado' }"
            elevation="1"
            rounded="md"
            @click.stop="emit('select-event', event)"
          >
            <div class="d-flex justify-space-between align-center mb-1 ga-1">
              <div class="d-flex align-center text-caption font-weight-bold text-white text-no-wrap">
                <v-icon size="13" class="mr-1">{{ iconeStatus(event.status) }}</v-icon>
                <span>{{ event.hora }}{{ event.hora_fim ? ` - ${event.hora_fim}` : '' }}</span>
              </div>
              <v-chip
                size="x-small"
                color="white"
                variant="outlined"
                class="text-white text-truncate"
                style="max-width: 95px"
              >
                {{ event.servico }}
              </v-chip>
            </div>

            <div
              class="text-caption text-white text-truncate font-weight-medium"
              :class="{ 'text-decoration-line-through': event.status === 'Cancelado' }"
            >
              {{ event.cliente }}
            </div>

            <v-tooltip activator="parent" location="top">
              <div class="text-caption">
                <div class="font-weight-bold">{{ event.cliente }}</div>
                <div>Serviço: {{ event.servico }}</div>
                <div>
                  Horário: {{ event.hora }}{{ event.hora_fim ? ` às ${event.hora_fim}` : '' }}
                </div>
                <div>Status: {{ event.status }}</div>
                <div class="mt-1 text-grey-lighten-2 font-italic">
                  Clique para editar ou alterar status
                </div>
              </div>
            </v-tooltip>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCalendarGrid } from '@/composables/agenda/useCalendarGrid'
import { iconeStatus } from '@/utils/agenda/statusUtils'

const props = defineProps({
  year: { type: Number, required: true },
  month: { type: Number, required: true },
  events: { type: Array, default: () => [] },
})

const emit = defineEmits(['select-event', 'select-date'])

const { daysOfWeek, calendarDays } = useCalendarGrid(props)
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
  grid-auto-rows: 140px;
}
.calendar-cell {
  border-right: 1px solid #f0f0f0;
  border-bottom: 1px solid #f0f0f0;
  padding: 8px;
  background-color: #ffffff;
  overflow-y: auto;
  transition: background-color 0.15s ease;
}
.calendar-cell:nth-child(7n) {
  border-right: none;
}
.clickable-cell:hover {
  background-color: #fdf8f6;
}
.add-day-btn {
  opacity: 0;
  transition: opacity 0.2s ease;
}
.clickable-cell:hover .add-day-btn {
  opacity: 1;
}
.other-month {
  background-color: #f9f9f9;
  color: #bdbdbd;
}
.today {
  background-color: #fcf4f2;
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
  transition: transform 0.2s, box-shadow 0.2s;
}
.event-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.14) !important;
}
.event-cancelado {
  opacity: 0.72;
}
/* barra de rolagem customizada para células com muitos eventos */
.calendar-cell::-webkit-scrollbar {
  width: 4px;
}
.calendar-cell::-webkit-scrollbar-thumb {
  background: #e0e0e0;
  border-radius: 4px;
}
</style>
