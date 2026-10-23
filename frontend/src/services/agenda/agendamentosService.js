/**
 * Serviço responsável pelas requisições HTTP de agendamentos.
 */
import { httpRequest } from '@/services/httpClient'

// busca todos os agendamentos registrados
export async function listarAgendamentos() {
  return await httpRequest('/agendamentos')
}

// registra um novo agendamento
export async function criarAgendamentoApi(payload) {
  return await httpRequest('/agendamentos', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza os dados ou status de um agendamento existente
export async function atualizarAgendamentoApi(id, payload) {
  return await httpRequest(`/agendamentos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// exclui um agendamento pelo identificador
export async function excluirAgendamentoApi(id) {
  return await httpRequest(`/agendamentos/${id}`, {
    method: 'DELETE',
  })
}

