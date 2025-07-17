import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

fixada = False

DESCONTOS_ANO = {
    "Sem desconto": {'avista': 0, 'parcelado': 0},
    "Preventivo": {'avista': 30, 'parcelado': 0},
    "Outros": {},
    "2020/2021": {'avista': 50, 'parcelado': 25},
    "2022/2023": {'avista': 40, 'parcelado': 20},
    "2024/2025": {'avista': 20, 'parcelado': 10}
}

desconto_personalizado = {'avista': 0, 'parcelado': 0}

def obter_desconto_por_grupo(grupo, modalidade):
    if grupo == "Outros":
        return desconto_personalizado.get(modalidade, 0)
    descontos = DESCONTOS_ANO.get(grupo, {})
    return descontos.get(modalidade, 0)

def calcular():
    try:
        valor_bruto = entrada_valor.get()
        valor_limpo = re.sub(r"[^\d,]", "", valor_bruto).replace(".", "").replace(",", ".")
        valor_inicial = float(valor_limpo)

        grupo_ano = combo_ano.get()
        if not grupo_ano:
            messagebox.showerror("Erro", "Por favor, selecione o ano do contrato.")
            return

        if grupo_ano == "Outros":
            try:
                avista = float(entrada_avista.get())
                parcelado = float(entrada_parcelado.get())
                desconto_personalizado['avista'] = avista
                desconto_personalizado['parcelado'] = parcelado
            except ValueError:
                messagebox.showerror("Erro", "Preencha os campos de desconto personalizados corretamente.")
                return

        desconto_avista = obter_desconto_por_grupo(grupo_ano, 'avista')
        desconto_parcelado = obter_desconto_por_grupo(grupo_ano, 'parcelado')

        valor_avista = valor_inicial - (valor_inicial * (desconto_avista / 100))
        valor_parcelado = valor_inicial - (valor_inicial * (desconto_parcelado / 100))

        parcelas = 3
        valor_parcela = valor_parcelado / parcelas

        if valor_parcela < 50:
            parcelas = 2
            valor_parcela = valor_parcelado / parcelas
            if valor_parcela < 50:
                parcelas = 0

        resultado = f"*SEGUE ABAIXO VALORES E CONDIÇÕES:*\n"
        resultado += f"Valor total: *R$ {valor_inicial:.2f}*\n"

        if desconto_avista > 0:
            resultado += f"Valor com desconto (À vista): *R$ {valor_avista:.2f}*\n"

        if parcelas >= 2:
            resultado += f"Parcelamento: em até *{parcelas}x de R$ {valor_parcela:.2f}*\n\n"
            resultado += "Qual a melhor forma de pagamento? *Digite 1 para à vista ou digite 2 para parcelado*\n"

        resultado += "Posso encaminhar seu boleto para pagamento *HOJE* mesmo?"

        texto_resultado.config(state=tk.NORMAL)
        texto_resultado.delete(1.0, tk.END)
        texto_resultado.insert(tk.END, resultado)
        texto_resultado.config(state=tk.DISABLED)

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Por favor, digite um valor válido (ex: 150, 150,50, R$ 150,50)."
        )

def copiar():
    texto_resultado.config(state=tk.NORMAL)
    resultado = texto_resultado.get(1.0, tk.END)
    janela.clipboard_clear()
    janela.clipboard_append(resultado.strip())
    janela.update()
    texto_resultado.config(state=tk.DISABLED)

def alternar_fixacao():
    global fixada
    fixada = not fixada
    janela.attributes("-topmost", fixada)
    botao_fixar.config(text="Desafixar" if fixada else "Fixar")

def ao_selecionar_ano(event):
    if combo_ano.get() == "Outros":
        label_avista.grid(row=2, column=0, sticky="w")
        entrada_avista.grid(row=2, column=1, sticky="ew", pady=5)

        label_parcelado.grid(row=3, column=0, sticky="w")
        entrada_parcelado.grid(row=3, column=1, sticky="ew", pady=5)
    else:
        label_avista.grid_remove()
        entrada_avista.grid_remove()
        label_parcelado.grid_remove()
        entrada_parcelado.grid_remove()

