/**
 * Serviço para consultas de endereços via Nominatim (OpenStreetMap).
 */
export const fetchNominatimAddress = async (query) => {
  if (!query || query.length < 4) return []

  try {
    // Limita a busca ao Brasil e pede os detalhes do endereço (addressdetails=1)
    const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&countrycodes=br&limit=5&addressdetails=1`)
    
    if (!res.ok) {
      throw new Error('Falha ao comunicar com a API Nominatim')
    }

    const data = await res.json()
    
    return data.map(item => {
      const addr = item.address || {}
      // Tenta pegar rua, bairro e cidade dos vários nomes possíveis que o Nominatim retorna
      const rua = addr.road || addr.pedestrian || addr.square || ''
      const bairro = addr.suburb || addr.neighbourhood || addr.city_district || ''
      const cidade = addr.city || addr.town || addr.village || addr.municipality || ''
      
      let parts = []
      // Se tiver rua, inclui. Se a pessoa já buscou com número, ele vem no addr.house_number
      if (rua) {
        parts.push(addr.house_number ? `${rua}, ${addr.house_number}` : rua)
      }
      if (bairro) parts.push(bairro)
      if (cidade) parts.push(cidade)
      
      // Fallback para o display_name caso a API não consiga quebrar em partes
      const formatted = parts.length > 0 ? parts.join(', ') : item.display_name
      
      return {
        ...item,
        formatted_address: formatted
      }
    })
  } catch (error) {
    console.error('Erro no serviço Nominatim:', error)
    return []
  }
}
