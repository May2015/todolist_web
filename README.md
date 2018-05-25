#todolist_web

day2:
思路：
用flask-sqlalchemy來配置數據庫， 建立user模型
後發現出現包循環導入的bug
嘗試將app 與 view路由功能切爲兩個文件 的確是沒有包互相導入的問題

但是發現，view中的路由並沒起作用
查資料發現，困爲app並不是全局創建，app.route並不起作用
解決方法是引入藍圖

利用藍圖進行程序結構重新組織，爲簡化，config文件沒有獨立出來
將login register功能加入auth 認證藍圖

此時完成：
register頁面表格由form實現，bootstrap渲染，加入藍圖後，此頁面正常顯示

下一步：
login 頁面也由form正常顯示
