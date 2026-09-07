# -*- coding: utf-8 -*-
"""あいことばで開く（認証）10ページ を生成する。
確定ルール：
  ・すべて position:absolute の座標指定（中央揃え・paddingは効かない）
  ・枠線(border/stroke)は取り込まれない → 色ベタのdivを2枚重ねて枠にする
  ・SVGは矢印など「どうしても図形が要るもの」だけ。数を増やすと全部消える
  ・画像は絶対URL
"""
import io, sys

O = []
def add(s): O.append(s)

def frame(x, y, w, h, line, fill, r=12, t=4):
    """枠。外側に線の色のベタ、内側に塗りのベタを重ねる。"""
    add(f'<div class="a" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{line};border-radius:{r}px"></div>')
    add(f'<div class="a" style="left:{x+t}px;top:{y+t}px;width:{w-t*2}px;height:{h-t*2}px;background:{fill};border-radius:{max(r-3,0)}px"></div>')

# 矢印の字の実測値（font-size=F に対する比。2026-09-07 に書き出し画像から測定）
#   lsb=左の余白 / w=字の幅 / cy=字の中心の高さ
# かなの中心は 0.584F。cy がこれに近い字は「本文と同じ書体」で出ている。
ARROW_METRICS = {
    "→": (0.087, 0.819, 0.591),   # →  本文と同じ書体
    "⇒": (0.113, 0.781, 0.591),   # ⇒  本文と同じ書体
    "▶": (0.062, 0.406, 0.591),   # ▶  本文と同じ書体
    "➜": (0.056, 0.700, 0.628),   # ➜  別の書体（フォールバック）
    "➡": (0.056, 0.744, 0.628),   # ➡  別の書体（フォールバック）
}
ARROW_GLYPH = "→"      # 既定。本文と同じ書体で出る字にすること
ARROW_BOLD  = True           # 細く見えるので太字にする

def arrow(x, y, w, h, color="#3d3d3d", left=False):
    """矢印は1文字のテキストで置く。
    図形を組み合わせるとCanva上で1本の矢印にならず、動かすと崩れるため。
    Canvaは line-height を落とすので、字の中心が実測値どおりに来るよう座標を逆算する。
    x,y,w,h は矢印を置きたい範囲。その中央に置く。"""
    g = ARROW_GLYPH
    lsb, gw, gcy = ARROW_METRICS[g]
    f  = int(h * 1.4)                       # 字の大きさ
    cx = x + w / 2                          # 置きたい中心
    cy = y + h / 2
    gx = int(cx - (lsb + gw / 2) * f)       # 字の左端 = 中心 -（左余白＋幅の半分）
    # 180度回すと、字の中心が箱の中心を挟んで反対側に移る（箱の高さ＝字の大きさ）
    gy = int(cy - (1 - gcy if left else gcy) * f)
    st = f'left:{gx}px;top:{gy}px;font-size:{f}px;color:{color};line-height:1'
    if ARROW_BOLD: st += ';font-weight:bold'
    if left:       st += ';transform:rotate(180deg)'
    add(f'<div class="a" style="{st}">{g}</div>')

def txt(x, y, s, cls="", style=""):
    c = f' class="a {cls}"' if cls else ' class="a"'
    st = f'left:{x}px;top:{y}px' + (';' + style if style else '')
    add(f'<div{c} style="{st}">{s}</div>')

def band(title):
    add('<div class="a" style="left:100px;top:70px;width:1720px;height:76px;background:#f2f2f2"></div>')
    add('<div class="a" style="left:100px;top:70px;width:14px;height:76px;background:#888"></div>')
    txt(140, 84, title, "h2")

def page(label, notes):
    add(f'<section class="page" data-document-role="page" data-label="{label}"\n data-speaker-notes="{notes}">')

def end():
    add('</section>\n')

