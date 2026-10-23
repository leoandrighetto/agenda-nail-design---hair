import { defineStore } from 'pinia'

const API_BASE = 'http://127.0.0.1:5000/api'

// mapeia a cor do card de acordo com o status do agendamento
function obterCorPorStatus(status) {
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

// converte o objeto retornado pela API para o formato enriquecido usado na interface
function normalizarAgendamento(item) {
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

export const useAgendaStore = defineStore('agenda', {
  state: () => ({
    agendamentos: [],
    clientes: [],
    servicos: [],
    loading: false,
    erro: null,
  }),

  getters: {
    // retorna os agendamentos filtrados por ano e mês (mês de 0 a 11)
    getAgendamentosPorMes: (state) => (ano, mes) => {
      const prefixoMes = `${ano}-${String(mes + 1).padStart(2, '0')}`
      return state.agendamentos.filter((ag) => ag.data && ag.data.startsWith(prefixoMes))
    },
  },

  actions: {
    // carrega agendamentos, clientes e serviços em paralelo
    async carregarDadosAgenda() {
      this.loading = true
      this.erro = null
      try {
        await Promise.all([
          this.fetchAgendamentos(),
          this.fetchClientes(),
          this.fetchServicos(),
        ])
      } catch (err) {
        this.erro = err.message || 'Erro ao carregar dados da agenda'
        throw err
      } finally {
        this.loading = false
      }
    },

    // busca todos os agendamentos cadastrados no backend
    async fetchAgendamentos() {
      const res = await fetch(`${API_BASE}/agendamentos`)
      if (!res.ok) {
        throw new Error('Não foi possível carregar os agendamentos')
      }
      const dados = await res.json()
      this.agendamentos = dados.map(normalizarAgendamento)
      return this.agendamentos
    },

    // busca a lista de clientes para seleção no agendamento
    async fetchClientes() {
      const res = await fetch(`${API_BASE}/clientes`)
      if (!res.ok) {
        throw new Error('Não foi possível carregar os clientes')
      }
      this.clientes = await res.json()
      return this.clientes
    },

    // busca o catálogo de serviços com status de recursos disponíveis
    async fetchServicos() {
      const res = await fetch(`${API_BASE}/servicos`)
      if (!res.ok) {
        throw new Error('Não foi possível carregar os serviços')
      }
      this.servicos = await res.json()
      return this.servicos
    },

    // cria um novo agendamento na API e atualiza a lista local
    async criarAgendamento(payload) {
      const res = await fetch(`${API_BASE}/agendamentos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.erro || 'Erro ao criar agendamento')
      }
      await this.fetchAgendamentos()
      return data
    },

    // atualiza um agendamento existente (status, horário, cliente ou serviço)
    async atualizarAgendamento(id, payload) {
      const res = await fetch(`${API_BASE}/agendamentos/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.erro || 'Erro ao atualizar agendamento')
      }
      await this.fetchAgendamentos()
      return data
    },

    // remove um agendamento do banco de dados
    async deletarAgendamento(id) {
      const res = await fetch(`${API_BASE}/agendamentos/${id}`, {
        method: 'DELETE',
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.erro || 'Erro ao excluir agendamento')
      }
      await this.fetchAgendamentos()
      return data
    },
  },
})
