---
marp: true
footer: "by **＠yuya_mizuki**"
paginate: true

---
<style>
@import 'default';
/* Bootstrap */
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css');
@import url('https://fonts.googleapis.com/css2?family=Kosugi&family=Roboto+Mono&display=swap');
</style>
<style>
section {
    font-family: "Arial", "Hiragino Maru Gothic ProN";
    font-size: 30px;
    padding: 40px;
    background-color: lightyellow;
}

section.title h1 {
    color: green;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 96px;
    text-align: center;
}

section.title {
    color: black;
    font-family: "Arial", "Hiragino Maru Gothic ProN";
    font-size: 36px;
    text-align: center;
    padding: 40px;
}

</style>
<!--
class: title
-->

# Docker の<br/>(おそらく)基本的な話
2023/1/5

---
<!--
class: slides
-->
<style>
section.slides h1 {
    color: green;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 36px;
    position: absolute;
    left: 50px; top: 50px;
}

section.slides h2 {
    color: lightseagreen;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 32px;
}

section.slides .target {
    color: darkred;
}

section.slides .strong {
    color: lightseagreen;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 36px;
    text-align: center;
}

section.slides .question{
    color: lightseagreen;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 48px;
    text-align: center;
}
section.slides .notice{
    color: darkred;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 1em; 
}

section.slides .box-knowledge{
    padding: 10px;
    margin-top: 0.5em;
    border: 3px solid #0059b3;
    color: black;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 32px;
    position: relative;
}
section.slides .box-knowledge::before{
    position: absolute;
    top: -0.75em;
    padding: 3px;
    background: lightyellow;
    display: inline-block;      /* インラインボックス定義  */
    box-sizing: border-box;        /* 罫線・余白も含む大きさ  */
    line-height: 1;   
    content: attr(title); 
    color: green;
}
section.slides .badge{
    font-size: 16px;
    position: relative;
    display: inline;
    background-color: skyblue;
    color: black;
}
section.slides .footer {
    position: fixed;
	bottom: 60px;
}
section.slides .memo{
    padding: 10px;
    margin-top: 10px;
    border: 1px solid red;
    color: black;
    font-family: "Arial", "Hiragino Kaku Gothic ProN";
    font-size: 16px;
}
section.slides .memo::before{
    position: absolute;
    top: -0.5em;
    padding: 10px;
    background: lightyellow;
    display: inline-block;      /* インラインボックス定義  */
    box-sizing: border-box;        /* 罫線・余白も含む大きさ  */
    line-height: 1;   
    content: attr(title); 
    color: green;
}
section.slides {
    font-size: 24px;
}
</style>

# 自己紹介

## 名前
水木佑哉 (@yuya-mizuki)

## 今の主なお仕事
大規模案件の開発 with Java/Spring

## 経歴
Public Cloud屋さん → Backend屋さん


![bg right](./img/cat.jpeg)

---

# Dockerの(おそらく)基本的な話

年末年始に、
[Dockerの公式ベストプラクティス集](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)などを読んで、
周辺知識含めてアップデートした。

ベストプラクティスに関連して基本的な知識から細かい話まで諸々話してみる。

<span class=notice>※もう知っているよって人は、「こんな知識・事例もあるで」みたいなことをコメントしてもらえると!!</span>

---
# ベストプラクティスが目指すところ

- イメージサイズの軽量化(push/pullコストを下げる)
    - レイヤを少なくするなど
- ビルドの高速化
    - ビルドコンテキストの最小化・キャッシュの利用・並列ビルドなど
- buildによって非機能を担保しやすい成果物が生成される
    - スケーラビリティなど
- Dockerfile自体が変更しやすい

---
# build contextを使いこなす

<span class="badge">ビルド高速化</span>

<div class="box-knowledge" title="豆知識">
 Dockerfile の配置場所とbuild context はそれぞれ個別に設定できる
</div>
例えば、下記のような構成にして、

```
.
├── contexts
│   ├── context1
│   └── context2
└── dockerfiles
    ├── Dockerfile1
    └── Dockerfile2
```

下記のようなコマンドを実行する
```
docker build -f dockerfiles/Dockerfile1 contexts/context1
```

<div class="footer">
    <div class="memo" title="※build context って何?">
    `docker build .` の `.` の部分を指します。
    作業ディレクトリのことを build context だったり context とか読んだりします(github urlを指定することもできます)
    </div>
</div>

---
# dockerfileをstdinで渡してみる<span class="badge">ビルド高速化</span>

<div class="box-knowledge" title="豆知識">
Dockerfileはファイル定義しなくても、<br/>docker build に stdin経由で渡すことができる
</div>

<br/>

例えば、build-contextすら渡したくない場合は、下記のように実行することができる。
```
`echo -e 'FROM busybox\nRUN echo "hello world"' | docker build -`
```

build-contextは設定したい場合は、`-f-`を使って、下記のように実行することができる。
```
docker build -t myimage:latest -f- . <<EOF
FROM busybox
COPY somefile.txt ./
RUN cat /somefile.txt
EOF
```

---

# docker ignoreを使いこなす<span class="badge">ビルド高速化</span>


<div class="box-knowledge" title="豆知識">
.dockerignore を必要十分にかこう
</div>

`.dockerignore`を build contextのルートに配置しましょう

---

