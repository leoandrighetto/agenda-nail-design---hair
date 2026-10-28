// Composables
import { createVuetify } from 'vuetify'
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const rosadosTheme = {
  dark: false,
  colors: {
    background: '#FAF3EC', // Cream (Creme / Off-white)
    surface: '#FFFFFF', // Cards brancos para contraste limpo
    primary: '#B76E79', // Rosa Ouro (Rose Gold)
    secondary: '#F2D4D0', // Blush (Rosa-bebê suave)
    accent: '#8E5E66', // Mauve (Malva)
    info: '#B87333', // Copper (Cobre)
    error: '#D32F2F', // Mantido para feedback visual de erro
    success: '#2E7D32', // Mantido para feedback visual de sucesso
    warning: '#ED6C02', // Mantido para feedback visual de aviso
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
