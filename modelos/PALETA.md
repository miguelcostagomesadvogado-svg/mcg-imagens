# Paleta MCG (aprovada pelo Dr. Miguel a 24 nov. 2026)

Aplicar em todas as peças novas (carrosséis, imagens, Stories e Reels).

| Cor | HEX | Uso |
|---|---|---|
| Navy | #0F1F3D | Fundo de todas as peças (nunca preto). Gradientes navy permitidos. |
| Dourado | #E3C167 | Títulos, selos, filetes e destaques. Contraste sobre navy 9,42:1. |
| Marfim | #F6F1E6 | Blocos de texto («O Advogado comenta»), fundos claros de Stories, texto corrido sobre navy (14,5:1). Único marfim da marca: não usar #F3EEE4 nem #F4EFE6. |
| Bordô | #7A1F2B | Só no selo da linha «Património» e em pequenos acentos. Nunca como fundo da peça. Dourado sobre bordô 5,87:1; marfim sobre bordô 9,1:1. |
| Azul-névoa | #B9C3DC | Texto secundário sobre navy (9,3:1). |

Regras:
- Nunca dourado sobre marfim (1,5:1). Sobre marfim, o texto vai em navy.
- Cores néon das peças temáticas (#FF7A6B, #36E6FF, #FF3EC8, etc.) só como acento, até cerca de 20% da peça.
- Reels (modelos/reels-pesquisa/gen.py) já usam #E3C167 e #F6F1E6.

Selo da linha «Património» (CSS):

```css
.selo.pat{left:50%;right:auto;transform:translateX(-50%);background:#7a1f2b;color:#e3c167;
  border:1px solid #e3c167;padding:12px 22px 12px 34px;border-radius:2px;white-space:nowrap}
```
(o padding à esquerda maior compensa o letter-spacing de 12px no fim da palavra)

Paleta no Coolors: https://coolors.co/0f1f3d-e3c167-f6f1e6-7a1f2b-b9c3dc
