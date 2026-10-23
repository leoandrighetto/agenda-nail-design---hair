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

  // consulta sugestões de endereço após aguardar pausa na digitação (debounce de 300ms)
  function fetchAddressSuggestions(query) {
    if (!query || query.length < 4) {
      addressSuggestions.value = []
      return
    }

    if (addressTimeout) clearTimeout(addressTimeout)

    addressTimeout = setTimeout(async () => {
      addressLoading.value = true
      try {
        addressSuggestions.value = await fetchNominatimAddress(query)
      } finally {
        addressLoading.value = false
      }
    }, 300)
  }

  // limpa o estado de busca e cancela qualquer requisição pendente do debounce
  function resetAddressSearch() {
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

