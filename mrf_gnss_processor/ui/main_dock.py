from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import (
    QDockWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QFrame, QComboBox,
    QCheckBox, QProgressBar, QTabWidget, QTextEdit, QSplitter, QLineEdit,
    QSpinBox, QHeaderView, QSizePolicy
)
from qgis.PyQt.QtGui import QFont

from ..themes.theme_manager import ThemeManager


class Card(QFrame):
    def __init__(self, title="", accent="blue", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 8, 10, 10)
        self.layout.setSpacing(8)
        if title:
            label = QLabel(title)
            label.setObjectName(f"sectionTitle_{accent}")
            self.layout.addWidget(label)


class MRFProcessorDock(QDockWidget):
    def __init__(self, iface, parent=None):
        super().__init__("MRF GNSS Processor", parent)
        self.iface = iface
        self.theme_manager = ThemeManager()
        self.setObjectName("MRFGNSSProcessorDock")
        self.setMinimumWidth(1180)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        root = QWidget()
        self.setWidget(root)
        main = QHBoxLayout(root)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)
        self.sidebar = self._build_sidebar()
        main.addWidget(self.sidebar)
        main.addWidget(self._build_workspace(), 1)
        self.theme_manager.apply(root, "light")

    def _build_sidebar(self):
        side = QFrame()
        side.setObjectName("sidebar")
        side.setFixedWidth(190)
        lay = QVBoxLayout(side)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(10)
        logo = QLabel("MRF\nGNSS PROCESSOR")
        logo.setObjectName("logo")
        lay.addWidget(logo)
        nav_items = [
            ("1", "Projeto"), ("2", "PPP-IBGE"), ("3", "RINEX / Observações"),
            ("4", "Base Fixa"), ("5", "Configuração RTKLIB"), ("6", "Processamento"),
            ("7", "QC Técnico"), ("8", "MTGIR / SIGEF"), ("9", "Relatórios"), ("10", "Exportação"),
        ]
        for number, text in nav_items:
            b = QPushButton(f"{number}   {text}")
            b.setObjectName("navButtonActive" if number in {"2", "6"} else "navButton")
            b.setCursor(Qt.PointingHandCursor)
            lay.addWidget(b)
        lay.addStretch(1)
        for text in ["Fila de Processos", "Configurações", "Sobre o Plugin"]:
            b = QPushButton(text)
            b.setObjectName("sideTool")
            lay.addWidget(b)
        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("Tema"))
        light = QPushButton("Claro")
        dark = QPushButton("Escuro")
        light.clicked.connect(lambda: self.theme_manager.apply(self.widget(), "light"))
        dark.clicked.connect(lambda: self.theme_manager.apply(self.widget(), "dark"))
        theme_row.addWidget(light)
        theme_row.addWidget(dark)
        lay.addLayout(theme_row)
        return side

    def _build_workspace(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        layout.addWidget(self._build_topbar())
        top = QHBoxLayout()
        top.addWidget(self._build_ppp_card(), 1)
        top.addWidget(self._build_lote_card(), 1)
        top.addWidget(self._build_qc_card(), 1)
        layout.addLayout(top)
        mid = QHBoxLayout()
        mid.addWidget(self._build_rinex_card(), 2)
        mid.addWidget(self._build_rtklib_card(), 2)
        layout.addLayout(mid)
        layout.addWidget(self._build_processing_card(), 2)
        bottom = QSplitter(Qt.Horizontal)
        bottom.addWidget(self._build_detail_tabs())
        bottom.addWidget(self._build_map_placeholder())
        bottom.setSizes([650, 500])
        layout.addWidget(bottom, 2)
        layout.addWidget(self._build_console(), 1)
        status = QLabel("✓ Projeto salvo: MRF_PROJETO_001.gnssproj     |     Arquivos: 1 base / 30 rovers     |     Processados: 30/30")
        status.setObjectName("footer")
        layout.addWidget(status)
        return page

    def _build_topbar(self):
        bar = QFrame()
        bar.setObjectName("topbar")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(10, 6, 10, 6)
        lay.addWidget(QLabel("Projeto Atual\nMRF_PROJETO_001"))
        lay.addWidget(QLabel("Sistema de Coordenadas\nSIRGAS 2000 / UTM zone 19S"))
        lay.addWidget(QLabel("Motor\nRTKLIB (RNX2RTKP)"))
        lay.addStretch(1)
        for t in ["Preferências", "Ajuda", "Sobre"]:
            lay.addWidget(QPushButton(t))
        return bar

    def _build_ppp_card(self):
        c = Card("PPP-IBGE (BASE)", "green")
        row = QHBoxLayout()
        ibge = QLabel("IBGE\nPPP")
        ibge.setAlignment(Qt.AlignCenter)
        ibge.setObjectName("ibgeBox")
        row.addWidget(ibge)
        msg = QLabel("✓ VÁLIDO\nBase e rover compatíveis.\nTempo comum encontrado.\nArquivo da base importado.")
        msg.setObjectName("successBox")
        row.addWidget(msg, 1)
        c.layout.addLayout(row)
        grid = QGridLayout()
        data = [("Arquivo", "ReachBaseMR_raw_20250413131812.25O"), ("Estação", "SIPG (943010001)"), ("Data", "13/04/2025"), ("Antena", "JAVRINGANT_DM"), ("Altura antena", "1,485 m")]
        for i, (k, v) in enumerate(data):
            grid.addWidget(QLabel(k), i, 0)
            val = QLabel(v)
            val.setObjectName("value")
            grid.addWidget(val, i, 1)
        c.layout.addLayout(grid)
        return c

    def _build_lote_card(self):
        c = Card("INDICADORES GERAIS (LOTE)", "blue")
        grid = QGridLayout()
        data = [("Total de rovers", "30"), ("Processados", "30"), ("FIX", "24  |  80,0%"), ("FLOAT", "4  |  13,3%"), ("Sem solução", "2  |  6,7%"), ("Tempo comum médio", "00:38:20")]
        for i, (k, v) in enumerate(data):
            grid.addWidget(QLabel(k), i, 0)
            val = QLabel(v)
            val.setObjectName("metric")
            grid.addWidget(val, i, 1)
        c.layout.addLayout(grid)
        return c

    def _build_qc_card(self):
        c = Card("CONFORMIDADE MTGIR", "purple")
        for txt in ["Classe esperada: A (≤ 2 cm)", "Conformidade do lote: ATENÇÃO", "Rovers conformes: 22/30 (73,3%)", "Pior RMS H: 0,038 m", "Pior RMS V: 0,055 m"]:
            c.layout.addWidget(QLabel(txt))
        return c

    def _build_rinex_card(self):
        c = Card("DADOS RINEX (SOMENTE OBSERVAÇÕES)", "blue")
        buttons = QHBoxLayout()
        for text in ["Adicionar Observações", "Adicionar Pasta", "Detectar NAV", "Validar com GFZRNX"]:
            buttons.addWidget(QPushButton(text))
        buttons.addStretch(1)
        c.layout.addLayout(buttons)
        table = QTableWidget(4, 8)
        table.setHorizontalHeaderLabels(["Tipo", "Nome do Arquivo (Obs)", "Início UTC", "Fim UTC", "Duração", "Antena", "NAV Detectado", "Status"])
        rows = [
            ["BASE", "ReachBaseMR_raw_20250413131812.25O", "13:18:32", "18:12:19", "4h53m47s", "1,740", "GPS+GLO+BDS", "OK"],
            ["ROVER", "MLZU-M-1001.25O", "14:11:01", "14:51:03", "40m01s", "2,300", "GPS+GLO", "OK"],
            ["ROVER", "MLZU-M-1002.25O", "14:11:03", "14:51:03", "40m00s", "2,300", "GPS+GLO", "OK"],
            ["ROVER", "MLZU-M-1003.25O", "14:11:10", "14:50:48", "39m38s", "2,300", "GPS+GLO", "OK"],
        ]
        self._fill_table(table, rows)
        c.layout.addWidget(table)
        c.layout.addWidget(QLabel("▾ Arquivos auxiliares detectados: GPS NAV OK | GLONASS NAV OK | BeiDou NAV OK | Erros/Avisos: 0"))
        return c

    def _build_rtklib_card(self):
        c = Card("CONFIGURAÇÃO RTKLIB", "blue")
        tabs = QTabWidget()
        for name in ["Geral", "Frequência / Sinais", "Ambiguidade", "Modelos Atmosféricos", "Precisão / QC", "Saída"]:
            w = QWidget()
            grid = QGridLayout(w)
            fields = ["Modo de posicionamento", "Frequência", "Sistema de coordenadas", "Máscara de elevação", "Intervalo", "Tipo de solução"]
            for i, field in enumerate(fields):
                grid.addWidget(QLabel(field), i, 0)
                combo = QComboBox(); combo.addItems(["Estático - Alta Precisão", "Estático Rápido", "Automático"])
                grid.addWidget(combo, i, 1)
            tabs.addTab(w, name)
        c.layout.addWidget(tabs)
        return c

    def _build_processing_card(self):
        c = Card("PROCESSAMENTO DOS ROVERS (LOTE)", "blue")
        row = QHBoxLayout()
        for text in ["▶ Iniciar Todos", "Pausar", "Cancelar", "Reprocessar Selecionados", "Limpar"]:
            row.addWidget(QPushButton(text))
        row.addStretch(1)
        row.addWidget(QLabel("Filtro:")); row.addWidget(QComboBox())
        row.addWidget(QLineEdit("Buscar rover..."))
        c.layout.addLayout(row)
        table = QTableWidget(8, 14)
        table.setHorizontalHeaderLabels(["#", "Proc.", "Rover", "Progresso", "Solução", "% FIX", "Épocas", "σN", "σE", "σU", "RMS H", "RMS V", "Status", "Ações"])
        rows = []
        for i, name in enumerate(["MLZU-M-1001", "MLZU-M-1002", "MLZU-M-1003", "MLZU-M-1004", "...", "MRF-M-1029", "MRF-M-1030", "MRF-M-1031"], 1):
            rows.append([str(i), "☑", name, "100%", "FIX" if i not in [2,6,7] else ("FLOAT" if i !=7 else "SEM SOL."), "98,7%", "2.401", "0,008", "0,009", "0,015", "0,012", "0,019", "Concluído", "▦  👁"])
        self._fill_table(table, rows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        c.layout.addWidget(table)
        return c

    def _build_detail_tabs(self):
        tabs = QTabWidget()
        detail = QLabel("DETALHE DO ROVER SELECIONADO\n\nRover: MLZU-M-1001\nSolução: FIX\n% FIX: 98,7%\nσN: 0,008 m\nσE: 0,009 m\nσU: 0,015 m\nRMS H: 0,012 m\nRMS V: 0,019 m\nBaseline: 245,67 m")
        timeline = QLabel("LINHA DO TEMPO DA SOLUÇÃO\n\nFIX/FLOAT por época será renderizado com PyQtGraph.")
        sat = QLabel("SATÉLITES / C/N0\n\nGráficos técnicos serão renderizados com PyQtGraph.")
        tabs.addTab(detail, "Detalhe")
        tabs.addTab(timeline, "Timeline FIX/FLOAT")
        tabs.addTab(sat, "Satélites / C/N0")
        return tabs

    def _build_map_placeholder(self):
        c = Card("MAPA / BASELINES", "blue")
        m = QLabel("Canvas QGIS\n\nBASE → múltiplos vetores para ROVERS\nCores: FIX / FLOAT / SEM SOLUÇÃO\nZoom, seleção e destaque do rover selecionado")
        m.setAlignment(Qt.AlignCenter)
        m.setObjectName("mapBox")
        c.layout.addWidget(m, 1)
        return c

    def _build_console(self):
        console = QTextEdit()
        console.setObjectName("console")
        console.setReadOnly(True)
        console.setText("[INFO] Iniciando processamento em lote (30 rovers)...\n[INFO] Configuração carregada: ESTÁTICO - ALTA PRECISÃO\n[INFO] Processando MLZU-M-1001 ... Concluído (FIX 98,7%)\n[WARNING] MRF-M-1029 ... FLOAT 68,5%\n[ERROR] MRF-M-1030 ... Sem solução\n[SUCCESS] Processamento concluído: 30/30 rovers.")
        return console

    def _fill_table(self, table, rows):
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter if c != 1 else Qt.AlignVCenter | Qt.AlignLeft)
                table.setItem(r, c, item)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
