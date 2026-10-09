import { defineStore } from 'pinia'

export const useAgendaStore = defineStore('agenda', {
  state: () => {
    // Helper para gerar datas simuladas baseadas em hoje
    const today = new Date()
    const formatDate = (date) => {
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    }

    const todayStr = formatDate(today)
    
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)
    const tomorrowStr = formatDate(tomorrow)

    return {
      agendamentos: [
        {
          id: 1,
          data: todayStr,
          hora: '14:00',
          cliente: 'Maria Oliveira',
          servico: 'Mechas',
          color: 'primary',
          descricao: 'Cabelo longo, trazer touca extra.'
        },
        {
          id: 2,
          data: todayStr,
          hora: '16:00',
          cliente: 'Ana Costa',
          servico: 'Corte',
          color: 'secondary',
          descricao: 'Corte repicado nas pontas.'
        },
        {
          id: 3,
          data: tomorrowStr,
          hora: '09:00',
          cliente: 'Fernanda Lima',
          servico: 'Manicure',
          color: 'accent',
          descricao: 'Esmaltação em gel.'
        }
      ]
    }
  },
  getters: {
    getAgendamentosPorMes: (state) => (ano, mes) => {
      return state.agendamentos;
    }
  }
})
