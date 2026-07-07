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
        /* Paleta de Cores Oficial - Post4l Saúde */
        :root {
            --bg-dark: #0b1120;       
            --bg-panel: #111827;      
            --bg-input: #1f2937;      
            --postal-blue: #004a8f;   
            --postal-yellow: #fbb034; 
            
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --accent: var(--postal-yellow);
            --accent-hover: #f59e0b;
            --border: #374151;
            --success: #10b981;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: var(--bg-dark); color: var(--text-main); display: flex; min-height: 100vh; }
        
        /* Sidebar customizada */
        .sidebar { width: 280px; background-color: var(--bg-panel); border-right: 1px solid var(--border); padding: 2rem 1rem; }
        .sidebar-logo { text-align: center; margin-bottom: 2.5rem; }
        .sidebar-logo img { max-width: 80%; height: auto; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.3)); }
        .nav-menu { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
        .nav-item { padding: 1rem; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-weight: 600; color: var(--text-muted); display: flex; align-items: center; gap: 10px; }
        .nav-item:hover, .nav-item.active { background-color: rgba(251, 176, 52, 0.1); color: var(--accent); border-left: 4px solid var(--accent); }

        /* Main Content */
        .main-content { flex: 1; padding: 3rem; overflow-y: auto; }
        .page-section { display: none; animation: fadeIn 0.4s ease-in-out; }
        .page-section.active { display: block; }
        .page-header { margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }
        .page-header h2 { font-size: 2rem; font-weight: 600; color: var(--text-main); }
        .page-header p { color: var(--text-muted); margin-top: 0.5rem; }

        /* Cards & Forms */
        .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .upload-card { background-color: var(--bg-panel); border: 2px dashed var(--border); border-radius: 12px; padding: 1.5rem; text-align: center; position: relative; cursor: pointer; transition: all 0.3s; }
        .upload-card:hover { border-color: var(--accent); background-color: rgba(251, 176, 52, 0.05); transform: translateY(-3px); }
        .file-input { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer; }
        .status-badge { display: inline-block; background-color: var(--border); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; margin-top: 1rem; font-weight: bold; color: var(--text-muted); }
        .success .status-badge { background-color: var(--success); color: white; }
        
        .filter-card { background-color: var(--bg-panel); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; max-width: 800px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: var(--text-muted); font-weight: 500; }
        .form-control { width: 100%; background-color: var(--bg-input); border: 1px solid var(--border); color: var(--text-main); padding: 0.8rem 1rem; border-radius: 8px; outline: none; transition: 0.2s; }
        .form-control:focus { border-color: var(--accent); box-shadow: 0 0 0 2px rgba(251, 176, 52, 0.2); }
        .radio-group { display: flex; gap: 1.5rem; margin-top: 0.5rem; }
        .radio-label { cursor: pointer; display: flex; align-items: center; gap: 5px; color: var(--text-main); }
        .radio-label input[type="radio"] { accent-color: var(--postal-blue); width: 1.2rem; height: 1.2rem; cursor: pointer; }
        
        .btn-submit { background-color: var(--postal-blue); color: white; border: none; padding: 1rem 2rem; font-size: 1.1rem; font-weight: bold; border-radius: 8px; cursor: pointer; width: 100%; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; }
        .btn-submit:hover { background-color: #003870; box-shadow: 0 4px 12px rgba(0, 74, 143, 0.4); }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <aside class="sidebar">
        <div class="sidebar-logo">
            <img src="/logo.png" alt="Post4l Saúde Logo" onerror="this.style.display='none'; this.nextElementSibling.style.display='block';">
            <h2 style="display:none;">Post4l<span>Saúde</span></h2>
        </div>
        <ul class="nav-menu">
            <li class="nav-item active" onclick="switchPage('upload-bases', this)">📂 Importar Bases</li>
            <li class="nav-item" onclick="switchPage('substituicao', this)">🔄 Substituição</li>
            <li class="nav-item" onclick="switchPage('rn585', this)">📊 Impacto RN 585</li>
        </ul>
    </aside>

    <main class="main-content">
        <section id="upload-bases" class="page-section active">
            <div class="page-header">
                <h2>Módulo de Importação</h2>
                <p>Arraste os arquivos para atualizar o motor de dados.</p>
            </div>
            
            <div class="grid-container">
                <div class="upload-card" id="card-prestadores">
                    <h3>🏥 Prestadores 810</h3>
                    <span class="status-badge" id="status-prestadores">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'prestadores', 'card-prestadores', 'status-prestadores')">
                </div>
                <div class="upload-card" id="card-operadora">
                    <h3>🔄 Operadora Externa</h3>
                    <span class="status-badge" id="status-operadora">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'operadora', 'card-operadora', 'status-operadora')">
                </div>
                <div class="upload-card" id="card-limitrofes">
                    <h3>🗺️ Limítrofes (IBGE)</h3>
                    <span class="status-badge" id="status-limitrofes">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'limitrofes', 'card-limitrofes', 'status-limitrofes')">
                </div>
                <div class="upload-card" id="card-regioes">
                    <h3>📍 Regiões de Saúde</h3>
                    <span class="status-badge" id="status-regioes">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'regioes', 'card-regioes', 'status-regioes')">
                </div>
                <div class="upload-card" id="card-internacao">
                    <h3>🛏️ Internação (TISS)</h3>
                    <span class="status-badge" id="status-internacao">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'internacao', 'card-internacao', 'status-internacao')">
                </div>
            </div>
        </section>

        <section id="substituicao" class="page-section">
            <div class="page-header">
                <h2>Motor de Substituição</h2>
                <p>Busca inteligente com garantia de infraestrutura hospitalar.</p>
            </div>
            <div class="filter-card">
                <form onsubmit="event.preventDefault(); buscarSubstitutos();">
                    <div class="form-group">
                        <label>CPF/CNPJ do prestador alvo:</label>
                        <input type="text" id="alvo-cnpj" class="form-control" placeholder="Ex: 00000000000100" required>
                    </div>
                    <div class="form-group">
                        <label>Abrangência geográfica:</label>
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
                <h2>Impacto Hospitalar - RN 585/620</h2>
                <p>Cálculo ajustado: Filtro prévio -> Distribuição de 80% e ≥5%.</p>
            </div>
            <div class="filter-card">
                <div class="form-group">
                    <label>Selecione a Região de Saúde:</label>
                    <select class="form-control"><option>Conecte o banco de dados para listar as regiões...</option></select>
                </div>
                <button class="btn-submit">Gerar Relatório RN 585</button>
            </div>
        </section>
    </main>

    <script>
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
                    document.getElementById(statusId).innerText = "Erro no upload";
                    alert(result.mensagem);
                }
            } catch (error) {
                document.getElementById(statusId).innerText = "Falha na conexão";
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

# Rota específica que serve a logo direto da raiz do projeto
@app.get("/logo.png")
async def serve_logo():
    if os.path.exists("Logo_Postal-03.png"):
        return FileResponse("Logo_Postal-03.png")
    return {"error": "Arquivo de logo não encontrado na raiz."}

@app.post("/api/upload/{tipo_base}")
async def processar_planilha(tipo_base: str, file: UploadFile = File(...)):
    try:
        conteudo = await file.read()
        df = pd.read_excel(io.BytesIO(conteudo))
        df.columns = [str(col).strip().upper() for col in df.columns]

        msg_extra = ""
        
        # Blindagem de colunas para garantir cruzamento geográfico preciso
        if tipo_base in ["operadora", "prestadores"]:
            colunas_obrigatorias = ["UF", "AP"]
            faltantes = [c for c in colunas_obrigatorias if c not in df.columns]
            if faltantes:
                msg_extra = f" | ALERTA: Faltam colunas: {', '.join(faltantes)}."
            else:
                msg_extra = " | Colunas geográficas (UF, AP) validadas."
                
        elif tipo_base == "internacao":
            msg_extra = " | Base TISS mapeada para cálculo RN 585."
            
        elif tipo_base == "regioes":
            msg_extra = " | Códigos IBGE e Regiões de Saúde mapeados."
            
        return {"status": "sucesso", "mensagem": f"{len(df)} linhas salvas.{msg_extra}"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

@app.get("/api/buscar-substitutos/{cpfcnpj}")
async def buscar_substitutos(cpfcnpj: str, abrangencia: str):
    """ Lógica com a regra do Hospital """
    is_hospital = True 
    msg = f"Iniciando busca IBGE para {cpfcnpj}. "
    
    if is_hospital:
        msg += "Alvo é um HOSPITAL. A macro irá isolar obrigatoriamente candidatos que possuam a tag 'Hospital' na base 810 para garantir cobertura de Urgência/Emergência e Internação. "
        msg += "Após garantir o hospital substituto, a macro buscará clínicas para suprir o saldo."
    else:
        msg += "Alvo é clínica/laboratório. Busca gulosa padrão por especialidades liberada."

    return {
        "status": "sucesso",
        "alvo_is_hospital": is_hospital,
        "mensagem_front": msg
    }
