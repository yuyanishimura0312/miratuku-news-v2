# 妖怪データベース拡張リサーチ

## 現状分析（2026-04-29）

### データベース概要
- **総数**: 1,010体 / 195文化
- **全フィールド充填率**: 100%（scholarly_summary, cultural_notes, personality_deep, composition, supernatural_abilities, data_sources, encounter_scenarios, related_yokai）
- **ソース**: yokai-sns（yokai-data.json）→ miratuku-news-v2に移設済み

### 地域分布
| 地域 | 件数 | 比率 |
|------|------|------|
| その他・普遍 | 392 | 38.8% |
| 東アジア | 117 | 11.6% |
| ヨーロッパ | 113 | 11.2% |
| 日本 | 83 | 8.2% |
| アフリカ | 77 | 7.6% |
| 南北アメリカ | 70 | 6.9% |
| 南アジア | 53 | 5.2% |
| 中東 | 45 | 4.5% |
| 東南アジア | 39 | 3.9% |
| オセアニア | 21 | 2.1% |

### Descola分類分布
| 分類 | 件数 | 比率 |
|------|------|------|
| アニミズム | 653 | 64.7% |
| アナロジズム | 334 | 33.1% |
| ナチュラリズム | 10 | 1.0% |
| ハイブリッド | 9 | 0.9% |
| トーテミズム | 4 | 0.4% |

### 主要文化圏（上位15）
Japanese (335), Chinese (62), Universal (42), Hindu (40), 日本 (37), Korean (26), Ancient Egyptian (20), Norse (20), Yoruba (17), Celtic (16), Slavic (16), Greek (16), Arabic (15), Ancient Mesopotamian (15), Germanic (11)

---

## Part 1: 地域別拡張候補リスト

### 1.1 オセアニア（現21体 → 目標50+体）

**ポリネシア伝統**（マオリ・サモア・ハワイ・トンガ・タヒチ）

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Taniwha（タニーファ） | マオリ | 水域制御・形態変換 | 水源保護 | animism |
| Patupaiarehe | マオリ | 透明化・歌による誘引 | 森林の妖精 | animism |
| Aitu（アイツ） | サモア | 夢での通信・憑依 | 祖先ガイド/懲罰 | animism |
| Menehune（メネフネ） | ハワイ | 透明化・瞬間移動 | 古代構造物建設者 | totemism |
| Tipua | マオリ | 変身・自然操作 | 自然の変身する精霊 | animism |
| Moʻo（モオ） | ハワイ | 水域支配・形態変換 | 水の守護竜 | animism |
| Tūrehu | マオリ | 歌・音楽の魔力 | 霧の民 | animism |

**メラネシア伝統**（パプアニューギニア・ソロモン諸島・バヌアツ・フィジー）

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Adaro（アダロ） | ソロモン諸島 | 虹を橋とする・雨の制御 | 日光精霊・季節制御 | animism |
| Masalai（マサライ） | パプアニューギニア | 善悪の切替 | 森林保全の報酬・罰 | animism |
| Bariaus（バリアウス） | パプアニューギニア | 憑依 | 禁忌教育 | totemism |
| Dakuwaqa | フィジー | 海洋制御 | 鮫の神 | animism |
| Vui（ヴイ） | バヌアツ | 自然操作 | 精霊 | animism |

**ミクロネシア伝統**（パラオ・マーシャル諸島・カロリン諸島）

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Ani（アニ） | カロリン諸島 | 保護・治癒・漁獲支援 | 祖先精霊 | animism |
| Olifat（オリファット） | マーシャル諸島 | 造形力・変身 | 文化英雄/悪戯者 | animism |

**オーストラリア先住民ドリームタイム伝統**（トーテミズムの主要ソース）

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Rainbow Serpent（虹蛇） | 汎オーストラリア | 水資源制御・地形形成 | 創造者精霊・水源管理 | **totemism** |
| Wandjina（ワンジナ） | アーネムランド | 洪水制御・雲/雨操作 | 雲・雨精霊 | **totemism** |
| Bunyip（バンイップ） | 汎オーストラリア | 水辺支配 | 水辺の怪物 | animism |
| Yowie（ヨウイ） | 汎オーストラリア | 隠蔽・巨大力 | 巨人/野人 | animism |
| Min Min Lights | 汎オーストラリア | 光操作・誘引 | 不可思議な光 | animism |
| ドリームタイム祖先群 | 各部族 | 動物↔人間変換 | 種族的食料・領域管理 | **totemism** |