add('''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><title>あいことばで開く</title>
<style>
 *{box-sizing:border-box;margin:0;padding:0}
 body{font-family:"BIZ UDPGothic","Yu Gothic",sans-serif;color:#1a1a1a}
 .page{width:1920px;height:1080px;position:relative;background:#fff;overflow:hidden}
 .a{position:absolute}
 .h2{font-size:44px;font-weight:bold}
 .q{font-size:64px;font-weight:bold;line-height:1.4}
 .c{font-size:38px;line-height:1.45}
 .b{font-size:40px;line-height:1.5}
 .teach{font-size:28px;color:#777}
 .cap{font-size:30px;color:#555}
 .navy{color:#1f4e79;font-weight:bold}
</style></head><body>
''')

# --- p1 表紙 -------------------------------------------------------------
page("表紙", "単元名はスライド表紙の文言に合わせる。ver表記を忘れない。")
add('<div class="a" style="left:0;top:0;width:1920px;height:1080px;background:linear-gradient(135deg,#1f4e79,#3a7bd5)"></div>')
txt(120, 300, "あいことばで開く", style="font-size:96px;font-weight:bold;color:#fff")
txt(120, 450, "── 認証のしくみをつくる", style="font-size:64px;font-weight:bold;color:#fff")
txt(120, 600, "中学技術　情報の技術／AkaDakoシリーズ「__DEV__」", style="font-size:42px;color:#eaf2fb")
txt(1480, 960, "ver.0.2（案）", style="font-size:30px;color:#cfe0f5")
end()

# --- p2 質問① -----------------------------------------------------------
page("質問①", "全員が手を挙げられる問いにする。知識を問う場面にしない。小さなお願いを1つ聞いてもらうことで、以後の指示が通りやすくなる。")
add('<div class="a" style="left:100px;top:70px;width:220px;height:64px;background:#c0392b"></div>')
txt(143, 82, "質問", style="font-size:40px;color:#fff")
txt(100, 200, "今日、スマホや端末の<br>ロックを解除しましたか？", "q")
for i, (n, s) in enumerate([("①","していない"),("②","1〜2回"),("③","3〜5回"),("④","6回以上")]):
    x = 100 + i*440
    frame(x, 470, 400, 130, "#555", "#fff")
    txt(x+40, 515, n, "c"); txt(x+94, 515, s, "c")
txt(100, 960, "このあと「では、正確に何回か言える人？」と問う。ほとんど誰も答えられない。", "teach")
end()

# --- p3 質問② -----------------------------------------------------------
page("質問②", "答えは③。①か②と答える生徒が多い。ここでは答えを軽く示すだけにとどめる。")
add('<div class="a" style="left:100px;top:70px;width:220px;height:64px;background:#c0392b"></div>')
txt(143, 82, "質問", style="font-size:40px;color:#fff")
txt(100, 200, "ATMで暗証番号を入れたとき、<br>合っているかを確かめているのはどこでしょう？", "q")
for i, (n, s) in enumerate([("①","ATMの機械の中"),("②","キャッシュ<br>カードの中"),("③","銀行の<br>コンピュータ"),("④","確かめていない")]):
    x = 100 + i*440
    frame(x, 490, 400, 180, "#555", "#fff")
    txt(x+40, 540, n, "c"); txt(x+94, 540, s, "c", "width:250px")
end()


# --- p4 3つの疑問と学習問題 ----------------------------------------------
page("3つの疑問と学習問題", "3つの疑問は板書に残す。銀行のコンピュータは見に行けないので、同じものを教室の中で作って確かめる、と宣言する。")
band("答えは ③ 銀行のコンピュータ")
frame(100, 210, 420, 140, "#444", "#fafafa", 14, 5)
txt(140, 240, "あなた", style="font-size:38px;font-weight:bold")
txt(140, 292, "暗証番号を入れる", style="font-size:30px")
arrow(550, 250, 220, 80)
frame(800, 210, 440, 140, "#d08000", "#ffe9c7", 14, 5)
txt(840, 240, "銀行のコンピュータ", style="font-size:38px;font-weight:bold;color:#c25e00")
txt(840, 292, "合っているか確かめる", style="font-size:30px")
arrow(1260, 250, 110, 80, left=True)
frame(1380, 210, 440, 140, "#3a7bd5", "#eaf4ff", 14, 5)
txt(1420, 240, "OK / NG が返る", style="font-size:38px;font-weight:bold;color:#14385f")
txt(1420, 292, "あの数秒は、返事待ち", style="font-size:30px")
for i, s in enumerate(["なぜ、カードの中で確かめないのだろう？",
                      "遠くのコンピュータに聞くとき、何が行き来している？",
                      "その行き来を、他の人が見ることはできる？"]):
    y = 440 + i*80
    txt(110, y, "①②③"[i], "b"); txt(164, y, s, "b", "width:1600px")
