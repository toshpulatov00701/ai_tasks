# 1.18. LOF (Local Outlier Factor) asosida anomal ob’ektlarni aniqlash

### 1.18. 

Berilgan $A=\{a_{ij}\}_{mn}$ jadvalda $E_{0} = (S_{1}, \ldots, S_{m})$ obyektlarning $n$ miqdoriy alomatlar bo‘yicha tavsifi keltirilgan.  

Ikkita $S_{u}, S_{v} \in E_{0}$ obyektlar o‘rtasidagi masofa $\rho(x,y)$ Evklid metrikasi bilan hisoblanadi.  

Tanlanmaning $S$ obyektining $k$ ta eng yaqin qo‘shnilarini $N_{k}(S)$ bilan, $k\text{–}dis(S)$ orqali $S$ obyektidan $k$ – yaqin qo‘shnigacha bo‘lgan masofani belgilaylik.  

$S_{v}$ obyektidan $S_{u}$ obyektgacha erishiluvchi masofa  

$$
RD_{k}(S_{u}, S_{v}) = \max \{k\text{–}dis(S_{v}), \, \rho(S_{u}, S_{v}) \}
$$  

sifatida aniqlanadi (1.a-rasmga qarang).  

$S_{u}$ obyektga erishuvchanlik lokal zichligi  

$$
lrd(S_{u}) = \left( \frac{ \sum\limits_{S_{v} \in N_{k}(S_{u})} RD_{k}(S_{u}, S_{v}) }{ |N_{k}(S_{u})| } \right)^{-1}
$$  

formula bilan aniqlanadi va $S_{u}$ obyektga uning qo‘shnilaridan erishish masofalarining o‘rta arifmetigiga nisbatan teskarisi hisoblanadi.  

Erishishning lokal zichligi qo‘shnilarining erishish lokal zichligi bilan  

$$
LOF_{k}(S_{u}) = \frac{ \sum\limits_{S_{v} \in N_{k}(S_{u})} \dfrac{lrd(S_{v})}{lrd(S_{u})} }{ |N_{k}(S_{u})| }
$$  

formula orqali aniqlanadi.

Berilgan $A = \{ a_{ij} \}_{m \times n}$ jadvalda $E_{0} = (S_{1}, \ldots, S_{m})$ ob’ektlarning n miqdoriy alomatlar bo‘yicha tavsifi keltirilgan. Ikkita $S_{u}, S_{v} \in E_{0}$ ob’ektlar o‘rtasidagi masofa $\rho(x,y)$ еvklid metrikasi bilan hisoblanadi. Tanlanmaning $S$ ob’ektining $k$ ta eng yaqin qo‘shnilarini $N_{k}(S)$ bilan, $k\text{-}dis(S)$ orqali $S$ ob’ektdan $k$ – yaqin qo‘shnigacha bo‘lgan masofani belgilaylik. $S_{v}$ ob’ektdan $S_{u}$ ob’ektgacha erishiluvchi masofa $RD_{k}(S_{u}, S_{v}) = \max \{\, k\text{-}dis(S_{v}), \; \rho(S_{u}, S_{v}) \,\}$ sifatida aniqlanadi (1.a-rasmga qarang).
Su ob’ektga erishuvchanlikning lokal zichligi

$$
RD_{k}(S_{u}, S_{v}) = \max \{\, k\text{-}dis(S_{v}), \; \rho(S_{u}, S_{v}) \,\}
$$

formula bilan aniqlanadi va Su ob’ektga uning qo‘shnilaridan erishish masofalarining o‘rta arifmetikiga nisbatan teskari hisoblanadi. Erishishning lokal zichligi qo‘shnilarning erishish lokal zichligi bilan
ko‘rinishda taqqoslanadi, ya’ni qo‘shnilarga erishishning o‘rtacha lokal zichligini ob’ektning o‘zining erishish lokal zichligiga bo‘lish orqali.
Agar LOFk(Su), 1 yaqin yaqin qiymat teng bo‘lsa, Su ob’ektni qo‘shnilar bilan qiyoslash mumkin bo‘ladi (u holda bu ob’ekt anomal emas (sachratqi)). Birdan kichik qiymatlar zich sohani anglatadi (u ichki soha bo‘lishi mumkin), birdan еtarlicha katta bo‘lgan qiymatlar ob’ektning anomalligidan guvoh beradi.
Berilgan E0 tanlanmaning k=3,5,7 holatlar uchun barcha anomal ob’ektlari aniqlansin.

1-rasm. Anomal ob’ektlarni aniqlash
 (1-рис. Оbнaружeниe aномaльных оbъeктов)
1.a – rasmda V va S ob’ektlari bir xil erishish masofasiga ega (k=3) bo‘lgan holda D ob’ekt k- yaqin qo‘shni bo‘lmaydi. 1.b-rasmda A nuqta boshqa qo‘shnilariga nisbatan kam zichlikka ega. 
1.18. В заданной таблице A={aij}m*n содержатся описание объектов E0=(S1,…,Sm) по n количественным признакам. Расстояние между объектами Su,Sv∈E0 вычисляется по метрике Евклида ρ(x,y). Обозначим через Nk(S) – множество из k ближайших соседей к объекту S и k-dis(S) – расстояние от S до k-го ближайшего соседа. Достижимое расстояние объекта Su из Sv определяется как RDk(Su,Sv)= max{k-dis(Sv), ρ(Su,Sv)} (см. рис.1.а).
Локальная плотность достижимости объекта Su определяется как
и является обратным значением среднему расстоянию достижимости объекта Su из его соседей. Локальная плотность достижимости сравниваются с локальными плотностями достижимости соседей,
которая есть средняя локальная плотность достижимости соседей, делённая на локальную плотность достижимости самого объекта. 
Значение LOFk(Su), примерно равное 1, означает, что объект Su сравним с его соседями (а тогда он не является выбросом). Значение меньше 1 означает плотную область (которая может быть внутренностью), а значения, существенно большие 1, свидетель-ствуют о выбросах. 
В рис. 1.а объекты B и C имеют одно и то же расстояние достижимости (k=3), в то время как D не является k-ближайшим соседом, а в рис.1.b точка A имеет меньшую плотность по сравнению с соседями.
Определить все объекты E0, являющиеся выбросами при k=3,5,7.
