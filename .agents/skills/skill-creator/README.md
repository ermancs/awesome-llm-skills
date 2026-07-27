# Skill Creator (Gold Standard)

> **Skill ID:** `skill-creator` | **Version:** 2.0.0 | **Author:** Hermes Agent
>
> Hermes Agent'ta yeni skill'ler oluşturmak, test etmek, benchmark'lamak ve paketlemek için meta-skill.

## Quick Start

1. **Yeni bir skill oluştur:**
   ```bash
   python ~/.hermes/skills/skill-creator/scripts/new_skill.py "skill-adi" -d "açıklama"
   ```
   Bu komut 10 dizinli, 31 dosyalı altın standart yapıyı oluşturur.

2. **[[FILL: ...]] marker'larını doldur** — her dosyadaki placeholder'ları gerçek içerikle değiştir.

3. **Testleri yaz ve çalıştır:**
   ```bash
   pytest tests/
   ```

4. **Skill'i doğrula:**
   ```bash
   python ~/.hermes/skills/skill-creator/scripts/quick_validate.py <skill-dir>
   ```

5. **Paketle:**
   ```bash
   python ~/.hermes/skills/skill-creator/scripts/package_skill.py <skill-dir>
   ```

## What It Does

Skill-creator, bir skill'in tüm yaşam döngüsünü yönetir:

1. **Tasarım** — Kullanıcıyla görüşme, niyet yakalama, SKILL.md + manifest.json yazımı
2. **Scaffold** — `new_skill.py` ile 10 dizinli altın standart yapıyı tek komutta oluşturma
3. **Test** — Subagent'lerle paralel test koşumu, baseline karşılaştırması
4. **Eval** — Assertion grading, benchmark, analiz
5. **İterasyon** — Kullanıcı feedback'i ile skill'i iyileştirme döngüsü
6. **Optimizasyon** — Açıklama (description) optimizasyonu, tetikleme doğruluğu
7. **Paketleme** — `.skill` dosyası olarak dağıtıma hazırlama

## What It Doesn't Do

- Sıfırdan skill fikri üretmez — kullanıcının ne istediğini bilmesi gerekir
- Skill'leri production'da izlemez (monitoring ayrı bir concern)
- CI/CD pipeline'ı kurmaz

## Dependencies

- Python >= 3.11
- PyYAML >= 6.0
- Hermes Agent (subagent desteği için)

## Configuration

Bkz. `config/default.yaml` ve `config/schema.json`.

## Testing

```bash
pytest tests/
```

## Directory Structure

```
skill-creator/
├── SKILL.md              # Ana ajan dosyası
├── manifest.json         # Metadata ve registry
├── README.md             # Bu dosya
├── LICENSE               # MIT
├── CHANGELOG.md          # Sürüm geçmişi
├── config/               # Çalışma parametreleri + güvenlik sınırları
├── errors/               # Hata kataloğu
├── instructions/         # Prompt ayrıştırması
├── references/           # Derinlemesine dokümantasyon
├── scripts/              # Çalıştırılabilir araçlar
├── agents/               # Subagent talimatları
└── assets/               # Template'ler ve HTML
```

## License

MIT — see `LICENSE` file.