# anim-system
## Wdrożenie zamysłu na obsługę animacji
System animacji wspiera dwa rodzaje animowanych sprite'ów - zapętlone i zależne od parametru.
Pierwszy typ ma zastosowanie na przykład gdy chcemy dodać wydech rakiet do statku gracza. 
Dodatkowa możliwość obsługi różnych "stanów" tego typu animacji pozwala na zmianę rozmiaru lub kolorów płomieni przy odpowiednich akcjach gracza.
Drugi typ pozwala na tłumaczenie wektora na stan sprite'a na siatce 5x5 (docelowo NxN) z dowolnym thresholdem przeskoku animacji ze stanu przejściowego na skrajny i na odwrót.