### 1.2 東南アジア（現39体 → 目標80+体）

**タイ伝統**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Phaya Naga（ファヤナガ） | メコン川流域 | 水源管理・宝物保護 | 河川精神支配 | animism |
| Phi Tai Hong（ピータイホン） | タイ全域 | 憑依・疾病 | 突然死・悲劇死の霊 | animism |
| Phi Am（ピーアム） | タイ全域 | 睡眠麻痺誘発 | 睡眠規律の精霊 | animism |
| Nang Ta-khian | タイ | 木の保護・成長 | 樹木精霊 | animism/totemism |
| Nang Tani | タイ | 人間関係操作 | バナナの木の精霊 | animism |

**ベトナム伝統**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Thần Trùng（タンチュン） | ベトナム | 新死者への拷問 | 墓地精霊 | animism |
| Ma Da（マーダー） | ベトナム | 人間略奪 | 溺水警告の水死霊 | animism |
| Cô Hồn（コーホン） | ベトナム | 財産盗難 | 飢餓的放浪霊 | animism |
| Hồ Tinh（ホーティン） | ベトナム | 変身・誘惑 | 道徳テスターの狐精霊 | animism |

**フィリピン伝統**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Aswang（アスワング） | フィリピン全域 | 変身・夜行捕食 | 社会的脅威の象徴 | animism |
| Manananggal | フィリピン | 胴体分離・飛行 | 妊婦保護警告 | animism |
| Diwata | フィリピン | 自然操作・祝福 | 自然の精霊 | animism |
| Kapre | フィリピン | 幻惑・巨大力 | 巨大な木の精 | animism |
| Tikbalang | フィリピン | 迷路化・幻覚 | 馬頭の怪物 | animism |
| Sigbin（シグビン） | フィリピン | 影を通じた血液吸収 | 児童保護警告 | animism |
| Tiyanak（ティヤナク） | フィリピン | 泣き声で誘引 | 遺棄児童の象徴 | animism |

**マレーシア・インドネシア伝統**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Pontianak/Kuntilanak | マレー/インドネシア | 内臓捕食 | 周産期致死率警告 | animism |
| Pocong（ポチョン） | インドネシア | 跳躍移動 | 埋葬儀式の重要性 | animism |
| Penanggalan | マレー | 頭部・内臓分離 | 夜間外出警告 | animism |
| Toyol（トヨル） | マレー | 窃盗・詐欺 | 所有物保護警告 | animism |
| Orang Bunian | マレー | 不可視・長寿 | 自然領域の真の所有者 | **totemism** |
| Hyang（ヒャン） | ジャワ・バリ | 全能的超自然力 | 存在論的基盤 | analogism |
| Leyak | バリ | 変身 | 悪霊 | animism |
| Jenglot | ジャワ | 血液吸収 | ミイラ状の存在 | animism |
| Nyi Roro Kidul | ジャワ | 海洋支配・誘引 | 南海の女王 | analogism |
| Genderuwa | インドネシア | 人間領域侵入 | 森林・居住地境界標示 | animism |

**ミャンマー・カンボジア・ラオス伝統**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| 37 Nats | ミャンマー | 保護・害 | 社会秩序維持 | animism |
| Thagyamin | ミャンマー | 管理・仏教統合 | 37ナッツの首位 | animism |
| Neak Ta（ネアクタ） | カンボジア | 地域監視・加護 | 祖先的守護精霊 | **totemism** |
| Mrenh Kongveal | カンボジア | 狩猟成功仲介 | 象を狩る精霊 | **totemism** |
| Krasue（クラスエ） | カンボジア/タイ | 浮遊・臓器ぶら下げ | 夜間外出警告 | animism |
| Naga/Nak | ラオス | 雨・農業・精神制御 | メコン川の蛇 | animism |
| Seua Saming | ラオス | 虎への変身 | 大型捕食者警告 | animism |
| Phi Kong Koi | ラオス | 人間追跡不可能 | 家族・敬老警告 | animism |

### 1.3 アフリカ（現77体 → 目標120+体）

**中央アフリカ**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Jengu/Miengu | カメルーン・サワ | 疾病治癒・幸運獲得 | 水精霊・健康バランサー | animism |
| Simbi（シムビ） | バコンゴ | ガイダンス・肥沃度保護 | 河川精霊 | animism |
| Amazimu（アマジム） | 中央アフリカ | 形態変換・人間食 | 危険な自然力象徴 | animism |
| Mokele-mbembe | コンゴ盆地 | 水棲支配 | 水棲生物 | animism |

