/**
 * Store Pinia da agenda integrada aos serviços HTTP de agendamentos, clientes e serviços.
 */
import { defineStore } from 'pinia'
import {
  listarAgendamentos,
  criarAgendamentoApi,
  atualizarAgendamentoApi,
  excluirAgendamentoApi,
} from '@/services/agenda/agendamentosService'
import { listarClientes } from '@/services/clientes/clientesService'
import { listarServicos } from '@/services/servicos/servicosService'
import { normalizarAgendamento } from '@/utils/agenda/statusUtils'

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

    // busca todos os agendamentos cadastrados no backend via service
    async fetchAgendamentos() {
      const dados = await listarAgendamentos()
      this.agendamentos = dados.map(normalizarAgendamento)
      return this.agendamentos
    },

    // busca a lista de clientes para seleção no agendamento via service
    async fetchClientes() {
      this.clientes = await listarClientes()
      return this.clientes
    },

    // busca o catálogo de serviços com status de recursos disponíveis via service
    async fetchServicos() {
      this.servicos = await listarServicos()
      return this.servicos
    },

    // cria um novo agendamento na API e atualiza a lista local
    async criarAgendamento(payload) {
      const data = await criarAgendamentoApi(payload)
      await this.fetchAgendamentos()
      return data
    },

    // atualiza um agendamento existente (status, horário, cliente ou serviço)
    async atualizarAgendamento(id, payload) {
      const data = await atualizarAgendamentoApi(id, payload)
      await this.fetchAgendamentos()
      return data
    },

    // remove um agendamento do banco de dados
    async deletarAgendamento(id) {
      const data = await excluirAgendamentoApi(id)
      await this.fetchAgendamentos()
      return data
    },
  },
})
