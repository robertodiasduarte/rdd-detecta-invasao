#!/usr/bin/env python3
"""Detector de cadencia robotica (metronomo) em series de login/renovacao.

Uso:
    python cadencia.py acessos.txt [--limiar-eventos 36] [--limiar-cv 0.05]

Entrada: arquivo texto com um timestamp por linha (ISO 8601 ou formatos comuns
de export: "2026-01-15 07:35:12", "15/01/2026 07:35", etc.). Linhas vazias e
comentarios (#) sao ignorados.

Veredito METRONOMO quando existe uma sequencia de eventos consecutivos com:
  - pelo menos --limiar-eventos eventos (default 36; ~1,5 dia no ritmo 1/hora), e
  - coeficiente de variacao dos intervalos < --limiar-cv (default 5%).

O limiar alto de eventos e deliberado: uma aba de navegador aberta renova token
em cadencia durante o expediente e para; automacao atravessa a madrugada.
Limiar baixo (ex.: 10) marcaria qualquer expediente humano como bot.

Somente stdlib. Nao acessa rede.
"""

import argparse
import statistics
import sys
from datetime import datetime

FORMATS = (
    "%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M",
    "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M",
)


def parse_ts(line):
    line = line.strip().rstrip("Zz")
    for fmt in FORMATS:
        try:
            dt = datetime.strptime(line, fmt)
            return dt.replace(tzinfo=None)
        except ValueError:
            continue
    return None


def fmt_secs(s):
    if s >= 3600:
        return f"{s / 3600:.1f}h"
    if s >= 60:
        return f"{s / 60:.1f}min"
    return f"{s:.0f}s"


def longest_regular_run(deltas, limiar_cv):
    """Maior janela de intervalos consecutivos com cv < limiar_cv.

    Retorna (inicio, tamanho_em_intervalos, media, cv) da melhor janela.
    """
    best = (0, 0, 0.0, 0.0)
    n = len(deltas)
    for i in range(n):
        for j in range(i + 2, n + 1):  # janela de pelo menos 2 intervalos
            window = deltas[i:j]
            mean = statistics.fmean(window)
            if mean <= 0:
                break
            cv = statistics.pstdev(window) / mean
            if cv < limiar_cv:
                if j - i > best[1]:
                    best = (i, j - i, mean, cv)
            else:
                # janela deixou de ser regular; comecar de outro ponto
                break
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("arquivo", help="arquivo com um timestamp por linha")
    ap.add_argument("--limiar-eventos", type=int, default=36,
                    help="minimo de eventos consecutivos regulares (default 36)")
    ap.add_argument("--limiar-cv", type=float, default=0.05,
                    help="coef. de variacao maximo para 'regular' (default 0.05)")
    args = ap.parse_args()

    with open(args.arquivo, encoding="utf-8") as f:
        lines = [ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")]

    stamps, invalidas = [], 0
    for ln in lines:
        ts = parse_ts(ln)
        if ts is None:
            invalidas += 1
        else:
            stamps.append(ts)

    if invalidas:
        print(f"aviso: {invalidas} linha(s) nao reconhecida(s) como data — ignoradas")
    if len(stamps) < 3:
        print("ERRO: preciso de pelo menos 3 timestamps validos.")
        return 2

    stamps.sort()
    deltas = [(b - a).total_seconds() for a, b in zip(stamps, stamps[1:])]
    span_h = (stamps[-1] - stamps[0]).total_seconds() / 3600
    mean_all = statistics.fmean(deltas)
    cv_all = statistics.pstdev(deltas) / mean_all if mean_all > 0 else float("inf")

    i, run_len, mean_run, cv_run = longest_regular_run(deltas, args.limiar_cv)
    eventos_regulares = run_len + 1 if run_len else 0

    print(f"eventos: {len(stamps)} | janela total: {span_h:.1f}h")
    print(f"intervalo medio (serie inteira): {fmt_secs(mean_all)} | cv: {cv_all:.1%}")
    if eventos_regulares:
        ini, fim = stamps[i], stamps[i + run_len]
        madrugada = any(0 <= stamps[k].hour < 6 for k in range(i, i + run_len + 1))
        print(f"maior sequencia regular: {eventos_regulares} eventos "
              f"({ini:%d/%m %H:%M} -> {fim:%d/%m %H:%M}), "
              f"intervalo {fmt_secs(mean_run)}, cv {cv_run:.1%}"
              + (" — atravessa a madrugada" if madrugada else ""))
    else:
        print("maior sequencia regular: nenhuma (intervalos irregulares)")

    if eventos_regulares >= args.limiar_eventos:
        print(f"\nVEREDITO: METRONOMO — {eventos_regulares} eventos consecutivos em "
              f"cadencia cravada (cv {cv_run:.1%} < {args.limiar_cv:.0%}). "
              "Padrao compativel com automacao, nao com uso humano.")
        return 1
    print(f"\nVEREDITO: sem padrao de metronomo (limiar: {args.limiar_eventos} "
          "eventos regulares consecutivos). Isso NAO prova ausencia de "
          "automacao — cruze com origem (ASN), tipo de login e volume de leitura.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
