<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="KdBシラバスの教材・参考文献と筑波大学図書館所蔵を対応づける静的Webアプリ" />
  <title>ITF Library BookMap</title>
  <link rel="stylesheet" href="./assets/style.css" />
  <script src="https://cdn.jsdelivr.net/npm/papaparse@5.4.1/papaparse.min.js" defer></script>
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js" defer></script>
  <script type="module" src="./assets/app.js"></script>
</head>
<body>
  <noscript>
    <div class="noscript">このアプリを利用するには JavaScript を有効にしてください。</div>
  </noscript>

  <header class="hero">
    <div class="hero__inner">
      <div>
        <p class="eyebrow">KdB × 筑波大学附属図書館</p>
        <h1>ITF Library BookMap</h1>
        <p class="lead">シラバスの「教材・参考文献・配付資料等」から文献を抽出し、授業・教員・学生の視点で所蔵状況を確認します。</p>
      </div>
      <div class="hero__panel" aria-label="読み込み状況">
        <div class="metric compact">
          <span class="metric__label">科目</span>
          <strong id="metricCourses">0</strong>
        </div>
        <div class="metric compact">
          <span class="metric__label">抽出文献</span>
          <strong id="metricRefs">0</strong>
        </div>
        <div class="metric compact">
          <span class="metric__label">照合済み</span>
          <strong id="metricHoldings">0</strong>
        </div>
      </div>
    </div>
  </header>

  <main class="layout">
    <aside class="sidebar" aria-label="設定">
      <section class="card">
        <h2>データ</h2>
        <p class="hint">`docs/data/courses.csv` がある場合は自動で読み込みます。未配置時はサンプルデータを使います。</p>
        <label class="fileDrop" for="fileInput">
          <span>CSV / Excelをアップロード</span>
          <small>KdBのCourse List CSV/Excelを想定</small>
        </label>
        <input id="fileInput" class="sr-only" type="file" accept=".csv,.tsv,.xlsx,.xls" />
        <div class="buttonRow">
          <button id="reloadBundledData" class="button secondary" type="button">同梱CSVを再読込</button>
          <button id="resetSampleData" class="button secondary" type="button">サンプルに戻す</button>
        </div>
        <div id="dataStatus" class="status muted">初期化中...</div>
      </section>

      <section class="card">
        <h2>CiNii Books照合</h2>
        <p class="hint">アプリケーションIDは画面入力のみで利用し、リポジトリには保存しません。</p>
        <label>CiNiiアプリケーションID
          <input id="ciniiAppId" type="password" autocomplete="off" placeholder="appid" />
        </label>
        <label>機関ID
          <input id="ciniiKid" type="text" value="KI000174" />
        </label>
        <label>図書館ID（任意）
          <input id="ciniiFano" type="text" placeholder="例: FA001652" />
        </label>
        <label>今回の照合上限
          <input id="lookupLimit" type="number" min="1" max="500" value="30" />
        </label>
        <div class="buttonRow">
          <button id="lookupVisible" class="button primary" type="button">未照合の本を照合</button>
          <button id="clearHoldings" class="button danger" type="button">照合結果を消去</button>
        </div>
        <div id="lookupStatus" class="status muted">未照合</div>
      </section>

      <section class="card">
        <h2>出力</h2>
        <div class="buttonRow vertical">
          <button id="downloadRefsCsv" class="button secondary" type="button">全リストCSV</button>
          <button id="downloadCoursesCsv" class="button secondary" type="button">科目CSV</button>
          <button id="downloadHoldingsCsv" class="button secondary" type="button">照合結果CSV</button>
        </div>
      </section>
    </aside>

    <section class="workspace">
      <nav class="tabs" aria-label="モード選択">
        <button class="tab active" data-tab="student" type="button">学生用</button>
        <button class="tab" data-tab="teacher" type="button">教員用</button>
        <button class="tab" data-tab="admin" type="button">管理</button>
      </nav>

      <section id="student" class="tabPanel active" aria-labelledby="学生用">
        <div class="sectionHead">
          <div>
            <h2>学生用モード</h2>
            <p>履修予定の授業を選び、その授業で指定された教材・参考文献の所蔵状況を確認します。</p>
          </div>
          <button id="downloadSelectedCsv" class="button secondary" type="button">選択科目の文献CSV</button>
        </div>
        <div class="filters" id="studentFilters"></div>
        <div class="twoCol">
          <section class="card stretch">
            <div class="panelTitle">
              <h3>科目を選択</h3>
              <div class="buttonRow tight">
                <button id="selectVisibleCourses" class="button secondary small" type="button">表示中を選択</button>
                <button id="clearSelectedCourses" class="button secondary small" type="button">選択解除</button>
              </div>
            </div>
            <div id="studentCourseList" class="checkList"></div>
          </section>
          <section class="card stretch">
            <div class="panelTitle">
              <h3>選択科目の文献</h3>
              <span id="selectedCourseCount" class="pill">0科目</span>
            </div>
            <div id="selectedRefsTable" class="tableWrap"></div>
          </section>
        </div>
      </section>

      <section id="teacher" class="tabPanel" aria-labelledby="教員用">
        <div class="sectionHead">
          <div>
            <h2>教員用モード</h2>
            <p>図書を検索し、同じ図書を使っている他の授業・担当教員を調べます。</p>
          </div>
        </div>
        <div class="searchBar">
          <input id="teacherBookSearch" type="search" placeholder="書名・著者・ISBNで検索 例: Quantum Computation / Nielsen / 9781107002173" />
        </div>
        <div class="twoCol wideLeft">
          <section class="card stretch">
            <div class="panelTitle">
              <h3>図書候補</h3>
              <span id="teacherBookCount" class="pill">0件</span>
            </div>
            <div id="teacherBooksTable" class="tableWrap"></div>
          </section>
          <section class="card stretch">
            <div class="panelTitle">
              <h3>使用授業</h3>
              <span id="teacherSelectedBook" class="pill muted">未選択</span>
            </div>
            <div id="teacherBookDetails" class="tableWrap"></div>
          </section>
        </div>
      </section>

      <section id="admin" class="tabPanel" aria-labelledby="管理">
        <div class="sectionHead">
          <div>
            <h2>管理モード</h2>
            <p>全科目・全文献の一覧、抽出結果、所蔵照合結果を確認します。</p>
          </div>
        </div>
        <div class="metrics">
          <div class="metric"><span class="metric__label">科目数</span><strong id="adminCourses">0</strong></div>
          <div class="metric"><span class="metric__label">抽出文献数</span><strong id="adminRefs">0</strong></div>
          <div class="metric"><span class="metric__label">図書候補</span><strong id="adminBookRefs">0</strong></div>
          <div class="metric"><span class="metric__label">重複除去後</span><strong id="adminUniqueBooks">0</strong></div>
        </div>
        <div class="filters" id="adminFilters"></div>
        <div class="card">
          <div class="panelTitle">
            <h3>全リスト</h3>
            <div class="buttonRow tight">
              <select id="materialTypeFilter" aria-label="資料種別フィルター">
                <option value="">資料種別: すべて</option>
              </select>
              <input id="adminSearch" type="search" placeholder="全文検索" />
            </div>
          </div>
          <div id="adminRefsTable" class="tableWrap large"></div>
        </div>
      </section>
    </section>
  </main>

  <footer class="footer">
    <p>静的GitHub Pages版。処理はブラウザ内で行われます。大量照合時はCiNii・図書館側への負荷を避け、件数を絞って実行してください。</p>
  </footer>
</body>
</html>
