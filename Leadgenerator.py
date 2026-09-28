import time
import pandas as pd
from playwright.sync_api import sync_playwright
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

console = Console()


def exibir_banner():
    banner = """
[bold cyan]╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🔍  PROCURADOR DE LEADS - CRIAÇÃO DE SITES  🔍    ║
║                                                      ║
║   Encontre empresas que precisam de um site!         ║
║                                                      ║
╚══════════════════════════════════════════════════════╝[/bold cyan]
    """
    console.print(banner)


def exibir_menu():
    console.print()
    console.print(Panel.fit(
        "[bold yellow]MENU PRINCIPAL[/bold yellow]\n\n"
        "[1] 🔎 Buscar leads\n"
        "[2] 📋 Ver leads salvos\n"
        "[3] 🌐 Filtrar leads SEM site\n"
        "[4] 🗑️  Limpar arquivo de leads\n"
        "[5] ❌ Sair",
        border_style="cyan",
        box=box.ROUNDED
    ))


def extrair_dados_card(item, termo_busca):
    """Extrai nome, site, telefone e link do Google Maps de um card."""
    lead = {
        "Empresa": "",
        "Termo Busca": termo_busca,
        "Site": "",
        "Tem Site": "Não",
        "Telefone": "",
        "Link Maps": "",
    }

    try:
        # Nome da empresa
        nome_el = item.locator('div.qBF1Pd').first
        if nome_el.count() > 0:
            lead["Empresa"] = nome_el.inner_text().strip()

        # Link do Google Maps (href do próprio card)
        try:
            link_el = item.locator('a.hfpxzc').first
            if link_el.count() > 0:
                lead["Link Maps"] = link_el.get_attribute("href") or ""
        except Exception:
            pass

        # Site oficial (botão "Website" dentro do card)
        try:
            site_el = item.locator('a[data-value="Website"]').first
            if site_el.count() > 0:
                site = site_el.get_attribute("href") or ""
                if site:
                    lead["Site"] = site
                    lead["Tem Site"] = "Sim"
        except Exception:
            pass

        # Telefone (o Google Maps exibe em um span com classe específica)
        try:
            telefone_el = item.locator('span.UsdlK').first
            if telefone_el.count() > 0:
                lead["Telefone"] = telefone_el.inner_text().strip()
        except Exception:
            pass

    except Exception:
        pass

    return lead


def buscar_leads():
    console.print()
    console.print("[bold cyan]═══ CONFIGURAÇÃO DA BUSCA ═══[/bold cyan]\n")

    termo_busca = Prompt.ask("[bold yellow]Digite o termo de busca[/bold yellow] (ex: academias em Nova Iguacu)")
    if not termo_busca.strip():
        console.print("[bold red]❌ Termo de busca não pode ser vazio![/bold red]")
        return

    quantidade_scrolls = IntPrompt.ask(
        "[bold yellow]Quantas vezes rolar a página?[/bold yellow] (mais rolagens = mais leads)",
        default=5
    )

    leads = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("[cyan]Iniciando navegador...", total=None)

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=False)
            except Exception as e:
                console.print(f"[bold red]❌ Erro ao abrir navegador: {e}[/bold red]")
                console.print("[yellow]💡 Rode: python -m playwright install chromium[/yellow]")
                return

            page = browser.new_page()
            url = f"https://www.google.com/maps/search/{termo_busca.replace(' ', '+')}"

            progress.update(task, description=f"[cyan]Buscando: {termo_busca}...")
            page.goto(url)
            page.wait_for_timeout(3000)

            progress.update(task, description="[cyan]Rolando página para carregar leads...")
            try:
                sidebar = page.locator('div[role="feed"]')
                for _ in range(quantidade_scrolls):
                    sidebar.evaluate("element => element.scrollBy(0, 2000)")
                    time.sleep(2)
            except Exception:
                pass

            progress.update(task, description="[cyan]Coletando informações dos cards...")

            listings = page.locator('div.Nv2PK').all()
            total = len(listings)

            for idx, item in enumerate(listings, 1):
                progress.update(
                    task,
                    description=f"[cyan]Extraindo lead {idx}/{total}..."
                )
                lead = extrair_dados_card(item, termo_busca)
                if lead["Empresa"]:
                    leads.append(lead)

            browser.close()

    if not leads:
        console.print("[bold red]❌ Nenhum lead encontrado. Tente outro termo ou aumente as rolagens.[/bold red]")
        return

    exibir_tabela_leads(leads, titulo=f"🎯 {len(leads)} Leads Encontrados")

    # Salvar em CSV
    df = pd.DataFrame(leads)
    try:
        df_existente = pd.read_csv("leads_encontrados.csv", encoding="utf-8-sig")
        df_final = pd.concat([df_existente, df], ignore_index=True)
        df_final = df_final.drop_duplicates(subset=["Empresa", "Termo Busca"])
    except FileNotFoundError:
        df_final = df

    df_final.to_csv("leads_encontrados.csv", index=False, encoding="utf-8-sig")

    sem_site = sum(1 for l in leads if l["Tem Site"] == "Não")
    com_site = len(leads) - sem_site

    console.print(f"\n[bold green]✅ {len(leads)} leads processados! Total no arquivo: {len(df_final)}[/bold green]")
    console.print(f"[bold cyan]📊 Com site: {com_site} | [/bold cyan][bold yellow]🚀 Sem site (oportunidades): {sem_site}[/bold yellow]")
    console.print("[bold green]📁 Arquivo: leads_encontrados.csv[/bold green]")