**南部アフリカ**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Amadlozi（アマドロジ） | ズールー・コーサ・ソト | アドバイス・保護 | 祖先精霊・社会秩序維持 | **totemism** |
| Tokoloshe（トコロシェ） | ズールー | 魔法・いたずら | 道徳的教訓精霊 | animism |
| Impundulu（インプンドゥル） | ズールー/コーサ | 嵐召喚・血液吸収 | 雷鳥・気象制御 | animism |
| Inkanyamba | ズールー | 竜巻・洪水制御 | 大蛇・水文支配 | animism |
| Mamlambo（マムランボ） | ズールー | 溺死による捕食 | 水中危険警告 | animism |
| /Kaggen | サン族 | トリックスター・変身 | カマキリの文化英雄 | **totemism** |

**東アフリカ**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Shetani（シェターニ） | 東アフリカ | 多形態変換 | 脅威・警告象徴 | animism |
| Popobawa（ポポバワ） | ザンジバル | コウモリ翼・硫黄臭 | 社会的逸脱警告 | animism |
| Ayana（アヤナ） | マチャ・オロモ | 神聖と人間の通信 | 宗教実践の中核 | animism |

**西アフリカ補強**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Aziza（アジザ） | フォン・エウェ | 良い魔法・知識提供 | 狩猟成功媒介 | **totemism** |
| Ogbanje（オグバンジェ） | イグボ | 子供に偽装・再投生 | 家族への苦しみ | animism |
| Alusi（アルシ） | イグボ | 領域管轄 | 下級神・領域秩序維持 | **totemism** |
| Mami Wata | 汎アフリカ | 富・幸運・危険 | 河川・海洋精霊 | animism |
| Adze（アッゼ） | エウェ | 蛍に変身・吸血 | 吸血妖怪 | animism |
| Ninki Nanka | ガンビア | 水域支配 | 龍蛇 | animism |

### 1.4 南北アメリカ（現70体 → 目標110+体）

**アマゾン先住民**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Curupira（クルピラ） | トゥピ・グアラニ | 森林操作・迷路化 | 森の守護者 | **totemism** |
| Xapiripë | ヤノマミ | 幻視媒介 | 微小精霊・シャーマン補助 | animism |
| Mapinguari | アマゾン | 巨大力・悪臭 | 巨大な獣 | animism |
| Dolphin Spirits | アマゾン | 夜間人間変身 | 河川危険警告 | animism |
| Anaconda Spirits | アマゾン | 水位・河川制御 | 水文系支配 | animism |

**アンデス先住民**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Pachamama | ケチュア・アイマラ | 肥沃性・生命の源 | 大地母 | animism |
| Apus（アプス） | ケチュア | 知恵・天候制御 | 聖山精霊 | animism |
| Supay（スパイ） | アンデス | 生死の閾値操作 | 冥界の仲介者 | analogism |
| Pishtaco/Kharisiri | アンデス | 脂肪吸収 | 植民地支配への文化的応答 | animism |
| Wayra Tata | アンデス | 気象支配 | 風の父 | animism |

**北極/イヌイット**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Sedna/Nuliayuk | イヌイット | 海獣制御 | 海の女神・狩猟資源媒介 | animism |
| Tupilaq（トゥピラック） | グリーンランド | 呪詛攻撃 | 魔術的復讐媒介 | animism |
| Ijiraat（イジラート） | イヌイット | 北極動物への変身 | 自然形態の守護 | **totemism** |
| Qalupalik | イヌイット | 水中誘引 | 子供保護警告 | animism |
| Mahaha | イヌイット | くすぐり殺害 | 野外危険警告 | animism |

**プレーンズ/北西海岸**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Thunderbird | 平原諸族 | 嵐支配・戦闘 | 気象・秩序制御 | animism |
| Wakan Tanka | ラコタ | 万物内在 | 存在論的基盤 | analogism |
| Bear Doctor | ラコタ | 熊精霊の治癒力 | 治癒仲介 | **totemism** |
| Skinwalker | ナバホ | 動物変身 | 変身者 | animism |
| Dzunukwa | クワキウトル | 巨大力・子供捕食 | 野生の女巨人 | animism |

