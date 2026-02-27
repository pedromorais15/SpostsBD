from flask import Flask, render_template, request
import requests

app = Flask(__name__)
BASE_URL = "https://www.thesportsdb.com/api/v1/json/3/"

 # SEU DICIONÁRIO DE LOGOS (Prioridade máxima)
CLUB_LOGOS = {

    # --- BRASIL ---
    "Flamengo": "https://logodetimes.com/times/flamengo/logo-flamengo-256.png",

    "Palmeiras": "https://logodetimes.com/times/palmeiras/logo-palmeiras-256.png",

    "Corinthians": "https://logodetimes.com/times/corinthians/logo-corinthians-256.png",

    "Sao Paulo": "https://logodetimes.com/times/sao-paulo/logo-sao-paulo-256.png",

    "Santos": "https://logodetimes.com/times/santos/logo-santos-256.png",

    "Gremio": "https://logodetimes.com/times/gremio/logo-gremio-256.png",

    "Internacional": "https://logodetimes.com/times/internacional/logo-internacional-256.png",

    "Cruzeiro": "https://logodetimes.com/times/cruzeiro/logo-cruzeiro-256.png",

    "Atletico Mineiro": "https://logodetimes.com/times/atletico-mineiro/logo-atletico-mineiro-256.png",

    "Fluminense": "https://logodetimes.com/times/fluminense/logo-fluminense-256.png",

    "Vasco": "https://logodetimes.com/times/vasco/logo-vasco-256.png",

    "Botafogo": "https://logodetimes.com/times/botafogo/logo-botafogo-256.png",

    # --- INGLATERRA ---
    "Manchester United": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg",
    "Manchester City": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    "Liverpool": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
    "Chelsea": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    "Arsenal": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
    "Tottenham": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg",

    # --- ESPANHA ---
    "Real Madrid": "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
    "Barcelona": "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
    "Atletico Madrid": "https://upload.wikimedia.org/wikipedia/en/f/f4/Atletico_Madrid_2017_logo.svg",
    "Sevilla": "https://upload.wikimedia.org/wikipedia/en/3/3b/Sevilla_FC_logo.svg",

    # --- ITALIA ---
    "Juventus": "https://upload.wikimedia.org/wikipedia/commons/1/15/Juventus_FC_2017_logo.svg",
    "AC Milan": "https://upload.wikimedia.org/wikipedia/commons/d/d0/AC_Milan_logo.svg",
    "Inter": "https://upload.wikimedia.org/wikipedia/commons/0/05/FC_Internazionale_Milano_2021.svg",
    "Napoli": "https://upload.wikimedia.org/wikipedia/commons/2/2d/SSC_Neapel.svg",
    "Roma": "https://upload.wikimedia.org/wikipedia/en/f/f7/AS_Roma_logo_%282017%29.svg",

    # --- ALEMANHA ---
    "Bayern Munich": "https://upload.wikimedia.org/wikipedia/en/1/1f/FC_Bayern_Munich_logo_%282017%29.svg",
    "Borussia Dortmund": "https://upload.wikimedia.org/wikipedia/commons/6/67/Borussia_Dortmund_logo.svg",
    "Bayer Leverkusen": "https://upload.wikimedia.org/wikipedia/en/5/59/Bayer_04_Leverkusen_logo.svg",

    # --- FRANÇA ---
    "Paris Saint Germain": "https://upload.wikimedia.org/wikipedia/en/a/a7/Paris_Saint-Germain_F.C..svg",
    "Marseille": "https://upload.wikimedia.org/wikipedia/en/2/2b/Olympique_de_Marseille_logo.svg",
    "Lyon": "https://upload.wikimedia.org/wikipedia/en/c/c6/Olympique_Lyonnais.svg",

    # --- PORTUGAL ---
    "Benfica": "https://upload.wikimedia.org/wikipedia/en/a/a2/SL_Benfica_logo.svg",
    "FC Porto": "https://upload.wikimedia.org/wikipedia/en/f/f1/FC_Porto.svg",
    "Sporting CP": "https://upload.wikimedia.org/wikipedia/en/e/e1/Sporting_Clube_de_Portugal_logo.svg",

    # --- ARGENTINA ---
    "Boca Juniors": "https://upload.wikimedia.org/wikipedia/commons/4/41/CABJ70.png",
    "River Plate": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Logo_River_Plate.svg",
    "Independiente": "https://upload.wikimedia.org/wikipedia/commons/4/48/CA_Independiente_logo.svg",

    # --- HOLANDA ---
    "Ajax": "https://upload.wikimedia.org/wikipedia/en/7/79/Ajax_Amsterdam.svg",
    "PSV Eindhoven": "https://upload.wikimedia.org/wikipedia/en/0/05/PSV_Eindhoven.svg",
    "Feyenoord": "https://upload.wikimedia.org/wikipedia/en/7/79/Feyenoord_logo.svg",

    # --- ARABIA ---
    "Al Hilal": "https://upload.wikimedia.org/wikipedia/en/5/55/Al_Hilal_SFC_Logo.svg",
    "Al Nassr": "https://upload.wikimedia.org/wikipedia/en/a/a9/Al-Nassr_FC_logo.svg",

    # --- AFRICA ---
    "Al Ahly": "https://upload.wikimedia.org/wikipedia/en/9/9f/Al_Ahly_SC_logo.svg",
    "Zamalek": "https://upload.wikimedia.org/wikipedia/en/0/0c/Zamalek_SC_logo.svg",

    "Lyon": "https://upload.wikimedia.org/wikipedia/en/c/c6/Olympique_Lyonnais.svg.png",

    "Al Nassr": "https://upload.wikimedia.org/wikipedia/en/a/a9/Al-Nassr_FC_logo.svg.png",

    "Newcastle": "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg.png",

    "Brentford": "https://upload.wikimedia.org/wikipedia/en/2/2a/Brentford_FC_crest.svg.png",

    "Fulham": "https://upload.wikimedia.org/wikipedia/en/e/eb/Fulham_FC_%28shield%29.svg.png",

    "Nottingham Forest": "https://upload.wikimedia.org/wikipedia/en/e/e5/Nottingham_Forest_F.C._logo.svg.png",

    "West Ham": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg.png",

    "Real Betis": "https://upload.wikimedia.org/wikipedia/en/1/13/Real_Betis_logo.svg.png"
}

