非加分題：
1.執行web_server.py
2.在瀏覽器網址列打127.0.0.1:8787
3.網頁出現

加分題：
一、
1.執行threading_web_server.py
2.在瀏覽器網址列打127.0.0.1:8787
3.點擊網頁出現的網址
4.到新的port了
5.重新整理127.0.0.1:8787
6.點擊新出現的網址
7.又到了一個新的port
注：若一段時間沒有新的request到新的port，則該port的socket會自動關閉，之後再送新的request就不會有反應了

二、
1.執行web_server.py
2.執行python Client.py 127.0.0.1 8787 / or python Client.py 127.0.0.1 8787 /index.html
3.網頁內容及http資訊出現