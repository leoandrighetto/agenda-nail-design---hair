/**
 * Serviço responsável pelas requisições HTTP do controle financeiro de cursos e matrículas.
 */
import { httpRequest } from '@/services/httpClient'

// monta a query string para filtros opcionais de pagamentos
function montarQueryPagamentos(filtros = {}) {
  const params = new URLSearchParams()
  if (filtros.aluno_id) params.append('aluno_id', filtros.aluno_id)
  if (filtros.curso_id) params.append('curso_id', filtros.curso_id)
  if (filtros.matricula_id) params.append('matricula_id', filtros.matricula_id)
  if (filtros.status) params.append('status', filtros.status)
  const query = params.toString()
  return query ? `?${query}` : ''
}

// busca todos os pagamentos cadastrados, permitindo filtros opcionais
export async function listarPagamentos(filtros = {}) {
  return await httpRequest(`/pagamentos${montarQueryPagamentos(filtros)}`)
}

// registra uma nova cobrança ou pagamento de curso
export async function criarPagamento(payload) {
  return await httpRequest('/pagamentos', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

// atualiza os dados de um pagamento existente (baixa, status, valores ou datas)
export async function atualizarPagamento(id, payload) {
  return await httpRequest(`/pagamentos/${id}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

// remove um lançamento financeiro pelo identificador
export async function excluirPagamento(id) {
  return await httpRequest(`/pagamentos/${id}`, {
    method: 'DELETE',
  })
}