def abrir_janela_boleto():
    janela_boleto = tk.Toplevel(janela)
    janela_boleto.title("Solicitar Boleto")
    janela_boleto.geometry("420x520")

    frame_boleto = ttk.Frame(janela_boleto, padding=20)
    frame_boleto.pack(fill="both", expand=True)

    ttk.Label(frame_boleto, text="CPF:").grid(row=0, column=0, sticky="w")
    entrada_cpf = ttk.Entry(frame_boleto)
    entrada_cpf.grid(row=0, column=1, sticky="ew", pady=5)

    ttk.Label(frame_boleto, text="Valor Total (R$):").grid(row=1, column=0, sticky="w")
    entrada_valor_total = ttk.Entry(frame_boleto)
    entrada_valor_total.grid(row=1, column=1, sticky="ew", pady=5)

    ttk.Label(frame_boleto, text="Ano do contrato:").grid(row=2, column=0, sticky="w")
    anos_sem_outros = [ano for ano in DESCONTOS_ANO.keys() if ano != "Outros"]
    combo_ano_boleto = ttk.Combobox(frame_boleto, values=anos_sem_outros)
    combo_ano_boleto.set("")
    combo_ano_boleto.grid(row=2, column=1, sticky="ew", pady=5)

    ttk.Label(frame_boleto, text="Desconto manual (% para modalidade selecionada):").grid(row=3, column=0, sticky="w")
    entrada_desconto_manual = ttk.Entry(frame_boleto)
    entrada_desconto_manual.grid(row=3, column=1, sticky="ew", pady=5)

    ttk.Label(frame_boleto, text="Modalidade:").grid(row=4, column=0, sticky="w")
    combo_modalidade = ttk.Combobox(frame_boleto, values=["avista", "parcelado"])
    combo_modalidade.set("")
    combo_modalidade.grid(row=4, column=1, sticky="ew", pady=5)

    ttk.Label(frame_boleto, text="Data do pagamento (ddmm):").grid(row=5, column=0, sticky="w")
    entrada_data_pagamento = ttk.Entry(frame_boleto)
    entrada_data_pagamento.grid(row=5, column=1, sticky="ew", pady=5)

    ttk.Label(frame_boleto, text="Mensagem gerada:").grid(row=6, column=0, sticky="w")
    texto_resultado_boleto = tk.Text(frame_boleto, height=10)
    texto_resultado_boleto.grid(row=7, column=0, columnspan=2, sticky="nsew")
    texto_resultado_boleto.config(state=tk.DISABLED)

    def gerar_mensagem_boleto():
        cpf_raw = entrada_cpf.get().strip()
        valor_str = entrada_valor_total.get()
        grupo_ano = combo_ano_boleto.get()
        desconto_manual_str = entrada_desconto_manual.get().strip()
        modalidade = combo_modalidade.get()
        data_pagamento_raw = entrada_data_pagamento.get().strip()

        if not (cpf_raw and valor_str and grupo_ano and modalidade and data_pagamento_raw):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        cpf_digits = re.sub(r"\D", "", cpf_raw)
        if len(cpf_digits) != 11:
            messagebox.showerror("Erro", "O CPF deve conter 11 números.")
            return

        cpf_formatado = f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"

        try:
            valor_limpo = re.sub(r"[^\d,]", "", valor_bruto).replace(".", "").replace(",", ".")
            valor_total = float(valor_limpo)
        except ValueError:
            messagebox.showerror("Erro", "Valor inválido!")
            return

        desconto_aplicado = None
        if desconto_manual_str:
            try:
                desconto_aplicado = float(desconto_manual_str)
                if desconto_aplicado < 0 or desconto_aplicado > 100:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erro", "Desconto manual inválido! Digite um número entre 0 e 100.")
                return
        else:
            desconto_aplicado = obter_desconto_por_grupo(grupo_ano, modalidade)

        valor_com_desconto = valor_total - (valor_total * desconto_aplicado / 100)

        data_digits = re.sub(r"\D", "", data_pagamento_raw)
        if len(data_digits) != 4:
            messagebox.showerror("Erro", "A data deve ter 4 dígitos: dia e mês (ex: 1107 para 11/07).")
            return

        data_formatada = f"{data_digits[:2]}/{data_digits[2:]}"

        mensagem = f"*SOLICITAÇÃO DE BOLETO COM DESCONTO*\n\n"
        mensagem += f"*CPF:* {cpf_formatado}\n"
        mensagem += f"*Valor atualizado:* R$ {valor_total:.2f}\n"

        if modalidade == "parcelado":
            parcelas = 3
            valor_parcela = valor_com_desconto / parcelas
            if valor_parcela < 50:
                parcelas = 2
                valor_parcela = valor_com_desconto / parcelas
                if valor_parcela < 50:
                    parcelas = 0

            if parcelas >= 2:
                mensagem += f"*Parcelamento:* em até {parcelas}x de R$ {valor_parcela:.2f}\n"
            
        else:
            mensagem += f"*Valor com desconto:* R$ {valor_com_desconto:.2f}\n"

        if desconto_aplicado.is_integer():
            desconto_str = f"{int(desconto_aplicado)}%"
        else:
            desconto_str = f"{desconto_aplicado}%"

        mensagem += f"*% aplicada:* {desconto_str}\n"
        mensagem += f"*Data do pagamento:* {data_formatada}\n"

        texto_resultado_boleto.config(state=tk.NORMAL)
        texto_resultado_boleto.delete(1.0, tk.END)
        texto_resultado_boleto.insert(tk.END, mensagem)
        texto_resultado_boleto.config(state=tk.DISABLED)

    botao_gerar = ttk.Button(frame_boleto, text="Gerar Mensagem", command=gerar_mensagem_boleto)
    botao_gerar.grid(row=8, column=0, columnspan=2, sticky="ew", pady=10)

    def copiar_boleto():
        texto_resultado_boleto.config(state=tk.NORMAL)
        texto = texto_resultado_boleto.get(1.0, tk.END).strip()
        if texto:
            janela_boleto.clipboard_clear()
            janela_boleto.clipboard_append(texto)
            janela_boleto.update()
        texto_resultado_boleto.config(state=tk.DISABLED)

    botao_copiar_boleto = ttk.Button(frame_boleto, text="Copiar Mensagem", command=copiar_boleto)
    botao_copiar_boleto.grid(row=9, column=0, columnspan=2, sticky="ew", pady=5)

    frame_boleto.columnconfigure(0, weight=1)
    frame_boleto.columnconfigure(1, weight=1)
    frame_boleto.rowconfigure(7, weight=1)

