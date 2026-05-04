import os
import requests
import argparse
import json


def download_dir_from_github(owner, repo, path, target_dir):
    """
    Baixa recursivamente uma pasta do GitHub via API (sem necessidade de git clone).
    Não requer autenticação para repositórios públicos.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})

    if response.status_code == 404:
        return False  # Caminho não encontrado
    if response.status_code != 200:
        print(f"Erro ao acessar GitHub API ({response.status_code}): {api_url}")
        return False

    items = response.json()
    if not isinstance(items, list):
        print(f"Resposta inesperada da GitHub API.")
        return False

    os.makedirs(target_dir, exist_ok=True)

    for item in items:
        item_name = item["name"]
        item_type = item["type"]
        item_path = item["path"]
        local_path = os.path.join(target_dir, item_name)

        if item_type == "dir":
            download_dir_from_github(owner, repo, item_path, local_path)
        elif item_type == "file":
            download_url = item.get("download_url")
            if download_url:
                file_response = requests.get(download_url)
                if file_response.status_code == 200:
                    with open(local_path, 'wb') as f:
                        f.write(file_response.content)
                    print(f"  [OK] {item_path}")
                else:
                    print(f"  [ERRO] Não foi possível baixar: {item_path}")

    return True


def find_skill_path_in_repo(owner, repo, skill_name):
    """
    Tenta localizar a pasta da skill no repositório GitHub buscando
    em subpastas comuns como 'skills/', a raiz '/' e 'agents/'.
    Também tenta variações do nome removendo prefixos (ex: 'vercel-').
    """
    # Gerar variações de nome: original + sem prefixos conhecidos
    name_variations = [skill_name]
    # Remover prefixo do owner (ex: vercel-react-best-practices -> react-best-practices)
    if skill_name.startswith(owner + "-"):
        name_variations.append(skill_name[len(owner) + 1:])
    # Remover primeiro segmento separado por hífen (ex: vercel-react-... -> react-...)
    parts = skill_name.split('-', 1)
    if len(parts) == 2 and parts[1] not in name_variations:
        name_variations.append(parts[1])

    base_dirs = ["skills", "", "agents", "packages"]

    for name in name_variations:
        for base in base_dirs:
            path = f"{base}/{name}".strip("/")
            api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
            response = requests.get(api_url, headers={"Accept": "application/vnd.github.v3+json"})
            if response.status_code == 200:
                items = response.json()
                # Verifica se tem SKILL.md
                if isinstance(items, list) and any(i["name"] == "SKILL.md" for i in items):
                    print(f"  -> Encontrada como '{path}' (alias: '{skill_name}')")
                    return path

    return None


def download_skill(skill_id, base_path):
    print(f"Iniciando download da skill: {skill_id}")

    # --- Parse do ID: owner/repo/skill-name ---
    parts = skill_id.split('/')
    if len(parts) < 3:
        print("Formato de ID inválido. Esperado: owner/repo/skill-name")
        print("Exemplo: vercel-labs/agent-skills/vercel-react-best-practices")
        return

    owner = parts[0]
    repo = parts[1]
    skill_name = parts[-1]  # nome do skillId (último segmento)

    print(f"Buscando skill '{skill_name}' em github.com/{owner}/{repo}...")

    # Tentar localizar o path real da skill no repositório
    skill_path = find_skill_path_in_repo(owner, repo, skill_name)

    if not skill_path:
        print(f"Aviso: Skill '{skill_name}' não encontrada diretamente. Buscando pelo SKILL.md no repositório...")
        # Listar a raiz do repositório para orientar o usuário
        root_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        root_resp = requests.get(root_url, headers={"Accept": "application/vnd.github.v3+json"})
        if root_resp.status_code == 200:
            dirs = [i["name"] for i in root_resp.json() if i["type"] == "dir"]
            print(f"Subpastas disponíveis na raiz: {dirs}")
        print("Não foi possível localizar a skill automaticamente. Verifique o ID e tente novamente.")
        return

    print(f"Skill encontrada em: {skill_path}")

    # Destino: pasta local com o nome da skill
    target_folder = os.path.join(base_path, skill_name)
    if os.path.exists(target_folder):
        import shutil
        print(f"Substituindo instalação anterior em: {target_folder}")
        shutil.rmtree(target_folder)

    print(f"Baixando arquivos para: {target_folder}")
    success = download_dir_from_github(owner, repo, skill_path, target_folder)

    if success:
        print(f"\n[OK] Skill '{skill_name}' instalada com sucesso!")
        print(f"Local: {target_folder}")
    else:
        print(f"\n[ERRO] Falha ao baixar a skill '{skill_name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloader de skills do skills.sh via GitHub API")
    parser.add_argument("--id", required=True,
                        help="ID completo da skill (ex: vercel-labs/agent-skills/vercel-react-best-practices)")
    parser.add_argument("--path", required=True,
                        help="Pasta base de destino (ex: C:\\Users\\natha\\Documents\\Projetos\\SKILLS)")

    args = parser.parse_args()
    download_skill(args.id, args.path)
