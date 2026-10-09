"""Tests for database.py. Run with: python -m pytest tests/ -v

Every test uses its own temporary database file (pytest's tmp_path
fixture), passed in through the db_path argument, so the real
expenses.db is never touched.
"""

from datetime import date, timedelta

import pytest

import database


@pytest.fixture
def db(tmp_path):
    """A fresh, empty database file for each test."""
    db_path = str(tmp_path / "test.db")
    database.init_db(db_path)
    return db_path


# ---------- naira_to_kobo ----------

def test_naira_to_kobo_1500_50():
    assert database.naira_to_kobo(1500.50) == 150050


def test_naira_to_kobo_500_50():
    assert database.naira_to_kobo(500.50) == 50050


def test_naira_to_kobo_0_10_has_no_float_residue():
    assert database.naira_to_kobo(0.10) == 10


# ---------- add / get ----------

def test_add_expense_and_get_all_expenses(db):
    new_id = database.add_expense(150050, "Food", "2026-10-07", "Rice", db)
    expenses = database.get_all_expenses(db)

    assert len(expenses) == 1
    assert expenses[0]["id"] == new_id
    assert expenses[0]["amount_kobo"] == 150050
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["date"] == "2026-10-07"
    assert expenses[0]["description"] == "Rice"


def test_get_expense_by_id_returns_the_expense(db):
    new_id = database.add_expense(35000, "Transport", "2026-10-08", "Bus", db)

    expense = database.get_expense_by_id(new_id, db)

    assert expense["id"] == new_id
    assert expense["category"] == "Transport"
    assert expense["description"] == "Bus"


def test_get_expense_by_id_returns_none_for_missing_id(db):
    assert database.get_expense_by_id(9999, db) is None


def test_get_all_expenses_returns_newest_first(db):
    database.add_expense(100, "Food", "2026-10-01", "old", db)
    database.add_expense(200, "Food", "2026-10-05", "newer", db)

    expenses = database.get_all_expenses(db)

    assert [e["description"] for e in expenses] == ["newer", "old"]


# ---------- update / delete ----------

def test_update_expense_changes_the_row(db):
    new_id = database.add_expense(100, "Food", "2026-10-01", "Rice", db)

    database.update_expense(new_id, 250075, "Transport", "2026-10-02",
                            "Bus fare", db)

    expense = database.get_expense_by_id(new_id, db)
    assert expense["amount_kobo"] == 250075
    assert expense["category"] == "Transport"
    assert expense["date"] == "2026-10-02"
    assert expense["description"] == "Bus fare"


def test_delete_expense_removes_the_row(db):
    new_id = database.add_expense(100, "Food", "2026-10-01", "Rice", db)

    database.delete_expense(new_id, db)

    assert database.get_all_expenses(db) == []


# ---------- search_expenses ----------

@pytest.fixture
def sample_db(db):
    """A database with four known expenses for search tests."""
    database.add_expense(150050, "Food", "2026-10-01", "Rice and stew", db)
    database.add_expense(35000, "Transport", "2026-10-03", "Bus fare", db)
    database.add_expense(50000, "Food", "2026-10-05", "Groceries", db)
    database.add_expense(120000, "Entertainment", "2026-10-05",
                         "Cinema night", db)
    return db


def test_search_text_is_case_insensitive_and_partial(sample_db):
    results = database.search_expenses(text="RICE", db_path=sample_db)
    assert [e["description"] for e in results] == ["Rice and stew"]

    results = database.search_expenses(text="grocer", db_path=sample_db)
    assert [e["description"] for e in results] == ["Groceries"]


def test_search_category_filter_matches_exactly(sample_db):
    results = database.search_expenses(category="Food", db_path=sample_db)

    assert len(results) == 2
    assert all(e["category"] == "Food" for e in results)


def test_search_date_range_is_inclusive(sample_db):
    results = database.search_expenses(date_from="2026-10-03",
                                       date_to="2026-10-05",
                                       db_path=sample_db)

    assert len(results) == 3
    assert {e["date"] for e in results} == {
        "2026-10-03", "2026-10-05"}


def test_search_blank_values_mean_no_limit(sample_db):
    results = database.search_expenses(text="", category=None,
                                       date_from="", date_to=None,
                                       db_path=sample_db)
    assert len(results) == 4


def test_search_conditions_combine_with_and(sample_db):
    results = database.search_expenses(text="fare", category="Transport",
                                       date_from="2026-10-01",
                                       date_to="2026-10-31",
                                       db_path=sample_db)

    assert len(results) == 1
    assert results[0]["description"] == "Bus fare"


def test_search_conditions_combine_with_and_no_match(sample_db):
    results = database.search_expenses(text="fare", category="Food",
                                       db_path=sample_db)
    assert results == []


def test_search_percent_matches_only_literal_percent(sample_db):
    database.add_expense(100, "Other", "2026-10-06", "Got 50% off", sample_db)

    results = database.search_expenses(text="%", db_path=sample_db)
    assert [e["description"] for e in results] == ["Got 50% off"]


def test_search_underscore_matches_only_literal_underscore(sample_db):
    database.add_expense(100, "Other", "2026-10-06", "item_42", sample_db)

    results = database.search_expenses(text="_", db_path=sample_db)
    assert [e["description"] for e in results] == ["item_42"]


# ---------- summary functions ----------

def test_total_spending_is_zero_on_empty_database(db):
    total = database.get_total_spending(db)
    assert total == 0
    assert total is not None


def test_total_spending_sums_all_expenses(db):
    database.add_expense(150050, "Food", "2026-10-01", "a", db)
    database.add_expense(49950, "Transport", "2026-10-02", "b", db)

    assert database.get_total_spending(db) == 200000


def test_month_spending_is_zero_on_empty_database(db):
    total = database.get_month_spending(db)
    assert total == 0
    assert total is not None


def test_month_spending_counts_this_month_only(db):
    today = date.today()
    this_month_day = today.strftime("%Y-%m-%d")
    same_month_last_year = today.replace(year=today.year - 1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)

    database.add_expense(1000, "Food", this_month_day, "this month", db)
    database.add_expense(2000, "Food",
                         same_month_last_year.strftime("%Y-%m-%d"),
                         "same month last year", db)
    database.add_expense(4000, "Food",
                         last_day_last_month.strftime("%Y-%m-%d"),
                         "end of last month", db)

    assert database.get_month_spending(db) == 1000


def test_totals_by_category_empty_database(db):
    assert database.get_totals_by_category(db) == []


def test_totals_by_category_correct_sums_highest_first(db):
    database.add_expense(150050, "Food", "2026-10-01", "a", db)
    database.add_expense(50000, "Food", "2026-10-02", "b", db)
    database.add_expense(120000, "Transport", "2026-10-03", "c", db)

    totals = database.get_totals_by_category(db)

    assert totals[0] == ("Food", 200050)
    assert totals[1] == ("Transport", 120000)
    assert len(totals) == 2