# multi stage build を利用する <span class="badge">イメージ軽量化</span>

コードのコンパイル・トランスパイル用の依存や環境と実行のための依存・環境を分離できない課題の解法


```
# ビルド用
FROM golang:1.17-alpine AS build

RUN apk add --no-cache git
WORKDIR /go/src/project/
COPY go.mod go.sum /go/src/project/
RUN go mod download
COPY . /go/src/project/
RUN go build -o /bin/project

# 実行用
FROM scratch AS executor
COPY --from=build /bin/project /bin/project
ENTRYPOINT ["/bin/project"]
CMD ["--help"]

```

---
# 不要なパッケージのインストール禁止 <span class="badge">イメージ軽量化</span> <span class="badge">ビルド高速化</span>

<div class="box-knowledge" title="豆知識">
<code>apt-get install</code> するときは、下記の利用を考える

- <code>--no-install-recommends</code>オプションの活用
- レイヤーの縮小 (<code>apt-get -y clean</code>, <code>rm -rf /var/lib/apt/lists/*</code>など)

</div>

---
# アプリケーションを切り離す <span class="badge">非機能担保</span>

<div class="box-knowledge" title="豆知識">
1コンテナ1プロセスにしておく

(１コンテナ内で、APIアプリケーションもBFFも起動とかはやらない)
</div>
<div class="notice">※厳密には、親プロセスは１つ</div>
<div class="notice">※wrapperスクリプトで無理やり親プロセスを１つにするのもSIGTERMハンドリング観点でNG</div>

---
# レイヤの数を最小に <span class="badge">イメージ軽量化</span>

<div class="box-knowledge" title="豆知識">

- 実は、レイヤの数には上限がある。現状は125 (<a href="https://github.com/moby/moby/blob/f15d5a0661aed3d77b4f48b4cc6aef9bbbb5d934/layer/layer_store.go#L28">参照</a>)
- 最新版のdockerでは、RUN/COPY/ADD でのみレイヤが作成される

</div>

---
# ビルド・キャッシュの活用 <span class="badge">ビルド高速化</span>

<div class="box-knowledge" title="豆知識" >
build時に使えるキャッシュ色々 (experimentalなものを含む)

- レイヤーキャッシュ
    - Dockerfile を工夫する (<code>COPY . .</code>は最後にするなど)
    - ghaなど dindなCI環境では build時に <code>--cache-from</code>を指定する
- ローカルキャッシュ
    - <code>--mount=type=cache</code>を利用する(基本ローカル向け)
</div>

---
# おまけ: 軽量ベースイメージは slim を使っておくとはまりにくそう
[軽量Dockerイメージに安易にAlpineを使うのはやめたほうがいいという話](https://blog.inductor.me/entry/alpine-not-recommended), 
[base-image-journey-2018](https://speakerdeck.com/stormcat24/base-image-journey-2018) という話もある。

そこで、改めて軽量ベースイメージの系譜を出してみる(参考: ubuntu 26 MB)

- scratch系: docker が規定するemptyイメージであり、始祖のイメージ
- busybox系: from scratch
- alpine系: from busy-box node:18-busybox -> 50 MB程度
    - 標準 C ライブラリがglibcではないのでハマる可能性がある
    - apkだとパッケージの pinning が難しい
- slim: node:18-slim -> 75 MB 程度
- distroless系 [nodejs18-debian11](https://console.cloud.google.com/gcr/images/distroless/GLOBAL/nodejs18-debian11)-> 50 MB程度 若干癖あり

multi-stage buildで ubuntu(build用)+slim(成果物用)とかがイメージの軽さとDockerfileのシンプルさのバランスが良い気がしている

---
# おまけ: nodejs docker image ベストプラクティス
[10 best practices to containerize Node.js web applications with Docker](https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/)
より抜粋

- `FROM node:xx.xx.xx-bullseye-slim` (バージョンPinning + use slim)
- `RUN npm ci --only=production`
- `-e "NODE_ENV=production"` or `ENV NODE_ENV production`
- process実行前に`USER node` (root user を利用しない)
- `CMD ["node", "server.js"]` (sigterm/sighup をハンドリングできるように)
    - x: `CMD "npm" "start"` (npmやyarnはシグナルを飲み込んでしまう)
- `docker run --init` or use tini
    - nodeに限らず起きるPID1問題の対応(ゾンビプロセスなど)
    - NodeをPID1で動かすと、SIGTERMをうまくハンドリングできないので、ラップする

---
# おまけ: CI環境でのmulti-stage buildとキャッシュ利用
結構大変。
現状、buildxを使えるようにしないとあんまりうまくいかない。
そういった意味で、GitHub Actionsとの相性がとても良いというのが現状。

参考:
- [CI での Docker Build のベストプラクティスを考えてみた](https://blog.recruit.co.jp/rls/2020-09-25-docker-build/)
    - CodeBuildでbuildx使う上での、Overheadが減っていれば便利になるはず。(未検証)
- [GitHub ActionsでDocker Buildするときのキャッシュテクニック](https://cockscomb.hatenablog.com/entry/2022/02/16/092538)
- [Rust のアプリで --mount=type=cache + multi-stage build してハマった](https://zenn.dev/ragnar1904/articles/rust-dockerbuildkit-pitfall)
    - cache頑張りすぎると、間違ってしまうこともあるので要注意