**メソアメリカ補強**

| 名前 | 文化圏 | 能力 | 文化的役割 | Descola分類 |
|------|--------|------|-----------|-------------|
| Alux（アルクス） | マヤ | 透明化・物理的接触 | 自然保全警告 | animism |
| Nahual（ナワル） | アステカ | 動物変身 | 社会的力の仲介 | animism |
| Chaneques | メソアメリカ | 自然管理・嘘 | 自然秩序の矛盾面 | animism |

---

## Part 2: 構造的拡張フレームワーク

### 2.1 学術分類フレームワーク（Descolaを超えて）

Descolaの4つのオントロジー（内部性と物理性の類似/相違の組み合わせ）は基本構造として優れているが、以下の拡張が必要である。

**Viveiros de Castroの多自然主義（multinaturalism）**: 「統一的な魂と複数性のある身体」という逆説的構造。各存在が異なる視点から世界を知覚する。アマゾン先住民の存在論に特に有用。単一の文化的解釈ではなく、複数の認識論的立場が同時に妥当であることを認める。

**Tim Ingoldの「住居のオントロジー」**: 存在と環境を分離不可能な関係の場として理解する。妖怪が単なる「存在」ではなく、特定の場所・季節・感覚的環境との関係を通じてのみ理解可能であることを示す。

**Eduardo Kohnの「フォレストシンク」**: 人間以外の存在がそれ自体の意味世界を持つことを示唆。妖怪の「Umwelt」（感覚世界）を科学的に記述することの理論的根拠を提供。

**Briggsの3層分類**: 群生型（trooping）、独居型（solitary）、取り込み型（domesticated）。日本の妖怪にも直接応用可能（ナマハゲ=群生型、橋の下の妖怪=独居型、座敷わらし=取り込み型）。

### 2.2 学術データベース・リソース

| リソース | 内容 | 連携方法 |
|----------|------|----------|
| Stith Thompson Motif-Index | 6巻・19大カテゴリの民間文学モチーフ | motif_id フィールドで紐付け |
| ATU Tale Type Index | 1000+ tale type | atu_type フィールドで紐付け |
| eHRAF World Cultures | 360+文化の超文化的比較 | culture_code フィールドで紐付け |
| Murdock Ethnographic Atlas | 1,291社会 | murdock_id フィールドで紐付け |
| D-PLACE | 1,400+社会の地理・言語・文化・環境データ | dplace_id フィールドで紐付け |
| 怪異・妖怪伝承DB（国際日文研） | 日本の妖怪学術DB | nichibun_id フィールドで紐付け |
| Wikidata | 構造化データ | wikidata_qid フィールドで紐付け |

### 2.3 Umwelt/感覚生態学の拡張

現在のdata_sourcesに追加すべき科学的パラメーター:

| データソース | 説明 | 関連する妖怪タイプ |
|-------------|------|-------------------|
| geomagnetic | 地磁気異常 | 古墳周辺・地質活発地域の妖怪 |
| infrared | 赤外線・熱感知 | 熱感知能力を持つ存在 |
| infrasound | 超低周波音（20Hz以下） | 幽霊屋敷・不安誘発の存在 |
| bioluminescence | 生物発光・化学発光 | 鬼火・will-o'-the-wisp |
| chemical_ecology | フェロモン・毒素・揮発性有機化合物 | 温泉地の妖怪・薬用植物関連 |
| electromagnetic | 電磁波 | 現代的都市妖怪 |
| dream_consciousness | 夢・意識状態 | シャーマニズム関連 |

infrasoundは科学的に不安感・恐怖感・視覚的幻覚を誘発することが確認されており、多くの「幽霊屋敷」報告は老朽化した配管や換気システムの超低周波音で説明可能。bioluminescenceは鬼火（リン化水素やメタンの酸化）やPanellus stipticus等の発光菌類と関連。

### 2.4 関係性タイプの構造化

現在のrelated_yokaiはIDリストのみ。以下の型付き関係を追加:

| 関係タイプ | 説明 | 例 |
|-----------|------|-----|
| antagonist | 対立関係 | 河童 vs 猿 |
| symbiotic | 共生関係 | バク（悪夢を食べ、人間は安眠を得る） |
| transformation | 変身関係 | 猫 → 化け猫 |
| regional_variant | 地域変異体 | Penanggalan（マレー）≈ Manananggal（フィリピン） |
| cultural_equivalent | 異文化間の対応 | オーストロネシア言族内の共通構造 |
| hierarchy | 上下関係（眷属） | — |
| kinship | 親族関係 | — |
| ritual_associate | 同じ儀式に関連 | アカマタ・クロマタと他の来訪神 |

