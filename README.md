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

此時，登錄認證沒有加入郵件確認，但是可以正常與數據庫交互
頁面根據登錄狀態選擇性顯示sigin signout
注冊與登錄功能正常
