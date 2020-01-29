import json
from src.resources.data_usage import DataUsagesAmongAPI
from src.schemas.data_usage import StatusDataUsagesAmong


def test_data_usage_current_billing_cycle_fake(client):
    response = client.get('/api/data-usages/1/')
    assert response.status_code == 404


def test_usaged_data_succed(
        client, current_billing_cycle, subscription, data_usages
):
    response = client.get(f'/api/data-usages/{subscription.id}/')
    data_usage = json.loads(response.get_data().decode("utf-8"))
    assert response.status_code == 200
    assert data_usage['status'] == "succeed"
    assert data_usage['gb_used'] == 0.6


def test_usaged_data_over_allocated(
        client, current_billing_cycle, subscription, data_usages_over_allocated
):
    response = client.get(f'/api/data-usages/{subscription.id}/')
    data_usage = json.loads(response.get_data().decode("utf-8"))
    assert response.status_code == 200
    assert data_usage['status'] == "error"
    assert data_usage['gb_used'] == 6.0


def test_calculate_usage_memory(data_usages):
    instance = DataUsagesAmongAPI()
    gb_used = instance._calculate_among_data_usage(data_usages)
    assert gb_used == 10.60


def test_calculate_usage_memory_fake():
    instance = DataUsagesAmongAPI()
    gb_used = instance._calculate_among_data_usage(None)
    assert gb_used == 0


def test_elaborate_status(plan):
    plan.mb_available = 11000
    instance = DataUsagesAmongAPI()
    status = instance._elaborate_status(float(10), plan)
    assert StatusDataUsagesAmong.succeed == status


def test_elaborate_status_over_located(plan):
    plan.mb_available = 1000
    instance = DataUsagesAmongAPI()
    status = instance._elaborate_status(float(10), plan)
    assert StatusDataUsagesAmong.error == status


def test_elaborate_status_plan_unlimited(plan):
    plan.is_unlimited = True
    instance = DataUsagesAmongAPI()
    status = instance._elaborate_status(float(1000), plan)
    assert StatusDataUsagesAmong.succeed == status


def test_among_data_usage_with_plan_is_unlimited(data_usages, plan):
    plan.is_unlimited = True
    instance = DataUsagesAmongAPI()
    status = instance.among_data_usage(data_usages, plan)
    assert status["status"] == StatusDataUsagesAmong.succeed
    assert status["gb_used"] == 10.60


def test_data_usages_summary_succeed(data_usages, plan):
    plan.mb_available = 11000
    instance = DataUsagesAmongAPI()
    summary = instance.among_data_usage(data_usages, plan)
    assert summary["status"] == StatusDataUsagesAmong.succeed
    assert summary["gb_used"] == 10.60


def test_among_data_usage_error(data_usages, plan) -> None:
    plan.mb_available = 1000
    instance = DataUsagesAmongAPI()
    summary = instance.among_data_usage(data_usages, plan)
    assert summary["status"] == StatusDataUsagesAmong.error
    assert summary["gb_used"] == 10.60

