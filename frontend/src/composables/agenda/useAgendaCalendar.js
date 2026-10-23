/**
 * Composable para navegação de calendário, filtragem reativa e cálculo de KPIs da agenda.
 */
import { ref, computed } from 'vue'

export function useAgendaCalendar(store) {
  const today = new Date()
  const hojeIso = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

  const currentYear = ref(today.getFullYear())
  const currentMonth = ref(today.getMonth())

  const monthNames = [
    'janeiro',
    'fevereiro',
    'março',
    'abril',
    'maio',
    'junho',
    'julho',
    'agosto',
    'setembro',
    'outubro',
    'novembro',
    'dezembro',
  ]

  const monthName = computed(() => monthNames[currentMonth.value])

  // estados reativos de busca textual e filtro por status
  const termoBusca = ref('')
  const filtroStatus = ref('TODOS')

  // filtra os agendamentos da store conforme busca e status selecionados
  const eventosFiltrados = computed(() => {
    return store.agendamentos.filter((ag) => {
      const passaStatus = filtroStatus.value === 'TODOS' || ag.status === filtroStatus.value
      if (!passaStatus) return false

      if (!termoBusca.value) return true
      const termo = termoBusca.value.toLowerCase().trim()
      return (
        (ag.cliente && ag.cliente.toLowerCase().includes(termo)) ||
        (ag.servico && ag.servico.toLowerCase().includes(termo))
      )
    })
  })

  // indicadores (KPIs) calculados em tempo real
  const agendamentosHoje = computed(() => {
    return store.agendamentos
      .filter((ag) => ag.data === hojeIso && ag.status !== 'Cancelado')
      .sort((a, b) => a.hora.localeCompare(b.hora))
  })

  const proximoAtendimentoHoje = computed(() => {
    return agendamentosHoje.value.find(
      (ag) => ag.status === 'Pendente' || ag.status === 'Confirmado'
    )
  })

  const agendamentosDoMes = computed(() => {
    return store.getAgendamentosPorMes(currentYear.value, currentMonth.value)
  })

  const pendentesOuConfirmadosMes = computed(() => {
    return agendamentosDoMes.value.filter(
      (ag) => ag.status === 'Pendente' || ag.status === 'Confirmado'
    ).length
  })

  const canceladosMes = computed(() => {
    return agendamentosDoMes.value.filter((ag) => ag.status === 'Cancelado').length
  })

  const concluidosMes = computed(() => {
    return agendamentosDoMes.value.filter((ag) => ag.status === 'Concluído').length
  })

  const receitaConcluidaMes = computed(() => {
    return agendamentosDoMes.value
      .filter((ag) => ag.status === 'Concluído')
      .reduce((soma, ag) => {
        if (ag.valor_total != null) {
          return soma + Number(ag.valor_total)
        }
        if (ag.servicos && Array.isArray(ag.servicos) && ag.servicos.length > 0) {
          return soma + ag.servicos.reduce((acc, s) => acc + Number(s.preco || 0), 0)
        }
        const servicoObj = store.servicos.find((s) => s.id === ag.servico_id)
        return soma + (servicoObj?.preco ? Number(servicoObj.preco) : 0)
      }, 0)
  })

  // retrocede um mês no calendário
  function prevMonth() {
    if (currentMonth.value === 0) {
      currentMonth.value = 11
      currentYear.value--
    } else {
      currentMonth.value--
    }
  }

  // avança um mês no calendário
  function nextMonth() {
    if (currentMonth.value === 11) {
      currentMonth.value = 0
      currentYear.value++
    } else {
      currentMonth.value++
    }
  }

  // reposiciona o calendário no mês e ano atuais
  function irParaHoje() {
    const agora = new Date()
    currentYear.value = agora.getFullYear()
    currentMonth.value = agora.getMonth()
  }

  return {
    hojeIso,
    currentYear,
    currentMonth,
    monthName,
    termoBusca,
    filtroStatus,
    eventosFiltrados,
    agendamentosHoje,
    proximoAtendimentoHoje,
    agendamentosDoMes,
    pendentesOuConfirmadosMes,
    canceladosMes,
    concluidosMes,
    receitaConcluidaMes,
    prevMonth,
    nextMonth,
    irParaHoje,
  }
}
