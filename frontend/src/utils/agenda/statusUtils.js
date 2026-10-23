/**
 * Utilitários puros para mapeamento visual e normalização de status de agendamentos.
 */

// retorna o ícone representativo para cada status do agendamento
export function iconeStatus(status) {
  switch (status) {
    case 'Confirmado':
      return 'mdi-calendar-check'
    case 'Concluído':
      return 'mdi-check-decagram'
    case 'Cancelado':
      return 'mdi-cancel'
    case 'Pendente':
    default:
      return 'mdi-clock-outline'
  }
}

// mapeia a cor do tema de acordo com o status do agendamento
export function obterCorPorStatus(status) {
  switch (status) {
    case 'Confirmado':
      return 'primary'
    case 'Concluído':
      return 'success'
    case 'Cancelado':
      return 'grey-darken-1'
    case 'Pendente':
    default:
      return 'accent'
  }
}

// converte o objeto retornado pela API para o formato enriquecido usado na interface do calendário
export function normalizarAgendamento(item) {
  const inicioStr = item.data_hora_inicio || ''
  const fimStr = item.data_hora_fim || ''

  const [dataParte, horaParteCompleta] = inicioStr.split('T')
  const horaInicio = horaParteCompleta ? horaParteCompleta.substring(0, 5) : '00:00'

  const [, horaFimCompleta] = fimStr.split('T')
  const horaFim = horaFimCompleta ? horaFimCompleta.substring(0, 5) : ''

  return {
    ...item,
    data: dataParte || '',
    hora: horaInicio,
    hora_fim: horaFim,
    cliente: item.cliente_nome || 'Cliente não informado',
    servico: item.servico_nome || 'Serviço não informado',
    color: obterCorPorStatus(item.status),
  }
}

