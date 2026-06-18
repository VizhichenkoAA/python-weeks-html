# SQL-проверки — неделя 5 (вариант 03, таблица mart_variant_03)

Подключение (пример):

```bat
docker exec -it tp-v03-postgres psql -U tp_user -d tp_variant_03
```

Или через Python/SQLAlchemy с тем же `DATABASE_URL`, что и `load.py` (порт **5433** в Docker).

Если `load` падает с `UnicodeDecodeError` на Windows — проверьте, что на 5432 не занят другой Postgres; наш контейнер слушает **5433**.

---

## 1. Таблица не пустая

```sql
SELECT COUNT(*) AS row_count FROM mart_variant_03;
```

Ожидание: `row_count > 0` (для нашей витрины — 14 дней).

---

## 2. Диапазон дат

```sql
SELECT MIN(date) AS min_date, MAX(date) AS max_date
FROM mart_variant_03;
```

Ожидание: `min_date = 2025-01-01`, `max_date = 2025-01-14`.

---

## 3. NULL в ключевых колонках

```sql
SELECT
  SUM(CASE WHEN city_id IS NULL THEN 1 ELSE 0 END) AS null_city_id,
  SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) AS null_date
FROM mart_variant_03;
```

Ожидание: оба счётчика = 0.

---

## 4. Дубли по бизнес-ключу (city_id + date)

```sql
SELECT city_id, date, COUNT(*) AS cnt
FROM mart_variant_03
GROUP BY city_id, date
HAVING COUNT(*) > 1;
```

Ожидание: 0 строк.

---

## 5. Проверка KPI (осадки и температура)

```sql
SELECT
  ROUND(AVG(t_mean)::numeric, 2) AS avg_t_mean,
  ROUND(SUM(p_sum)::numeric, 2) AS total_precip,
  MAX(wind_max) AS max_wind
FROM mart_variant_03;
```

Ожидание: осмысленные значения; `total_precip >= 0`, `max_wind > 0`.

---

## 6. (доп.) Повторная загрузка не удваивает строки

После второго запуска `scripts\run_load.bat`:

```sql
SELECT COUNT(*) FROM mart_variant_03;
```

Ожидание: то же число строк, что и после первой загрузки (стратегия `replace`).

---

## 7. (доп.) Отрицательные осадки

```sql
SELECT COUNT(*) AS bad_precip
FROM mart_variant_03
WHERE p_sum < 0;
```

Ожидание: `bad_precip = 0`.
