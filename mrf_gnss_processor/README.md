# MRF GNSS Processor

Plugin QGIS para processamento GNSS relativo estático/rápido-estático com fluxo profissional:

PPP-IBGE → Base fixa → RINEX de observação → RTKLIB/RNX2RTKP → QC técnico → MTGIR/SIGEF.

## Estado atual

Versão 0.1.0-dev:

- Estrutura modular do plugin;
- Dock principal no QGIS;
- Interface profissional inicial;
- Tema claro/escuro;
- Tabela RINEX somente com observações;
- Bloco de configuração RTKLIB;
- Tabela de processamento em lote;
- Console técnico;
- Placeholders para mapa/QC/relatórios;
- Esqueleto para parser PPP-IBGE, RINEX, RTKLIB e QC.

## Próxima etapa

Implementar parser real do PPP-IBGE e importação RINEX usando os arquivos de teste fornecidos.