CLUB_TITLES = {

    # --- BRASIL ---
    "Flamengo": ["38x Carioca", "8x Brasileirão", "4x Libertadores", "5x Copa do Brasil", "1x Mundial"],
    "Palmeiras": ["26x Paulista", "12x Brasileirão", "3x Libertadores", "4x Copa do Brasil", "1x Mundial"],
    "Sao Paulo": ["22x Paulista", "6x Brasileirão", "3x Libertadores", "1x Copa do Brasil", "3x Mundial"],
    "Santos": ["22x Paulista", "8x Brasileirão", "3x Libertadores", "1x Copa do Brasil", "2x Mundial"],
    "Corinthians": ["30x Paulista", "7x Brasileirão", "1x Libertadores", "3x Copa do Brasil", "2x Mundial"],
    "Gremio": ["43x Gauchão", "2x Brasileirão", "3x Libertadores", "5x Copa do Brasil", "1x Mundial"],
    "Internacional": ["45x Gauchão", "3x Brasileirão", "2x Libertadores", "1x Copa do Brasil", "1x Mundial"],
    "Cruzeiro": ["38x Mineiro", "4x Brasileirão", "2x Libertadores", "6x Copa do Brasil"],
    "Atletico Mineiro": ["49x Mineiro", "2x Brasileirão", "1x Libertadores", "2x Copa do Brasil"],
    "Fluminense": ["33x Carioca", "4x Brasileirão", "1x Libertadores", "1x Copa do Brasil"],
    "Vasco": ["24x Carioca", "4x Brasileirão", "1x Libertadores", "1x Copa do Brasil"],
    "Botafogo": ["21x Carioca", "2x Brasileirão", "1x Conmebol"],
    "Bahia": ["50x Baiano", "2x Brasileirão"],
    "Athletico Paranaense": ["28x Paranaense", "1x Brasileirão", "2x Sul-Americana", "1x Copa do Brasil"],
    "Fortaleza": ["46x Cearense", "2x Copa do Nordeste"],
    "Coritiba": ["39x Paranaense", "1x Brasileirão"],
    "Goias": ["28x Goiano"],
    "Sport": ["44x Pernambucano", "1x Copa do Brasil", "1x Brasileirão"],

    # --- INGLATERRA ---
    "Manchester City": ["10x Premier League", "1x Champions League", "7x FA Cup", "1x Mundial"],
    "Liverpool": ["19x Premier League", "6x Champions League", "8x FA Cup", "1x Mundial"],
    "Manchester United": ["20x Premier League", "3x Champions League", "13x FA Cup", "1x Mundial"],
    "Arsenal": ["13x Premier League", "14x FA Cup"],
    "Chelsea": ["6x Premier League", "2x Champions League", "8x FA Cup", "1x Mundial"],
    "Tottenham": ["2x Premier League", "8x FA Cup"],
    "Newcastle": ["4x Premier League", "6x FA Cup"],
    "Aston Villa": ["7x Premier League", "1x Champions League", "7x FA Cup"],

    # --- ESPANHA ---
    "Real Madrid": ["36x La Liga", "15x Champions League", "20x Copa del Rey", "5x Mundial"],
    "Barcelona": ["27x La Liga", "5x Champions League", "31x Copa del Rey", "3x Mundial"],
    "Atletico Madrid": ["11x La Liga", "10x Copa del Rey", "3x Europa League"],
    "Sevilla": ["1x La Liga", "7x Europa League"],
    "Valencia": ["6x La Liga", "1x UEFA Cup"],

    # --- ITALIA ---
    "Juventus": ["36x Serie A", "2x Champions League", "15x Coppa Italia"],
    "AC Milan": ["19x Serie A", "7x Champions League", "5x Coppa Italia", "1x Mundial"],
    "Inter": ["20x Serie A", "3x Champions League", "9x Coppa Italia", "1x Mundial"],
    "Napoli": ["3x Serie A", "6x Coppa Italia"],
    "Roma": ["3x Serie A", "9x Coppa Italia", "1x Conference League"],
    "Lazio": ["2x Serie A", "7x Coppa Italia"],

    # --- ALEMANHA ---
    "Bayern Munich": ["33x Bundesliga", "6x Champions League", "20x DFB-Pokal", "2x Mundial"],
    "Borussia Dortmund": ["8x Bundesliga", "1x Champions League", "5x DFB-Pokal"],
    "Bayer Leverkusen": ["1x Bundesliga", "1x DFB-Pokal", "1x UEFA Cup"],
    "Hamburg": ["6x Bundesliga", "1x Champions League"],
    "Werder Bremen": ["4x Bundesliga"],

    # --- PORTUGAL ---
    "Benfica": ["38x Primeira Liga", "2x Champions League", "26x Taça de Portugal"],
    "FC Porto": ["30x Primeira Liga", "2x Champions League", "20x Taça de Portugal", "2x Mundial"],
    "Sporting CP": ["20x Primeira Liga", "17x Taça de Portugal"],
    "Braga": ["3x Taça de Portugal"],

    # --- FRANÇA ---
    "Paris Saint Germain": ["12x Ligue 1", "15x Coupe de France"],
    "Marseille": ["9x Ligue 1", "1x Champions League"],
    "Lyon": ["7x Ligue 1"],
    "Monaco": ["8x Ligue 1"],

    # --- ARGENTINA ---
    "Boca Juniors": ["35x Liga Argentina", "6x Libertadores", "3x Intercontinental"],
    "River Plate": ["38x Liga Argentina", "4x Libertadores", "1x Intercontinental"],
    "Independiente": ["16x Liga Argentina", "7x Libertadores"],
    "Racing": ["18x Liga Argentina", "1x Libertadores"],

    # --- URUGUAI ---
    "Penarol": ["51x Liga Uruguaia", "5x Libertadores", "3x Intercontinental"],
    "Nacional": ["49x Liga Uruguaia", "3x Libertadores", "3x Intercontinental"],

    # --- ARABIA SAUDITA ---
    "Al Hilal": ["19x Saudi Pro League", "4x AFC Champions League"],
    "Al Nassr": ["9x Saudi Pro League"],
    "Al Ittihad": ["9x Saudi Pro League"],
    "Al Ahli": ["3x Saudi Pro League"],

    # --- MLS ---
    "LA Galaxy": ["5x MLS Cup", "1x Concacaf Champions"],
    "Seattle Sounders": ["2x MLS Cup", "1x Concacaf Champions"],
    "Inter Miami": ["1x Leagues Cup"],

    # --- HOLANDA ---
    "Ajax": ["36x Eredivisie", "4x Champions League"],
    "PSV Eindhoven": ["25x Eredivisie", "1x Champions League"],
    "Feyenoord": ["16x Eredivisie", "1x Champions League"],

    # --- TURQUIA ---
    "Galatasaray": ["24x Süper Lig", "1x UEFA Cup"],
    "Fenerbahce": ["19x Süper Lig"],
    "Besiktas": ["16x Süper Lig"],

    # --- AFRICA ---
    "Al Ahly": ["44x Egyptian Premier League", "12x CAF Champions League"],
    "Zamalek": ["14x Egyptian Premier League", "5x CAF Champions League"],
        # --- BRASIL (ADICIONAIS) ---
    "Bragantino": ["1x Paulista"],
    "Ceara": ["46x Cearense"],
    "Vitoria": ["30x Baiano"],
    "Santa Cruz": ["29x Pernambucano"],
    "Nautico": ["24x Pernambucano"],
    "America Mineiro": ["16x Mineiro"],
    "Chapecoense": ["7x Catarinense", "1x Sul-Americana"],

    # --- INGLATERRA (ADICIONAIS) ---
    "Leicester City": ["1x Premier League", "1x FA Cup"],
    "Everton": ["9x Premier League", "5x FA Cup"],
    "West Ham": ["3x FA Cup", "1x Conference League"],
    "Leeds United": ["3x Premier League"],
    "Nottingham Forest": ["1x Premier League", "2x Champions League"],

    # --- ESPANHA (ADICIONAIS) ---
    "Real Betis": ["1x La Liga", "3x Copa del Rey"],
    "Villarreal": ["1x Europa League"],
    "Real Sociedad": ["2x La Liga", "3x Copa del Rey"],
    "Athletic Bilbao": ["8x La Liga", "24x Copa del Rey"],

    # --- ITALIA (ADICIONAIS) ---
    "Atalanta": ["1x Europa League"],
    "Fiorentina": ["2x Serie A", "6x Coppa Italia"],
    "Torino": ["7x Serie A"],
    "Bologna": ["7x Serie A"],

    # --- ALEMANHA (ADICIONAIS) ---
    "RB Leipzig": ["2x DFB-Pokal"],
    "Schalke 04": ["7x Bundesliga", "5x DFB-Pokal", "1x UEFA Cup"],
    "Eintracht Frankfurt": ["1x Europa League"],
    "Stuttgart": ["5x Bundesliga"],

    # --- FRANÇA (ADICIONAIS) ---
    "Lille": ["4x Ligue 1"],
    "Saint Etienne": ["10x Ligue 1"],
    "Bordeaux": ["6x Ligue 1"],
    "Nice": ["4x Ligue 1"],

    # --- PORTUGAL (ADICIONAIS) ---
    "Boavista": ["1x Primeira Liga"],
    "Vitoria Guimaraes": ["1x Taca de Portugal"],

    # --- ARGENTINA (ADICIONAIS) ---
    "San Lorenzo": ["15x Liga Argentina", "1x Libertadores"],
    "Estudiantes": ["6x Liga Argentina", "4x Libertadores"],
    "Velez Sarsfield": ["10x Liga Argentina", "1x Libertadores"],
    "Newells Old Boys": ["6x Liga Argentina"],

    # --- CHILE ---
    "Colo Colo": ["33x Campeonato Chileno", "1x Libertadores"],
    "Universidad de Chile": ["18x Campeonato Chileno", "1x Sul-Americana"],
    "Universidad Catolica": ["16x Campeonato Chileno"],

    # --- COLOMBIA ---
    "Atletico Nacional": ["17x Liga Colombiana", "2x Libertadores"],
    "Millonarios": ["16x Liga Colombiana"],
    "America de Cali": ["15x Liga Colombiana"],

    # --- MEXICO ---
    "Club America": ["14x Liga MX", "7x Concacaf Champions"],
    "Chivas Guadalajara": ["12x Liga MX"],
    "Cruz Azul": ["9x Liga MX", "6x Concacaf Champions"],
    "Pumas UNAM": ["7x Liga MX"],

    # --- MLS (ADICIONAIS) ---
    "Atlanta United": ["1x MLS Cup"],
    "New York City FC": ["1x MLS Cup"],
    "Columbus Crew": ["3x MLS Cup"],

    # --- JAPAO ---
    "Kashima Antlers": ["8x J1 League", "1x AFC Champions League"],
    "Urawa Red Diamonds": ["3x AFC Champions League"],
    "Yokohama F Marinos": ["5x J1 League"],

    # --- COREIA DO SUL ---
    "Jeonbuk Hyundai Motors": ["9x K League 1", "2x AFC Champions League"],
    "Pohang Steelers": ["5x K League 1", "3x AFC Champions League"],

    # --- AFRICA (ADICIONAIS) ---
    "Wydad Casablanca": ["22x Botola", "3x CAF Champions League"],
    "Raja Casablanca": ["13x Botola", "3x CAF Champions League"],
    "Esperance": ["32x Tunisian League", "4x CAF Champions League"],

    # --- TURQUIA (ADICIONAIS) ---
    "Trabzonspor": ["7x Super Lig"],

    # --- ESCÓCIA ---
    "Celtic": ["54x Scottish League", "1x Champions League"],
    "Rangers": ["55x Scottish League", "1x Cup Winners Cup"],
    
    # --- FRANÇA ---
    "Lyon": [
        "7x Ligue 1",
        "5x Coupe de France",
        "8x Supercopa da França"
    ],

    # --- ARÁBIA SAUDITA ---
    "Al Nassr": [
        "9x Saudi Pro League",
        "6x King Cup",
        "2x Supercopa Saudita",
        "1x Arab Club Champions Cup"
    ],

    # --- INGLATERRA ---
    "Newcastle": [
        "4x Premier League",
        "6x FA Cup",
        "1x Inter-Cities Fairs Cup"
    ],

    "Brentford": [
        "2x Championship",
        "1x League One"
    ],

    "Fulham": [
        "3x Championship",
        "1x Intertoto Cup"
    ],

    "Nottingham Forest": [
        "1x Premier League",
        "2x Champions League",
        "4x League Cup"
    ],

    "West Ham": [
        "3x FA Cup",
        "1x Europa Conference League",
        "1x Cup Winners Cup"
    ],

    # --- ESPANHA ---
    "Real Betis": [
        "1x La Liga",
        "3x Copa del Rey"
    ]
}

