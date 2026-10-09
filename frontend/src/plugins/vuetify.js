// Composables
import { createVuetify } from 'vuetify'
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const rosadosTheme = {
  dark: false,
  colors: {
    background: '#FDF4F0', // Fundo nude bem claro, suave e feminino
    surface: '#FFFFFF', // Cards brancos para dar contraste limpo
    primary: '#853C40', // O tom marsala/vinho profundo do texto do flyer
    secondary: '#D0A09A', // Um rosê intermediário para detalhes
    accent: '#613333', // O marrom mais escuro da caixa de agendamento do rodapé
    info: '#A88D8A', // Um tom pastel acinzentado-rosado
    error: '#D32F2F', // Vermelho das unhas, como cor de erro/destaque
    success: '#388E3C',
    warning: '#F57C00',
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
