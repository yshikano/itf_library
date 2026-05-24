# ITF Library BookMap

KdBシラバスの「教材・参考文献・配付資料等」から文献を抽出し、筑波大学附属図書館/CiNii Booksの所蔵状況を確認するための静的Webアプリです。

GitHub Pagesで公開できるよう、アプリ本体は `docs/` 以下のHTML/CSS/JavaScriptだけで動作します。サーバーは不要です。

## 公開URL

GitHub Pagesを有効にすると、通常は次のURLで公開されます。

```text
https://yshikano.github.io/itf_library/
```

## 使い方

### 1. GitHub Pagesを有効化

リポジトリの **Settings → Pages** で、次のどちらかを選んでください。

#### 推奨: GitHub Actionsで公開

1. **Build and deployment → Source** を `GitHub Actions` にする
2. `main` ブランチにpushする
3. `.github/workflows/pages.yml` が `docs/` をGitHub Pagesへデプロイする

#### 代替: docsフォルダから公開

1. **Build and deployment → Source** を `Deploy from a branch` にする
2. Branchを `main`、folderを `/docs` にする

### 2. KdBデータを読み込む

方法は2つあります。

#### ブラウザからアップロード

アプリ左側の「CSV / Excelをアップロード」から、KdBのCSVまたはExcelを読み込みます。

#### 公開サイトに同梱する

KdBから取得したCSVを以下に置いてください。

```text
docs/data/courses.csv
```

このファイルが存在する場合、アプリ起動時に自動で読み込みます。存在しない場合は `docs/data/sample_courses.csv` を読み込みます。

### 3. CiNii Booksで所蔵照合

アプリ左側の「CiNii Books照合」にCiNiiアプリケーションIDを入力し、「未照合の本を照合」を押します。

- 既定の機関IDは筑波大学の `KI000174` です。
- 中央図書館だけに限定する場合は図書館IDに `FA001652` を入力してください。
- API照合結果はブラウザのlocalStorageに保存されます。
- アプリケーションIDはリポジトリには保存しません。

## 3つのモード

### 学生用モード

履修予定科目を検索・選択し、その授業で使う教材・参考文献の所蔵状況を確認できます。

### 教員用モード

書名・著者・ISBNで本を検索し、同じ本を使っている他の授業を確認できます。

### 管理モード

全科目・全文献の一覧を表示し、CSVとして出力できます。文献抽出結果、所蔵照合結果、CiNii/OPACリンクも確認できます。

## KdB CSVで認識する主な列名

完全一致でなくても、近い列名は自動で対応します。

| 内部項目 | 代表的な列名 |
|---|---|
| 年度 | 年度, Academic year, year |
| 科目番号 | 科目番号, Course Number, 科目コード |
| 科目名 | 科目名, Course Name, 授業科目名 |
| 担当教員 | 担当教員, Instructor, 教員 |
| 開設組織 | 組織, 開設組織, 学群, 学位プログラム |
| 開講時期 | 開講時期, Term, 学期, モジュール |
| 曜時限 | 曜時限, 曜日・時限, Weekday and Period |
| 教材・参考文献 | 教材・参考文献・配付資料等, 参考文献, 教材, Course Materials |

## 注意

- このアプリは静的GitHub Pages版です。処理はブラウザ内で実行されます。
- CiNii Booksへの大量問い合わせは避け、上限件数を絞って実行してください。
- ISBNがある文献は比較的安定して照合できますが、ISBNなし文献は「候補」扱いになることがあります。
- 配付資料、manaba資料、Web資料は図書館所蔵照合の対象外として分類します。
