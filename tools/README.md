# 開發工具（建置與自動測試）

- `src.html`：遊戲原始碼（單一檔案）。`build.py` 把它建置成網站根目錄的 `index.html` 與 `assets/`。
- `chk.sh`：語法檢查＋建置。`srv.py`：本機測試伺服器（8765／8766）。`runall.sh`：批次執行測試。
- `tests/`：Playwright 自動測試（需要 Chrome）。
  - `tact1.py` 第一幕、`tact2.py` 第二幕、`tact3.py` 第三幕、`tact4.py` 第四幕、`tact5.py` 第五幕、`tact6.py` 第六幕、`tepi.py` 序章尾聲、`tpre2.py` 第二幕前置（存檔結構、掛勾點）
  - `pix.py` + `pix_base.json`：第一幕逐像素比對基準（`python3 pix.py check`）
  - 其餘 `t*.py`：列車遊戲回歸測試
- 注意：腳本內的路徑是開發環境的絕對路徑，換環境時需要調整。
- `tquiet.py`：序章期間不插入隨機登車、乘客邀約、航行小事件（序章結束後恢復）
- `play.py` + `play_train.py`：序章試跑機器人（只點畫面上看得到的按鈕與 ✦ 徽章，從新遊戲玩到序章尾聲；`python3 play.py epi a6` 可從存點接續）