def exibir_tabela_leads(leads, titulo="📋 Leads"):
    tabela = Table(title=titulo, box=box.ROUNDED, border_style="green", show_lines=False)
    tabela.add_column("#", style="dim", width=4)
    tabela.add_column("Empresa", style="bold cyan", max_width=28, overflow="ellipsis")
    tabela.add_column("Site?", justify="center", width=6)
    tabela.add_column("Site / Contato", style="blue", max_width=38, overflow="ellipsis")
    tabela.add_column("Telefone", style="magenta", width=18)
    tabela.add_column("Maps", style="green", width=8, justify="center")

    for i, lead in enumerate(leads, 1):
        tem_site = lead.get("Tem Site", "Não")

        if tem_site == "Sim":
            badge = "[bold green]✅[/bold green]"
            site_display = lead.get("Site", "")
        else:
            badge = "[bold red]❌[/bold red]"
            site_display = "[dim]— sem site —[/dim]"

        telefone = lead.get("Telefone", "") or "[dim]—[/dim]"

        link_maps = lead.get("Link Maps", "")
        if link_maps:
            maps_display = f"[link={link_maps}]🔗[/link]"
        else:
            maps_display = "[dim]—[/dim]"

        tabela.add_row(
            str(i),
            lead["Empresa"],
            badge,
            site_display,
            telefone,
            maps_display,
        )

    console.print(tabela)


def ver_leads():
    try:
        df = pd.read_csv("leads_encontrados.csv", encoding="utf-8-sig")
    except FileNotFoundError:
        console.print("[bold yellow]⚠️  Nenhum arquivo de leads encontrado ainda.[/bold yellow]")
        return

    if df.empty:
        console.print("[bold yellow]⚠️  Arquivo de leads está vazio.[/bold yellow]")
        return

    # Garante que colunas novas existam em CSVs antigos
    for col in ["Site", "Tem Site", "Telefone", "Link Maps"]:
        if col not in df.columns:
            df[col] = ""

    leads = df.to_dict("records")
    exibir_tabela_leads(leads, titulo=f"📋 Leads Salvos ({len(leads)} total)")

    sem_site = sum(1 for l in leads if l.get("Tem Site") != "Sim")
    console.print(f"\n[bold yellow]🚀 Leads SEM site (oportunidades): {sem_site}[/bold yellow]")


def filtrar_sem_site():
    try:
        df = pd.read_csv("leads_encontrados.csv", encoding="utf-8-sig")
    except FileNotFoundError:
        console.print("[bold yellow]⚠️  Nenhum arquivo de leads encontrado ainda.[/bold yellow]")
        return

    if "Tem Site" not in df.columns:
        console.print("[bold yellow]⚠️  Arquivo antigo sem coluna 'Tem Site'. Rode uma nova busca.[/bold yellow]")
        return

    sem_site_df = df[df["Tem Site"] != "Sim"]

    if sem_site_df.empty:
        console.print("[bold green]✅ Todos os leads já têm site![/bold green]")
        return

    leads = sem_site_df.to_dict("records")
    exibir_tabela_leads(leads, titulo=f"🚀 {len(leads)} Leads SEM SITE — Oportunidades!")

    exportar = Prompt.ask(
        "[bold yellow]Exportar esses leads para CSV separado?[/bold yellow] (s/n)",
        default="s"
    )
    if exportar.lower() == "s":
        sem_site_df.to_csv("leads_sem_site.csv", index=False, encoding="utf-8-sig")
        console.print("[bold green]📁 Salvo em: leads_sem_site.csv[/bold green]")


def limpar_leads():
    confirmacao = Prompt.ask(
        "[bold red]⚠️  Tem certeza que deseja apagar todos os leads?[/bold red] (s/n)",
        default="n"
    )
    if confirmacao.lower() == "s":
        try:
            import os
            os.remove("leads_encontrados.csv")
            console.print("[bold green]✅ Arquivo de leads removido com sucesso![/bold green]")
        except FileNotFoundError:
            console.print("[bold yellow]⚠️  Nenhum arquivo para remover.[/bold yellow]")
    else:
        console.print("[bold cyan]Operação cancelada.[/bold cyan]")


def main():
    exibir_banner()

    while True:
        exibir_menu()
        opcao = Prompt.ask(
            "[bold yellow]Escolha uma opção[/bold yellow]",
            choices=["1", "2", "3", "4", "5"]
        )

        if opcao == "1":
            buscar_leads()
        elif opcao == "2":
            ver_leads()
        elif opcao == "3":
            filtrar_sem_site()
        elif opcao == "4":
            limpar_leads()
        elif opcao == "5":
            console.print("\n[bold cyan]👋 Até logo! Bons negócios![/bold cyan]\n")
            break


if __name__ == "__main__":
    main()