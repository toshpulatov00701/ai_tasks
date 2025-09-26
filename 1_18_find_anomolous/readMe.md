# 1.18. LOF (Local Outlier Factor) asosida anomal ob’ektlarni aniqlash

Berilgan $A=\{a_{ij}\}_{mn}$ jadvalda $E_{0} = (S_{1}, \ldots, S_{m})$ obyektlarning $\(n\)$ miqdoriy alomatlar bo‘yicha tavsifi keltirilgan.

Ikkita $$\(S_{u}, S_{v} \in E_{0}\)$$ obyektlar o‘rtasidagi masofa $\(\rho(x,y)\)$ Evklid metrikasi bilan hisoblanadi.

Tanlanmaning \(S\) obyektining \(k\) ta eng yaqin qo‘shnilarini $\(N_{k}(S)\)$ bilan, \(k\text{-}dis(S)\) orqali \(S\) obyektidan \(k\) – yaqin qo‘shnigacha bo‘lgan masofani belgilaylik.

Berilgan $A=\{a_{ij}\}_{mn}$ jadvalda $E_{0} = (S_{1}, \ldots, S_{m})$ obyektlarning

$$
RD_{k}(S_{u}, S_{v})=\max\{\,k\text{-}dis(S_{v}),\ \rho(S_{u},S_{v})\,\}
$$

\(S_{u}\) obyektga erishuvchanlik lokal zichligi:

$$
lrd(S_{u})=\left(\frac{\sum\limits_{S_{v}\in N_{k}(S_{u})} RD_{k}(S_{u},S_{v})}{\lvert N_{k}(S_{u})\rvert}\right)^{-1}
$$

LOF (Local Outlier Factor) qiymati esa quyidagicha aniqlanadi:

$$
LOF_{k}(S_{u})=\frac{\sum\limits_{S_{v}\in N_{k}(S_{u})}\dfrac{lrd(S_{v})}{lrd(S_{u})}}{\lvert N_{k}(S_{u})\rvert}
$$
