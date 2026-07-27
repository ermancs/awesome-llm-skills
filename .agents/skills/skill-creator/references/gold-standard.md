# Gold Standard (Altın Standart) Skill Yapısı

> **Version:** 2.0.0 | **Author:** Hermes Agent
>
> Bu belge, skill-creator'ın ürettiği her skill için zorunlu olan altın standart
> klasör yapısını ve tasarım ilkelerini tanımlar. SKILL.md'de bu belgeye atıf
> yapılır; detaylar burada tutulur (progressive disclosure).

---

## 📁 Klasör Ağacı

```
skills/
└── my-skill-name/
    ├── SKILL.md                 # ZORUNLU — Ajanın okuduğu ana dosya
    ├── manifest.json            # ZORUNLU — Metadata ve kayıt dosyası
    ├── README.md                # İnsan geliştiriciler için dokümantasyon
    ├── LICENSE                  # Kullanım lisansı (default: MIT)
    ├── CHANGELOG.md             # Sürüm geçmişi (Keep a Changelog formatı)
    │
    ├── instructions/            # Prompt ve davranış tanımları
    │   ├── system.md            # Sistem prompt'u (rol, yetenekler, araçlar)
    │   ├── constraints.md       # Kısıtlamalar (yapılmayacaklar, sınırlar)
    │   └── style.md             # Çıktı stili (dil, ton, format)
    │
    ├── tools/                   # Araç tanımları (function schemas)
    │   ├── tool_1.json          # Her tool için JSON Schema
    │   ├── tool_2.json
    │   └── schemas.py           # Python'da tool tanımları (opsiyonel)
    │
    ├── examples/                # Few-shot örnekler
    │   ├── basic/               # Temel kullanım örnekleri
    │   │   └── example_01.md
    │   ├── edge_cases/          # Sınır vakaları
    │   │   └── missing_data.md
    │   └── conversational/      # Konuşma akışı örnekleri
    │       └── example_01.md
    │
    ├── tests/                   # Test paketi (üç katmanlı)
    │   ├── unit/                # Tool'ları izole test
    │   │   └── test_*.py
    │   ├── integration/         # SKILL.md → araçlar akışı
    │   │   └── test_full_flow.py
    │   ├── eval/                # Model + skill birlikte değerlendirme
    │   │   └── evals.json
    │   └── fixtures/            # Test verileri
    │       └── sample.csv
    │
    ├── config/                  # Konfigürasyon
    │   ├── default.yaml         # Varsayılan çalışma parametreleri
    │   ├── production.yaml      # Prodüksiyon override'ları
    │   └── schema.json          # Konfigürasyon şeması
    │
    ├── src/                     # Çalıştırılabilir kod
    │   ├── main.py              # Ana giriş noktası
    │   ├── utils.py             # Yardımcı fonksiyonlar
    │   └── handlers/            # İşleyiciler (opsiyonel)
    │       └── __init__.py
    │
    ├── data/                    # Statik veri veya kaynaklar
    │   ├── templates/           # Çıktı şablonları
    │   │   └── output.md
    │   ├── knowledge/           # Domain bilgisi (reference docs)
    │   │   └── reference.md
    │   └── seeds/               # Başlangıç verileri
    │       └── seed.json
    │
    ├── scripts/                 # Yardımcı scriptler
    │   ├── run.py               # Deterministik ana script
    │   ├── validate.py          # Skill doğrulama
    │   └── benchmark.py         # Benchmark koşucusu
    │
    └── errors/                  # Hata kataloğu
        └── error_codes.json     # Tüm hata kodları ve fallback'ler
```

---

## 📄 Kritik Dosya İçerikleri

### 1. SKILL.md — Ajanın Beyni

```yaml
---
name: my-skill-name
version: 1.0.0
description: >
  Tek cümlede ne yaptığı. Use when ... ile başla.
  Tetikleyici ifadeleri, bağlamları, dosya türlerini belirt.
triggers:
  - "tetikleyici ifade 1"
  - "tetikleyici ifade 2"
---

# Amaç
Kullanıcıya ne kazandırdığı.

# Ne Zaman Kullanılır
- Tetikleyici durumlar
- İlgili fiiller/ifadeler

# Ne Zaman Kullanılmaz
- Kapsam dışı durumlar (→ alternatif skill)

# Araçlar
1. `tool_name(params)` — açıklama

# Davranış Kuralları
- Kural 1
- Kural 2

# Hata Yönetimi
Hata durumunda `errors/error_codes.json`'a bak.
```

### 2. manifest.json — Kayıt ve Metadata

```json
{
  "id": "my-skill-name",
  "name": "My Skill Name",
  "version": "1.0.0",
  "author": "Hermes Agent",
  "license": "MIT",
  "runtime": {
    "min_model_tier": "sonnet-class",
    "context_window_required": 32000,
    "languages": ["tr", "en"]
  },
  "entry_point": "src/main.py",
  "tools": [
    {"name": "tool_name", "schema": "tools/tool_name.json"}
  ],
  "dependencies": {
    "python": ">=3.11",
    "packages": []
  },
  "evals": {
    "pass_rate": null,
    "last_run": null
  },
  "tags": ["tag1", "tag2"],
  "security": {
    "allow_network": false,
    "allow_file_write": true,
    "blocked_paths": ["/etc", "/sys", "~/.ssh"],
    "max_cost_per_call": 5.0
  }
}
```

### 3. tools/*.json — Function Calling Şemaları

