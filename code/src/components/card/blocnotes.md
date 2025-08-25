Avant modifs:
```log
INFO:root:global: PyQt5.QtCore.QRectF(0.0, 0.0, 308.0, 89.0)
INFO:root:top: PyQt5.QtCore.QRectF(0.0, 0.0, 76.0, 13.0)
INFO:root:left: PyQt5.QtCore.QRectF(0.0, 0.0, 95.0, 23.0)
INFO:root:center: PyQt5.QtCore.QRectF(0.0, 0.0, 95.0, 23.0)
INFO:root:right: PyQt5.QtCore.QRectF(0.0, 0.0, 88.0, 23.0)
INFO:root:bottom: PyQt5.QtCore.QRectF(0.0, 0.0, 290.0, 23.0)
```

bon la zone fait `308.0 Width` et `89.0 Height`
donc __top__ a comme vecteur Y(0.0 -> 13.0) et X(0.0 -> 308.0)
donc __bottom__ a comme vecteur Y(66.0 -> 89.0) et X(0.0 -> 308.0)
donc __left__ a comme vecteur Y(13.0 -> 36.0) et X(0.0 -> 95.0)
donc __center__ a comme vecteur Y(13.0 -> 36.0) et X(95.0 -> 190.0)
donc __right__ a comme vecteur Y(13.0 -> 36.0) et X(190.0 -> 278.0)


Les valeurs que j'utilise sont:
```python
var_qrect_global = self.rect()
var_qrect_obj = widget.rect()
var_position_obj = self.card_layout.getItemPosition(self.card_layout.indexOf(widget))
left_margin, top_margin, right_margin, bottom_margin = self.card_layout.getContentsMargins()

```

```log
INFO:root:global: PyQt5.QtCore.QRectF(0.0, 0.0, 308.0, 89.0)
INFO:root:top: PyQt5.QtCore.QRectF(9.0, 9.0, 94.0, 31.0)
INFO:root:left: PyQt5.QtCore.QRectF(10.0, 9.0, 113.0, 41.0)
INFO:root:center: PyQt5.QtCore.QRectF(10.0, 10.0, 113.0, 41.0)
INFO:root:right: PyQt5.QtCore.QRectF(10.0, 11.0, 106.0, 41.0)
INFO:root:bottom: PyQt5.QtCore.QRectF(11.0, 9.0, 308.0, 41.0)
```

|Zone|Coordonnée X de départ|Coordonnée Y de départ|Largeur (Width)|Hauteur (Height)|Coordonnée X de fin|Coordonnée Y de fin|
|:---|:--:|:--:|:--:|:--:|:--:|:--:|
| **global** | 0.0 | 0.0 | 308.0 | 89.0 | 308.0 | 89.0  |
| **top**  | 0.0-9.0 | 0.0-9.0 | 76.0-94.0  | 13.0-31.0 | 76.0-103.0 | 13.0-40.0  |
| **left** | 0.0-10.0 | 0.0-9.0 | 95.0-113.0 | 23.0-41.0 | 95.0-123.0 | 23.0-50.0  |
| **center** | 0.0-10.0 | 0.0-10.0 | 95.0-113.0 | 23.0-41.0 | 95.0-123.0 | 23.0-51.0  |
| **right**  | 0.0-10.0 | 0.0-11.0 | 88.0-106.0 | 23.0-41.0 | 88.0-116.0 | 23.0-52.0  |
| **bottom** | 0.0-11.0 | 0.0-9.0 | 290.0-308.0 | 23.0-41.0 | 290.0-319.0 | 23.0-50.0  |

```log
INFO:root:top: PyQt5.QtCore.QRectF(9.0, 9.0, 85.0, 22.0)
INFO:root:left: PyQt5.QtCore.QRectF(10.0, 9.0, 104.0, 32.0)
INFO:root:center: PyQt5.QtCore.QRectF(10.0, 10.0, 104.0, 32.0)
INFO:root:right: PyQt5.QtCore.QRectF(10.0, 11.0, 97.0, 32.0)
INFO:root:bottom: PyQt5.QtCore.QRectF(11.0, 9.0, 299.0, 32.0)

INFO:root:top: PyQt5.QtCore.QRectF(18.0, 18.0, 85.0, 22.0)
INFO:root:left: PyQt5.QtCore.QRectF(18.0, 37.0, 104.0, 32.0)
INFO:root:center: PyQt5.QtCore.QRectF(119.0, 37.0, 104.0, 32.0)
INFO:root:right: PyQt5.QtCore.QRectF(220.0, 37.0, 97.0, 32.0)
INFO:root:bottom: PyQt5.QtCore.QRectF(18.0, 66.0, 299.0, 32.0)
```