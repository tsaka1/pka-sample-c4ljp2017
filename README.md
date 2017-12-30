# pka-sample-c4ljp2017

This is a tiny sample of public-key authentication enabled web application
presented at the Code4Lib JAPAN Conference 2017 on 3rd September 2017.
(http://wiki.code4lib.jp/wiki/C4ljp2017)

The slide show presented at Code4Lib JAPAN Confenrece 2017 is
https://www.slideshare.net/TetsuoSakaguchi/web-79381367
(in Japanese).

Following descriptions are written in *Japanese*.

# 公開鍵認証を用いた Web アプリケーションのサンプルコード

*by Tetsuo Sakaguchi (阪口哲男), twitter @tsaka1*

## 背景/概要

2017年9月3日に「Code4Lib JAPAN Conference 2017」で発表した
HTML5 標準準拠な Web ブラウザで使用可能な公開鍵認証機能を
実装してみたサンプルコードです。
(Title: Webシステムのためのエンドユーザ向け公開鍵認証機能の開発)

もう少し詳しい説明を付け、コードももうちょっと整えようと思っている内に
2017年が終りそうになったので、不親切を承知で9月3日時点でのコードを公開します
(なので、commit の日付を 2017年9月にしている次第です)。
若い人はこういうコードの書き方を反面教師だと思ってください:-)

コードは「とりあえず公開鍵認証が機能する」ことを確認し、
パスワード認証との対比がある程度可能な形で書くことを目標と
しました。
そのため、セッション管理やユーザ登録過程等については十分な
セキュリティ的検証は行っていません。
また、関係する要素が少ない方が良いと考え、アプリケーションフレームワーク
を使わずに、CGI を用いています。
また、ブラウザに機能が十分備わっているかのチェックコードも入っていません。

ですので、もしこれを読んで自サービスに公開鍵認証を採り入れようと言う場合は、
このサンプルコードをそのまま使わないでください。
そのまま使用して何か不具合が生じても一切の責任は持てませんので、御了承
ください。

このサンプル自体を実用的なライブラリに再構成するなどを私自身が
実行するのは難しいと思うので、我こそはと思う方は

## サンプルでの公開鍵認証の仕組み(概要)

スライド https://www.slideshare.net/TetsuoSakaguchi/web-79381367
にも記載していますが、HTML5 の localStorage 機能によって、Webブラウザ
に鍵ペア(公開鍵と秘密鍵)を覚えさせています。そのため same-origin rule原則
の範囲でアクセス可能になるため、秘密鍵はパスフレーズでAES暗号化を
施しています。(この辺は他の公開鍵認証でもパスフレーズを付けるのが標準なので、
特殊ではないと思います。)

鍵ペアの内の公開鍵をサーバに預けます。認証が必要な場合にはサーバから
適当に生成した文字列をブラウザに送り、それにブラウザの秘密鍵で署名し、
その署名をサーバに送って公開鍵で検証成功すれば認証成功とみなしています。

一応、鍵ペアの export 機能も準備しています。

## サンプルの機能とファイル構成について

このサンプルはユーザがサインインすると、単に fortune の出力メッセージを
読むことができるというだけの、実用的な意味が皆無なものとなっています。
サインインした時のページは home.cgi で生成しています。

比較対象のためにパスワード認証にもできるようになっています。
その切替えや一部の設定は config.rb を修正すればできるようになっています。

ユーザの公開鍵等は sqlite3 を用いて RDBで管理しています。あと簡単な
ログも残します。それらのファイルは CGI スクリプトがおかれているディレクトリの
下にサブディレクトリ「data」を設けるようになっていますが、それも config.rb
で設定しています。

その他にいくつもファイルがありますが、概ね以下のように命名しています。

* signin-* - サインイン処理
* signup-* - サインアップ処理
* keychg-* - 公開鍵変更(またはパスワード変更)処理
* *-pka* - 上記の処理を公開鍵認証で行う
* *-pwd* - 上記の処理をパスワード認証で行う
* signout.cgi - サインアウト処理
* schema.sql - SQLite3 データベース用スキーマ定義ファイル(事前に要作成)

## 実行要件

* プログラミング言語: Ruby 2.3
    * 必要ライブラリ: sqlite3 (gem)
* RDBMS: SQLite3
* Webサーバ: Apache httpd 2.4 等CGIが利用可能なもの
* Webブラウザ: HTML5 のlocalStorageが利用可能なこと(含JavaScript)
* JavaScript用公開鍵暗号ライブラリ: jsrsasign (jsrsasign-all-min.js)
    * URL https://kjur.github.io/jsrsasign/
* /usr/games/fortune: home.cgi で使用、別に date コマンドでも構わない

## サンプルの試行環境について

https://sakura.sakalab.org/~saka/pka4/home.cgi

サインアップの際のキーワードは開発者の姓(ヘボン式)です。
上にも書いたようにかなりいい加減なので、問題が出ればクローズします。

