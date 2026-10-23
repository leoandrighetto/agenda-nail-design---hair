// Composables
import { createVuetify } from 'vuetify'
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const rosadosTheme = {
  dark: false,
  colors: {
    background: '#FDF5F5', // Fundo off-white com toque sutil rosado/avermelhado
    surface: '#FFFFFF', // Cards brancos para contraste limpo
    primary: '#A81C2C', // Vermelho carmim sofisticado e vibrante (sem marrom)
    secondary: '#DE5D6E', // Rosê avermelhado vivo e elegante
    accent: '#6B0F1A', // Bordô/vinho tinto profundo
    info: '#C25968', // Vermelho queimado suave
    error: '#D32F2F', // Vermelho vivo para alertas
    success: '#2E7D32',
    warning: '#ED6C02',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'rosadosTheme',
    themes: {
      rosadosTheme,
    },
  },
})
