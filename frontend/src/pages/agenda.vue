<template>
  <v-container fluid class="pa-4">
    <v-row align="center" justify="space-between" class="mb-6">
      <v-col cols="12" md="4">
        <h1 class="text-h4 text-primary font-weight-bold">Minha Agenda</h1>
        <p class="text-subtitle-1 text-grey-darken-1">Acompanhe seus horários de hoje.</p>
      </v-col>
      <v-col cols="12" md="4" class="d-flex align-center justify-center">
        <v-btn icon="mdi-chevron-left" variant="text" color="primary" @click="prevMonth"></v-btn>
        <span class="text-h5 mx-6 font-weight-bold text-secondary text-capitalize">{{ monthName }} {{ currentYear }}</span>
        <v-btn icon="mdi-chevron-right" variant="text" color="primary" @click="nextMonth"></v-btn>
      </v-col>
      <v-col cols="12" md="4" class="text-md-right text-center">
        <v-btn color="primary" rounded="pill" size="large" prepend-icon="mdi-plus" elevation="3">
          Novo Agendamento
        </v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <CalendarGrid 
          :year="currentYear" 
          :month="currentMonth" 
          :events="store.agendamentos" 
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import CalendarGrid from '@/components/CalendarGrid.vue'
import { useAgendaStore } from '@/stores/agenda'

const store = useAgendaStore()

const today = new Date()
const currentYear = ref(today.getFullYear())
const currentMonth = ref(today.getMonth())

const monthNames = [
  'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
  'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
]

const monthName = computed(() => monthNames[currentMonth.value])

function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value--
  } else {
    currentMonth.value--
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value++
  } else {
    currentMonth.value++
  }
}
</script>
