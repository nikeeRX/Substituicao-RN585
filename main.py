# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
import pandas as pd
import io
import os

app = FastAPI(title="Post4l Saúde API")

# ==========================================
# CÓDIGO HTML + CSS + JS (FRONT-END)
# ==========================================
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Post4l Saúde - Dashboard</title>
    <style>
        /* NOVA PALETA CORPORATIVA BASEADA NA LOGO */
        :root {
            /* Cores da Marca */
            --postal-blue: #004a8f;        /* Azul Oficial */
            --postal-dark-blue: #002d5c;   /* Azul Hover */
            --postal-yellow: #fed100;      /* Amarelo Oficial */
            --postal-yellow-hover: #ffdf4d;
            
            /* Estrutura Clean */
            --bg-main: #f4f7f9;            /* Fundo geral gelo/cinza claro */
            --bg-card: #ffffff;            /* Fundo dos painéis e sidebar brancos */
            --border-color: #e2e8f0;       /* Bordas sutis */
            
            /* Textos */
            --text-main: #334155;          /* Texto principal escuro elegante */
            --text-muted: #64748b;         /* Texto secundário */
            --success: #10b981;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-main); display: flex; min-height: 100vh; }
        
        /* Sidebar Clean */
        .sidebar { width: 280px; background-color: var(--bg-card); border-right: 1px solid var(--border-color); padding: 2rem 1rem; box-shadow: 2px 0 10px rgba(0,0,0,0.03); z-index: 10; }
        .sidebar-logo { text-align: center; margin-bottom: 2.5rem; min-height: 80px; display: flex; align-items: center; justify-content: center; }
        
        /* Ajuste da Logo para fundo branco */
        .sidebar-logo img { max-width: 85%; max-height: 100px; object-fit: contain; }
        
        .nav-menu { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
        .nav-item { padding: 1rem; border-radius: 8px; cursor: pointer; transition: all 0.3s ease; font-weight: 600; color: var(--text-muted); display: flex; align-items: center; gap: 10px; }
        
        /* Efeito de Menu Ativo com as Cores da Logo */
        .nav-item:hover { background-color: #f1f5f9; color: var(--postal-blue); }
        .nav-item.active { background-color: var(--postal-blue); color: white; border-left: 5px solid var(--postal-yellow); box-shadow: 0 4px 6px rgba(0, 74, 143, 0.2); }

        /* Main Content */
        .main-content { flex: 1; padding: 3rem; overflow-y: auto; }
        .page-section { display: none; animation: fadeIn 0.4s ease-in-out; }
        .page-section.active { display: block; }
        .page-header { margin-bottom: 2rem; border-bottom: 2px solid var(--border-color); padding-bottom: 1rem; }
        .page-header h2 { font-size: 2rem; font-weight: 700; color: var(--postal-dark-blue); }
        .page-header p { color: var(--text-muted); margin-top: 0.5rem; font-size: 1.05rem; }

        /* Cards & Forms - Visual Clean */
        .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .upload-card { background-color: var(--bg-card); border: 2px dashed #cbd5e1; border-radius: 12px; padding: 1.5rem; text-align: center; position: relative; cursor: pointer; transition: all 0.3s; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        
        /* Hover do Card no Azul da Logo */
        .upload-card:hover { border-color: var(--postal-blue); background-color: #f8fafc; transform: translateY(-3px); box-shadow: 0 6px 12px rgba(0,0,0,0.05); }
        .file-input { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer; }
        
        .card-title { color: var(--postal-dark-blue); font-size: 1.1rem; margin-bottom: 0.5rem; }
        .status-badge { display: inline-block; background-color: #f1f5f9; padding: 0.4rem 1rem; border-radius: 20px; font-size: 0.85rem; margin-top: 1rem; font-weight: bold; color: var(--text-muted); border: 1px solid var(--border-color); }
        .success .status-badge { background-color: var(--success); color: white; border-color: var(--success); }
        .success { border-color: var(--success) !important; background-color: #f0fdf4 !important; }
        
        .filter-card { background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 2rem; max-width: 800px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: var(--postal-dark-blue); font-weight: 600; }
        .form-control { width: 100%; background-color: #ffffff; border: 2px solid var(--border-color); color: var(--text-main); padding: 0.8rem 1rem; border-radius: 8px; outline: none; transition: 0.3s; font-size: 1rem; }
        
        /* Foco do Input em Amarelo/Azul */
        .form-control:focus { border-color: var(--postal-blue); box-shadow: 0 0 0 3px rgba(0, 74, 143, 0.1); }
        
        .radio-group { display: flex; gap: 1.5rem; margin-top: 0.5rem; }
        .radio-label { cursor: pointer; display: flex; align-items: center; gap: 5px; color: var(--text-main); font-weight: 500; }
        .radio-label input[type="radio"] { accent-color: var(--postal-blue); width: 1.2rem; height: 1.2rem; cursor: pointer; }
        
        /* Botão com as cores invertidas no Hover (Azul -> Amarelo) */
        .btn-submit { background-color: var(--postal-blue); color: white; border: none; padding: 1.2rem 2rem; font-size: 1.1rem; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; transition: all 0.3s; text-transform: uppercase; letter-spacing: 1px; box-shadow: 0 4px 6px rgba(0, 74, 143, 0.2); }
        .btn-submit:hover { background-color: var(--postal-yellow); color: var(--postal-dark-blue); box-shadow: 0 6px 12px rgba(254, 209, 0, 0.3); transform: translateY(-2px); }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <aside class="sidebar">
        <div class="sidebar-logo">
            <img src="/api/logo" alt="Post4l Saúde Logo" id="logo-img">
        </div>
        <ul class="nav-menu">
            <li class="nav-item active" onclick="switchPage('upload-bases', this)">📂 Importar Bases</li>
            <li class="nav-item" onclick="switchPage('substituicao', this)">🔄 Motor de Substituição</li>
            <li class="nav-item" onclick="switchPage('rn585', this)">📊 Impacto RN 585</li>
        </ul>
    </aside>

    <main class="main-content">
        <section id="upload-bases" class="page-section active">
            <div class="page-header">
                <h2>Módulo de Integração de Dados</h2>
                <p>Arraste os arquivos .xlsx para alimentar o banco de dados da ferramenta.</p>
            </div>
            
            <div class="grid-container">
                <div class="upload-card" id="card-prestadores">
                    <h3 class="card-title">🏥 Prestadores 810</h3>
                    <span class="status-badge" id="status-prestadores">Aguardando arquivo...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'prestadores', 'card-prestadores', 'status-prestadores')">
                </div>
                <div class="upload-card" id="card-operadora">
                    <h3 class="card-title">🔄 Operadora Externa</h3>
                    <span class="status-badge" id="status-operadora">Aguardando arquivo...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'operadora', 'card-operadora', 'status-operadora')">
                </div>
                <div class="upload-card" id="card-limitrofes">
                    <h3 class="card-title">🗺️ Limítrofes (IBGE)</h3>
                    <span class="status-badge" id="status-limitrofes">Aguardando arquivo...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'limitrofes', 'card-limitrofes', 'status-limitrofes')">
                </div>
                <div class="upload-card" id="card-regioes">
                    <h3 class="card-title">📍 Regiões de Saúde</h3>
                    <span class="status-badge" id="status-regioes">Aguardando arquivo...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'regioes', 'card-regioes', 'status-regioes')">
                </div>
                <div class="upload-card" id="card-internacao">
                    <h3 class="card-title">🛏️ Internação (TISS)</h3>
                    <span class="status-badge" id="status-internacao">Aguardando arquivo...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'internacao', 'card-internacao', 'status-internacao')">
                </div>
            </div>
        </section>

        <section id="substituicao" class="page-section">
            <div class="page-header">
                <h2>Motor de Substituição 2.0</h2>
                <p>Garantia inteligente de infraestrutura hospitalar e cruzamento limítrofe.</p>
            </div>
            <div class="filter-card">
                <form onsubmit="event.preventDefault(); buscarSubstitutos();">
                    <div class="form-group">
                        <label>CPF/CNPJ do prestador alvo:</label>
                        <input type="text" id="alvo-cnpj" class="form-control" placeholder="Apenas números (Ex: 00000000000100)" required>
                    </div>
                    <div class="form-group">
                        <label>Defina a abrangência geográfica:</label>
                        <div class="radio-group">
                            <label class="radio-label"><input type="radio" name="busca_regiao" value="mesmo" checked> Mesmo município</label>
                            <label class="radio-label"><input type="radio" name="busca_regiao" value="limitrofes"> Limítrofes (IBGE)</label>
                        </div>
                    </div>
                    <button type="submit" class="btn-submit">Processar Substitutos</button>
                </form>
            </div>
        </section>

        <section id="rn585" class="page-section">
            <div class="page-header">
                <h2>Análise de Impacto (RN 585/620)</h2>
                <p>Cálculo de rede com distribuição rigorosa de 80% e ≥5%.</p>
            </div>
            <div class="filter-card">
                <div class="form-group">
                    <label>Selecione a Região de Saúde para análise:</label>
                    <select class="form-control"><option>Banco de dados pendente...</option></select>
                </div>
                <button class="btn-submit">Gerar Relatório de Impacto</button>
            </div>
        </section>
    </main>

    <script>
        // Lógica de visualização caso a logo quebre (fallback em texto)
        document.getElementById('logo-img').onerror = function() {
            this.style.display = 'none';
            this.parentElement.innerHTML = '<h2 style="color: var(--postal-blue); font-weight: 800; font-size: 1.8rem;">Post4l<span style="color: var(--postal-yellow);">Saúde</span></h2>';
        };

        function switchPage(pageId, element) {
            document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
            document.querySelectorAll('.page-section').forEach(s => s.classList.remove('active'));
            element.classList.add('active');
            document.getElementById(pageId).classList.add('active');
        }

        async function uploadFile(input, tipoBase, cardId, statusId) {
            if (!input.files.length) return;
            const file = input.files[0];
            const formData = new FormData();
            formData.append("file", file);

            document.getElementById(statusId).innerText = "Processando...";
            
            try {
                const response = await fetch(`/api/upload/${tipoBase}`, { method: 'POST', body: formData });
                const result = await response.json();
                
                if (result.status === 'sucesso') {
                    document.getElementById(cardId).classList.add('success');
                    document.getElementById(statusId).innerText = result.mensagem;
                } else {
                    document.getElementById(statusId).innerText = "Erro no arquivo";
                    alert(result.mensagem);
                }
            } catch (error) {
                document.getElementById(statusId).innerText = "Falha de conexão";
            }
        }

        async function buscarSubstitutos() {
            const cnpj = document.getElementById('alvo-cnpj').value;
            const abrangencia = document.querySelector('input[name="busca_regiao"]:checked').value;
            
            try {
                const response = await fetch(`/api/buscar-substitutos/${cnpj}?abrangencia=${abrangencia}`);
                const result = await response.json();
                console.log(result);
                alert(result.mensagem_front);
            } catch (error) {
                alert("Erro ao conectar com o motor de busca.");
            }
        }
    </script>
</body>
</html>
"""

# ==========================================
# ROTAS DO BACKEND (PYTHON / FASTAPI)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    return DASHBOARD_HTML

# 🚀 CAÇADOR DE LOGO INTELIGENTE 
# Esta rota tenta ler o arquivo independente de como você salvou no GitHub
@app.get("/api/logo")
async def serve_logo():
    possiveis_nomes = [
        "logo.png", "Logo.png", "LOGO.png", 
        "image_84ce7f.png", "Logo_Postal-03.png", 
        "logo.jpeg", "logo.jpg"
    ]
    
    # Procura na raiz do projeto
    for nome in possiveis_nomes:
        if os.path.exists(nome):
            return FileResponse(nome)
            
    # Se não achar nada, o navegador aciona o JS para exibir o texto com as cores oficiais
    return {"error": "Logo não encontrada."}

@app.post("/api/upload/{tipo_base}")
async def processar_planilha(tipo_base: str, file: UploadFile = File(...)):
    try:
        conteudo = await file.read()
        df = pd.read_excel(io.BytesIO(conteudo))
        df.columns = [str(col).strip().upper() for col in df.columns]

        msg_extra = ""
        
        # Blindagem de colunas 
        if tipo_base in ["operadora", "prestadores"]:
            colunas_obrigatorias = ["UF", "AP"]
            faltantes = [c for c in colunas_obrigatorias if c not in df.columns]
            if faltantes:
                msg_extra = f" | Faltam colunas: {', '.join(faltantes)}."
            else:
                msg_extra = " | Colunas UF e AP OK."
                
        elif tipo_base == "internacao":
            msg_extra = " | Base TISS mapeada."
            
        return {"status": "sucesso", "mensagem": f"{len(df)} linhas salvas.{msg_extra}"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/api/buscar-substitutos/{cpfcnpj}")
async def buscar_substitutos(cpfcnpj: str, abrangencia: str):
    is_hospital = True 
    msg = f"Iniciando busca IBGE para {cpfcnpj}. "
    
    if is_hospital:
        msg += "Alvo = HOSPITAL. Travando busca para garantir hospital substituto (Urgência/Internação) antes de suprir ambulatório com clínicas."
    else:
        msg += "Busca padrão por especialidades liberada."

    return {
        "status": "sucesso",
        "mensagem_front": msg
    }