janela = tk.Tk()
janela.title("Agius app (Master)")
janela.geometry("450x600")

frame = ttk.Frame(janela, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(6, weight=1)

ttk.Label(frame, text="Digite o valor (R$):").grid(row=0, column=0, sticky="w")
entrada_valor = ttk.Entry(frame)
entrada_valor.grid(row=0, column=1, sticky="ew", pady=5)

ttk.Label(frame, text="Selecione o ano do contrato:").grid(row=1, column=0, sticky="w")
combo_ano = ttk.Combobox(frame, values=list(DESCONTOS_ANO.keys()))
combo_ano.set("")
combo_ano.grid(row=1, column=1, sticky="ew", pady=5)
combo_ano.bind("<<ComboboxSelected>>", ao_selecionar_ano)

label_avista = ttk.Label(frame, text="Desconto à vista (%):")
entrada_avista = ttk.Entry(frame)

label_parcelado = ttk.Label(frame, text="Desconto parcelado (%):")
entrada_parcelado = ttk.Entry(frame)

label_avista.grid_remove()
entrada_avista.grid_remove()
label_parcelado.grid_remove()
entrada_parcelado.grid_remove()

ttk.Button(frame, text="Calcular", command=calcular).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

ttk.Label(frame, text="Resultado:").grid(row=5, column=0, sticky="w")
texto_resultado = tk.Text(frame, height=10)
texto_resultado.grid(row=6, column=0, columnspan=2, sticky="nsew")
texto_resultado.config(state=tk.DISABLED)

botao_copiar = ttk.Button(frame, text="Copiar", command=copiar)
botao_copiar.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)

botao_fixar = ttk.Button(frame, text="Fixar", command=alternar_fixacao)
botao_fixar.grid(row=8, column=0, columnspan=2, sticky="ew", pady=5)

botao_boleto = ttk.Button(frame, text="Solicitar Boleto", command=abrir_janela_boleto)
botao_boleto.grid(row=9, column=0, columnspan=2, sticky="ew", pady=5)

janela.mainloop()