```json
{
  "name": "tool_name",
  "description": "Tool açıklaması",
  "parameters": {
    "type": "object",
    "properties": {
      "param1": {
        "type": "string",
        "description": "Parametre açıklaması"
      }
    },
    "required": ["param1"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "result": {"type": "string"}
    }
  },
  "errors": ["ERROR_CODE_1", "ERROR_CODE_2"]
}
```

### 4. config/default.yaml — Çalışma Parametreleri

```yaml
skill:
  name: my-skill-name
  max_iterations: 5
  timeout_seconds: 30

sampling:
  default_size: 1000
  max_size: 100000

output:
  max_recommendations: 5
  language: tr
  format: markdown

safety:
  allow_network: false
  allow_file_write: true
  blocked_paths: ["/etc", "/sys", "~/.ssh"]
  max_cost_per_call: 5.0
```

### 5. errors/error_codes.json — Hata Sözlüğü

```json
{
  "ERROR_CODE": {
    "user_message": "Kullanıcıya gösterilecek mesaj: {param}",
    "retry": false,
    "fallback_action": "ask_user_for_input",
    "severity": "error"
  }
}
```

---

## 🎯 Tasarım İlkeleri (7 Altın Kural)

### 1. Bağımsızlık (Composability)
Skill tek başına çalışabilmeli, başka skill'lere bağımlı olmamalı.
Bağımlılık varsa `manifest.json`'da açıkça belirtilmeli.

### 2. Gözlemlenebilirlik (Observability)
Her çağrı loglanmalı: `skill_name`, `tool_name`, `latency_ms`, `tokens`, `result_hash`.
Bu, `evals/pass_rate`'i hesaplamak için şart.

### 3. Sürümleme (Semver)
- **MAJOR**: Şema kırılması, prompt yapısı değişikliği
- **MINOR**: Yeni araç, geriye dönük uyumlu
- **PATCH**: Bug fix, dokümantasyon

### 4. Yüksek Sinyal / Düşük Gürültü
SKILL.md en fazla 300-500 kelime. Ajanlar uzun prompt'larda "talimat kaybı" yaşar.
Detaylar `instructions/` altında tutulur, gerektiğinde dinamik yüklenir.

### 5. Test Edilebilirlik
Bir skill `pytest tests/` komutuyla tüm testlerden geçebilmeli.
CI/CD entegrasyonu için kritik.

### 6. Güvenlik Sınırları
`config/` içinde `blocked_paths`, `allow_network`, `max_cost_per_call` gibi
sınırlar açıkça tanımlanmalı.

### 7. Dil Bağımsızlığı
SKILL.md çok dilli olabilir; ajan `manifest.json`'daki `languages` alanına
göre uygun dili yükler.

---

## 🔁 Skill Yaşam Döngüsü

```
1. TASARIM      → SKILL.md taslağı + manifest.json
2. PROTOTİP     → src/ + tools/ (en az 1 tool)
3. ÖRNEKLER     → examples/ (basic + edge_cases)
4. TEST         → tests/ (unit → integration → eval)
5. EVAL         → LLM-as-judge ile pass_rate ölçümü
6. DOKÜMANTASYON → README.md (insanlar için)
7. VERSİYONLAMA → git tag + CHANGELOG.md
8. YAYIN        → registry'ye push
9. İZLEME       → production telemetry + haftalık eval
10. İTERASYON   → kullanım verisine göre prompt/tools iyileştirme
```

---

## ⚡ 10 Soruluk Altın Standart Kontrol Listesi

| # | Soru | Kontrol Noktası |
|---|------|-----------------|
| 1 | SKILL.md 2 dakikada anlaşılıyor mu? | `instructions/system.md` net mi? |
| 2 | manifest.json var mı? | ZORUNLU — yükleme için şart |
| 3 | Tüm tool'lar JSON schema ile tanımlı mı? | `tools/*.json` |
| 4 | En az 3 örnek var mı? | basic + edge_cases + conversational |
| 5 | pytest ile tüm testler geçiyor mu? | `pytest tests/` |
| 6 | pass_rate > %90 mı? (son 30 gün) | `manifest.json → evals.pass_rate` |
| 7 | Hata durumları için fallback tanımlı mı? | `errors/error_codes.json` |
| 8 | Güvenlik sınırları config'de belirtilmiş mi? | `config/default.yaml → safety` |
| 9 | Sürüm numarası Semver'e uyuyor mu? | `manifest.json → version` |
| 10 | README 5 dakikada öğretiyor mu? | `README.md` |

---

## 🔄 Eski 7-Pillar → Altın Standart Dönüşüm

| Eski (v1.x) | Yeni (v2.0 Gold) | Not |
|-------------|-----------------|-----|
| SKILL.md | SKILL.md | Format güncellendi, manifest.json eklendi |
| — | manifest.json | **YENİ — ZORUNLU** |
| — | README.md | **YENİ** |
| — | LICENSE | **YENİ** |
| CHANGELOG.md | CHANGELOG.md | Aynı |
| — | instructions/ | **YENİ** — system.md, constraints.md, style.md |
| — | tools/ | **YENİ** — JSON function schemas |
| — | examples/ | **YENİ** — few-shot kütüphanesi |
| evals/ | tests/eval/ | Taşındı |
| — | tests/unit/, integration/, fixtures/ | **YENİ** |
| — | config/ | **YENİ** — default.yaml, schema.json |
| scripts/run.py | src/main.py + scripts/run.py | Ayrıştırıldı |
| references/ | data/knowledge/ | Taşındı |
| assets/templates/ | data/templates/ | Taşındı |
| — | errors/ | **YENİ** — error_codes.json |