### 2.5 新規フィールド候補

| フィールド名 | 説明 | 学術的価値 |
|-------------|------|-----------|
| unesco_ich_link | UNESCO無形文化遺産との関連 | 伝承の危機状況追跡 |
| language_family | 名前の属する言語族 | 交差文化的パターン発見 |
| fossil_evidence | 考古学的証拠へのリンク | 伝説の物質的基盤 |
| ecological_context | 生態系特性（植生、地質等） | TEK（伝統的生態知識）としての解析 |
| source_precision | 出版年・記録者・記録方法・信頼度 | 時代的変化の追跡 |
| motif_index_id | Thompson Motif-Index番号 | 国際比較 |
| atu_type_id | ATU物語類型番号 | 構造的同等性特定 |
| wikidata_qid | Wikidata識別子 | Linked Data相互運用 |
| morphological_ops | 形態学的変換（垂直拡大/水平混成/位置的転移等） | 文化的変容の体系的追跡 |

### 2.6 ナレッジグラフ化（長期目標）

将来的には、OWL/RDFベースのナレッジグラフへの移行が推奨される:
- 「妖怪」クラスのサブクラス（来訪神、死霊、物怪等）の形式的定義
- Wikidata/DBpediaとのマッピングによる相互運用性
- SPARQLクエリ対応（「秋に出現し、水域に関連し、悪意のない妖怪はどれか」等）

---

## 拡張実行計画

### Phase 1（即時）: 分類バランス改善
- オーストラリア先住民ドリームタイム系 20体追加（totemism主体）
- 北米先住民トーテム系 10体追加
- アフリカ・東南アジアのtotemism候補 10体追加
- **目標**: totemismを0.4% → 4%に引き上げ

### Phase 2: 地域カバレッジ改善
- 東南アジア 40体追加（タイ・フィリピン・インドネシア・ベトナム中心）
- アフリカ 40体追加（中央・南部・東アフリカ中心）
- **目標**: 全地域で最低5%カバレッジ

### Phase 3: アメリカ・構造拡張
- 南北アメリカ 40体追加（アマゾン・アンデス・イヌイット中心）
- 関係性タイプ（relationship_type）フィールド追加
- 形態学的変換タグ追加

### Phase 4: 学術DB連携
- Motif-Index/ATU/Wikidata IDの付与
- Umwelt拡張（infrasound, geomagnetic, bioluminescence等）
- UNESCO ICHリンク

---

## 参考文献

### 学術分類フレームワーク
- Descola, P. (2013). *Beyond Nature and Culture*. University of Chicago Press.
- Viveiros de Castro, E. (1998). Cosmological Deixis and Amerindian Perspectivism. *JRAI*.
- Ingold, T. (2000). *The Perception of the Environment*. Routledge.
- Kohn, E. (2013). *How Forests Think*. University of California Press.
- Pedersen, M.A. (2001). Totemism, Animism and North Asian Indigenous Ontologies. *JRAI*.

### フォークロア分類
- Thompson, S. (1955-58). *Motif-Index of Folk-Literature*. Indiana University Press.
- Uther, H.J. (2004). *The Types of International Folktales (ATU)*. Academia Scientiarum Fennica.
- Briggs, K. (1976). *A Dictionary of Fairies*. Penguin.
- Foster, M.D. (2009). *Pandemonium and Parade*. University of California Press.

### エスノグラフィック比較
- eHRAF World Cultures. Yale University. https://ehrafworldcultures.yale.edu/
- D-PLACE Database. https://d-place.org/
- 怪異・妖怪伝承データベース. 国際日本文化研究センター. https://www.nichibun.ac.jp/YoukaiDB/

### 地域別民族誌
- Warner, L. (1939). *A Black Civilisation*. Harper.
- Elkin, A.P. (1938). *The Australian Aborigines*. Angus & Robertson.
- Allerton, C. (2016). Spiritual Landscapes of Southeast Asia. *Anthropological Forum*.
- Canadian Geographic. Shamans, Spirits, and Faith in the Inuit North.

### Umwelt理論
- Uexküll, J. von (1934). *A Foray into the Worlds of Animals and Humans*.
