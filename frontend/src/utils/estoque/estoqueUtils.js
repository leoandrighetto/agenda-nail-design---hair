/**
 * Utilitários puros para verificação de disponibilidade de materiais e equipamentos.
 */

// verifica se um material ou equipamento está marcado como disponível e possui estoque positivo
export function isResourceAvailable(item) {
  return Boolean(item && item.disponivel && item.quantidade > 0)
}

// retorna a lista de nomes dos materiais e equipamentos indisponíveis vinculados a um serviço
export function listarRecursosIndisponiveis(servico) {
  if (!servico) return []
  const indisponiveis = []

  if (Array.isArray(servico.materiais)) {
    servico.materiais.forEach((m) => {
      if (!isResourceAvailable(m)) {
        indisponiveis.push(`${m.nome} (Material)`)
      }
    })
  }

  if (Array.isArray(servico.equipamentos)) {
    servico.equipamentos.forEach((eq) => {
      if (!isResourceAvailable(eq)) {
        indisponiveis.push(`${eq.nome} (Equipamento)`)
      }
    })
  }

  return indisponiveis
}