@app.route('/', methods=['GET', 'POST'])
def index():
    club_data = None
    players = []
    past_events = []
    honors = []
    error_msg = None
    logo_final = None
    
    if request.method == 'POST':
        team_name = request.form.get('team_name').strip()
        try:
            # 1. Busca os dados básicos do time na API
            response = requests.get(f"{BASE_URL}searchteams.php?t={team_name}")
            data = response.json()
            
            if data.get('teams'):
                # Pegamos o primeiro resultado (mais relevante)
                club_data = data['teams'][0]
                team_id = club_data['idTeam']
                official_name = club_data['strTeam']
                
                # --- LÓGICA DE ESCUDO (LOGO) ---
                # Prioridade: Dicionário manual -> API -> Fallback Genérico
                logo_final = CLUB_LOGOS.get(official_name, CLUB_LOGOS.get(team_name))
                if not logo_final:
                    logo_final = club_data.get('strTeamBadge')
                if not logo_final:
                    logo_final = "https://logodetimes.com/wp-content/uploads/2017/12/default.png"
                
                # --- LÓGICA DE TÍTULOS (HONORS) ---
                # Busca inteligente: verifica se o nome oficial ou o termo digitado 
                # existe como chave no seu dicionário de títulos.
                for key in CLUB_TITLES:
                    if key.lower() in official_name.lower() or key.lower() in team_name.lower():
                        honors = CLUB_TITLES[key]
                        break

                # --- DADOS EXTRAS DA API ---
                # Busca o elenco (players)
                p_resp = requests.get(f"{BASE_URL}lookup_all_players.php?id={team_id}")
                players = p_resp.json().get('player', []) or []
                
                # Busca últimos resultados (past events)
                past_resp = requests.get(f"{BASE_URL}eventslast.php?id={team_id}")
                past_events = past_resp.json().get('results', []) or []

            else:
                error_msg = f"Clube '{team_name}' não encontrado no banco de dados global."
        
        except Exception as e:
            print(f"Erro: {e}")
            error_msg = "Erro ao conectar com o servidor de esportes. Tente novamente."

    return render_template('index.html', 
                           club=club_data, 
                           players=players, 
                           past=past_events, 
                           honors=honors, 
                           error=error_msg,
                           logo=logo_final)
@app.errorhandler(404)
def page_not_found(e):
    # O segundo valor é o código de status do erro
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)