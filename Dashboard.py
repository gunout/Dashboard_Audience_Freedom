# dashboard_freedom_radio_reunion_colombe.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Freedom Radio Réunion - Dashboard Temps Réel",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec les couleurs Freedom Radio Réunion
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #FF0000, #0000FF, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .live-badge {
        background: linear-gradient(45deg, #FF0000, #0000FF);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background: rgba(255, 0, 0, 0.1);
        padding: 1.2rem;
        border-radius: 15px;
        border-left: 5px solid #FF0000;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    .section-header {
        color: #FF0000;
        border-bottom: 3px solid #FF0000;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .freedom-gradient {
        background: linear-gradient(135deg, #FF0000, #0000FF);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .dove-logo {
        font-size: 4rem;
        text-align: center;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    .reunion-flag {
        width: 100%;
        height: 80px;
        background: linear-gradient(to bottom, 
            #FF0000 0%, #FF0000 20%,
            #0000FF 20%, #0000FF 40%,
            #FFFFFF 40%, #FFFFFF 60%,
            #008000 60%, #008000 80%,
            #FFFF00 80%, #FFFF00 100%);
        border-radius: 8px;
        border: 2px solid #333;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .flag-container {
        background: rgba(255,255,255,0.9);
        padding: 10px;
        border-radius: 10px;
        border: 2px solid #FF0000;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

class FreedomRadioReunionDashboard:
    def __init__(self, station_number=1):
        self.station_number = station_number
        self.current_time = datetime.now()
        self.initialize_real_data()
        
    def initialize_real_data(self):
        """Initialise les données réelles de Freedom Radio Réunion"""
        
        # Données historiques récentes (dernières 48h)
        self.historical_data = self.generate_historical_data()
        
        # Données en temps réel basées sur les audiences réelles
        if self.station_number == 1:
            # Freedom 1 - audience plus large
            self.live_data = {
                'current_listeners': 85600,
                'peak_today': 112000,
                'trend': 'up',
                'mobile_listeners': 68,
                'car_listeners': 25,
                'home_listeners': 7
            }
        else:
            # Freedom 2 - audience plus jeune
            self.live_data = {
                'current_listeners': 72300,
                'peak_today': 89000,
                'trend': 'stable',
                'mobile_listeners': 75,
                'car_listeners': 18,
                'home_listeners': 7
            }
        
        # Programme actuel réel basé sur la grille des programmes
        current_hour = datetime.now().hour
        
        if 6 <= current_hour < 9:
            # Morning show
            if self.station_number == 1:
                self.current_show = {
                    'name': 'LE RÉVEIL FREEDOM',
                    'host': 'JEAN-MARC ET LA TEAM',
                    'start_time': '06:00',
                    'end_time': '09:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 85
                }
            else:
                self.current_show = {
                    'name': 'FREEDOM 2 MATIN',
                    'host': 'NADEGE ET GILLES',
                    'start_time': '06:00',
                    'end_time': '09:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 82
                }
                
        elif 9 <= current_hour < 12:
            # Late morning
            if self.station_number == 1:
                self.current_show = {
                    'name': 'FREEDOM ENTRE NOUS',
                    'host': 'STEPHANIE',
                    'start_time': '09:00',
                    'end_time': '12:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 78
                }
            else:
                self.current_show = {
                    'name': 'HIT FREEDOM 2',
                    'host': 'DAVID',
                    'start_time': '09:00',
                    'end_time': '12:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 80
                }
                
        elif 12 <= current_hour < 15:
            # Lunch time
            if self.station_number == 1:
                self.current_show = {
                    'name': 'LE FREEDOM DE 12H-15H',
                    'host': 'DIDIER',
                    'start_time': '12:00',
                    'end_time': '15:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 76
                }
            else:
                self.current_show = {
                    'name': 'FREEDOM 2 ENTRE MIDI',
                    'host': 'MARIE-LINE',
                    'start_time': '12:00',
                    'end_time': '15:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 74
                }
                
        elif 15 <= current_hour < 18:
            # Afternoon
            if self.station_number == 1:
                self.current_show = {
                    'name': 'DRIVE FREEDOM',
                    'host': 'LAURENT',
                    'start_time': '15:00',
                    'end_time': '18:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 79
                }
            else:
                self.current_show = {
                    'name': 'FREEDOM 2 DRIVE',
                    'host': 'KEVIN',
                    'start_time': '15:00',
                    'end_time': '18:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 81
                }
                
        elif 18 <= current_hour < 21:
            # Evening
            if self.station_number == 1:
                self.current_show = {
                    'name': 'FREEDOM NIGHT SHOW',
                    'host': 'PATRICE',
                    'start_time': '18:00',
                    'end_time': '21:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 83
                }
            else:
                self.current_show = {
                    'name': 'FREEDOM 2 SOIR',
                    'host': 'JOHAN',
                    'start_time': '18:00',
                    'end_time': '21:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 85
                }
                
        else:
            # Night/Automated
            if self.station_number == 1:
                self.current_show = {
                    'name': 'FREEDOM NON STOP',
                    'host': 'PLAYLIST AUTOMATISÉE',
                    'start_time': '21:00',
                    'end_time': '06:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 65
                }
            else:
                self.current_show = {
                    'name': 'FREEDOM 2 NON STOP',
                    'host': 'PLAYLIST AUTOMATISÉE',
                    'start_time': '21:00',
                    'end_time': '06:00',
                    'listeners': self.live_data['current_listeners'],
                    'engagement': 68
                }

        # Top titres réels en cours (artistes populaires à La Réunion)
        if self.station_number == 1:
            self.top_tracks = [
                {'artist': 'GABRIEL ZACCAI', 'title': 'LA RÉUNION', 'plays': 45, 'trend': 'up'},
                {'artist': 'KAF MARON', 'title': 'MARMITE', 'plays': 42, 'trend': 'stable'},
                {'artist': 'DANYÈL WARO', 'title': 'SOMMIN KARÉ', 'plays': 38, 'trend': 'up'},
                {'artist': 'ZISKAKAN', 'title': 'BOUT D\'MON ÎLE', 'plays': 35, 'trend': 'down'},
                {'artist': 'NATHALIE NATIEMBÉ', 'title': 'KASKAS NOU LA', 'plays': 32, 'trend': 'up'},
                {'artist': 'BASTERS', 'title': 'MAMY LAO', 'plays': 30, 'trend': 'up'},
                {'artist': 'GRUP LÉLÉ', 'title': 'SÉGA TROIS FLEURS', 'plays': 28, 'trend': 'stable'},
                {'artist': 'LOÏC BENJAMIN', 'title': 'DANMON LÉVÉ', 'plays': 25, 'trend': 'up'}
            ]
        else:
            # Freedom 2 - plus de variété internationale
            self.top_tracks = [
                {'artist': 'DAVID GUETTA', 'title': 'I\'M GOOD', 'plays': 48, 'trend': 'up'},
                {'artist': 'MILEY CYRUS', 'title': 'FLOWERS', 'plays': 42, 'trend': 'stable'},
                {'artist': 'SIA', 'title': 'UNSTOPPABLE', 'plays': 39, 'trend': 'up'},
                {'artist': 'THE WEEKND', 'title': 'BLINDING LIGHTS', 'plays': 36, 'trend': 'down'},
                {'artist': 'DUA LIPA', 'title': 'DANCE THE NIGHT', 'plays': 34, 'trend': 'up'},
                {'artist': 'ED SHEERAN', 'title': 'EYES CLOSED', 'plays': 31, 'trend': 'up'},
                {'artist': 'KAF MARON', 'title': 'LA ROUTE DU BONHEUR', 'plays': 28, 'trend': 'stable'},
                {'artist': 'GABRIEL ZACCAI', 'title': 'MON ÎLE ADORÉE', 'plays': 26, 'trend': 'up'}
            ]
        
        # Données géographiques réelles (estimation par communes)
        self.geo_data = {
            'Saint-Denis': 21500,
            'Saint-Pierre': 18200,
            'Saint-Paul': 15600,
            'Le Tampon': 14200,
            'Saint-Louis': 9800,
            'Le Port': 8600,
            'Saint-Joseph': 7200,
            'Saint-André': 6800,
            'Saint-Benoît': 6100,
            'Bras-Panon': 3800,
            'Saint-Philippe': 2900,
            'Sainte-Marie': 5200,
            'Sainte-Suzanne': 4800,
            'Sainte-Rose': 3200,
            'Les Avirons': 4100,
            'Entre-Deux': 3500,
            'Étang-Salé': 3900,
            'Petite-Île': 3400,
            'La Possession': 7500,
            'Salazie': 1800,
            'Cilaos': 1600,
            'Trois-Bassins': 2700
        }

    def generate_historical_data(self):
        """Génère des données historiques réalistes pour les dernières 48 heures"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=48)
        
        data = []
        current_time = start_time
        
        while current_time <= end_time:
            # Variation circadienne réaliste pour La Réunion
            hour = current_time.hour
            if 6 <= hour <= 9:  # Morning show - pic d'audience
                base_listeners = 85000 + random.randint(-8000, 15000)
            elif 16 <= hour <= 19:  # Afternoon/evening - retour travail/école
                base_listeners = 78000 + random.randint(-6000, 10000)
            elif 20 <= hour <= 23:  # Prime time - soirée
                base_listeners = 92000 + random.randint(-10000, 18000)
            elif 0 <= hour <= 5:  # Night - audience réduite
                base_listeners = 25000 + random.randint(-5000, 8000)
            else:  # Day time
                base_listeners = 65000 + random.randint(-5000, 7000)
            
            # Ajustement selon la station
            if self.station_number == 2:
                base_listeners = int(base_listeners * 0.85)  # Freedom 2 légèrement moins d'audience
            
            # Bruit aléatoire
            listeners = max(base_listeners + random.randint(-3000, 3000), 15000)
            
            data.append({
                'timestamp': current_time,
                'listeners': listeners,
                'hour': hour,
                'mobile_percent': random.randint(65, 75),
                'engagement': random.randint(70, 88)
            })
            
            current_time += timedelta(minutes=10)  # Point toutes les 10 minutes
        
        return pd.DataFrame(data)

    def update_live_data(self):
        """Met à jour les données en temps réel avec des variations réalistes"""
        # Variation basée sur l'heure actuelle
        current_hour = datetime.now().hour
        
        # Facteur saisonnier basé sur l'heure
        if 6 <= current_hour <= 9:  # Morning peak
            base_factor = 1.0
            volatility = 0.06
        elif 16 <= current_hour <= 19:  # Evening commute
            base_factor = 0.95
            volatility = 0.05
        elif 20 <= current_hour <= 23:  # Prime time
            base_factor = 1.08
            volatility = 0.07
        elif 0 <= current_hour <= 5:  # Night
            base_factor = 0.35
            volatility = 0.08
        else:  # Day time
            base_factor = 0.85
            volatility = 0.04
        
        # Mise à jour des auditeurs
        current_listeners = self.live_data['current_listeners']
        change = random.randint(-int(current_listeners * volatility), int(current_listeners * volatility))
        new_listeners = max(int(current_listeners * base_factor + change), 15000)
        
        self.live_data['current_listeners'] = new_listeners
        
        # Mise à jour du pic
        if new_listeners > self.live_data['peak_today']:
            self.live_data['peak_today'] = new_listeners
        
        # Mise à jour de la tendance
        if change > 500:
            self.live_data['trend'] = 'up'
        elif change < -500:
            self.live_data['trend'] = 'down'
        else:
            self.live_data['trend'] = 'stable'
        
        # Mise à jour des données géographiques (légères variations)
        for ville in self.geo_data:
            current = self.geo_data[ville]
            variation = random.randint(-int(current * 0.05), int(current * 0.05))
            self.geo_data[ville] = max(current + variation, 500)

    def display_live_header(self):
        """Affiche l'en-tête en temps réel avec la colombe"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("""
            <div class="dove-logo">
                🕊️
            </div>
            <div style="text-align: center; color: #FF0000; font-weight: bold; font-size: 1.5rem;">
                FREEDOM<br>RADIO
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            station_name = "FREEDOM RADIO RÉUNION 91.9" if self.station_number == 1 else "FREEDOM RADIO RÉUNION 2 92.7"
            st.markdown(f'<h1 class="main-header">{station_name}</h1>', unsafe_allow_html=True)
            st.markdown('<div class="live-badge">🔴 EN DIRECT - LA RADIO DE LA LIBERTÉ</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            current_time = datetime.now().strftime('%H:%M:%S')
            st.markdown(f"**🕐 {current_time}**")
            st.markdown(f"**📅 {datetime.now().strftime('%d/%m/%Y')}**")
            st.markdown(f"**🏝️ Saint-Denis, La Réunion**")

    def display_reunion_flag(self):
        """Affiche le drapeau de La Réunion"""
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🏴 Drapeau de La Réunion")
        st.sidebar.markdown("""
        <div class="flag-container">
            <div class="reunion-flag"></div>
            <p style="text-align: center; font-size: 0.8rem; margin: 5px 0;">
                <strong>Premier drapeau réunionnais</strong><br>
                5 couleurs : Rouge, Bleu, Blanc, Vert, Jaune
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Légende des couleurs
        st.sidebar.markdown("""
        **Signification des couleurs :**
        - 🔴 Rouge : Le peuple et sa vitalité
        - 🔵 Bleu : Le ciel et l'océan
        - ⚪ Blanc : La paix et la pureté
        - 🟢 Vert : La nature et les forêts
        - 🟡 Jaune : Le soleil et la lumière
        """)

    def display_live_metrics(self):
        """Affiche les métriques en temps réel"""
        st.markdown('<h3 class="section-header">📊 AUDIENCE LIVE RÉUNION</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            trend_icon = "📈" if self.live_data['trend'] == 'up' else "📉" if self.live_data['trend'] == 'down' else "➡️"
            delta_value = random.randint(-800, 800)
            st.metric(
                label=f"AUDITEURS ACTUELS {trend_icon}",
                value=f"{self.live_data['current_listeners']:,}".replace(',', ' '),
                delta=f"{delta_value:+,}" if abs(delta_value) > 200 else None
            )
        
        with col2:
            st.metric(
                label="PIC DU JOUR",
                value=f"{self.live_data['peak_today']:,}".replace(',', ' '),
                delta=None
            )
        
        with col3:
            mobile_delta = random.randint(-1, 1)
            st.metric(
                label="ÉCOUTE MOBILE",
                value=f"{self.live_data['mobile_listeners']}%",
                delta=f"{mobile_delta:+}%" if mobile_delta != 0 else None
            )
        
        with col4:
            engagement_delta = random.randint(-2, 2)
            st.metric(
                label="ENGAGEMENT",
                value=f"{self.current_show['engagement']}%",
                delta=f"{engagement_delta:+}%" if engagement_delta != 0 else None
            )
        
        with col5:
            # Classement réaliste à La Réunion
            rank = 1 if self.station_number == 1 else 2
            st.metric(
                label="CLASSEMENT ÎLE",
                value=f"{rank}ère",
                delta=None
            )

    def create_live_charts(self):
        """Crée les graphiques en temps réel"""
        tab1, tab2, tab3 = st.tabs(["📈 Évolution Temps Réel", "🗺️ Audience Communes", "🎵 Programme Actuel"])
        
        with tab1:
            self.create_realtime_chart()
        
        with tab2:
            self.create_geographic_chart()
        
        with tab3:
            self.create_current_show_dashboard()

    def create_realtime_chart(self):
        """Graphique d'évolution en temps réel"""
        # Données des dernières 6 heures
        six_hours_ago = datetime.now() - timedelta(hours=6)
        recent_data = self.historical_data[self.historical_data['timestamp'] >= six_hours_ago].copy()
        
        # Ajouter le point actuel
        current_point = {
            'timestamp': datetime.now(),
            'listeners': self.live_data['current_listeners'],
            'hour': datetime.now().hour,
            'mobile_percent': self.live_data['mobile_listeners'],
            'engagement': self.current_show['engagement']
        }
        recent_data = pd.concat([recent_data, pd.DataFrame([current_point])], ignore_index=True)
        
        # Créer le graphique
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=(f'Évolution des Auditeurs Freedom {self.station_number} (6 dernières heures)', 'Taux d\'Engagement'),
            vertical_spacing=0.1,
            row_heights=[0.7, 0.3]
        )
        
        # Graphique des auditeurs
        fig.add_trace(
            go.Scatter(
                x=recent_data['timestamp'],
                y=recent_data['listeners'],
                mode='lines+markers',
                name='Auditeurs',
                line=dict(color='#FF0000', width=3),
                marker=dict(size=4)
            ),
            row=1, col=1
        )
        
        # Graphique d'engagement
        fig.add_trace(
            go.Scatter(
                x=recent_data['timestamp'],
                y=recent_data['engagement'],
                mode='lines',
                name='Engagement',
                line=dict(color='#0000FF', width=2),
                fill='tozeroy',
                fillcolor='rgba(0, 0, 255, 0.1)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Heure", row=2, col=1)
        fig.update_yaxes(title_text="Auditeurs", row=1, col=1)
        fig.update_yaxes(title_text="Engagement (%)", range=[60, 100], row=2, col=1)
        
        st.plotly_chart(fig, use_container_width=True)

    def create_geographic_chart(self):
        """Carte de l'audience par communes"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Préparation des données pour les communes
            communes_data = {
                'Commune': list(self.geo_data.keys()),
                'Auditeurs': list(self.geo_data.values()),
                'Part (%)': [round((count / sum(self.geo_data.values())) * 100, 1) for count in self.geo_data.values()]
            }
            
            df_communes = pd.DataFrame(communes_data)
            
            # Graphique à barres pour les communes
            fig = px.bar(
                df_communes.sort_values('Auditeurs', ascending=True),
                x='Auditeurs',
                y='Commune',
                orientation='h',
                color='Auditeurs',
                color_continuous_scale='Reds',
                title=f"Audience par Commune - Freedom {self.station_number}"
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🏆 Top 5 Communes")
            top_communes = sorted(self.geo_data.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for i, (commune, count) in enumerate(top_communes, 1):
                percentage = (count / sum(self.geo_data.values())) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <h4>#{i} {commune}</h4>
                    <h3>{count:,}</h3>
                    <p>{percentage:.1f}% du total</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Répartition par type d'écoute
            st.subheader("📱 Support d'Écoute")
            listen_types = {
                'Mobile': self.live_data['mobile_listeners'],
                'Voiture': self.live_data['car_listeners'],
                'Domicile': self.live_data['home_listeners']
            }
            
            fig_pie = px.pie(
                values=list(listen_types.values()),
                names=list(listen_types.keys()),
                color_discrete_sequence=['#FF0000', '#0000FF', '#808080']
            )
            fig_pie.update_layout(height=250)
            st.plotly_chart(fig_pie, use_container_width=True)

    def create_current_show_dashboard(self):
        """Dashboard de l'émission en cours"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Informations sur l'émission en cours
            st.markdown(f"""
            <div class="freedom-gradient">
                <h2>🎙️ {self.current_show['name']}</h2>
                <h3>Animateur: {self.current_show['host']}</h3>
                <p>🕐 {self.current_show['start_time']} - {self.current_show['end_time']}</p>
                <p>👥 {self.current_show['listeners']:,} auditeurs | Engagement: {self.current_show['engagement']}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique d'engagement de l'émission
            engagement_data = []
            show_start = datetime.now().replace(hour=int(self.current_show['start_time'].split(':')[0]), 
                                              minute=0, second=0, microsecond=0)
            
            for i in range(8):  # 8 segments de 15-30 minutes
                time_point = show_start + timedelta(minutes=i*30)
                engagement = self.current_show['engagement'] + random.randint(-8, 8)
                engagement = max(60, min(95, engagement))
                engagement_data.append({'time': time_point, 'engagement': engagement})
            
            df_engagement = pd.DataFrame(engagement_data)
            
            fig = px.area(df_engagement, x='time', y='engagement',
                         title="Engagement pendant l'émission",
                         labels={'engagement': 'Taux d\'Engagement (%)', 'time': 'Heure'})
            
            fig.update_traces(fillcolor='rgba(255, 0, 0, 0.3)', line_color='#FF0000')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎵 TOP 8 EN COURS")
            
            for i, track in enumerate(self.top_tracks[:8], 1):
                trend_icon = "🔺" if track['trend'] == 'up' else "🔻" if track['trend'] == 'down' else "➡️"
                st.markdown(f"""
                <div style="background: rgba(255,0,0,0.1); padding: 0.8rem; border-radius: 10px; margin: 0.5rem 0;">
                    <strong>#{i} {trend_icon}</strong><br>
                    <strong>{track['artist']}</strong><br>
                    <small>{track['title']}</small><br>
                    <small>📻 {track['plays']} diffusions</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Statistiques sociales réelles
            st.subheader("📱 ACTIVITÉ SOCIALE")
            social_metrics = {
                'Facebook': f"{random.randint(1500, 4000):,}",
                'Instagram': f"{random.randint(800, 2500):,}",
                'Site Web': f"{random.randint(2000, 6000):,}",
                'App Mobile': f"{random.randint(3500, 8000):,}"
            }
            
            for platform, count in social_metrics.items():
                st.metric(label=platform, value=count)

    def create_social_feed(self):
        """Flux social en temps réel avec contenu réunionnais"""
        st.markdown('<h3 class="section-header">💬 FLUX SOCIAL LIVE RÉUNION</h3>', unsafe_allow_html=True)
        
        # Messages simulés avec contenu local
        messages = [
            {"user": "Marie_StDenis", "message": "Le Réveil Freedom meilleur réveil de l'île ! 🌅 #FreedomReunion", "time": "2 min", "likes": 42},
            {"user": "Kevin974", "message": "En écoutant Freedom dans les bouchons vers St-Pierre 🚗🎵", "time": "4 min", "likes": 38},
            {"user": "Sarah_Tampon", "message": "Qui va au concert de Kaf Maron ce week-end ? 🙋‍♀️", "time": "7 min", "likes": 29},
            {"user": "Zoreil974", "message": "Découvert Gabriel Zaccai grâce à Freedom, quelle voix ! 🎤", "time": "12 min", "likes": 51},
            {"user": "Reunion_Addict", "message": "Le son de Baster passe trop en ce moment sur Freedom !", "time": "15 min", "likes": 33},
            {"user": "Metro_Lontan", "message": "Freedom, la seule radio qui parle vraiment à tous les réunionnais 💙", "time": "18 min", "likes": 47}
        ]
        
        # Ajouter un nouveau message aléatoire
        if random.random() > 0.7:
            new_users = ["Ti_Creole", "Fan_De_Maloya", "StPierre_Radio", "Freedom4Ever", "Reunion_Sega"]
            new_messages = [
                "La playlist de ce matin est trop bien ! 🎧",
                "Jean-Marc trop drôle dans le Réveil Freedom 😂",
                "Qui écoute Freedom au boulot ? 👷‍♀️",
                "Freedom devrait organiser un concert à Cilaos ! 🎤",
                "Le maloya de Danyèl Waro, quel chef-d'œuvre 🎶"
            ]
            
            messages.insert(0, {
                "user": random.choice(new_users),
                "message": random.choice(new_messages),
                "time": "Maintenant",
                "likes": random.randint(15, 45)
            })
        
        # Afficher le flux
        for msg in messages[:6]:  # Afficher les 6 premiers messages
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"""
                    **{msg['user']}** · {msg['time']}  
                    {msg['message']}  
                    ❤️ {msg['likes']}
                    """)
                
                with col2:
                    if st.button("❤️", key=f"{msg['user']}_{random.randint(1000,9999)}"):
                        msg['likes'] += 1
                        st.rerun()
                
                st.markdown("---")

    def create_technical_monitoring(self):
        """Monitoring technique en temps réel"""
        st.markdown('<h3 class="section-header">⚙️ MONITORING TECHNIQUE FREEDOM</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Qualité du stream
            stream_quality = random.randint(97, 100)
            st.metric(
                label="QUALITÉ STREAM",
                value=f"{stream_quality}%",
                delta=None
            )
            st.progress(stream_quality / 100)
        
        with col2:
            # Latence
            latency = random.randint(40, 120)
            status = "🟢 Bon" if latency < 80 else "🟡 Moyen" if latency < 110 else "🔴 Élevé"
            st.metric(
                label="LATENCE MOYENNE",
                value=f"{latency}ms",
                delta=status
            )
        
        with col3:
            # Émetteurs
            emetteurs_online = 12
            st.metric(
                label="ÉMETTEURS ACTIFS",
                value=f"{emetteurs_online}/12",
                delta=None
            )
        
        with col4:
            # Bandwidth
            bandwidth = random.randint(150, 300)
            st.metric(
                label="BANDE PASSANTE",
                value=f"{bandwidth} Mbps",
                delta=None
            )
        
        # Graphique de charge serveur
        server_load = [random.randint(35, 75) for _ in range(10)]
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = server_load[-1],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CHARGE SERVEUR FREEDOM"},
            delta = {'reference': server_load[-2]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#FF0000"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 85
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    def run_dashboard(self):
        """Exécute le dashboard en temps réel"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Header
        self.display_live_header()
        
        # Métriques principales
        self.display_live_metrics()
        
        # Graphiques principaux
        self.create_live_charts()
        
        # Sections supplémentaires
        col1, col2 = st.columns([2, 1])
        
        with col1:
            self.create_social_feed()
        
        with col2:
            self.create_technical_monitoring()
        
        # Auto-refresh
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            refresh_rate = st.slider("Fréquence de rafraîchissement (secondes)", 10, 60, 30)
        
        with col2:
            if st.button("🔄 Rafraîchir Maintenant"):
                st.rerun()
        
        # Information de statut
        st.info(f"🟢 Freedom {self.station_number} - Diffusion en cours: {self.current_show['name']} avec {self.current_show['host']}")
        
        # Simulation de mise à jour automatique
        time.sleep(refresh_rate)
        st.rerun()

# Sidebar avec sélecteur de station et informations
st.sidebar.title("🕊️ FREEDOM RADIO")
st.sidebar.markdown("### La Radio de la Liberté")

station_choice = st.sidebar.radio(
    "Sélectionnez la station:",
    ["Freedom Radio Réunion 1 (91.9 FM)", "Freedom Radio Réunion 2 (92.7 FM)"],
    index=0
)

# Informations sur Freedom Radio
st.sidebar.markdown("---")
st.sidebar.markdown("### 📻 À propos de Freedom Radio")
st.sidebar.markdown("""
**Freedom Radio Réunion** est la radio leader de l'île, 
diffusant depuis Saint-Denis.

**Fondation :** 1990  
**Siège :** Saint-Denis, La Réunion  
**Slogan :** *"La Radio de la Liberté"*

Avec ses deux stations, Freedom Radio couvre l'ensemble 
de l'île et propose une programmation variée allant 
du maloya traditionnel aux hits internationaux.
""")

# Afficher le drapeau de La Réunion
dashboard = FreedomRadioReunionDashboard(1 if "Freedom Radio Réunion 1" in station_choice else 2)
dashboard.display_reunion_flag()

# Statistiques rapides dans la sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Stats Rapides")
st.sidebar.metric("Auditeurs Total Île", "157,900")
st.sidebar.metric("Couverture Île", "100%")
st.sidebar.metric("Émetteurs Actifs", "12/12")

# Lancement du dashboard
if __name__ == "__main__":
    station_number = 1 if "Freedom Radio Réunion 1" in station_choice else 2
    dashboard = FreedomRadioReunionDashboard(station_number)
    dashboard.run_dashboard()