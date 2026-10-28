/**
 * Utilitários puros para mapeamento visual, opções de seleção e cálculos do módulo de cursos.
 */

// opções de status de matrícula aceitas pela API
export const opcoesStatusMatricula = [
  { valor: 'EM_ANDAMENTO', rotulo: 'Em Andamento', cor: 'primary', icone: 'mdi-progress-clock' },
  { valor: 'CONCLUIDO', rotulo: 'Concluído', cor: 'success', icone: 'mdi-school-outline' },
  { valor: 'TRANCADO', rotulo: 'Trancado', cor: 'warning', icone: 'mdi-pause-circle-outline' },
  { valor: 'CANCELADO', rotulo: 'Cancelado', cor: 'error', icone: 'mdi-close-circle-outline' },
]

// opções de tipo de cobrança aceitas pela API
export const opcoesTipoCobranca = [
  { valor: 'MATRICULA', rotulo: 'Taxa de Matrícula', icone: 'mdi-badge-account-horizontal-outline' },
  { valor: 'MENSALIDADE', rotulo: 'Mensalidade / Parcela', icone: 'mdi-calendar-sync' },
  { valor: 'TAXA_EXTRA', rotulo: 'Taxa Extra / Material', icone: 'mdi-cash-plus' },
]

// opções de status de pagamento aceitas pela API
export const opcoesStatusPagamento = [
  { valor: 'PENDENTE', rotulo: 'Pendente', cor: 'warning', icone: 'mdi-clock-outline' },
  { valor: 'PAGO', rotulo: 'Pago', cor: 'success', icone: 'mdi-check-decagram' },
  { valor: 'ATRASADO', rotulo: 'Atrasado', cor: 'error', icone: 'mdi-alert-circle-outline' },
  { valor: 'CANCELADO', rotulo: 'Cancelado', cor: 'grey-darken-1', icone: 'mdi-cancel' },
]

// opções de forma de pagamento aceitas pela API
export const opcoesFormaPagamento = [
  { valor: 'PIX', rotulo: 'PIX', icone: 'mdi-qrcode-scan' },
  { valor: 'CARTAO_CREDITO', rotulo: 'Cartão de Crédito', icone: 'mdi-credit-card-outline' },
  { valor: 'CARTAO_DEBITO', rotulo: 'Cartão de Débito', icone: 'mdi-credit-card-fast-outline' },
  { valor: 'DINHEIRO', rotulo: 'Dinheiro', icone: 'mdi-cash' },
  { valor: 'BOLETO', rotulo: 'Boleto', icone: 'mdi-barcode' },
  { valor: 'TRANSFERENCIA', rotulo: 'Transferência', icone: 'mdi-bank-transfer' },
  { valor: 'CARTAO', rotulo: 'Cartão (Geral)', icone: 'mdi-credit-card' },
]

// retorna os metadados visuais (rótulo, cor, ícone) de um status de matrícula
export function obterMetaStatusMatricula(status) {
  return (
    opcoesStatusMatricula.find((op) => op.valor === status) || {
      valor: status,
      rotulo: status || 'Desconhecido',
      cor: 'grey',
      icone: 'mdi-help-circle-outline',
    }
  )
}

// retorna os metadados visuais de um status de pagamento considerando atraso automático
export function obterMetaStatusPagamento(pagamento) {
  const statusEfetivo =
    pagamento?.status === 'PENDENTE' && pagamento?.em_atraso ? 'ATRASADO' : pagamento?.status
  return (
    opcoesStatusPagamento.find((op) => op.valor === statusEfetivo) || {
      valor: statusEfetivo,
      rotulo: statusEfetivo || 'Pendente',
      cor: 'warning',
      icone: 'mdi-clock-outline',
    }
  )
}

// retorna o rótulo amigável para o tipo de cobrança
export function formatarTipoCobranca(tipo) {
  const encontrado = opcoesTipoCobranca.find((op) => op.valor === tipo)
  return encontrado ? encontrado.rotulo : tipo || '-'
}

// retorna o rótulo amigável para a forma de pagamento
export function formatarFormaPagamento(forma) {
  if (!forma) return '-'
  const encontrado = opcoesFormaPagamento.find((op) => op.valor === forma)
  return encontrado ? encontrado.rotulo : forma
}

// extrai até duas iniciais de um nome completo para exibição em avatares
export function obterIniciaisNome(nome) {
  if (!nome || !String(nome).trim()) return 'AL'
  const partes = String(nome).trim().split(/\s+/)
  if (partes.length === 1) return partes[0].substring(0, 2).toUpperCase()
  return `${partes[0][0]}${partes[partes.length - 1][0]}`.toUpperCase()
}

