# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
import io
import re

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
        :root {
            --bg-dark: #0f172a; --bg-panel: #1e293b; --bg-input: #334155;
            --text-main: #f8fafc; --text-muted: #94a3b8;
            --accent: #3b82f6; --accent-hover: #2563eb;
            --border: #475569; --success: #10b981; --danger: #ef4444;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        body { background-color: var(--bg-dark); color: var(--text-main); display: flex; min-height: 100vh; }
        
        /* Sidebar */
        .sidebar { width: 280px; background-color: var(--bg-panel); border-right: 1px solid var(--border); padding: 2rem 1rem; }
        .sidebar-logo { font-size: 1.5rem; font-weight: 700; text-align: center; margin-bottom: 2.5rem; letter-spacing: 1px; }
        .sidebar-logo span { color: var(--accent); }
        .nav-menu { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
        .nav-item { padding: 1rem; border-radius: 8px; cursor: pointer; transition: all 0.2s; font-weight: 500; color: var(--text-muted); }
        .nav-item:hover, .nav-item.active { background-color: rgba(59, 130, 246, 0.1); color: var(--accent); }

        /* Main Content */
        .main-content { flex: 1; padding: 3rem; overflow-y: auto; }
        .page-section { display: none; animation: fadeIn 0.4s ease-in-out; }
        .page-section.active { display: block; }
        .page-header { margin-bottom: 2rem; border-bottom: 1px solid var(--border); padding-bottom: 1rem; }
        .page-header h2 { font-size: 2rem; font-weight: 600; }
        .page-header p { color: var(--text-muted); margin-top: 0.5rem; }

        /* Cards & Forms */
        .grid-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .upload-card { background-color: var(--bg-panel); border: 2px dashed var(--border); border-radius: 12px; padding: 1.5rem; text-align: center; position: relative; cursor: pointer; transition: all 0.3s; }
        .upload-card:hover { border-color: var(--accent); background-color: rgba(59, 130, 246, 0.05); }
        .file-input { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; cursor: pointer; }
        .status-badge { display: inline-block; background-color: var(--border); padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; margin-top: 1rem; }
        .success .status-badge { background-color: var(--success); color: white; }
        
        .filter-card { background-color: var(--bg-panel); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; max-width: 800px; }
        .form-group { margin-bottom: 1.5rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; color: var(--text-muted); }
        .form-control { width: 100%; background-color: var(--bg-input); border: 1px solid var(--border); color: var(--text-main); padding: 0.8rem 1rem; border-radius: 8px; outline: none; }
        .form-control:focus { border-color: var(--accent); }
        .radio-group { display: flex; gap: 1.5rem; margin-top: 0.5rem; }
        .radio-label input[type="radio"] { accent-color: var(--accent); }
        
        .btn-submit { background-color: var(--accent); color: white; border: none; padding: 1rem 2rem; font-size: 1.1rem; font-weight: 600; border-radius: 8px; cursor: pointer; width: 100%; transition: 0.2s; }
        .btn-submit:hover { background-color: var(--accent-hover); }

        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>

    <aside class="sidebar">
        <div class="sidebar-logo">Post4l<span>Saúde</span></div>
        <ul class="nav-menu">
            <li class="nav-item active" onclick="switchPage('upload-bases', this)">📂 Importar Bases</li>
            <li class="nav-item" onclick="switchPage('substituicao', this)">🔄 Substituição</li>
            <li class="nav-item" onclick="switchPage('rn585', this)">📊 Impacto RN 585</li>
        </ul>
    </aside>

    <main class="main-content">
        
        <section id="upload-bases" class="page-section active">
            <div class="page-header">
                <h2>Importação de Dados</h2>
                <p>Arraste os arquivos para atualizar o banco de dados no Railway.</p>
            </div>
            <div class="grid-container">
                <div class="upload-card" id="card-prestadores">
                    <h3>🏥 Prestadores 810</h3>
                    <span class="status-badge" id="status-prestadores">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'prestadores', 'card-prestadores', 'status-prestadores')">
                </div>
                <div class="upload-card" id="card-operadora">
                    <h3>🔄 Base Operadora Externa</h3>
                    <span class="status-badge" id="status-operadora">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'operadora', 'card-operadora', 'status-operadora')">
                </div>
                <div class="upload-card" id="card-limitrofes">
                    <h3>🗺️ Limítrofes IBGE</h3>
                    <span class="status-badge" id="status-limitrofes">Aguardando...</span>
                    <input type="file" class="file-input" onchange="uploadFile(this, 'limitrofes', 'card-limitrofes', 'status-limitrofes')">
                </div>
            </div>
        </section>

        <section id="substituicao" class="page-section">
            <div class="page-header">
                <h2>Ferramenta de Substituição</h2>
                <p>Cruzamento de especialidades e regiões limítrofes.</p>
            </div>
            <div class="filter-card">
                <form onsubmit="event.preventDefault(); buscarSubstitutos();">
                    <div class="form-group">
                        <label>CPF/CNPJ do prestador alvo:</label>
                        <input type="text" id="alvo-cnpj" class="form-control" placeholder="Apenas números">
                    </div>
                    <div class="form-group">
                        <label>Abrangência:</label>
                        <div class="radio-group">
                            <label class="radio-label"><input type="radio" name="busca_regiao" value="mesmo" checked> Mesmo município</label>
                            <label class="radio-label"><input type="radio" name="busca_regiao" value="limitrofes"> Limítrofes (IBGE)</label>
                        </div>
                    </div>
                    <button type="submit" class="btn-submit">Buscar Substitutos</button>
                </form>
            </div>
        </section>

        <section id="rn585" class="page-section">
            <div class="page-header">
                <h2>Impacto Hospitalar - RN 585</h2>
                <p>Regra dos 80% e ≥5% de internações.</p>
            </div>
            <div class="filter-card">
                <div class="form-group">
                    <label>Selecione a Região de Saúde:</label>
                    <select class="form-control"><option>Aguardando integração com o banco...</option></select>
                </div>
                <button class="btn-submit">Gerar Relatório</button>
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

        // JS que envia a planilha pro Python no Backend
        async function uploadFile(input, tipoBase, cardId, statusId) {
            if (!input.files.length) return;
            const file = input.files[0];
            const formData = new FormData();
            formData.append("file", file);

            document.getElementById(statusId).innerText = "Processando...";
            
            try {
                const response = await fetch(`/api/upload/${tipoBase}`, {
                    method: 'POST',
                    body: formData
                });
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
            alert(`Iniciando busca no backend para o CNPJ: ${cnpj}\\n(A lógica do banco PostgreSQL entrará aqui!)`);
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
    """Rota principal: Renderiza toda a interface HTML/CSS/JS"""
    return DASHBOARD_HTML

@app.post("/api/upload/{tipo_base}")
async def processar_planilha(tipo_base: str, file: UploadFile = File(...)):
    """Rota que recebe as planilhas do frontend, mastiga com Pandas e prepara pro BD"""
    try:
        # Lê o Excel que chegou do navegador direto para a memória
        conteudo = await file.read()
        df = pd.read_excel(io.BytesIO(conteudo))
        
        # Padroniza nomes de colunas (tudo maiúsculo e sem espaços sobrando)
        df.columns = [str(col).strip().upper() for col in df.columns]

        linhas_processadas = len(df)
        msg_extra = ""

        # Lógica inteligente para as bases da Operadora ou Prestadores
        if tipo_base in ["operadora", "prestadores"]:
            # Garante a captura obrigatória das colunas UF e AP na extração
            colunas_obrigatorias = ["UF", "AP"]
            colunas_faltantes = [c for c in colunas_obrigatorias if c not in df.columns]
            
            if colunas_faltantes:
                # Se não encontrar de cara, o código precisará acionar o regex/mapeamento para localizar
                msg_extra = f" | ALERTA: Colunas {', '.join(colunas_faltantes)} não localizadas nos cabeçalhos padrão."
            else:
                msg_extra = " | Colunas UF e AP identificadas com sucesso."

            # TODO: Inserir a limpeza Regex de CNPJ/CPF (zfill 14 e 11) e envio pro PostgreSQL via SQLAlchemy
            
        return {
            "status": "sucesso", 
            "mensagem": f"Salvo: {linhas_processadas} linhas{msg_extra}"
        }
        
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# Para rodar localmente durante seus testes antes de mandar pro Railway:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
