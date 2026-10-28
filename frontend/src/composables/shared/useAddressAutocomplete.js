/**
 * Composable compartilhado para busca inteligente de endereços com debounce via Nominatim.
 */
import { ref } from 'vue'
import { fetchNominatimAddress } from '@/services/nominatimService'

export function useAddressAutocomplete() {
  const addressSearch = ref('')
  const addressSuggestions = ref([])
  const addressLoading = ref(false)
  let addressTimeout = null
  let currentRequestId = 0

  // consulta sugestões de endereço após aguardar pausa na digitação (debounce de 300ms)
  function fetchAddressSuggestions(query) {
    if (!query || query.length < 4) {
      currentRequestId++
      if (addressTimeout) clearTimeout(addressTimeout)
      addressSuggestions.value = []
      addressLoading.value = false
      return
    }

    if (addressTimeout) clearTimeout(addressTimeout)
    const requestId = ++currentRequestId

    addressTimeout = setTimeout(async () => {
      addressLoading.value = true
      try {
        const resultados = await fetchNominatimAddress(query)
        // garante que respostas atrasadas não sobrescrevam o estado após um reset
        if (requestId === currentRequestId) {
          addressSuggestions.value = resultados
        }
      } finally {
        if (requestId === currentRequestId) {
          addressLoading.value = false
        }
      }
    }, 300)
  }

  // limpa o estado de busca e invalida qualquer requisição em andamento ou agendada
  function resetAddressSearch() {
    currentRequestId++
    if (addressTimeout) clearTimeout(addressTimeout)
    addressSearch.value = ''
    addressSuggestions.value = []
    addressLoading.value = false
  }

  return {
    addressSearch,
    addressSuggestions,
    addressLoading,
    fetchAddressSuggestions,
    resetAddressSearch,
  }
}