frame(100, 720, 1720, 130, "#1f4e79", "#f7fafd", 14, 5)
txt(148, 748, "学習問題", style="font-size:30px;color:#5a7ea6")
txt(148, 790, "私たちは、どうやって「本人だ」と確かめられているのだろうか。", "b navy")
txt(100, 960, "教師は答えを言い切らない。疑問は板書に残したまま第1時に入る。", "teach")
end()

# --- p5 学習目標と用意するもの --------------------------------------------
page("学習目標と用意するもの", "学習目標は最後の振り返りで戻ってくる。用意するものは本体とPCだけ。")
band("学習目標と、用意するもの")
frame(100, 190, 1720, 180, "#1f4e79", "#fff", 14, 5)
txt(148, 232, "認証のしくみを理解し、大切な情報を安全に守る方法を", "b navy")
txt(148, 292, "考えられるようになろう。", "b navy")
add('<img class="a" src="https://aoki-tfab.github.io/akadako-slide-test/img/__IMG__" style="left:100px;top:440px;width:620px" alt="__DEV__">')
txt(100, 830, "__DEV__（2人で1台）", "cap")
frame(840, 510, 330, 160, "#444", "#fafafa", 12, 5)
txt(880, 570, "利用者役", style="font-size:36px")
arrow(1200, 555, 120, 70)
frame(1350, 510, 330, 160, "#d08000", "#ffe9c7", 12, 5)
txt(1390, 570, "サーバー役", style="font-size:36px;color:#c25e00")
txt(1160, 710, "2人1組・2台", style="font-size:32px")
end()

# --- p6 本人だと確かめられた場面 ------------------------------------------
page("本人だと確かめられた場面", "p.2の質問①とつなげる。生徒からの例を出させる。板書は横に集める。")
band("第1時　本人確認って、どうやっている？")
txt(100, 230, "あなたが「本人だ」と<br>確かめられた場面を挙げてください。", "q")
txt(100, 520, "出てきた例を板書に集める。", style="font-size:34px;color:#666")
for i, s in enumerate(["スマホのロック", "駅の改札", "出席確認", "家の鍵"]):
    x = 100 + i*360
    frame(x, 590, 330, 90, "#8aa9c9", "#eef3f9", 45, 3)
    txt(x+50, 615, s, "c")
end()

# --- p7 どれも同じ形 ------------------------------------------------------
page("どれも同じ形", "生徒の挙げた例を、示す→確かめる→返る の3つに整理する。冒頭の疑問②に接続する。")
band("どれも、同じ形をしている")
frame(120, 320, 440, 160, "#444", "#fafafa", 16, 6)
txt(160, 375, "示す", style="font-size:44px;font-weight:bold")
arrow(590, 370, 210, 100)
frame(820, 320, 440, 160, "#d08000", "#ffe9c7", 16, 6)
txt(860, 375, "確かめる", style="font-size:44px;font-weight:bold;color:#c25e00")
arrow(1290, 370, 210, 100)
frame(1520, 320, 280, 160, "#3a7bd5", "#eaf4ff", 16, 6)
txt(1560, 375, "返る", style="font-size:44px;font-weight:bold;color:#14385f")
txt(100, 640, "行って、返ってくる。", "b")
txt(100, 710, "往復しないと、認証にならない。", "b navy")
txt(100, 960, "冒頭の疑問②「何が行き来している？」に戻る場面。", "teach")
end()

