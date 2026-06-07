# Manual de Uso - Google Maps Scraper

Este aplicativo é um script em Python que realiza a extração (scraping) de informações de estabelecimentos comerciais diretamente do Google Maps utilizando a biblioteca Playwright.

## Como Executar

O comando principal para iniciar o script é:

```powershell
python main.py [argumentos]
```

## Argumentos Disponíveis

| Argumento Curto | Argumento Longo | Tipo | Descrição |
| :--- | :--- | :--- | :--- |
| `-s` | `--search` | `string` | Termo de busca único a ser pesquisado no Google Maps (ex: `"restaurantes em São Paulo"`). |
| `-f` | `--file` | `string` | Caminho de um arquivo de texto (.txt) contendo várias queries de pesquisa (uma por linha) para processamento em lote. |
| `-t` | `--total` | `int` | Número máximo de estabelecimentos a extrair por pesquisa (padrão: `50`). |
| `-o` | `--output` | `string` | Nome ou caminho do arquivo CSV gerado (padrão: `result.csv`). |
| | `--append` | `flag` | Adiciona os novos resultados ao final do arquivo CSV existente em vez de substituí-lo. |
| | `--oculto` | `flag` | Executa o navegador em segundo plano (*headless*), ou seja, sem exibir a interface gráfica do navegador. |

---

## Exemplos Práticos

### 1. Busca Rápida (com navegador visível)
Para buscar 10 padarias em Pinheiros mostrando o navegador:
```powershell
python main.py -s "padarias em Pinheiros" -t 10
```

### 2. Busca Oculta com Arquivo de Saída Customizado
Para buscar 30 dentistas em Curitiba sem exibir a tela do navegador e salvar em `dentistas.csv`:
```powershell
python main.py -s "dentistas em Curitiba" -t 30 -o dentistas.csv --oculto
```

### 3. Processamento em Lote (Lendo de um arquivo txt)
Se você tiver um arquivo chamado `termos.txt` contendo termos como:
```text
mecanicas em Osasco
auto peças em Barueri
borracharias em Carapicuiba
```
Você pode processar todos de forma oculta acumulando as informações no mesmo arquivo:
```powershell
python main.py -f termos.txt -t 20 -o oficinas.csv --append --oculto
```
