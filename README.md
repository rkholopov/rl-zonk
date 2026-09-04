# RL для игры Zonk

Обучение агентов Reinforcement Learning в среде Zonk. Реализованы пять алгоритмов:  
- **Monte-Carlo** (обычный и с Weighted Importance Sampling)  
- **Cross-Entropy Method**  
- **Baseline** (Основан на знаниях об окружении, см. Stratagy_by_math_expectation)  
- **Q-Learning** (табличный)  

Проект структурирован так, чтобы легко менять агентов и гиперпараметры без правки кода.

---

## Структура

```
.
├── Agents/               # Классы всех агентов
│   ├── Monte_Carlo.py
│   ├── MonteCarloWIS.py
│   ├── CrossEntropy.py
│   ├── Baseline.py
│   └── QLearning.py
├── Enviroment/           # Среда Zonk
│   └── Zonk.py
├── Stratagy_by_math_expectation/   # Стратегия построенная на знании окружения
│   ├── best_expect.py
│   ├── Distribution_of_SBME.xlsx
│   ├── multiple_distribution.py
│   └── six_cubes.py
├── training/             # Скрипт обучения
│   └── training.py
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/rkholopov/rl-zonk.git
   cd rl-zonk
   ```

2. Создайте виртуальное окружение (рекомендуется):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

---

## Запуск обучения

Из корневой папки проекта выполните:

```bash
python training/training.py --agent QLearning --episodes 50000
```

### Доступные агенты
- `MonteCarlo`
- `MonteCarloWIS`
- `CrossEntropy`
- `Baseline`
- `QLearning`

### Основные аргументы командной строки

| Аргумент | Описание | По умолчанию |
|----------|----------|--------------|
| `--agent` | Имя агента | `Baseline` |
| `--soft` | Параметр мягкой стратегии (`0.1` – для e-мягкой стратегии, `Sampling` – для сэмплирования) | `0.1` |
| `--alpha` | Скорость обучения (для Q-Learning) | `0.3` |
| `--percentile` | Процент элитных траекторий (для Cross-Entropy) | `85.0` |
| `--episodes` | Общее число эпизодов обучения | `100000` |
| `--eval_interval` | Как часто (в эпизодах) проводить оценку | `10000` |
| `--eval_episodes` | Число эпизодов для оценки | `10000` |

Пример с полным набором параметров:
```bash
python training/training.py --agent CrossEntropy --percentile 90 --episodes 200000 --eval_interval 5000
```

---

## Что выводится в консоль

Каждые `eval_interval` эпизодов печатаются две средние награды:
- **На обучении** – средняя награда за последние `eval_interval` эпизодов.
- **На инференсе** – средняя награда при детерминированном выборе действий (без исследования) за `eval_episodes` эпизодов.

Пример вывода:
```
На обучении: 12.34, На инференсе: 15.67
```

---

## Примечания по среде Zonk

- Среда возвращает состояние `s` и награду `r`, а в `info['possible_moves']` передаются доступные ходы.
- Агенты используют количество доступных ходов для обучения.
- В `agent.action(s, pos_moves, optimal=False)` параметр `optimal=True` включает жадный (детерминированный) выбор.

---

## Автор

Роман Холопов  
GitHub: [rkholopov](https://github.com/rkholopov)