# --- p8 準備 --------------------------------------------------------------
page("準備", "通信グループIDは既習なら復習。簡単なIDにすると他の班と混ざることに触れる。")
band("準備　2人1組で、通信グループIDを決める")
for i, s in enumerate(["2人1組になり、2台のPCにそれぞれ本体をつなぐ。",
                       "班で相談して、通信グループIDを1つ決める。他の班と同じにならないようにする。",
                       "2台とも、同じIDを入力する。"]):
    y = 230 + i*90
    txt(110, y, "①②③"[i], "b"); txt(164, y, s, "b", "width:1600px")
frame(100, 540, 1720, 150, "#d08000", "#fff8e6", 14, 4)
txt(148, 568, "注意", style="font-size:30px;color:#c25e00")
txt(148, 610, "かんたんなIDにすると、他の班の通信と混ざったり、のぞかれたりする。", "c", "width:1560px")
end()

# --- p9 やってみよう① ----------------------------------------------------
page("やってみよう①", "まず完成例を見せてから作らせる。動いた瞬間を必ず共有する。")
band("やってみよう①　数字を送って、画面に出す")
frame(120, 240, 560, 160, "#444", "#fafafa", 16, 6)
txt(160, 285, "送る側", style="font-size:40px;font-weight:bold")
txt(160, 340, "数字を送る", style="font-size:32px")
arrow(710, 290, 190, 100)
frame(1000, 240, 560, 160, "#3a7bd5", "#eaf4ff", 16, 6)
txt(1040, 285, "受け取る側", style="font-size:40px;font-weight:bold;color:#14385f")
txt(1040, 340, "画面に表示する", style="font-size:32px")
for i, s in enumerate(["送る側は「通信01 データを送る」を使い、好きな数字を送る。",
                       "受け取る側は「通信02 データを受け取る」と「制御09 表示する」で画面に出す。",
                       "数字を変えて何度か送ってみる。役割を交代してもよい。"]):
    y = 500 + i*90
    txt(110, y, "①②③"[i], "b"); txt(164, y, s, "b", "width:1600px")
txt(100, 960, "動いたら必ず共有する。「できた」の声を拾ってほめる。", "teach")
end()

# --- p10 これは認証と言えますか -------------------------------------------
page("これは認証と言えますか", "第1時の山場。表示できて満足したところで問う。先に答えを言わない。")
band("問い")
txt(100, 230, "これは、認証と言えますか？", "q")
frame(120, 430, 560, 160, "#444", "#fafafa", 16, 6)
txt(160, 490, "送る側", style="font-size:40px;font-weight:bold")
arrow(710, 480, 190, 100)
frame(1000, 430, 560, 160, "#444", "#fafafa", 16, 6)
txt(1040, 490, "受け取る側", style="font-size:40px;font-weight:bold")
txt(1610, 490, "…だけ？", style="font-size:40px;color:#c0392b")
txt(100, 700, "足りないのは", "b")
txt(100, 770, "「確かめる」と「返す」の2つ。", "b navy")
txt(100, 960, "ここで答えを言わない。次の時間に自分たちで作る。", "teach")
end()

add("</body></html>")
html = "\n".join(O)
import re
for name, dev, img in [("slide_tm.html","タコラッチ・ミニ","device_tm.png"),
                       ("slide_at.html","AkaDako探究ツール","device_at.png"),
                       ("slide_ki.html","AIラッチ","device_ki.png")]:
    out = html.replace("__DEV__", dev).replace("__IMG__", img)
    open(name, "w", encoding="utf-8", newline="\n").write(out)
    print(f'{name}  {len(out.encode()):6d}バイト  ページ{out.count("data-document-role"):3d}  svg{out.count("<svg"):3d}  未置換{out.count("__"):3d}')
